# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy.orm import Session

from wazo_router_confd.auth import Principal
from wazo_router_confd.models.domain import Domain
from wazo_router_confd.schemas import domain as schema
from wazo_router_confd.services import tenant as tenant_service


def get_domain_by_id(db: Session, principal: Principal, domain_id: int) -> Domain:
    db_domain = db.query(Domain).filter(Domain.id == domain_id)
    if principal is not None and principal.tenant_uuids:
        db_domain = db_domain.filter(Domain.tenant_uuid.in_(principal.tenant_uuids))
    return db_domain.first()


def get_domain(db: Session, principal: Principal, domain: str) -> Domain:
    db_domain = db.query(Domain).filter(Domain.domain == domain)
    if principal is not None and principal.tenant_uuids:
        db_domain = db_domain.filter(Domain.tenant_uuid.in_(principal.tenant_uuids))
    return db_domain.first()


def get_domains(
    db: Session, principal: Principal, offset: int = 0, limit: int = 100
) -> schema.DomainList:
    items = db.query(Domain)
    if principal is not None and principal.tenant_uuid:
        items = items.filter(Domain.tenant_uuid == principal.tenant_uuid)
    items = items.offset(offset).limit(limit).all()
    return schema.DomainList(items=items)


def create_domain(
    db: Session, principal: Principal, domain: schema.DomainCreate
) -> Domain:
    domain.tenant_uuid = tenant_service.get_uuid(principal, db, domain.tenant_uuid)
    db_domain = Domain(domain=domain.domain, tenant_uuid=domain.tenant_uuid)
    db.add(db_domain)
    db.commit()
    db.refresh(db_domain)
    return db_domain


def update_domain(
    db: Session, principal: Principal, domain_id: int, domain: schema.DomainUpdate
) -> Domain:
    db_domain = get_domain_by_id(db, principal, domain_id)
    if db_domain is not None:
        db_domain.domain = (
            domain.domain if domain.domain is not None else db_domain.domain
        )
        db_domain.tenant_uuid = (
            domain.tenant_uuid
            if domain.tenant_uuid is not None
            else db_domain.tenant_uuid
        )
        db.commit()
        db.refresh(db_domain)
    return db_domain


def delete_domain(db: Session, principal: Principal, domain_id: int) -> Domain:
    db_domain = get_domain_by_id(db, principal, domain_id)
    if db_domain is not None:
        db.delete(db_domain)
        db.commit()
    return db_domain
