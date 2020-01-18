# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy.orm import Session

from wazo_router_confd.models.domain import Domain
from wazo_router_confd.models.ipbx import IPBX
from wazo_router_confd.schemas import ipbx as schema
from wazo_router_confd.services import password as password_service


def get_ipbx(db: Session, ipbx_id: int) -> IPBX:
    return db.query(IPBX).filter(IPBX.id == ipbx_id).first()


def get_ipbxs(db: Session, offset: int = 0, limit: int = 100) -> schema.IPBXList:
    return schema.IPBXList(items=db.query(IPBX).offset(offset).limit(limit).all())


def create_ipbx(db: Session, ipbx: schema.IPBXCreate) -> IPBX:
    domain = db.query(Domain).filter(Domain.id == ipbx.domain_id).first()
    db_ipbx = IPBX(
        tenant_uuid=ipbx.tenant_uuid,
        domain_id=ipbx.domain_id,
        customer=ipbx.customer,
        ip_fqdn=ipbx.ip_fqdn,
        port=ipbx.port,
        ip_address=ipbx.ip_address,
        registered=ipbx.registered,
        username=ipbx.username,
        password=password_service.hash(ipbx.password),
        password_ha1=password_service.hash_ha1(
            ipbx.username, domain.domain, ipbx.password
        ),
        realm=ipbx.realm,
    )
    db.add(db_ipbx)
    db.commit()
    db.refresh(db_ipbx)
    return db_ipbx


def update_ipbx(db: Session, ipbx_id: int, ipbx: schema.IPBXUpdate) -> IPBX:
    db_ipbx = db.query(IPBX).filter(IPBX.id == ipbx_id).first()
    if db_ipbx is not None:
        db_ipbx.tenant_uuid = (
            ipbx.tenant_uuid if ipbx.tenant_uuid is not None else db_ipbx.tenant_uuid
        )
        db_ipbx.domain_id = (
            ipbx.domain_id if ipbx.domain_id is not None else db_ipbx.domain_id
        )
        db_ipbx.customer = (
            ipbx.customer if ipbx.customer is not None else db_ipbx.customer
        )
        db_ipbx.ip_fqdn = ipbx.ip_fqdn if ipbx.ip_fqdn is not None else db_ipbx.ip_fqdn
        db_ipbx.port = ipbx.port if ipbx.port is not None else db_ipbx.port
        db_ipbx.ip_address = (
            ipbx.ip_address if ipbx.ip_address is not None else db_ipbx.ip_address
        )
        db_ipbx.registered = (
            ipbx.registered if ipbx.registered is not None else db_ipbx.registered
        )
        db_ipbx.username = (
            ipbx.username if ipbx.username is not None else db_ipbx.username
        )
        if ipbx.password is not None:
            domain = db.query(Domain).filter(Domain.id == ipbx.domain_id).first()
            db_ipbx.password = password_service.hash(ipbx.password)
            db_ipbx.password_ha1 = (
                password_service.hash_ha1(ipbx.username, domain.domain, ipbx.password),
            )
        db_ipbx.realm = ipbx.realm if ipbx.realm is not None else db_ipbx.realm
        db.commit()
        db.refresh(db_ipbx)
    return db_ipbx


def delete_ipbx(db: Session, ipbx_id: int) -> IPBX:
    db_ipbx = db.query(IPBX).filter(IPBX.id == ipbx_id).first()
    if db_ipbx is not None:
        db.delete(db_ipbx)
        db.commit()
    return db_ipbx
