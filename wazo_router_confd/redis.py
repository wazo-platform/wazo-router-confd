# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import aioredis  # type: ignore

from json import loads, dumps
from typing import Optional

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response


class Redis(object):
    uri: str
    flush_on_connect: bool
    pool: aioredis.ConnectionsPool

    def __init__(self, uri, flush_on_connect=False):
        self.uri = uri
        self.flush_on_connect = flush_on_connect

    async def connect(self):
        self.pool = await aioredis.create_redis_pool(self.uri)
        if self.flush_on_connect:
            await self.flushdb()

    def disconnect(self):
        self.pool.close()

    async def get_value(self, key: str) -> Optional[dict]:
        value = await self.pool.get(key)
        return loads(value) if value is not None else None

    async def set_value(self, key: str, value: dict):
        await self.pool.set(key, dumps(value, default=str))

    async def flushdb(self):
        await self.pool.flushdb()


def get_redis(request: Request) -> Redis:
    return request.state.redis


def setup_redis(app: FastAPI, config: dict):
    redis_uri = config['redis_uri']
    redis = Redis(
        redis_uri, flush_on_connect=bool(config.get('redis_flush_on_connect'))
    )
    setattr(app, 'redis', redis)

    app.add_event_handler("startup", redis.connect)
    app.add_event_handler("shutdown", redis.disconnect)

    # pylint: disable= unused-variable
    @app.middleware("http")
    async def db_aioredis_database_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        request.state.redis = redis
        response = await call_next(request)
        if (
            request.method not in ('HEAD', 'GET')
            and not request.url.path.startswith('/kamailio')
            and response.status_code >= 200
            and response.status_code < 300
        ):
            await redis.flushdb()
        return response

    return app
