# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def test_kamailio_auth_username(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.services import password

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        customer=1,
        ip_fqdn='mypbx.com',
        domain=domain,
        registered=True,
        username='user',
        password=password.hash('password'),
        password_ha1=password.hash_ha1('user', domain.domain, 'password'),
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.post(
        "/kamailio/auth", json={"source_ip": "10.0.0.1", "username": "user"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "tenant_id": ipbx.tenant_id,
        "carrier_trunk_id": None,
        "ipbx_id": ipbx.id,
        "domain": domain.domain,
        "username": ipbx.username,
        "password_ha1": ipbx.password_ha1,
    }


def test_kamailio_auth_username_password(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.services import password

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        customer=1,
        ip_fqdn='mypbx.com',
        domain=domain,
        registered=True,
        username='user',
        password=password.hash('password'),
        password_ha1=password.hash_ha1('user', domain.domain, 'password'),
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.post(
        "/kamailio/auth",
        json={"source_ip": "10.0.0.1", "username": "user", "password": "password"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "tenant_id": ipbx.tenant_id,
        "carrier_trunk_id": None,
        "ipbx_id": ipbx.id,
        "domain": domain.domain,
        "username": ipbx.username,
        "password_ha1": ipbx.password_ha1,
    }


def test_kamailio_auth_username_domain(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.services import password

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        customer=1,
        ip_fqdn='mypbx.com',
        domain=domain,
        registered=True,
        username='user',
        password=password.hash('password'),
        password_ha1=password.hash_ha1('user', domain.domain, 'password'),
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.post(
        "/kamailio/auth",
        json={"source_ip": "10.0.0.1", "username": "user", "domain": "testdomain.com"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "tenant_id": ipbx.tenant_id,
        "carrier_trunk_id": None,
        "ipbx_id": ipbx.id,
        "domain": domain.domain,
        "username": ipbx.username,
        "password_ha1": ipbx.password_ha1,
    }


def test_kamailio_auth_username_fails(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.services import password

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        customer=1,
        ip_fqdn='mypbx.com',
        domain=domain,
        registered=True,
        username='user',
        password_ha1=password.hash_ha1('user', domain.domain, 'password'),
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.post(
        "/kamailio/auth", json={"source_ip": "10.0.0.1", "username": "user_is_wrong"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": False,
        "tenant_id": None,
        "carrier_trunk_id": None,
        "ipbx_id": None,
        "domain": None,
        "username": None,
        "password_ha1": None,
    }


def test_kamailio_auth_username_domain_fails(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.services import password

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        customer=1,
        ip_fqdn='mypbx.com',
        domain=domain,
        registered=True,
        username='user',
        password=password.hash('password'),
        password_ha1=password.hash_ha1('user', domain.domain, 'password'),
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.post(
        "/kamailio/auth",
        json={
            "source_ip": "10.0.0.1",
            "username": "user",
            "domain": "anotherdomain.com",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": False,
        "tenant_id": None,
        "carrier_trunk_id": None,
        "ipbx_id": None,
        "domain": None,
        "username": None,
        "password_ha1": None,
    }


def test_kamailio_auth_ip_address_username(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.services import password

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        customer=1,
        ip_fqdn='mypbx.com',
        domain=domain,
        registered=True,
        ip_address="10.0.0.1",
        username='user',
        password=password.hash('password'),
        password_ha1=password.hash_ha1('user', domain.domain, 'password'),
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.post(
        "/kamailio/auth", json={"source_ip": "10.0.0.1", "username": "user"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "tenant_id": ipbx.tenant_id,
        "carrier_trunk_id": None,
        "ipbx_id": ipbx.id,
        "domain": domain.domain,
        "username": ipbx.username,
        "password_ha1": ipbx.password_ha1,
    }


def test_kamailio_auth_ip_address_username_fails(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.services import password

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        customer=1,
        ip_fqdn='mypbx.com',
        domain=domain,
        registered=True,
        ip_address="10.0.0.1",
        username='user',
        password_ha1=password.hash_ha1('user', domain.domain, 'password'),
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.post(
        "/kamailio/auth",
        json={
            "source_ip": "10.0.0.1",
            "username": "user",
            "password": "password_is_wrong",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": False,
        "tenant_id": None,
        "carrier_trunk_id": None,
        "ipbx_id": None,
        "domain": None,
        "username": None,
        "password_ha1": None,
    }


def test_kamailio_auth_ip_address(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        customer=1,
        ip_fqdn='mypbx.com',
        domain=domain,
        registered=False,
        ip_address="10.0.0.1",
        username=None,
        password=None,
        password_ha1=None,
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.post(
        "/kamailio/auth", json={"source_ip": "10.0.0.1", "username": ""}
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "tenant_id": ipbx.tenant_id,
        "carrier_trunk_id": None,
        "ipbx_id": ipbx.id,
        "domain": domain.domain,
        "username": ipbx.username,
        "password_ha1": ipbx.password_ha1,
    }


def test_kamailio_auth_ip_address_fails(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.services import password

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        customer=1,
        ip_fqdn='mypbx.com',
        domain=domain,
        registered=True,
        ip_address="10.0.0.2",
        username='user',
        password_ha1=password.hash_ha1('user', domain.domain, 'password'),
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.post(
        "/kamailio/auth", json={"source_ip": "10.0.0.1", "username": ""}
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": False,
        "tenant_id": None,
        "carrier_trunk_id": None,
        "ipbx_id": None,
        "domain": None,
        "username": None,
        "password_ha1": None,
    }


def test_kamailio_auth_ip_address_disabled(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.services import password

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        customer=1,
        ip_fqdn='mypbx.com',
        domain=domain,
        registered=True,
        ip_address=None,
        username='user',
        password_ha1=password.hash_ha1('user', domain.domain, 'password'),
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.post(
        "/kamailio/auth", json={"source_ip": "10.0.0.1", "username": ""}
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "tenant_id": ipbx.tenant_id,
        "carrier_trunk_id": None,
        "ipbx_id": ipbx.id,
        "domain": domain.domain,
        "username": ipbx.username,
        "password_ha1": ipbx.password_ha1,
    }
