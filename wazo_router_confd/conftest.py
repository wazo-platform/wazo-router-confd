import os
import pytest  # type: ignore
import uuid

import sqlalchemy

from sqlalchemy.orm.session import close_all_sessions  # type: ignore
from starlette.testclient import TestClient
from urllib.parse import urlsplit, urlunsplit

from wazo_router_confd.app import get_app
from wazo_router_confd.database import wait_for_database


@pytest.fixture(scope="session")
def database_uri(request):
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

    request.addfinalizer(close_all_sessions)
    return db_uri


@pytest.fixture(scope="function")
def app(request, database_uri):
    config = dict(database_uri=database_uri, database_upgrade=True, debug=True)
    app = get_app(config)

    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.query(Tenant).delete()
    session.commit()

    return app


@pytest.fixture(scope="function")
def client(request, app):
    return TestClient(app)
