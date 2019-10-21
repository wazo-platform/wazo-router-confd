# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from sqlalchemy.orm import Session

from wazo_router_confd.models.domain import Domain
from wazo_router_confd.models.tenant import Tenant
from wazo_router_confd.schemas import domain as schema


def get_domain_by_id(db: Session, domain_id: int) -> Domain:
    return db.query(Domain).filter(Domain.id == domain_id).first()


def get_domain(db: Session, domain: str) -> Domain:
    return db.query(Domain).filter(Domain.domain == domain).first()


def get_domains(db: Session, offset: int = 0, limit: int = 100) -> List[Domain]:
    return db.query(Domain).offset(offset).limit(limit).all()


def get_tenant_by_domains(db: Session, domains: List[str]) -> Tenant:
    return db.query(Tenant).join(Domain).filter(Domain.domain.in_(domains)).first()


def create_domain(db: Session, domain: schema.DomainCreate) -> Domain:
    db_domain = Domain(domain=domain.domain, tenant_id=domain.tenant_id)
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
        db_domain.tenant_id = (
            domain.tenant_id if domain.tenant_id is not None else db_domain.tenant_id
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
