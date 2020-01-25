# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def test_create_domain(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name='fabio', uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    session.add(tenant)
    session.commit()

    response = client_auth_with_token.post(
        "/1.0/domains",
        json={"domain": "testdomain.com", "tenant_uuid": str(tenant.uuid)},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": mock.ANY,
        "domain": "testdomain.com",
        "tenant_uuid": str(tenant.uuid),
    }


def test_create_duplicated_domain(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name='fabio', uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client_auth_with_token.post(
        "/1.0/domains",
        json={"domain": "testdomain.com", "tenant_uuid": str(tenant.uuid)},
    )
    assert response.status_code == 409


def test_get_domain(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name='fabio', uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client_auth_with_token.get("/1.0/domains/%s" % domain.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": domain.id,
        "domain": "testdomain.com",
        "tenant_uuid": str(tenant.uuid),
    }


def test_get_domain_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.get("/1.0/domains/1")
    assert response.status_code == 404


def test_get_domains(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name='fabio', uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client_auth_with_token.get("/1.0/domains")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                'id': domain.id,
                'domain': 'testdomain.com',
                'tenant_uuid': str(tenant.uuid),
            }
        ]
    }


def test_update_domain(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name='test', uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    tenant_2 = Tenant(name='test_2', uuid="38a334ec-8960-4367-80a3-b44c568df279")
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant, tenant_2])
    session.commit()
    #
    response = client_auth_with_token.put(
        "/1.0/domains/%s" % domain.id,
        json={'domain': 'otherdomain.com', 'tenant_uuid': str(tenant_2.uuid)},
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': domain.id,
        'domain': 'otherdomain.com',
        'tenant_uuid': str(tenant_2.uuid),
    }


def test_update_domain_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.put(
        "/1.0/domains/1",
        json={
            'domain': 'otherdomain.com',
            'tenant_uuid': "facf0787-c93b-4997-a130-749a1bc41740",
        },
    )
    assert response.status_code == 404


def test_delete_domain(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name='test', uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client_auth_with_token.delete("/1.0/domains/%s" % domain.id)
    assert response.status_code == 200
    assert response.json() == {
        'id': domain.id,
        'domain': 'testdomain.com',
        'tenant_uuid': str(tenant.uuid),
    }


def test_delete_domain_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.delete("/1.0/domains/1")
    assert response.status_code == 404
