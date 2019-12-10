# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

import aiopg  # type: ignore

from typing import Any, List, Tuple

from psycopg2.extras import DictCursor  # type: ignore

from wazo_router_confd.models.normalization import NormalizationProfile
from wazo_router_confd.schemas import kamailio as schema
from wazo_router_confd.schemas import cdr as cdr_schema
from wazo_router_confd.services import password as password_service
from wazo_router_confd.services import normalization as normalization_service


re_protocol_local_part_and_domain = re.compile(
    r'^([^:]+:)?([^@]+)@([^@:]+)(:[0-9]+)?$'
).match


def split_uri_to_parts(uri: str) -> Tuple[str, str, str, str]:
    m = re_protocol_local_part_and_domain(uri)
    if m is None:
        return ('', '', '', '')
    protocol, local_part, domain_name, port_number = m.groups()
    return (protocol or '', local_part, domain_name, port_number or '')


async def routing(
    pool: aiopg.Pool, request: schema.RoutingRequest
) -> schema.RoutingResponse:
    # auth the request, if needed
    auth_response = (
        await auth(
            pool,
            request=schema.AuthRequest(
                source_ip=request.source_ip,
                source_port=request.source_port,
                domain=request.domain,
                username=request.username,
            ),
        )
        if request.auth
        else None
    )
    async with pool.acquire() as conn:
        # routing
        routes = []
        # get the domain name from the to uri
        (
            from_protocol,
            from_local_part,
            from_domain_name,
            from_port_number,
        ) = split_uri_to_parts(request.from_uri)
        protocol, local_part, domain_name, port_number = split_uri_to_parts(
            request.to_uri
        )
        # normalize according ipbx/carrier trunk source
        normalization_profile = None
        if auth_response is not None and auth_response.ipbx_id:
            sql = (
                "SELECT ipbx.*, normalization_profiles.* "
                "FROM ipbx LEFT JOIN normalization_profiles ON (ipbx.normalization_profile_id = normalization_profiles.id) "
                "WHERE ipbx.id = %s"
            )
            async with conn.cursor(cursor_factory=DictCursor) as cur:
                await cur.execute(sql, [auth_response.ipbx_id])
                ipbx = await cur.fetchone()
                normalization_profile = (
                    NormalizationProfile(
                        name=ipbx['name'],
                        country_code=ipbx['country_code'],
                        area_code=ipbx['area_code'],
                        intl_prefix=ipbx['intl_prefix'],
                        ld_prefix=ipbx['ld_prefix'],
                        always_intl_prefix_plus=ipbx['always_intl_prefix_plus'],
                        always_ld=ipbx['always_ld'],
                    )
                    if ipbx is not None and ipbx.get('country_code')
                    else None
                )
        elif auth_response is not None and auth_response.carrier_trunk_id:
            sql = (
                "SELECT carrier_trunks.*, normalization_profiles.* "
                "FROM carrier_trunks LEFT JOIN normalization_profiles ON (carrier_trunks.normalization_profile_id = normalization_profiles.id) "
                "WHERE carrier_trunks.id = %s"
            )
            async with conn.cursor(cursor_factory=DictCursor) as cur:
                await cur.execute(sql, [auth_response.carrier_trunk_id])
                carrier_trunk = await cur.fetchone()
                normalization_profile = (
                    NormalizationProfile(
                        name=carrier_trunk['name'],
                        country_code=carrier_trunk['country_code'],
                        area_code=carrier_trunk['area_code'],
                        intl_prefix=carrier_trunk['intl_prefix'],
                        ld_prefix=carrier_trunk['ld_prefix'],
                        always_intl_prefix_plus=carrier_trunk[
                            'always_intl_prefix_plus'
                        ],
                        always_ld=carrier_trunk['always_ld'],
                    )
                    if carrier_trunk is not None and carrier_trunk.get('country_code')
                    else None
                )
        from_local_part = await normalization_service.normalize_local_number_to_e164(
            conn, from_local_part, profile=normalization_profile
        )
        local_part = await normalization_service.normalize_local_number_to_e164(
            conn, local_part, profile=normalization_profile
        )
        # get all the ipbxs linked to that domain
        where = ["domains.domain = %s"]
        where_args: List[Any] = [domain_name]
        # filter by tenant, if the request is authenticated
        if auth_response is not None and auth_response.tenant_uuid:
            where.append("ipbx.tenant_uuid = %s")
            where_args.append(auth_response.tenant_uuid)
        # get the list of ipbx, ordered by id
        ipbxs = []
        sql = (
            "SELECT ipbx.*, normalization_profiles.* "
            "FROM ipbx JOIN domains ON (ipbx.domain_id = domains.id) "
            "LEFT JOIN normalization_profiles ON (ipbx.normalization_profile_id = normalization_profiles.id) "
            "WHERE %s ORDER BY ipbx.id LIMIT 1;" % " AND ".join(where)
        )
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(sql, where_args)
            ipbx = await cur.fetchone()
            if ipbx is not None:
                ipbxs.append(ipbx)
        # get all the ipbxs linked to that DID
        prefixes = [local_part[:i] for i in range(0, min(10, len(local_part)))]
        where = ["dids.did_prefix = ANY(%s)"]
        where_args = [prefixes]
        # filter by tenant, if the request is authenticated
        if auth_response is not None and auth_response.tenant_uuid:
            where.append("ipbx.tenant_uuid = %s")
            where_args.append(auth_response.tenant_uuid)
        # get the list of ipbx, ordered by id
        sql = (
            "SELECT ipbx.*, normalization_profiles.*, dids.did_regex "
            "FROM ipbx JOIN dids ON (dids.ipbx_id = ipbx.id) "
            "LEFT JOIN normalization_profiles ON (ipbx.normalization_profile_id = normalization_profiles.id) "
            "WHERE %s ORDER BY ipbx.id;" % " AND ".join(where)
        )
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(sql, where_args)
            async for ipbx in cur:
                if re.match(ipbx['did_regex'], local_part):
                    ipbxs.append(ipbx)
                    break
        # build a route for each ipbx
        ipbx_auth = None
        for ipbx in ipbxs:
            # normalize from uri
            normalization_profile = (
                NormalizationProfile(
                    name=ipbx['name'],
                    country_code=ipbx['country_code'],
                    area_code=ipbx['area_code'],
                    intl_prefix=ipbx['intl_prefix'],
                    ld_prefix=ipbx['ld_prefix'],
                    always_intl_prefix_plus=ipbx['always_intl_prefix_plus'],
                    always_ld=ipbx['always_ld'],
                )
                if ipbx.get('country_code')
                else None
            )
            normalized_local_part = await normalization_service.normalize_e164_to_local_number(
                conn, from_local_part, profile=normalization_profile
            )
            normalized_from_uri = "%s%s@%s" % (
                from_protocol,
                normalized_local_part,
                from_domain_name,
            )
            # normalize to uri
            normalized_local_part = await normalization_service.normalize_e164_to_local_number(
                conn, local_part, profile=normalization_profile
            )
            normalized_to_uri = "%s%s@%s" % (
                protocol,
                normalized_local_part,
                domain_name,
            )
            #
            routes.append(
                {
                    "dst_uri": "sip:%s:%s" % (ipbx['ip_fqdn'], ipbx['port']),
                    "path": "",
                    "socket": "",
                    "headers": {
                        "from": {
                            "display": request.from_name,
                            "uri": normalized_from_uri,
                        },
                        "to": {"display": request.to_name, "uri": normalized_to_uri},
                        "extra": "",
                    },
                    "branch_flags": 8,
                    "fr_timer": 5000,
                    "fr_inv_timer": 30000,
                }
            )
            # if ipbx requires it, set the auth parameters
            if (
                ipbx['username'] is not None
                and ipbx['password'] is not None
                and ipbx['realm'] is not None
            ):
                ipbx_auth = dict(
                    auth_username=ipbx['username'],
                    auth_password=ipbx['password'],
                    realm=ipbx['realm'],
                )
            # we stop at the first ipbx found
            break
        # route by carrier trunk if the package is coming from a known IPBX
        where = ["ipbx.ip_fqdn = %s"]
        where_args = [request.source_ip]
        # filter by tenant, if the request is authenticated
        if auth_response is not None and auth_response.tenant_uuid:
            where.append("carriers.tenant_uuid = %s")
            where_args.append(auth_response.tenant_uuid)
        # get the list of carrier trunks, ordered by id
        carrier_trunk_auth = None
        sql = (
            "SELECT carrier_trunks.*, normalization_profiles.* "
            "FROM carrier_trunks JOIN carriers ON (carrier_trunks.carrier_id = carriers.id) "
            "JOIN ipbx ON (ipbx.tenant_uuid = carriers.tenant_uuid) "
            "LEFT JOIN normalization_profiles ON (carrier_trunks.normalization_profile_id = normalization_profiles.id) "
            "WHERE %s ORDER BY carrier_trunks.id LIMIT 1;" % " AND ".join(where)
        )
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(sql, where_args)
            carrier_trunk = await cur.fetchone()
            if carrier_trunk is not None:
                # normalize from uri
                normalization_profile = (
                    NormalizationProfile(
                        name=carrier_trunk['name'],
                        country_code=carrier_trunk['country_code'],
                        area_code=carrier_trunk['area_code'],
                        intl_prefix=carrier_trunk['intl_prefix'],
                        ld_prefix=carrier_trunk['ld_prefix'],
                        always_intl_prefix_plus=carrier_trunk[
                            'always_intl_prefix_plus'
                        ],
                        always_ld=carrier_trunk['always_ld'],
                    )
                    if carrier_trunk is not None and carrier_trunk.get('country_code')
                    else None
                )
                normalized_local_part = await normalization_service.normalize_e164_to_local_number(
                    conn, from_local_part, profile=normalization_profile
                )
                normalized_from_uri = "%s%s@%s%s" % (
                    from_protocol,
                    normalized_local_part,
                    from_domain_name,
                    from_port_number,
                )
                # normalize to uri
                normalized_local_part = await normalization_service.normalize_e164_to_local_number(
                    conn, local_part, profile=normalization_profile
                )
                normalized_to_uri = "%s%s@%s%s" % (
                    protocol,
                    normalized_local_part,
                    domain_name,
                    port_number,
                )
                #
                routes.append(
                    {
                        "dst_uri": "sip:%s:%s"
                        % (carrier_trunk['sip_proxy'], carrier_trunk['sip_proxy_port']),
                        "path": "",
                        "socket": "",
                        "headers": {
                            "from": {
                                "display": request.from_name,
                                "uri": normalized_from_uri,
                            },
                            "to": {
                                "display": request.to_name,
                                "uri": normalized_to_uri,
                            },
                            "extra": "",
                        },
                        "branch_flags": 8,
                        "fr_timer": 5000,
                        "fr_inv_timer": 30000,
                    }
                )
                # if carrier trunk is registered, set the auth parameters
                if (
                    carrier_trunk['auth_username'] is not None
                    and carrier_trunk['auth_password'] is not None
                    and carrier_trunk['realm'] is not None
                ):
                    carrier_trunk_auth = dict(
                        auth_username=carrier_trunk['auth_username'],
                        auth_password=carrier_trunk['auth_password'],
                        realm=carrier_trunk['realm'],
                    )
        # build the JSON document, compatible with the rtjson Kamailio module form
        rtjson = (
            {"success": True, "version": "1.0", "routing": "serial", "routes": routes}
            if routes
            else {"success": False}
        )
        # update with carrier trunk auth parameters, if set
        if carrier_trunk_auth is not None:
            rtjson.update(carrier_trunk_auth)
        # update with ipbx auth parameters, if set
        elif ipbx_auth is not None:
            rtjson.update(ipbx_auth)
        # return the routing and auth responses
        return schema.RoutingResponse(auth=auth_response, rtjson=rtjson)


