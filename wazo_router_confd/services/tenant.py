# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from json import dumps
from pydantic import UUID4
from typing import Optional
from uuid import uuid4, UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from wazo_router_confd.auth import Principal
from wazo_router_confd.models.tenant import Tenant
from wazo_router_confd.schemas import tenant as schema


def get_tenant(db: Session, principal: Principal, tenant_uuid: UUID4) -> Tenant:
    tenant = db.query(Tenant).filter(Tenant.uuid == tenant_uuid)
    if principal is not None and principal.tenant_uuids:
        tenant = tenant.filter(Tenant.uuid.in_(principal.tenant_uuids))
    return tenant.first()


def get_tenant_by_name(db: Session, principal: Principal, name: str) -> Tenant:
    tenant = db.query(Tenant).filter(Tenant.name == name)
    if principal is not None and principal.tenant_uuids:
        tenant = tenant.filter(Tenant.uuid.in_(principal.tenant_uuids))
    return tenant.first()


def get_tenant_by_uuid(db: Session, uuid: str) -> Tenant:
    return db.query(Tenant).filter(Tenant.uuid == uuid).first()


def get_tenants(
    db: Session, principal: Principal, offset: int = 0, limit: int = 100
) -> schema.TenantList:
    items = db.query(Tenant)
    if principal is not None and principal.tenant_uuid:
        items = items.filter(Tenant.uuid == principal.tenant_uuid)
    items = items.offset(offset).limit(limit).all()
    return schema.TenantList(items=items)


def create_tenant(
    db: Session, principal: Principal, tenant: schema.TenantCreate
) -> Tenant:
    tenant.uuid = get_uuid(principal, db, tenant.uuid, create=False)
    db_tenant = Tenant(name=tenant.name, uuid=tenant.uuid or uuid4().hex)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant


def update_tenant(
    db: Session, principal: Principal, tenant_uuid: UUID4, tenant: schema.TenantUpdate
) -> Tenant:
    db_tenant = get_tenant(db, principal, tenant_uuid)
    if db_tenant is not None:
        db_tenant.name = tenant.name
        db.commit()
        db.refresh(db_tenant)
    return db_tenant


def delete_tenant(db: Session, principal: Principal, tenant_uuid: UUID4) -> Tenant:
    db_tenant = get_tenant(db, principal, tenant_uuid)
    if db_tenant is not None:
        db.delete(db_tenant)
        db.commit()
    return db_tenant


def get_uuid(
    principal: Principal, db: Session, tenant_uuid: Optional[UUID], create: bool = True
) -> UUID4:
    if principal is None:
        if tenant_uuid is None:
            raise HTTPException(
                status_code=400,
                detail=dumps(
                    {
                        "detail": [
                            {
                                "loc": ["body", "tenant_uuid"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    }
                ),
                headers={"Content-Type": "text/json;charset=\"UTF8\""},
            )
    elif tenant_uuid is not None and tenant_uuid != UUID4(principal.tenant_uuid):
        raise HTTPException(
            status_code=403, detail="Token not valid for tenant_uuid %s" % tenant_uuid
        )
    else:
        tenant_uuid = UUID4(principal.tenant_uuid)
    if create and get_tenant_by_uuid(db, str(tenant_uuid)) is None:
        tenant = schema.TenantCreate(name=str(tenant_uuid), uuid=tenant_uuid)
        create_tenant(db, principal, tenant)
    return tenant_uuid
