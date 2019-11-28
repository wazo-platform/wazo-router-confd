# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def test_create_tenant(app, client):
    response = client.post(
        "/tenants/",
        json={"name": "fabio", "uuid": "fc8faf32-1bf8-47a4-9d82-f369799b3006"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": mock.ANY,
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
        "/tenants/",
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
    response = client.get("/tenants/%s" % tenant.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": tenant.id,
        "name": "fabio",
        "uuid": "fc8faf32-1bf8-47a4-9d82-f369799b3006",
    }


def test_get_tenant_not_found(app, client):
    response = client.get("/tenants/1")
    assert response.status_code == 404


def test_get_tenants(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid="fc8faf32-1bf8-47a4-9d82-f369799b3006")
    session.add(tenant)
    session.commit()
    #
    response = client.get("/tenants/")
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': tenant.id,
            'name': 'fabio',
            "uuid": "fc8faf32-1bf8-47a4-9d82-f369799b3006",
        }
    ]


def test_update_tenant(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid="fc8faf32-1bf8-47a4-9d82-f369799b3006")
    session.add(tenant)
    session.commit()
    #
    response = client.put("/tenants/%s" % tenant.id, json={'name': 'alex'})
    assert response.status_code == 200
    assert response.json() == {
        'id': tenant.id,
        'name': 'alex',
        "uuid": "fc8faf32-1bf8-47a4-9d82-f369799b3006",
    }


def test_update_tenant_not_found(app, client):
    response = client.put("/tenants/1", json={'name': 'alex'})
    assert response.status_code == 404


def test_delete_tenant(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid="fc8faf32-1bf8-47a4-9d82-f369799b3006")
    session.add(tenant)
    session.commit()
    #
    response = client.delete("/tenants/%s" % tenant.id)
    assert response.status_code == 200
    assert response.json() == {
        'id': tenant.id,
        'name': 'fabio',
        "uuid": "fc8faf32-1bf8-47a4-9d82-f369799b3006",
    }


def test_delete_tenant_not_found(app, client):
    response = client.delete("/tenants/1")
    assert response.status_code == 404