async def auth(pool: aiopg.Pool, request: schema.AuthRequest) -> schema.AuthResponse:
    async with pool.acquire() as conn:
        if request.source_ip or request.username:
            where = ["1 = 1"]
            where_args = []
            if request.source_ip:
                where.append("(ip_address IS NULL OR ip_address = %s)")
                where_args.append(request.source_ip)
            if request.username:
                where.append(
                    "(ipbx.username = %s OR (ipbx.password_ha1 IS NULL AND ipbx.username IS NULL))"
                )
                where_args.append(request.username)
            if request.domain:
                where.append("(domains.domain = %s)")
                where_args.append(request.domain)
            sql = (
                "SELECT ipbx.id, ipbx.tenant_uuid, ipbx.username, ipbx.password, ipbx.password_ha1, domains.domain "
                "FROM ipbx JOIN domains ON (ipbx.domain_id = domains.id) "
                "WHERE %s ORDER BY ipbx.id;" % " AND ".join(where)
            )
            async with conn.cursor(cursor_factory=DictCursor) as cur:
                await cur.execute(sql, where_args)
                async for ipbx in cur:
                    if (
                        not request.password
                        or ipbx['password']
                        and password_service.verify(ipbx['password'], request.password)
                    ):
                        await conn.close()
                        return schema.AuthResponse(
                            success=True,
                            tenant_uuid=ipbx['tenant_uuid'],
                            ipbx_id=ipbx['id'],
                            domain=ipbx['domain'],
                            username=ipbx['username'],
                            password_ha1=ipbx['password_ha1'],
                        )
            #
            if request.source_ip:
                sql = (
                    "SELECT carriers.tenant_uuid, carrier_trunks.id "
                    "FROM carrier_trunks JOIN carriers ON carrier_trunks.carrier_id = carriers.id "
                    "WHERE (carrier_trunks.ip_address IS NULL OR carrier_trunks.ip_address = %s) "
                    "ORDER BY carrier_trunks.id LIMIT 1;"
                )
                async with conn.cursor(cursor_factory=DictCursor) as cur:
                    await cur.execute(sql, [request.source_ip])
                    carrier_trunk = await cur.fetchone()
                    await conn.close()
                    if carrier_trunk is not None:
                        return schema.AuthResponse(
                            success=True,
                            tenant_uuid=carrier_trunk['tenant_uuid'],
                            carrier_trunk_id=carrier_trunk['id'],
                        )
    return schema.AuthResponse(success=False)


