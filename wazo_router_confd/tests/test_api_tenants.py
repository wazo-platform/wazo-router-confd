# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import get_app_and_client


@get_app_and_client
def test_create_tenant(app=None, client=None):
    response = client.post("/tenants/", json={"name": "fabio", "uuid": "fc8faf321bf847a49d82f369799b3006"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "fabio", "uuid": "fc8faf321bf847a49d82f369799b3006"}


@get_app_and_client
def test_create_duplicated_tenant(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.add(Tenant(name='fabio'))
    session.commit()
    #
    response = client.post("/tenants/", json={"name": "fabio"})
    assert response.status_code == 409


@get_app_and_client
def test_get_tenant(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.add(Tenant(name='fabio', uuid='fc8faf321bf847a49d82f369799b3006'))
    session.commit()
    #
    response = client.get("/tenants/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "fabio", "uuid": "fc8faf321bf847a49d82f369799b3006"}


@get_app_and_client
def test_get_tenant_not_found(app=None, client=None):
    response = client.get("/tenants/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_tenants(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.add(Tenant(name='fabio', uuid="fc8faf321bf847a49d82f369799b3006"))
    session.commit()
    #
    response = client.get("/tenants/")
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'name': 'fabio', "uuid": "fc8faf321bf847a49d82f369799b3006"}]


@get_app_and_client
def test_update_tenant(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.add(Tenant(name='fabio', uuid="fc8faf321bf847a49d82f369799b3006"))
    session.commit()
    #
    response = client.put("/tenants/1", json={'name': 'alex'})
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'alex', "uuid": "fc8faf321bf847a49d82f369799b3006"}


@get_app_and_client
def test_update_tenant_not_found(app=None, client=None):
    response = client.put("/tenants/1", json={'name': 'alex'})
    assert response.status_code == 404


@get_app_and_client
def test_delete_tenant(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.add(Tenant(name='fabio', uuid="fc8faf321bf847a49d82f369799b3006"))
    session.commit()
    #
    response = client.delete("/tenants/1")
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'fabio', "uuid": "fc8faf321bf847a49d82f369799b3006"}


@get_app_and_client
def test_delete_tenant_not_found(app=None, client=None):
    response = client.delete("/tenants/1")
    assert response.status_code == 404
