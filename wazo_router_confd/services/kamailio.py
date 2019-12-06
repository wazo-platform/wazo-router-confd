# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from typing import Tuple

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from wazo_router_confd.models.carrier import Carrier
from wazo_router_confd.models.carrier_trunk import CarrierTrunk
from wazo_router_confd.models.did import DID
from wazo_router_confd.models.domain import Domain
from wazo_router_confd.models.ipbx import IPBX
from wazo_router_confd.schemas import kamailio as schema
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


def routing(db: Session, request: schema.RoutingRequest) -> schema.RoutingResponse:
    # auth the request, if needed
    auth_response = (
        auth(
            db,
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
    # routing
    routes = []
    # get the domain name from the to uri
    (
        from_protocol,
        from_local_part,
        from_domain_name,
        from_port_number,
    ) = split_uri_to_parts(request.from_uri)
    protocol, local_part, domain_name, port_number = split_uri_to_parts(request.to_uri)
    # normalize according ipbx/carrier trunk source
    normalization_profile = None
    if auth_response is not None and auth_response.ipbx_id:
        ipbx = db.query(IPBX).filter(IPBX.id == auth_response.ipbx_id).first()
        normalization_profile = ipbx.normalization_profile
    elif auth_response is not None and auth_response.carrier_trunk_id:
        carrier_trunk = (
            db.query(CarrierTrunk)
            .filter(CarrierTrunk.id == auth_response.carrier_trunk_id)
            .first()
        )
        normalization_profile = carrier_trunk.normalization_profile
    from_local_part = normalization_service.normalize_local_number_to_e164(
        db, from_local_part, profile=normalization_profile
    )
    local_part = normalization_service.normalize_local_number_to_e164(
        db, local_part, profile=normalization_profile
    )
    # get all the ipbxs linked to that domain
    ipbxs = set()
    ipbxs_by_domain = db.query(IPBX).join(Domain).filter(Domain.domain == domain_name)
    # filter by tenant, if the request is authenticated
    if auth_response is not None and auth_response.tenant_id:
        ipbxs_by_domain.filter(IPBX.tenant_id == auth_response.tenant_id)
    # get the list of ipbx, ordered by id
    ipbxs_by_domain = ipbxs_by_domain.order_by(IPBX.id)
    for ipbx in ipbxs_by_domain:
        ipbxs.add(ipbx)
    # get all the ipbxs linked to that DID
    list_of_all_ipbx = db.query(IPBX)
    for ipbx in list_of_all_ipbx:
        prefixes = [local_part[:i] for i in range(0, min(10, len(local_part)))]
        dids = (
            db.query(DID)
            .filter(DID.ipbx_id == ipbx.id)
            .filter(DID.did_prefix.in_(prefixes))
        )
        # filter by tenant, if the request is authenticated
        if auth_response is not None and auth_response.tenant_id:
            dids.filter(DID.tenant_id == auth_response.tenant_id)
        # get the list of dids, ordered by id
        dids = dids.order_by(func.length(DID.did_prefix).desc(), DID.id)
        for did in dids:
            if re.match(did.did_regex, local_part):
                ipbxs.add(ipbx)
    # build a route for each ipbx
    ipbx_auth = None
    for ipbx in ipbxs:
        # normalize from uri
        normalized_local_part = normalization_service.normalize_e164_to_local_number(
            db, from_local_part, profile=ipbx.normalization_profile
        )
        normalized_from_uri = "%s%s@%s" % (
            from_protocol,
            normalized_local_part,
            from_domain_name,
        )
        # normalize to uri
        normalized_local_part = normalization_service.normalize_e164_to_local_number(
            db, local_part, profile=ipbx.normalization_profile
        )
        normalized_to_uri = "%s%s@%s" % (protocol, normalized_local_part, domain_name)
        #
        routes.append(
            {
                "dst_uri": "sip:%s:%s" % (ipbx.ip_fqdn, ipbx.port),
                "path": "",
                "socket": "",
                "headers": {
                    "from": {"display": request.from_name, "uri": normalized_from_uri},
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
            ipbx.username is not None
            and ipbx.password is not None
            and ipbx.realm is not None
        ):
            ipbx_auth = dict(
                auth_username=ipbx.username,
                auth_password=ipbx.password,
                realm=ipbx.realm,
            )
        # we stop at the first ipbx found
        break
    # route by carrier trunk if the package is coming from a known IPBX
    carrier_trunks = (
        db.query(CarrierTrunk)
        .join(Carrier)
        .join(IPBX, Carrier.tenant_id == IPBX.tenant_id)
        .filter(IPBX.ip_fqdn == request.source_ip)
    )
    # filter by tenant, if the request is authenticated
    if auth_response is not None and auth_response.tenant_id:
        carrier_trunks.filter(Carrier.tenant_id == auth_response.tenant_id)
    # get the list of carrier trunks, ordered by id
    carrier_trunk_auth = None
    for carrier_trunk in carrier_trunks:
        # normalize from uri
        normalized_local_part = normalization_service.normalize_e164_to_local_number(
            db, from_local_part, profile=carrier_trunk.normalization_profile
        )
        normalized_from_uri = "%s%s@%s%s" % (
            from_protocol,
            normalized_local_part,
            from_domain_name,
            from_port_number,
        )
        # normalize to uri
        normalized_local_part = normalization_service.normalize_e164_to_local_number(
            db, local_part, profile=carrier_trunk.normalization_profile
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
                % (carrier_trunk.sip_proxy, carrier_trunk.sip_proxy_port),
                "path": "",
                "socket": "",
                "headers": {
                    "from": {"display": request.from_name, "uri": normalized_from_uri},
                    "to": {"display": request.to_name, "uri": normalized_to_uri},
                    "extra": "",
                },
                "branch_flags": 8,
                "fr_timer": 5000,
                "fr_inv_timer": 30000,
            }
        )
        # if carrier trunk is registered, set the auth parameters
        if (
            carrier_trunk.auth_username is not None
            and carrier_trunk.auth_password is not None
            and carrier_trunk.realm is not None
        ):
            carrier_trunk_auth = dict(
                auth_username=carrier_trunk.auth_username,
                auth_password=carrier_trunk.auth_password,
                realm=carrier_trunk.realm,
            )
        # we stop at the first carrier trunk found
        break
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


def auth(db: Session, request: schema.AuthRequest) -> schema.AuthResponse:
    if request.source_ip or request.username:
        found_ipbx = None
        ipbxs = db.query(IPBX).order_by(IPBX.id)
        if request.source_ip:
            ipbxs = ipbxs.filter(
                or_(IPBX.ip_address.is_(None), IPBX.ip_address == request.source_ip)
            )
        if request.domain:
            ipbxs = ipbxs.join(Domain).filter(Domain.domain == request.domain)
        if request.username:
            ipbxs = ipbxs.filter(
                or_(
                    and_(IPBX.password_ha1.is_(None), IPBX.username.is_(None)),
                    IPBX.username == request.username,
                )
            )
        for ipbx in ipbxs:
            if (
                not request.password
                or ipbx.password
                and password_service.verify(ipbx.password, request.password)
            ):
                found_ipbx = ipbx
                break
        if found_ipbx is not None:
            return schema.AuthResponse(
                success=True,
                tenant_id=found_ipbx.tenant_id,
                ipbx_id=found_ipbx.id,
                domain=found_ipbx.domain.domain,
                username=found_ipbx.username,
                password_ha1=found_ipbx.password_ha1,
            )
    #
    if request.source_ip:
        carrier_trunk = (
            db.query(CarrierTrunk)
            .filter(
                or_(
                    CarrierTrunk.ip_address.is_(None),
                    CarrierTrunk.ip_address == request.source_ip,
                )
            )
            .order_by(CarrierTrunk.id)
            .first()
        )
        if carrier_trunk is not None:
            return schema.AuthResponse(
                success=True,
                tenant_id=carrier_trunk.carrier.tenant_id,
                carrier_trunk_id=carrier_trunk.id,
            )
    return schema.AuthResponse(success=False)


def dbtext_uacreg(db: Session) -> schema.DBText:
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
    carrier_trunks = (
        db.query(CarrierTrunk)
        .filter(CarrierTrunk.registered.is_(True))
        .order_by(CarrierTrunk.id)
    )
    for carrier_trunk in carrier_trunks:
        content.append(
            ":".join(
                map(
                    lambda x: x.replace(":", "\\:"),
                    [
                        "%s" % carrier_trunk.id,
                        carrier_trunk.auth_username,
                        carrier_trunk.from_domain,
                        carrier_trunk.auth_username,
                        carrier_trunk.from_domain,
                        carrier_trunk.realm,
                        carrier_trunk.auth_username,
                        carrier_trunk.auth_password,
                        "sip:%s" % carrier_trunk.registrar_proxy,
                        str(carrier_trunk.expire_seconds),
                        "16",
                        "0",
                    ],
                )
            )
            + "\n"
        )
    return schema.DBText(content="".join(content))