async def cdr(pool: aiopg.Pool, request: schema.CDRRequest) -> dict:
    async with pool.acquire() as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(
                "SELECT * FROM tenants WHERE uuid = %s;", [request.tenant_uuid]
            )
            tenant = await cur.fetchone()
            if tenant is None:
                return {"success": False, "cdr": None}
            cdr = cdr_schema.CDRCreate(
                tenant_uuid=tenant['uuid'],
                source_ip=request.source_ip,
                source_port=request.source_port,
                from_uri=request.from_uri,
                to_uri=request.to_uri,
                call_id=request.call_id,
                call_start=request.call_start,
                duration=request.duration,
            )
            await cur.execute(
                "INSERT INTO cdrs (tenant_uuid, source_ip, source_port, from_uri, to_uri, call_id, call_start, duration) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                [
                    cdr.tenant_uuid,
                    cdr.source_ip,
                    cdr.source_port,
                    cdr.from_uri,
                    cdr.to_uri,
                    cdr.call_id,
                    cdr.call_start,
                    cdr.duration,
                ],
            )
            return {"success": True, "cdr": cdr}


async def dbtext_uacreg(pool: aiopg.Pool) -> schema.DBText:
    content = []
    content.append(
        " ".join(
            [
                "l_uuid(string)",
                "l_username(string)",
                "l_domain(string)",
                "r_username(string)",
                "r_domain(string)",
                "realm(string)",
                "auth_username(string)",
                "auth_password(string)",
                "auth_proxy(string)",
                "expires(int)",
                "flags(int)",
                "reg_delay(int)",
            ]
        )
        + "\n"
    )
    async with pool.acquire() as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(
                "SELECT * FROM carrier_trunks WHERE registered = true ORDER BY id;"
            )
            async for carrier_trunk in cur:
                content.append(
                    ":".join(
                        map(
                            lambda x: x.replace(":", "\\:"),
                            [
                                "%s" % carrier_trunk['id'],
                                carrier_trunk['auth_username'],
                                carrier_trunk['from_domain'],
                                carrier_trunk['auth_username'],
                                carrier_trunk['from_domain'],
                                carrier_trunk['realm'],
                                carrier_trunk['auth_username'],
                                carrier_trunk['auth_password'],
                                "sip:%s" % carrier_trunk['registrar_proxy'],
                                str(carrier_trunk['expire_seconds']),
                                "16",
                                "0",
                            ],
                        )
                    )
                    + "\n"
                )
        await conn.close()
    return schema.DBText(content="".join(content))
