# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def test_create_carrier(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant")
    session = SessionLocal(bind=app.engine)
    session.add(tenant)
    session.commit()
    #
    response = client.post("/carriers/", json={"name": "carrier1", "tenant_id": tenant.id})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "carrier1", "tenant_id": tenant.id}


def test_create_duplicated_carrier(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant")
    carrier = Carrier(name='carrier1', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier])
    session.commit()
    #
    response = client.post("/carriers/", json={"name": "carrier1", "tenant_id": tenant.id})
    assert response.status_code == 409


def test_get_carrier(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant")
    carrier = Carrier(name='carrier1', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier])
    session.commit()
    #
    response = client.get("/carriers/%d" % carrier.id)
    assert response.status_code == 200
    assert response.json() == {"id": carrier.id, "name": "carrier1", "tenant_id": tenant.id}


def test_get_carrier_not_found(app, client):
    response = client.get("/carriers/1")
    assert response.status_code == 404


def test_get_carriers(app, client):
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
    assert response.json() == [{'id': carrier.id, 'name': 'carrier1', 'tenant_id': tenant.id}]


def test_update_carrier(app, client):
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
        "/carriers/%d" % carrier.id, json={'name': 'updated_carrier', 'tenant_id': tenant2.id}
    )
    assert response.status_code == 200
    assert response.json() == {'id': carrier.id, 'name': 'updated_carrier', 'tenant_id': tenant2.id}


def test_update_carrier_not_found(app, client):
    response = client.put(
        "/carriers/1", json={'name': 'updated_carrier', 'tenant_id': 2}
    )
    assert response.status_code == 404


def test_delete_carrier(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant")
    carrier = Carrier(name='carrier1', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier])
    session.commit()
    #
    response = client.delete("/carriers/%d" % carrier.id)
    assert response.status_code == 200
    assert response.json() == {'id': carrier.id, 'name': 'carrier1', 'tenant_id': tenant.id}


def test_delete_carrier_not_found(app, client):
    response = client.delete("/carriers/1")
    assert response.status_code == 404
