import pytest
import uuid

import sqlalchemy

from sqlalchemy.orm.session import close_all_sessions
from starlette.testclient import TestClient
from urllib.parse import urlsplit, urlunsplit

from wazo_router_confd.app import get_app
from wazo_router_confd.database import wait_for_database


@pytest.fixture(scope="session")
def database_uri(request):
    url = "postgresql://wazo:wazo@localhost:5432/wazo"
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
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.cdr import CDR
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.routing_group import RoutingGroup
    from wazo_router_confd.models.routing_rule import RoutingRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.query(Carrier).delete()
    session.query(CarrierTrunk).delete()
    session.query(RoutingGroup).delete()
    session.query(RoutingRule).delete()
    session.query(CDR).delete()
    session.query(Domain).delete()
    session.query(IPBX).delete()
    session.query(Tenant).delete()
    session.commit()

    return app


@pytest.fixture(scope="function")
def client(request, app):
    return TestClient(app)
