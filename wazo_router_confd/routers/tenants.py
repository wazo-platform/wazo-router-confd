# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from time import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import tenant as schema
from wazo_router_confd.services import tenant as service


router = APIRouter()


@router.post("/tenants/", response_model=schema.Tenant)
def create_tenant(tenant: schema.TenantCreate, db: Session = Depends(get_db)):
    db_tenant = service.get_tenant_by_name(db, name=tenant.name)
    if db_tenant:
        raise HTTPException(
            status_code=409,
            detail={
                "error_id": "invalid-data",
                "message": "Duplicated name",
                "resource": "tenant",
                "timestamp": time(),
                "details": {
                    "config": {
                        "name": {
                            "constraing_id": "name",
                            "constraint": {"unique": True},
                            "message": "Duplicated name",
                        }
                    }
                },
            },
        )
    return service.create_tenant(db=db, tenant=tenant)


@router.get("/tenants/", response_model=List[schema.Tenant])
def read_tenants(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tenants = service.get_tenants(db, offset=offset, limit=limit)
    return tenants


@router.get("/tenants/{tenant_uuid}", response_model=schema.Tenant)
def read_tenant(tenant_uuid: UUID4, db: Session = Depends(get_db)):
    db_tenant = service.get_tenant(db, tenant_uuid=tenant_uuid)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant


@router.put("/tenants/{tenant_uuid}", response_model=schema.Tenant)
def update_tenant(
    tenant_uuid: UUID4, tenant: schema.TenantUpdate, db: Session = Depends(get_db)
):
    db_tenant = service.update_tenant(db, tenant_uuid=tenant_uuid, tenant=tenant)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant


@router.delete("/tenants/{tenant_uuid}", response_model=schema.Tenant)
def delete_tenant(tenant_uuid: UUID4, db: Session = Depends(get_db)):
    db_tenant = service.delete_tenant(db, tenant_uuid=tenant_uuid)
    if db_tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return db_tenant
