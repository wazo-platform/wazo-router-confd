import pytest
import os
import uuid

import sqlalchemy

from sqlalchemy.orm.session import close_all_sessions
from starlette.testclient import TestClient
from urllib.parse import urlsplit, urlunsplit

from wazo_router_confd.app import get_app


@pytest.fixture(scope="session")
def app(request):
    url = os.getenv("DATABASE_URL", "postgresql://wazo:wazo@localhost/wazo")
    db_name = "test_{}".format(uuid.uuid4().hex)
    engine = sqlalchemy.create_engine(url)
    conn = engine.connect()
    conn.connection.set_isolation_level(0)
    conn.execute('CREATE DATABASE %s WITH TEMPLATE template0;' % db_name)

    def cleanup(conn, engine):
        close_all_sessions()
        conn.close()
        engine.dispose()

    request.addfinalizer(lambda: cleanup(conn, engine))

    url_parts = list(urlsplit(url))
    url_parts[2] = db_name  # path
    db_uri = urlunsplit(url_parts)

    config = dict(
        database_uri=db_uri, database_upgrade=True, debug=True
    )
    return get_app(config)


@pytest.fixture(scope="function")
def client(request, app):
    @request.addfinalizer
    def cleanup():
        from wazo_router_confd.database import SessionLocal
        from wazo_router_confd.models.tenant import Tenant
        session = SessionLocal(bind=app.engine)
        session.query(Tenant).delete()
        session.commit()
    return TestClient(app)
