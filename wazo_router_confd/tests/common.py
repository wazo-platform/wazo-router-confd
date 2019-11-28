# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import contextlib
import logging
import uuid
from urllib.parse import urlsplit, urlunsplit
import os

import sqlalchemy
from sqlalchemy.orm.session import close_all_sessions

from starlette.testclient import TestClient

from wazo_router_confd.app import get_app
from functools import wraps

LOG = logging.getLogger(__name__)


@contextlib.contextmanager
def temporary_database():
    url = os.getenv("DATABASE_URL")
    db_name = "test_{}".format(uuid.uuid4().hex)
    engine = sqlalchemy.create_engine(url)
    conn = engine.connect()
    conn.connection.set_isolation_level(0)
    conn.execute('CREATE DATABASE %s WITH TEMPLATE template0;' % db_name)

    url_parts = list(urlsplit(url))
    url_parts[2] = db_name  # path
    db_uri = urlunsplit(url_parts)

    yield db_uri

    # NOTE(sileht): We drop the database only if the test succeed for checking if
    # sqlalchemy resource leaks, but we must not raise it if the test fails
    close_all_sessions()
    engine.dispose()
    # conn.execute('DROP DATABASE %s;' % db_name)
    # conn.close()


def get_app_and_client(f):
    @wraps(f)
    def wrapper(*args, **kw):
        with temporary_database() as uri:
            config = dict(database_uri=uri, database_upgrade=True, debug=True)
            app = get_app(config)
            client = TestClient(app)
            try:
                return f(*args, app=app, client=client, **kw)
            finally:
                app.engine.dispose()

    return wrapper
