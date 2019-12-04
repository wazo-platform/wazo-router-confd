# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import uuid

from unittest import mock


def create_routing_rule(app, suffix=1):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.routing_rule import RoutingRule

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(
        name="tenant_{}".format(suffix), uuid=uuid.uuid4(),
    )
    domain = Domain(domain='testdomain_{}.com'.format(suffix), tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        password='password',
    )
    carrier = Carrier(name='carrier_{}'.format(suffix), tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk_{}'.format(suffix),
        carrier=carrier,
        sip_proxy='proxy.somedomain.com',
    )
    carrier_trunk_2 = CarrierTrunk(
        name='carrier_trunk_{}_bis'.format(suffix),
        carrier=carrier,
        sip_proxy='proxy.somedomain.com',
    )
    routing_rule = RoutingRule(
        prefix="39",
        carrier_trunk=carrier_trunk,
        ipbx=ipbx,
        did_regex=r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
        route_type="pstn",
    )

    session.add_all(
        [tenant, domain, carrier, carrier_trunk, carrier_trunk_2, ipbx, routing_rule]
    )
    session.commit()

    session.flush()

    return routing_rule, ipbx, carrier_trunk, tenant


def test_create_routing_rule(app, client):
    routing_rule, ipbx, carrier_trunk, tenant = create_routing_rule(app)
    #
    response = client.post(
        "/routing_rules/",
        json={
            "prefix": "39",
            "carrier_trunk_id": carrier_trunk.id,
            "ipbx_id": ipbx.id,
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "route_type": "pstn",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": mock.ANY,
        "prefix": "39",
        "carrier_trunk_id": carrier_trunk.id,
        "ipbx_id": ipbx.id,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "route_type": "pstn",
    }


def test_get_routing_rule(app, client):
    routing_rule, ipbx, carrier_trunk, tenant = create_routing_rule(app)
    #
    response = client.get("/routing_rules/%s" % routing_rule.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": routing_rule.id,
        "prefix": "39",
        "carrier_trunk_id": carrier_trunk.id,
        "ipbx_id": ipbx.id,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "route_type": "pstn",
    }


def test_get_routing_rule_not_found(app, client):
    response = client.get("/routing_rules/1")
    assert response.status_code == 404


def test_get_routing_rules(app, client):
    routing_rule, ipbx, carrier_trunk, tenant = create_routing_rule(app)
    #
    response = client.get("/routing_rules/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": routing_rule.id,
            "prefix": "39",
            "carrier_trunk_id": carrier_trunk.id,
            "ipbx_id": ipbx.id,
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "route_type": "pstn",
        }
    ]


def test_update_routing_rule(app, client):
    routing_rule, ipbx, carrier_trunk, tenant = create_routing_rule(app)
    routing_rule_2, ipbx_2, carrier_trunk_2, tenant_2 = create_routing_rule(app, 2)
    #
    response = client.put(
        "/routing_rules/%s" % routing_rule.id,
        json={
            'prefix': '40',
            'carrier_trunk_id': carrier_trunk_2.id,
            'ipbx_id': ipbx_2.id,
            'did_regex': r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
            'route_type': "pstn",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": routing_rule.id,
        "prefix": "40",
        "carrier_trunk_id": carrier_trunk_2.id,
        "ipbx_id": ipbx_2.id,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "route_type": "pstn",
    }


def test_update_routing_rule_not_found(app, client):
    response = client.put(
        "/routing_rules/1",
        json={
            'prefix': '40',
            'carrier_trunk_id': 2,
            'ipbx_id': 1,
            'did_regex': r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
            'route_type': "pstn",
        },
    )
    assert response.status_code == 404


def test_delete_routing_rule(app, client):
    routing_rule, ipbx, carrier_trunk, tenant = create_routing_rule(app)
    #
    response = client.delete("/routing_rules/%s" % routing_rule.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": routing_rule.id,
        "prefix": "39",
        "carrier_trunk_id": carrier_trunk.id,
        "ipbx_id": ipbx.id,
        "did_regex": r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
        "route_type": "pstn",
    }


def test_delete_routing_rule_not_found(app, client):
    response = client.delete("/routing_rules/1")
    assert response.status_code == 404
