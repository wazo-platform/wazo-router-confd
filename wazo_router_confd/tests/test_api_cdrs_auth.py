# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock

from dateutil.parser import parse


def test_create_cdr(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    session = SessionLocal(bind=app_auth.engine)
    session.add(tenant)
    session.commit()
    #
    response = client_auth_with_token.post(
        "/1.0/cdrs",
        json={
            "from_uri": "100@localhost",
            "to_uri": "200@localhost",
            "call_id": "1000",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "duration": 60,
            "call_start": "2019-09-01T00:00:00",
            "tenant_uuid": str(tenant.uuid),
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": mock.ANY,
        "from_uri": "100@localhost",
        "to_uri": "200@localhost",
        "call_id": "1000",
        "source_ip": "10.0.0.1",
        "source_port": 5060,
        "duration": 60,
        "call_start": "2019-09-01T00:00:00",
        "tenant_uuid": str(tenant.uuid),
    }


def test_get_cdr(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.cdr import CDR
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name="tenant", uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    cdr = CDR(
        from_uri="100@localhost",
        to_uri="200@localhost",
        call_id="1000",
        source_ip="10.0.0.1",
        source_port=5060,
        duration=60,
        call_start=parse("2019-09-01T00:00:00"),
        tenant=tenant,
    )
    session.add_all([tenant, cdr])
    session.commit()
    #
    response = client_auth_with_token.get("/1.0/cdrs/%s" % cdr.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": cdr.id,
        "from_uri": "100@localhost",
        "to_uri": "200@localhost",
        "call_id": "1000",
        "source_ip": "10.0.0.1",
        "source_port": 5060,
        "duration": 60,
        "call_start": "2019-09-01T00:00:00",
        "tenant_uuid": str(tenant.uuid),
    }


def test_get_cdr_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.get("/1.0/cdrs/1")
    assert response.status_code == 404


def test_get_cdrs(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.cdr import CDR
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name="tenant", uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    cdr = CDR(
        from_uri="100@localhost",
        to_uri="200@localhost",
        call_id="1000",
        source_ip="10.0.0.1",
        source_port=5060,
        duration=60,
        call_start=parse("2019-09-01T00:00:00"),
        tenant=tenant,
    )
    session.add_all([tenant, cdr])
    session.commit()
    #
    response = client_auth_with_token.get("/1.0/cdrs")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": cdr.id,
                "from_uri": "100@localhost",
                "to_uri": "200@localhost",
                "call_id": "1000",
                "source_ip": "10.0.0.1",
                "source_port": 5060,
                "duration": 60,
                "call_start": "2019-09-01T00:00:00",
                "tenant_uuid": str(tenant.uuid),
            }
        ]
    }


def test_update_cdr(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.cdr import CDR
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name="tenant", uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    cdr = CDR(
        from_uri="100@localhost",
        to_uri="200@localhost",
        call_id="1000",
        source_ip="10.0.0.1",
        source_port=5060,
        duration=60,
        call_start=parse("2019-09-01T00:00:00"),
        tenant=tenant,
    )
    session.add_all([tenant, cdr])
    session.commit()
    #
    response = client_auth_with_token.put(
        "/1.0/cdrs/%s" % cdr.id,
        json={
            "id": cdr.id,
            "from_uri": "100@localhost",
            "to_uri": "200@localhost",
            "call_id": "1000",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "duration": 61,
            "call_start": "2019-09-01T00:00:00",
            "tenant_uuid": str(tenant.uuid),
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": cdr.id,
        "from_uri": "100@localhost",
        "to_uri": "200@localhost",
        "call_id": "1000",
        "source_ip": "10.0.0.1",
        "source_port": 5060,
        "duration": 61,
        "call_start": "2019-09-01T00:00:00",
        "tenant_uuid": str(tenant.uuid),
    }


def test_update_cdr_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.put(
        "/1.0/cdrs/1",
        json={
            "id": 1,
            "from_uri": "100@localhost",
            "to_uri": "200@localhost",
            "call_id": "1000",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "duration": 60,
            "call_start": "2019-09-01T00:00:00",
            "tenant_uuid": "281f5d35-3089-4af3-9773-f8769dfcd878",
        },
    )
    assert response.status_code == 404


def test_delete_cdr(app_auth, client_auth_with_token):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.cdr import CDR
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app_auth.engine)
    tenant = Tenant(name="tenant", uuid="ffffffff-ffff-4c1c-ad1c-ffffffffffff")
    cdr = CDR(
        from_uri="100@localhost",
        to_uri="200@localhost",
        call_id="1000",
        source_ip="10.0.0.1",
        source_port=5060,
        duration=60,
        call_start=parse("2019-09-01T00:00:00"),
        tenant=tenant,
    )
    session.add_all([tenant, cdr])
    session.commit()
    #
    response = client_auth_with_token.delete("/1.0/cdrs/%s" % cdr.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": cdr.id,
        "from_uri": "100@localhost",
        "to_uri": "200@localhost",
        "call_id": "1000",
        "source_ip": "10.0.0.1",
        "source_port": 5060,
        "duration": 60,
        "call_start": "2019-09-01T00:00:00",
        "tenant_uuid": str(tenant.uuid),
    }


def test_delete_cdr_not_found(app_auth, client_auth_with_token):
    response = client_auth_with_token.delete("/1.0/cdrs/1")
    assert response.status_code == 404
