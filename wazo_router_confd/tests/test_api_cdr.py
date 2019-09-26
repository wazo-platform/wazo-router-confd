from .common import get_app_and_client

from dateutil.parser import parse


@get_app_and_client
def test_create_cdr(app=None, client=None):
    response = client.post(
        "/cdrs/",
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
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "from_uri": "100@localhost",
        "to_uri": "200@localhost",
        "call_id": "1000",
        "source_ip": "10.0.0.1",
        "source_port": 5060,
        "duration": 60,
        "call_start": "2019-09-01T00:00:00",
        "tenant_id": 1,
    }


@get_app_and_client
def test_get_cdr(app=None, client=None):
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
    response = client.get("/cdrs/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "from_uri": "100@localhost",
        "to_uri": "200@localhost",
        "call_id": "1000",
        "source_ip": "10.0.0.1",
        "source_port": 5060,
        "duration": 60,
        "call_start": "2019-09-01T00:00:00",
        "tenant_id": 1,
    }


@get_app_and_client
def test_get_cdr_not_found(app=None, client=None):
    response = client.get("/cdrs/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_cdrs(app=None, client=None):
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
            "id": 1,
            "from_uri": "100@localhost",
            "to_uri": "200@localhost",
            "call_id": "1000",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "duration": 60,
            "call_start": "2019-09-01T00:00:00",
            "tenant_id": 1,
        }
    ]


@get_app_and_client
def test_update_cdr(app=None, client=None):
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
        "/cdrs/1",
        json={
            "id": 1,
            "from_uri": "100@localhost",
            "to_uri": "200@localhost",
            "call_id": "1000",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "duration": 61,
            "call_start": "2019-09-01T00:00:00",
            "tenant_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "from_uri": "100@localhost",
        "to_uri": "200@localhost",
        "call_id": "1000",
        "source_ip": "10.0.0.1",
        "source_port": 5060,
        "duration": 61,
        "call_start": "2019-09-01T00:00:00",
        "tenant_id": 1,
    }


@get_app_and_client
def test_update_cdr_not_found(app=None, client=None):
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


@get_app_and_client
def test_delete_cdr(app=None, client=None):
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
    response = client.delete("/cdrs/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "from_uri": "100@localhost",
        "to_uri": "200@localhost",
        "call_id": "1000",
        "source_ip": "10.0.0.1",
        "source_port": 5060,
        "duration": 60,
        "call_start": "2019-09-01T00:00:00",
        "tenant_id": 1,
    }


@get_app_and_client
def test_delete_cdr_not_found(app=None, client=None):
    response = client.delete("/cdrs/1")
    assert response.status_code == 404
