# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from email.utils import parseaddr
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


def local_part_and_domain_from_uri(uri: str) -> Tuple[str, str]:
    _, address = parseaddr(uri)
    local_part, domain_name = address.rsplit('@', 1)
    return (local_part, domain_name)


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
    local_part, domain_name = local_part_and_domain_from_uri(request.to_uri)
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
    for ipbx in ipbxs:
        routes.append(
            {
                "dst_uri": "sip:%s:%s" % (ipbx.ip_fqdn, ipbx.port),
                "path": "",
                "socket": "",
                "headers": {
                    "from": {"display": request.from_name, "uri": request.from_uri},
                    "to": {"display": request.to_name, "uri": request.to_uri},
                    "extra": "",
                },
                "branch_flags": 8,
                "fr_timer": 5000,
                "fr_inv_timer": 30000,
            }
        )
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
    for carrier_trunk in carrier_trunks:
        routes.append(
            {
                "dst_uri": "sip:%s:%s"
                % (carrier_trunk.sip_proxy, carrier_trunk.sip_proxy_port),
                "path": "",
                "socket": "",
                "headers": {
                    "from": {"display": request.from_name, "uri": request.from_uri},
                    "to": {"display": request.to_name, "uri": request.to_uri},
                    "extra": "",
                },
                "branch_flags": 8,
                "fr_timer": 5000,
                "fr_inv_timer": 30000,
            }
        )
    # build the JSON document, compatible with the rtjson Kamailio module form
    rtjson = (
        {"success": True, "version": "1.0", "routing": "serial", "routes": routes}
        if routes
        else {"success": False}
    )
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
            .filter(CarrierTrunk.ip_address == request.source_ip)
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
