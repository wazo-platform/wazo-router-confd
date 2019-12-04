# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def test_create_ipbx(app, client):
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
        "id": mock.ANY,
        "tenant_id": tenant.id,
        "domain_id": domain.id,
        "normalization_profile_id": None,
        "customer": 1,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "ip_address": "10.0.0.1",
        "registered": True,
        "username": "user",
    }


def test_create_ipbx_password_too_long(app, client):
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


def test_get_ipbxs(app, client):
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
            "id": ipbx.id,
            "customer": 1,
            "normalization_profile_id": None,
            "ip_fqdn": "mypbx.com",
            "port": 5060,
            "ip_address": "10.0.0.1",
            "domain_id": domain.id,
            "tenant_id": tenant.id,
            "registered": True,
            "username": "user",
        }
    ]


def test_get_ipbx(app, client):
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
    response = client.get("/ipbx/%s" % ipbx.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": ipbx.id,
        "customer": 1,
        "normalization_profile_id": None,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "ip_address": "10.0.0.1",
        "domain_id": domain.id,
        "tenant_id": tenant.id,
        "registered": True,
        "username": "user",
    }


def test_get_ipbx_not_found(app, client):
    response = client.get("/ipbx/1")
    assert response.status_code == 404


def test_update_ipbx(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name='fabio')
    tenant_2 = Tenant(name='sileht')
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
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, tenant_2, domain, domain_2, ipbx])
    session.commit()
    #
    response = client.put(
        "/ipbx/%s" % ipbx.id,
        json={
            'ip_fqdn': 'mypbx2.com',
            'tenant_id': tenant_2.id,
            'domain_id': domain_2.id,
            'username': 'otheruser',
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
        "tenant_id": tenant_2.id,
        "registered": False,
        "username": "otheruser",
    }


def test_update_ipbx_not_found(app, client):
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


def test_delete_ipbx(app, client):
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
    response = client.delete("/ipbx/%s" % ipbx.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": ipbx.id,
        "customer": 1,
        "normalization_profile_id": None,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "ip_address": "10.0.0.1",
        "domain_id": domain.id,
        "tenant_id": tenant.id,
        "registered": True,
        "username": "user",
    }


def test_delete_ipbx_not_found(app, client):
    response = client.delete("/ipbx/1")
    assert response.status_code == 404
