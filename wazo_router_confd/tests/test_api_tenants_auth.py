# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def test_create_tenant(app_auth, client_auth_with_token):
    response = client_auth_with_token.post(
        "/1.0/tenants",
        json={"name": "fabio", "uuid": "ffffffff-ffff-4c1c-ad1c-ffffffffffff"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "fabio",
        "uuid": "ffffffff-ffff-4c1c-ad1c-ffffffffffff",
    }


def test_create_duplicated_tenant(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    session.add(Tenant(name='fabio', uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff"))
    session.commit()
    #
    response = client_auth_with_token.post(
        "/1.0/tenants",
        json={"name": "fabio", "uuid": "0da63438-02a2-47c3-b05d-344d5d16cef7"},
    )
    assert response.status_code == 409


def test_get_tenant(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name='fabio', uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    session.add(tenant)
    session.commit()
    #
    response = client_auth_with_token.get("/1.0/tenants/%s" % str(tenant.uuid))
    assert response.status_code == 200
    assert response.json() == {"uuid": str(tenant.uuid), "name": "fabio"}


def test_get_tenant_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.get(
        "/1.0/tenants/df1d954f-2f10-4a62-aa3f-a4b3b496d508"
    )
    assert response.status_code == 404


def test_get_tenants(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name='fabio', uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    session.add(tenant)
    session.commit()
    #
    response = client_auth_with_token.get("/1.0/tenants")
    assert response.status_code == 200
    assert response.json() == {"items": [{'uuid': str(tenant.uuid), 'name': 'fabio'}]}


def test_update_tenant(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name='fabio', uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    session.add(tenant)
    session.commit()
    #
    response = client_auth_with_token.put(
        "/1.0/tenants/%s" % tenant.uuid, json={'name': 'alex'}
    )
    assert response.status_code == 200
    assert response.json() == {'uuid': str(tenant.uuid), 'name': 'alex'}


def test_update_tenant_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.put(
        "/1.0/tenants/42f72d9e-cfe2-42dd-8ae7-3bb9559c8ddb", json={'name': 'alex'}
    )
    assert response.status_code == 404


def test_delete_tenant(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name='fabio', uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    session.add(tenant)
    session.commit()
    #
    response = client_auth_with_token.delete("/1.0/tenants/%s" % tenant.uuid)
    assert response.status_code == 200
    assert response.json() == {'uuid': str(tenant.uuid), 'name': 'fabio'}


def test_delete_tenant_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.delete(
        "/1.0/tenants/14baa2f7-ed11-4adf-b223-ffeb6e5648cd"
    )
    assert response.status_code == 404
