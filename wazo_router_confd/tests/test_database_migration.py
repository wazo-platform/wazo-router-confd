# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock
import pprint

from alembic import migration  # type: ignore
from alembic.autogenerate import compare_metadata  # type: ignore

from wazo_router_confd import database
from wazo_router_confd import conftest
from wazo_router_confd.models.base import Base


def test_database_migration():
    database_uri = conftest.create_temporary_database()
    config = dict(database_uri=database_uri)
    app = mock.Mock()
    app = database.setup_database(app, config)

    try:
        database.upgrade_database(app, config, force_migration=True)
        with app.engine.begin() as conn:
            ctx = migration.MigrationContext.configure(conn)
            diff = compare_metadata(ctx, Base.metadata)
            assert diff == [], pprint.pformat(diff, indent=2, width=20)
    finally:
        database.SessionLocal.close_all()
        app.engine.dispose()
