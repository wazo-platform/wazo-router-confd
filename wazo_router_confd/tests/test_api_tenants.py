# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def test_create_tenant(app, client):
    response = client.post(
        "/1.0/tenants",
        json={"name": "fabio", "uuid": "fc8faf32-1bf8-47a4-9d82-f369799b3006"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "fabio",
        "uuid": "fc8faf32-1bf8-47a4-9d82-f369799b3006",
    }


def test_create_duplicated_tenant(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.add(Tenant(name='fabio', uuid="fc8faf32-1bf8-47a4-9d82-f369799b3006"))
    session.commit()
    #
    response = client.post(
        "/1.0/tenants",
        json={"name": "fabio", "uuid": "0da63438-02a2-47c3-b05d-344d5d16cef7"},
    )
    assert response.status_code == 409


def test_get_tenant(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid="fc8faf32-1bf8-47a4-9d82-f369799b3006")
    session.add(tenant)
    session.commit()
    #
    response = client.get("/1.0/tenants/%s" % str(tenant.uuid))
    assert response.status_code == 200
    assert response.json() == {"uuid": str(tenant.uuid), "name": "fabio"}


def test_get_tenant_not_found(app, client):
    response = client.get("/1.0/tenants/df1d954f-2f10-4a62-aa3f-a4b3b496d508")
    assert response.status_code == 404


def test_get_tenants(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid="fc8faf32-1bf8-47a4-9d82-f369799b3006")
    session.add(tenant)
    session.commit()
    #
    response = client.get("/1.0/tenants")
    assert response.status_code == 200
    assert response.json() == {"items": [{'uuid': str(tenant.uuid), 'name': 'fabio'}]}


def test_update_tenant(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid="fc8faf32-1bf8-47a4-9d82-f369799b3006")
    session.add(tenant)
    session.commit()
    #
    response = client.put("/1.0/tenants/%s" % tenant.uuid, json={'name': 'alex'})
    assert response.status_code == 200
    assert response.json() == {'uuid': str(tenant.uuid), 'name': 'alex'}


def test_update_tenant_not_found(app, client):
    response = client.put(
        "/1.0/tenants/42f72d9e-cfe2-42dd-8ae7-3bb9559c8ddb", json={'name': 'alex'}
    )
    assert response.status_code == 404


def test_delete_tenant(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid="fc8faf32-1bf8-47a4-9d82-f369799b3006")
    session.add(tenant)
    session.commit()
    #
    response = client.delete("/1.0/tenants/%s" % tenant.uuid)
    assert response.status_code == 200
    assert response.json() == {'uuid': str(tenant.uuid), 'name': 'fabio'}


def test_delete_tenant_not_found(app, client):
    response = client.delete("/1.0/tenants/14baa2f7-ed11-4adf-b223-ffeb6e5648cd")
    assert response.status_code == 404
