# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import aiopg  # type: ignore

from fastapi import APIRouter, Depends

from wazo_router_confd.database import get_aiopg_pool
from wazo_router_confd.redis import Redis, get_redis
from wazo_router_confd.schemas import kamailio as schema
from wazo_router_confd.services import kamailio as service


router = APIRouter()


@router.post("/kamailio/routing")
async def kamailio_routing(
    request: schema.RoutingRequest,
    pool: aiopg.Pool = Depends(get_aiopg_pool),
    redis: Redis = Depends(get_redis),
):
    return await service.routing(pool, redis, request=request)


@router.post("/kamailio/cdr")
async def kamailio_cdr(
    request: schema.CDRRequest, pool: aiopg.Pool = Depends(get_aiopg_pool)
):
    return await service.cdr(pool, request)


@router.post("/kamailio/auth")
async def kamailio_auth(
    request: schema.AuthRequest,
    pool: aiopg.Pool = Depends(get_aiopg_pool),
    redis: Redis = Depends(get_redis),
):
    return await service.auth(pool, redis, request=request)


@router.get("/kamailio/dbtext/uacreg")
async def kamailio_dbtext_uacreg(pool: aiopg.Pool = Depends(get_aiopg_pool)):
    return await service.dbtext_uacreg(pool)
