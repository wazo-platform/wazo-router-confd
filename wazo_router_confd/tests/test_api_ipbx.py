# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def test_create_ipbx(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain])
    session.commit()
    #
    response = client.post(
        "/1.0/ipbx",
        json={
            "tenant_uuid": str(tenant.uuid),
            "domain_id": domain.id,
            "customer": 1,
            "ip_fqdn": "mypbx.com",
            "port": 5060,
            "ip_address": "10.0.0.1",
            "registered": True,
            "username": "user",
            "password": "password",
            "realm": "realm",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": mock.ANY,
        "tenant_uuid": str(tenant.uuid),
        "domain_id": domain.id,
        "normalization_profile_id": None,
        "customer": 1,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "ip_address": "10.0.0.1",
        "registered": True,
        "username": "user",
        "realm": "realm",
    }


def test_create_ipbx_password_too_long(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain])
    session.commit()
    #
    response = client.post(
        "/1.0/ipbx",
        json={
            "tenant_uuid": str(tenant.uuid),
            "domain_id": domain.id,
            "customer": 1,
            "ip_fqdn": "mypbx.com",
            "port": 5060,
            "ip_address": "10.0.0.1",
            "registered": True,
            "username": 'a' * 128,  # String(50)
            "password": 'a' * 248,  # String(192)
        },
    )
    assert response.status_code >= 400 and response.status_code < 500


def test_get_ipbxs(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX

    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        ip_address="10.0.0.1",
        registered=True,
        username='user',
        password='password',
        realm='realm',
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.get("/1.0/ipbx")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": ipbx.id,
            "customer": 1,
            "normalization_profile_id": None,
            "ip_fqdn": "mypbx.com",
            "port": 5060,
            "ip_address": "10.0.0.1",
            "domain_id": domain.id,
            "tenant_uuid": str(tenant.uuid),
            "registered": True,
            "username": "user",
            "realm": "realm",
        }
    ]


def test_get_ipbx(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX

    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        ip_address="10.0.0.1",
        registered=True,
        username='user',
        password='password',
        realm='realm',
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.get("/1.0/ipbx/%s" % ipbx.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": ipbx.id,
        "customer": 1,
        "normalization_profile_id": None,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "ip_address": "10.0.0.1",
        "domain_id": domain.id,
        "tenant_uuid": str(tenant.uuid),
        "registered": True,
        "username": "user",
        "realm": "realm",
    }


def test_get_ipbx_not_found(app, client):
    response = client.get("/1.0/ipbx/1")
    assert response.status_code == 404


def test_update_ipbx(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    tenant_2 = Tenant(name='sileht', uuid='ff69a896-8025-4b0c-993e-1ee6449091c5')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    domain_2 = Domain(domain='otherdomain.com', tenant=tenant_2)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        ip_address="10.0.0.1",
        registered=True,
        username='user',
        password='password',
        realm='realm',
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, tenant_2, domain, domain_2, ipbx])
    session.commit()
    #
    response = client.put(
        "/1.0/ipbx/%s" % ipbx.id,
        json={
            'ip_fqdn': 'mypbx2.com',
            'tenant_uuid': str(tenant_2.uuid),
            'domain_id': domain_2.id,
            'username': 'otheruser',
            'password': 'otherpassword',
            'registered': False,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": ipbx.id,
        "customer": 1,
        "normalization_profile_id": None,
        "ip_fqdn": "mypbx2.com",
        "port": 5060,
        "ip_address": "10.0.0.1",
        "domain_id": domain_2.id,
        "tenant_uuid": str(tenant_2.uuid),
        "registered": False,
        "username": "otheruser",
        "realm": "realm",
    }


def test_update_ipbx_not_found(app, client):
    response = client.put(
        "/1.0/ipbx/1",
        json={
            'ip_fqdn': 'mypbx2.com',
            'tenant_uuid': "2639b15e-4e36-4815-ad52-be57a06d7095",
            'domain_id': 3,
            'username': 'otheruser',
            'registered': False,
        },
    )
    assert response.status_code == 404


def test_delete_ipbx(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        ip_address="10.0.0.1",
        username='user',
        password='password',
        realm='realm',
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.delete("/1.0/ipbx/%s" % ipbx.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": ipbx.id,
        "customer": 1,
        "normalization_profile_id": None,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "ip_address": "10.0.0.1",
        "domain_id": domain.id,
        "tenant_uuid": str(tenant.uuid),
        "registered": True,
        "username": "user",
        "realm": "realm",
    }


def test_delete_ipbx_not_found(app, client):
    response = client.delete("/1.0/ipbx/1")
    assert response.status_code == 404
