# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def test_create_carrier(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    session = SessionLocal(bind=app_auth.engine)
    session.add(tenant)
    session.commit()
    #
    response = client_auth_with_token.post(
        "/1.0/carriers", json={"name": "carrier1", "tenant_uuid": str(tenant.uuid)}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": mock.ANY,
        "name": "carrier1",
        "tenant_uuid": str(tenant.uuid),
    }


def test_create_duplicated_carrier(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    carrier = Carrier(name='carrier1', tenant=tenant)
    session = SessionLocal(bind=app_auth.engine)
    session.add_all([tenant, carrier])
    session.commit()
    #
    response = client_auth_with_token.post(
        "/1.0/carriers", json={"name": "carrier1", "tenant_uuid": str(tenant.uuid)}
    )
    assert response.status_code == 409


def test_get_carrier(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    carrier = Carrier(name='carrier1', tenant=tenant)
    session = SessionLocal(bind=app_auth.engine)
    session.add_all([tenant, carrier])
    session.commit()
    #
    response = client_auth_with_token.get("/1.0/carriers/%d" % carrier.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": carrier.id,
        "name": "carrier1",
        "tenant_uuid": str(tenant.uuid),
    }


def test_get_carrier_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.get("/1.0/carriers/1")
    assert response.status_code == 404


def test_get_carriers(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    carrier = Carrier(name='carrier1', tenant=tenant)
    session = SessionLocal(bind=app_auth.engine)
    session.add_all([tenant, carrier])
    session.commit()
    #
    response = client_auth_with_token.get("/1.0/carriers")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {'id': carrier.id, 'name': 'carrier1', 'tenant_uuid': str(tenant.uuid)}
        ]
    }


def test_update_carrier(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant1 = Tenant(name="tenant1", uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    tenant2 = Tenant(name="tenant2", uuid="458eb1a1-1769-4b7a-9970-45c5c9c2abe3")
    carrier = Carrier(name='carrier1', tenant=tenant1)
    session = SessionLocal(bind=app_auth.engine)
    session.add_all([tenant1, tenant2, carrier])
    session.commit()
    #
    response = client_auth_with_token.put(
        "/1.0/carriers/%d" % carrier.id,
        json={'name': 'updated_carrier', 'tenant_uuid': str(tenant2.uuid)},
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': carrier.id,
        'name': 'updated_carrier',
        'tenant_uuid': str(tenant2.uuid),
    }


def test_update_carrier_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.put(
        "/1.0/carriers/1",
        json={
            'name': 'updated_carrier',
            'tenant_uuid': "458eb1a1-1769-4b7a-9970-45c5c9c2abe3",
        },
    )
    assert response.status_code == 404


def test_delete_carrier(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    carrier = Carrier(name='carrier1', tenant=tenant)
    session = SessionLocal(bind=app_auth.engine)
    session.add_all([tenant, carrier])
    session.commit()
    #
    response = client_auth_with_token.delete("/1.0/carriers/%d" % carrier.id)
    assert response.status_code == 200
    assert response.json() == {
        'id': carrier.id,
        'name': 'carrier1',
        'tenant_uuid': str(tenant.uuid),
    }


def test_delete_carrier_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.delete("/1.0/carriers/1")
    assert response.status_code == 404
