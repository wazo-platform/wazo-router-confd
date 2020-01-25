# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def create_routing_rule(app_auth, tenant_uuid, suffix=1):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.routing_group import RoutingGroup
    from wazo_router_confd.models.routing_rule import RoutingRule

    session = SessionLocal(bind=app_auth.engine)
    tenant = session.query(Tenant).filter(Tenant.uuid == tenant_uuid).first()
    if tenant is None:
        tenant = Tenant(name="tenant_{}".format(suffix), uuid=tenant_uuid)
        session.add(tenant)
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
    routing_group = RoutingGroup(tenant=tenant, routing_rule=routing_rule)

    session.add_all(
        [
            tenant,
            domain,
            carrier,
            carrier_trunk,
            carrier_trunk_2,
            ipbx,
            routing_rule,
            routing_group,
        ]
    )
    session.commit()

    session.flush()

    return routing_rule, ipbx, carrier_trunk, tenant, session


def test_create_routing_rule(app_auth, client_auth_with_token):
    _, ipbx, carrier_trunk, _, _ = create_routing_rule(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff"
    )
    #
    response = client_auth_with_token.post(
        "/1.0/routing-rules",
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


def test_get_routing_rule(app_auth, client_auth_with_token):
    routing_rule, ipbx, carrier_trunk, _, _ = create_routing_rule(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff"
    )
    #
    response = client_auth_with_token.get("/1.0/routing-rules/%s" % routing_rule.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": routing_rule.id,
        "prefix": "39",
        "carrier_trunk_id": carrier_trunk.id,
        "ipbx_id": ipbx.id,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "route_type": "pstn",
    }


def test_get_routing_rule_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.get("/1.0/routing-rules/1")
    assert response.status_code == 404


def test_get_routing_rules(app_auth, client_auth_with_token):
    routing_rule, ipbx, carrier_trunk, _, _ = create_routing_rule(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff"
    )
    #
    response = client_auth_with_token.get("/1.0/routing-rules")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": routing_rule.id,
                "prefix": "39",
                "carrier_trunk_id": carrier_trunk.id,
                "ipbx_id": ipbx.id,
                "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
                "route_type": "pstn",
            }
        ]
    }


def test_update_routing_rule(app_auth, client_auth_with_token):
    routing_rule, _, _, _, _ = create_routing_rule(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff"
    )
    _, ipbx_2, carrier_trunk_2, _, _ = create_routing_rule(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff", 2
    )
    #
    response = client_auth_with_token.put(
        "/1.0/routing-rules/%s" % routing_rule.id,
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


def test_update_routing_rule_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.put(
        "/1.0/routing-rules/1",
        json={
            'prefix': '40',
            'carrier_trunk_id': 2,
            'ipbx_id': 1,
            'did_regex': r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
            'route_type': "pstn",
        },
    )
    assert response.status_code == 404


def test_delete_routing_rule(app_auth, client_auth_with_token):
    routing_rule, ipbx, carrier_trunk, _, _ = create_routing_rule(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff"
    )
    #
    response = client_auth_with_token.delete("/1.0/routing-rules/%s" % routing_rule.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": routing_rule.id,
        "prefix": "39",
        "carrier_trunk_id": carrier_trunk.id,
        "ipbx_id": ipbx.id,
        "did_regex": r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
        "route_type": "pstn",
    }


def test_delete_routing_rule_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.delete("/1.0/routing-rules/1")
    assert response.status_code == 404
