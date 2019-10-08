# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from email.utils import parseaddr

from sqlalchemy.orm import Session

from wazo_router_confd.models.carrier import Carrier
from wazo_router_confd.models.carrier_trunk import CarrierTrunk
from wazo_router_confd.models.did import DID
from wazo_router_confd.models.domain import Domain
from wazo_router_confd.models.ipbx import IPBX
from wazo_router_confd.schemas import kamailio as schema


def routing(db: Session, request: schema.RoutingRequest) -> dict:
    routes = []
    # get the domain name from the to uri
    _, address = parseaddr(request.to_uri)
    local_part, domain_name = address.rsplit('@', 1)
    # get all the ipbxs linked to that domain
    ipbxs = set()
    ipbxs_by_domain = (
        db.query(IPBX)
        .join(Domain)
        .filter(Domain.domain == domain_name)
        .order_by(IPBX.id)
    )
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
        for did in dids:
            if re.match(did.did_regex, local_part):
                ipbxs.add(ipbx)
    # build a route for each ipbx
    for ipbx in ipbxs:
        routes.append(
            {
                "uri": "sip:%s@%s:%s" % (local_part, ipbx.ip_fqdn, ipbx.port),
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
    for carrier_trunk in carrier_trunks:
        routes.append(
            {
                "uri": "sip:%s@%s:%s"
                % (local_part, carrier_trunk.sip_proxy, carrier_trunk.sip_proxy_port),
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
    # return the JSON document, compatible with the rtjson Kamailio module form
    return {"version": "1.0", "routing": "serial", "routes": routes}
