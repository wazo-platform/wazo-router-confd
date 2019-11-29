# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock

from dateutil.parser import parse


def test_create_cdr(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant")
    session = SessionLocal(bind=app.engine)
    session.add(tenant)
    session.commit()
    #
    response = client.post(
        "/cdrs/",
        json={
            "from_uri": "100@localhost",
            "to_uri": "200@localhost",
            "call_id": "1000",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "duration": 60,
            "call_start": "2019-09-01T00:00:00",
            "tenant_id": tenant.id,
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
        "tenant_id": tenant.id,
    }


def test_get_cdr(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.cdr import CDR
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name="tenant")
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
    response = client.get("/cdrs/%s" % cdr.id)
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
        "tenant_id": tenant.id,
    }


def test_get_cdr_not_found(app, client):
    response = client.get("/cdrs/1")
    assert response.status_code == 404


def test_get_cdrs(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.cdr import CDR
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name="tenant")
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
    response = client.get("/cdrs/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": cdr.id,
            "from_uri": "100@localhost",
            "to_uri": "200@localhost",
            "call_id": "1000",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "duration": 60,
            "call_start": "2019-09-01T00:00:00",
            "tenant_id": tenant.id,
        }
    ]


def test_update_cdr(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.cdr import CDR
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name="tenant")
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
    response = client.put(
        "/cdrs/%s" % cdr.id,
        json={
            "id": cdr.id,
            "from_uri": "100@localhost",
            "to_uri": "200@localhost",
            "call_id": "1000",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "duration": 61,
            "call_start": "2019-09-01T00:00:00",
            "tenant_id": tenant.id,
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
        "tenant_id": tenant.id,
    }


def test_update_cdr_not_found(app, client):
    response = client.put(
        "/cdrs/1",
        json={
            "id": 1,
            "from_uri": "100@localhost",
            "to_uri": "200@localhost",
            "call_id": "1000",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "duration": 60,
            "call_start": "2019-09-01T00:00:00",
            "tenant_id": 1,
        },
    )
    assert response.status_code == 404


def test_delete_cdr(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.cdr import CDR
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name="tenant")
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
    response = client.delete("/cdrs/%s" % cdr.id)
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
        "tenant_id": tenant.id,
    }


def test_delete_cdr_not_found(app, client):
    response = client.delete("/cdrs/1")
    assert response.status_code == 404
