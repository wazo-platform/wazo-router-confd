# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import get_app_and_client


@get_app_and_client
def test_kamailio_auth_username_password(app=None, client=None):
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
        "ipbx": {
            "id": ipbx.id,
            "customer": ipbx.customer,
            "ip_fqdn": ipbx.ip_fqdn,
            "port": ipbx.port,
            "domain_id": ipbx.domain_id,
            "tenant_id": ipbx.tenant_id,
            "registered": ipbx.registered,
            "username": ipbx.username,
        },
    }


@get_app_and_client
def test_kamailio_auth_username_password_fails(app=None, client=None):
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
    assert response.json() == {"success": False, "ipbx": None}
