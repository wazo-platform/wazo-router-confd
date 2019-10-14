# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os

import alembic.config  # type: ignore
import alembic.command  # type: ignore
import alembic.migration  # type: ignore

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tenacity import (  # type: ignore
    after_log,
    before_log,
    retry,
    stop_after_attempt,
    wait_fixed,
)

from wazo_router_confd.models.base import Base

SessionLocal = sessionmaker(autocommit=False, autoflush=False)
logger = logging.getLogger(__name__)


def get_db(request: Request):
    return request.state.db


def setup_database(app: FastAPI, config: dict):
    database_uri = config['database_uri']
    connect_args = (
        {"check_same_thread": False} if database_uri.startswith('sqlite:') else {}
    )
    engine = create_engine(database_uri, connect_args=connect_args)
    setattr(app, 'engine', engine)

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            request.state.db = SessionLocal(bind=engine)
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response

    return app


def upgrade_database(app: FastAPI, config: dict):
    cur_dir = os.path.dirname(__file__)
    cfg = alembic.config.Config("{}/migrations/alembic.ini".format(cur_dir))
    cfg.set_main_option("script_location", "{}/migrations/alembic".format(cur_dir))
    cfg.set_main_option("sqlalchemy.url", config['database_uri'])

    engine = getattr(app, "engine")
    wait_for_database(engine)
    with engine.begin() as connection:
        ctxt = alembic.migration.MigrationContext.configure(connection)
        current_version = ctxt.get_current_revision()
        if current_version is None:
            Base.metadata.create_all(bind=engine)
            alembic.command.stamp(cfg, "head")
        else:
            alembic.command.upgrade(cfg, "head")
    logger.info("Database upgraded")


@retry(
    stop=stop_after_attempt(60 * 5),
    wait=wait_fixed(1),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def wait_for_database(connection):
    try:
        connection.execute("SELECT 1")
    except Exception as e:
        logger.warning("fail to connect to the database: %s", e)
        raise
