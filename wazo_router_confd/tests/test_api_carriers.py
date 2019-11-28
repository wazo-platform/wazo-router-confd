# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import get_app_and_client


@get_app_and_client
def test_create_carrier(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant")
    session = SessionLocal(bind=app.engine)
    session.add(tenant)
    session.commit()
    #
    response = client.post("/carriers/", json={"name": "carrier1", "tenant_id": 1})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "carrier1", "tenant_id": 1}


@get_app_and_client
def test_create_duplicated_carrier(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant")
    carrier = Carrier(name='carrier1', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier])
    session.commit()
    #
    response = client.post("/carriers/", json={"name": "carrier1", "tenant_id": 1})
    assert response.status_code == 409


@get_app_and_client
def test_get_carrier(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant")
    carrier = Carrier(name='carrier1', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier])
    session.commit()
    #
    response = client.get("/carriers/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "carrier1", "tenant_id": 1}


@get_app_and_client
def test_get_carrier_not_found(app=None, client=None):
    response = client.get("/carriers/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_carriers(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant")
    carrier = Carrier(name='carrier1', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier])
    session.commit()
    #
    response = client.get("/carriers/")
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'name': 'carrier1', 'tenant_id': 1}]


@get_app_and_client
def test_update_carrier(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant1 = Tenant(name="tenant1")
    tenant2 = Tenant(name="tenant2")
    carrier = Carrier(name='carrier1', tenant=tenant1)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant1, tenant2, carrier])
    session.commit()
    #
    response = client.put(
        "/carriers/1", json={'name': 'updated_carrier', 'tenant_id': 2}
    )
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'updated_carrier', 'tenant_id': 2}


@get_app_and_client
def test_update_carrier_not_found(app=None, client=None):
    response = client.put(
        "/carriers/1", json={'name': 'updated_carrier', 'tenant_id': 2}
    )
    assert response.status_code == 404


@get_app_and_client
def test_delete_carrier(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant")
    carrier = Carrier(name='carrier1', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier])
    session.commit()
    #
    response = client.delete("/carriers/1")
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'carrier1', 'tenant_id': 1}


@get_app_and_client
def test_delete_carrier_not_found(app=None, client=None):
    response = client.delete("/carriers/1")
    assert response.status_code == 404
