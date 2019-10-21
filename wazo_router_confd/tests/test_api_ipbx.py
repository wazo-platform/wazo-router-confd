# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import get_app_and_client


@get_app_and_client
def test_create_ipbx(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain])
    session.commit()
    #
    response = client.post(
        "/ipbx/",
        json={
            "tenant_id": tenant.id,
            "domain_id": domain.id,
            "customer": 1,
            "ip_fqdn": "mypbx.com",
            "port": 5060,
            "ip_address": "10.0.0.1",
            "registered": True,
            "username": "user",
            "password": "password",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "tenant_id": 1,
        "domain_id": 1,
        "customer": 1,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "ip_address": "10.0.0.1",
        "registered": True,
        "username": "user",
    }


@get_app_and_client
def test_create_ipbx_password_too_long(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain])
    session.commit()
    #
    response = client.post(
        "/ipbx/",
        json={
            "tenant_id": tenant.id,
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


@get_app_and_client
def test_get_ipbxs(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX

    tenant = Tenant(name='fabio')
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
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.get("/ipbx/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "customer": 1,
            "ip_fqdn": "mypbx.com",
            "port": 5060,
            "ip_address": "10.0.0.1",
            "domain_id": domain.id,
            "tenant_id": tenant.id,
            "registered": True,
            "username": "user",
        }
    ]


@get_app_and_client
def test_get_ipbx(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX

    tenant = Tenant(name='fabio')
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
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.get("/ipbx/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "customer": 1,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "ip_address": "10.0.0.1",
        "domain_id": domain.id,
        "tenant_id": tenant.id,
        "registered": True,
        "username": "user",
    }


@get_app_and_client
def test_get_ipbx_not_found(app=None, client=None):
    response = client.get("/ipbx/1")
    assert response.status_code == 404


@get_app_and_client
def test_update_ipbx(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name='fabio')
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
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.put(
        "/ipbx/1",
        json={
            'ip_fqdn': 'mypbx2.com',
            'tenant_id': 2,
            'domain_id': 3,
            'username': 'otheruser',
            'registered': False,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "customer": 1,
        "ip_fqdn": "mypbx2.com",
        "port": 5060,
        "ip_address": "10.0.0.1",
        "domain_id": 3,
        "tenant_id": 2,
        "registered": False,
        "username": "otheruser",
    }


@get_app_and_client
def test_update_ipbx_not_found(app=None, client=None):
    response = client.put(
        "/ipbx/1",
        json={
            'ip_fqdn': 'mypbx2.com',
            'tenant_id': 2,
            'domain_id': 3,
            'username': 'otheruser',
            'registered': False,
        },
    )
    assert response.status_code == 404


@get_app_and_client
def test_delete_ipbx(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name='fabio')
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
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.delete("/ipbx/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "customer": 1,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "ip_address": "10.0.0.1",
        "domain_id": 1,
        "tenant_id": 1,
        "registered": True,
        "username": "user",
    }


@get_app_and_client
def test_delete_ipbx_not_found(app=None, client=None):
    response = client.delete("/ipbx/1")
    assert response.status_code == 404
