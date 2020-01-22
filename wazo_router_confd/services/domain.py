# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy.orm import Session

from wazo_router_confd.models.domain import Domain
from wazo_router_confd.schemas import domain as schema


def get_domain_by_id(db: Session, domain_id: int) -> Domain:
    return db.query(Domain).filter(Domain.id == domain_id).first()


def get_domain(db: Session, domain: str) -> Domain:
    return db.query(Domain).filter(Domain.domain == domain).first()


def get_domains(db: Session, offset: int = 0, limit: int = 100) -> schema.DomainList:
    return schema.DomainList(items=db.query(Domain).offset(offset).limit(limit).all())


def create_domain(db: Session, domain: schema.DomainCreate) -> Domain:
    db_domain = Domain(domain=domain.domain, tenant_uuid=domain.tenant_uuid)
    db.add(db_domain)
    db.commit()
    db.refresh(db_domain)
    return db_domain


def update_domain(db: Session, domain_id: int, domain: schema.DomainUpdate) -> Domain:
    db_domain = db.query(Domain).filter(Domain.id == domain_id).first()
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


def delete_domain(db: Session, domain_id: int) -> Domain:
    db_domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if db_domain is not None:
        db.delete(db_domain)
        db.commit()
    return db_domain
