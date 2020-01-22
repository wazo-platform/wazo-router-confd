# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from .consul import setup_consul
from .database import setup_database, setup_aiopg_database, upgrade_database
from .redis import setup_redis
from .routers import carriers
from .routers import carrier_trunks
from .routers import cdr
from .routers import dids
from .routers import domains
from .routers import kamailio
from .routers import ipbx
from .routers import normalization
from .routers import routing_rules
from .routers import routing_group
from .routers import tenants


def get_app(config: dict):
    app = FastAPI(
        title="wazo-router-confd",
        description="Configuration API for Wazo C4 Router components",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
    )
    if config.get('consul_uri') is not None:
        app = setup_consul(app, config)
    app = setup_database(app, config)
    app = setup_aiopg_database(app, config)
    if config.get('database_upgrade'):
        upgrade_database(app, config)
    app = setup_redis(app, config)
    app.include_router(carriers.router, prefix="/1.0", tags=['carriers'])
    app.include_router(carrier_trunks.router, prefix="/1.0", tags=['carriers'])
    app.include_router(cdr.router, prefix="/1.0", tags=['cdr'])
    app.include_router(dids.router, prefix="/1.0", tags=['dids'])
    app.include_router(domains.router, prefix="/1.0", tags=['domains'])
    app.include_router(ipbx.router, prefix="/1.0", tags=['ipbx'])
    app.include_router(kamailio.router, prefix="/1.0", tags=['kamailio'])
    app.include_router(normalization.router, prefix="/1.0", tags=['normalization'])
    app.include_router(routing_rules.router, prefix="/1.0", tags=['routing'])
    app.include_router(routing_group.router, prefix="/1.0", tags=['routing'])
    app.include_router(tenants.router, prefix="/1.0", tags=['tenants'])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
