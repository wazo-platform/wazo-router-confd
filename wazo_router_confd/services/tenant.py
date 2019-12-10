# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from pydantic import UUID4
from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session

from wazo_router_confd.models.tenant import Tenant
from wazo_router_confd.schemas import tenant as schema


def get_tenant(db: Session, tenant_uuid: UUID4) -> Tenant:
    return db.query(Tenant).filter(Tenant.uuid == tenant_uuid).first()


def get_tenant_by_name(db: Session, name: str) -> Tenant:
    return db.query(Tenant).filter(Tenant.name == name).first()


def get_tenants(db: Session, offset: int = 0, limit: int = 100) -> List[Tenant]:
    return db.query(Tenant).offset(offset).limit(limit).all()


def create_tenant(db: Session, tenant: schema.TenantCreate) -> Tenant:
    db_tenant = Tenant(name=tenant.name, uuid=tenant.uuid or uuid4().hex)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant


def update_tenant(
    db: Session, tenant_uuid: UUID4, tenant: schema.TenantUpdate
) -> Tenant:
    db_tenant = db.query(Tenant).filter(Tenant.uuid == tenant_uuid).first()
    if db_tenant is not None:
        db_tenant.name = tenant.name
        db.commit()
        db.refresh(db_tenant)
    return db_tenant


def delete_tenant(db: Session, tenant_uuid: UUID4) -> Tenant:
    db_tenant = db.query(Tenant).filter(Tenant.uuid == tenant_uuid).first()
    if db_tenant is not None:
        db.delete(db_tenant)
        db.commit()
    return db_tenant
