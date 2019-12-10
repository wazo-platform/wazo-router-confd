# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def test_create_domain(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    session.add(tenant)
    session.commit()

    response = client.post(
        "/domains/", json={"domain": "testdomain.com", "tenant_uuid": str(tenant.uuid)}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": mock.ANY,
        "domain": "testdomain.com",
        "tenant_uuid": str(tenant.uuid),
    }


def test_create_duplicated_domain(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.post(
        "/domains/", json={"domain": "testdomain.com", "tenant_uuid": str(tenant.uuid)}
    )
    assert response.status_code == 409


def test_get_domain(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.get("/domains/%s" % domain.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": domain.id,
        "domain": "testdomain.com",
        "tenant_uuid": str(tenant.uuid),
    }


def test_get_domain_not_found(app, client):
    response = client.get("/domains/1")
    assert response.status_code == 404


def test_get_domains(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.get("/domains/")
    assert response.status_code == 200
    assert response.json() == [
        {'id': domain.id, 'domain': 'testdomain.com', 'tenant_uuid': str(tenant.uuid)}
    ]


def test_update_domain(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='test', uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    tenant_2 = Tenant(name='test_2', uuid="38a334ec-8960-4367-80a3-b44c568df279")
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant, tenant_2])
    session.commit()
    #
    response = client.put(
        "/domains/%s" % domain.id,
        json={'domain': 'otherdomain.com', 'tenant_uuid': str(tenant_2.uuid)},
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': domain.id,
        'domain': 'otherdomain.com',
        'tenant_uuid': str(tenant_2.uuid),
    }


def test_update_domain_not_found(app, client):
    response = client.put(
        "/domains/1",
        json={
            'domain': 'otherdomain.com',
            'tenant_uuid': "facf0787-c93b-4997-a130-749a1bc41740",
        },
    )
    assert response.status_code == 404


def test_delete_domain(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='test', uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.delete("/domains/%s" % domain.id)
    assert response.status_code == 200
    assert response.json() == {
        'id': domain.id,
        'domain': 'testdomain.com',
        'tenant_uuid': str(tenant.uuid),
    }


def test_delete_domain_not_found(app, client):
    response = client.delete("/domains/1")
    assert response.status_code == 404
