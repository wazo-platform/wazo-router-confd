from typing import List

from sqlalchemy.orm import Session

from wazo_router_confd.models.tenant import Tenant
from wazo_router_confd.schemas import tenant as schema


def get_tenant(db: Session, tenant_id: int) -> Tenant:
    return db.query(Tenant).filter(Tenant.id == tenant_id).first()


def get_tenant_by_name(db: Session, name: str) -> Tenant:
    return db.query(Tenant).filter(Tenant.name == name).first()


def get_tenants(db: Session, skip: int = 0, limit: int = 100) -> List[Tenant]:
    return db.query(Tenant).offset(skip).limit(limit).all()


def create_tenant(db: Session, tenant: schema.TenantCreate) -> Tenant:
    db_tenant = Tenant(name=tenant.name)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant


def update_tenant(db: Session, tenant_id: int, tenant: schema.TenantUpdate) -> Tenant:
    db_tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if db_tenant is not None:
        db_tenant.name = tenant.name
        db.commit()
        db.refresh(db_tenant)
    return db_tenant


def delete_tenant(db: Session, tenant_id: int) -> Tenant:
    db_tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if db_tenant is not None:
        db.delete(db_tenant)
        db.commit()
    return db_tenant
