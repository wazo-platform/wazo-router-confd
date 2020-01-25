import os
import pytest  # type: ignore
import requests
import uuid

import sqlalchemy

from starlette.testclient import TestClient
from urllib.parse import urlsplit, urlunsplit

from wazo_router_confd.app import get_app
from wazo_router_confd.database import SessionLocal, wait_for_database


def create_temporary_database():
    url = "postgresql://wazo:wazo@localhost:{}/wazo".format(
        os.getenv("POSTGRES_PORT", "5432")
    )
    db_name = "test_{}".format(uuid.uuid4().hex)

    engine = sqlalchemy.create_engine(url)
    wait_for_database(engine)
    with engine.begin() as conn:
        conn.connection.set_isolation_level(0)
        conn.execute('CREATE DATABASE %s WITH TEMPLATE template0;' % db_name)
    engine.dispose()

    url_parts = list(urlsplit(url))
    url_parts[2] = db_name  # path
    db_uri = urlunsplit(url_parts)
    return db_uri


@pytest.fixture(scope="session")
def database_uri(request):
    request.addfinalizer(SessionLocal.close_all)
    return create_temporary_database()


@pytest.fixture(scope="function")
def app(database_uri):
    config = dict(
        database_uri=database_uri,
        redis_uri='redis://localhost',
        redis_flush_on_connect=True,
        database_upgrade=True,
        debug=True,
    )
    app = get_app(config)

    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=getattr(app, 'engine'))
    session.query(Tenant).delete()
    session.commit()

    return app


@pytest.fixture(scope="function")
def client(app):
    client = TestClient(app)
    with client:
        yield client


@pytest.fixture(scope="session")
def wazo_auth_mock():
    response = requests.post(
        "https://localhost:9497/api/auth/_set_token",
        json={
            'auth_id': 'uuid',
            'token': 'wazo-router-confd',
            'metadata': {
                'uuid': 'uuid',
                'pbx_user_uuid': 'uuid',
                'tenant_uuid': 'ffffffff-ffff-4c1c-ad1c-ffffffffffff',
            },
        },
        verify=False,
    )
    assert response.status_code == 204
    #
    response = requests.post(
        "https://localhost:9497/api/auth/_set_token",
        json={
            'auth_id': 'uuid',
            'token': 'wazo-router-confd-no-tenant',
            'metadata': {
                'uuid': 'uuid',
                'pbx_user_uuid': 'uuid',
                'tenant_uuid': 'ffffffff-ffff-4c1c-ad1c-eeeeeeeeeeee',
            },
        },
        verify=False,
    )
    assert response.status_code == 204
    #
    response = requests.post(
        "https://localhost:9497/api/auth/_set_tenants",
        json=[{'uuid': 'ffffffff-ffff-4c1c-ad1c-ffffffffffff'}],
        verify=False,
    )
    assert response.status_code == 204


# pylint: disable= unused-argument
@pytest.fixture(scope="function")
def app_auth(request, database_uri, wazo_auth_mock):
    config = dict(
        database_uri=database_uri,
        redis_uri='redis://localhost',
        redis_flush_on_connect=True,
        database_upgrade=True,
        debug=True,
        wazo_auth=True,
        wazo_auth_url="https://localhost:9497/api/auth/0.1",
        wazo_auth_cert=None,
    )
    app = get_app(config)

    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=getattr(app, 'engine'))
    session.query(Tenant).delete()
    session.commit()

    return app


@pytest.fixture(scope="function")
def client_auth(request, app_auth):
    client_auth = TestClient(app_auth)
    with client_auth:
        yield client_auth


@pytest.fixture(scope="function")
def client_auth_with_token(client_auth):
    client_auth.headers.update(
        {
            'X-Auth-Token': 'wazo-router-confd',
            'Wazo-Tenant': 'ffffffff-ffff-4c1c-ad1c-ffffffffffff',
        }
    )
    return client_auth
