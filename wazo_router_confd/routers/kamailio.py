# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import kamailio as schema
from wazo_router_confd.schemas import cdr as cdr_schema
from wazo_router_confd.services import kamailio as service
from wazo_router_confd.services import cdr as cdr_service
from wazo_router_confd.services import tenant as tenant_service


router = APIRouter()


@router.post("/kamailio/routing")
def kamailio_routing(request: schema.RoutingRequest, db: Session = Depends(get_db)):
    return service.routing(db, request=request)


@router.post("/kamailio/cdr")
def kamailio_cdr(request: schema.CDRRequest, db: Session = Depends(get_db)):
    tenant = tenant_service.get_tenant(db=db, tenant_id=request.tenant_id)
    if tenant is None:
        return {"success": False, "cdr": None}
    cdr = cdr_schema.CDRCreate(
        tenant_id=tenant.id,
        source_ip=request.source_ip,
        source_port=request.source_port,
        from_uri=request.from_uri,
        to_uri=request.to_uri,
        call_id=request.call_id,
        call_start=request.call_start,
        duration=request.duration,
    )
    response = cdr_service.create_cdr(db, cdr=cdr)
    return {"success": bool(response), "cdr": cdr}


@router.post("/kamailio/auth")
def kamailio_auth(request: schema.AuthRequest, db: Session = Depends(get_db)):
    return service.auth(db, request=request)
