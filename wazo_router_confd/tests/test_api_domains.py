# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def test_create_domain(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    session.add(tenant)
    session.commit()

    response = client.post(
        "/domains/", json={"domain": "testdomain.com", "tenant_id": tenant.id}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": mock.ANY,
        "domain": "testdomain.com",
        "tenant_id": tenant.id,
    }


def test_create_duplicated_domain(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.post(
        "/domains/", json={"domain": "testdomain.com", "tenant_id": tenant.id}
    )
    assert response.status_code == 409


def test_get_domain(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.get("/domains/%s" % domain.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": domain.id,
        "domain": "testdomain.com",
        "tenant_id": tenant.id,
    }


def test_get_domain_not_found(app, client):
    response = client.get("/domains/1")
    assert response.status_code == 404


def test_get_domains(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.get("/domains/")
    assert response.status_code == 200
    assert response.json() == [
        {'id': domain.id, 'domain': 'testdomain.com', 'tenant_id': tenant.id}
    ]


def test_update_domain(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='test')
    tenant_2 = Tenant(name='test_2')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant, tenant_2])
    session.commit()
    #
    response = client.put(
        "/domains/%s" % domain.id,
        json={'domain': 'otherdomain.com', 'tenant_id': tenant_2.id},
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': domain.id,
        'domain': 'otherdomain.com',
        'tenant_id': tenant_2.id,
    }


def test_update_domain_not_found(app, client):
    response = client.put(
        "/domains/1", json={'domain': 'otherdomain.com', 'tenant_id': 2}
    )
    assert response.status_code == 404


def test_delete_domain(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='test')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.delete("/domains/%s" % domain.id)
    assert response.status_code == 200
    assert response.json() == {
        'id': domain.id,
        'domain': 'testdomain.com',
        'tenant_id': tenant.id,
    }


def test_delete_domain_not_found(app, client):
    response = client.delete("/domains/1")
    assert response.status_code == 404
