# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def create_routing_group(app_auth, tenant_uuid, suffix=1):
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

    routing_rule = RoutingRule(
        prefix="39",
        carrier_trunk=carrier_trunk,
        ipbx=ipbx,
        did_regex=r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
        route_type="pstn",
    )

    session.add_all([domain, carrier, ipbx, routing_rule])
    session.commit()

    routing_group = RoutingGroup(routing_rule=routing_rule, tenant=tenant)
    session.add(routing_group)

    session.commit()
    session.flush()

    return routing_group, routing_rule, tenant, session


def test_create_routing_group(app_auth, client_auth_with_token):
    routing_group, routing_rule, tenant, _ = create_routing_group(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff"
    )
    #
    response = client_auth_with_token.post(
        "/1.0/routing-groups",
        json={"routing_rule_id": routing_rule.id, "tenant_uuid": str(tenant.uuid)},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": routing_group.id + 1,
        "routing_rule_id": routing_rule.id,
        "tenant_uuid": str(tenant.uuid),
    }


def test_get_routing_group(app_auth, client_auth_with_token):
    routing_group, routing_rule, tenant, _ = create_routing_group(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff"
    )
    #
    response = client_auth_with_token.get("/1.0/routing-groups/%s" % routing_group.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": routing_group.id,
        "routing_rule_id": routing_rule.id,
        "tenant_uuid": str(tenant.uuid),
    }


def test_get_routing_group_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.get("/1.0/routing-groups/1")
    assert response.status_code == 404


def test_get_routing_groups(app_auth, client_auth_with_token):
    routing_group, routing_rule, tenant, _ = create_routing_group(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff"
    )
    #
    response = client_auth_with_token.get("/1.0/routing-groups")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": routing_group.id,
                "routing_rule_id": routing_rule.id,
                "tenant_uuid": str(tenant.uuid),
            }
        ]
    }


def test_update_routing_group(app_auth, client_auth_with_token):
    routing_group, _, _, _ = create_routing_group(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff"
    )
    _, routing_rule_2, tenant_2, _ = create_routing_group(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff", 2
    )
    #
    response = client_auth_with_token.put(
        "/1.0/routing-groups/%s" % routing_group.id,
        json={'routing_rule_id': routing_rule_2.id, 'tenant_uuid': str(tenant_2.uuid)},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": routing_group.id,
        "routing_rule_id": routing_rule_2.id,
        "tenant_uuid": str(tenant_2.uuid),
    }


def test_update_routing_group_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.put(
        "/1.0/routing-groups/1",
        json={
            'routing_rule_id': 2,
            'tenant_uuid': '7e614b21-a9c0-4118-a3e8-6748bc24c5ee',
        },
    )
    assert response.status_code == 404


def test_delete_routing_group(app_auth, client_auth_with_token):
    routing_group, routing_rule, tenant, _ = create_routing_group(
        app_auth, "ffffffff-ffff-4c1c-ad1c-ffffffffffff"
    )
    #
    response = client_auth_with_token.delete(
        "/1.0/routing-groups/%s" % routing_group.id
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": routing_group.id,
        "routing_rule_id": routing_rule.id,
        "tenant_uuid": str(tenant.uuid),
    }


def test_delete_routing_group_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.delete("/1.0/routing-groups/1")
    assert response.status_code == 404
