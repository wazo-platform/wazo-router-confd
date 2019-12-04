# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from sqlalchemy.orm import Session

from wazo_router_confd.models.cdr import CDR
from wazo_router_confd.schemas import cdr as schema


def get_cdr(db: Session, cdr_id: int) -> CDR:
    return db.query(CDR).filter(CDR.id == cdr_id).first()


def get_cdrs(db: Session, offset: int = 0, limit: int = 100) -> List[CDR]:
    return db.query(CDR).offset(offset).limit(limit).all()


def create_cdr(db: Session, cdr: schema.CDRCreate) -> CDR:
    db_cdr = CDR(
        tenant_uuid=cdr.tenant_uuid,
        source_ip=cdr.source_ip,
        source_port=cdr.source_port,
        from_uri=cdr.from_uri,
        to_uri=cdr.to_uri,
        call_id=cdr.call_id,
        call_start=cdr.call_start,
        duration=cdr.duration,
    )
    db.add(db_cdr)
    db.commit()
    db.refresh(db_cdr)
    return db_cdr


def update_cdr(db: Session, cdr_id: int, cdr: schema.CDRUpdate) -> CDR:
    db_cdr = db.query(CDR).filter(CDR.id == cdr_id).first()
    if db_cdr is not None:
        db_cdr.tenant_uuid = cdr.tenant_uuid if cdr.tenant_uuid else db_cdr.tenant_uuid
        db_cdr.source_ip = cdr.source_ip if cdr.source_ip else db_cdr.source_ip
        db_cdr.source_port = cdr.source_port if cdr.source_port else db_cdr.source_port
        db_cdr.from_uri = cdr.from_uri if cdr.from_uri else db_cdr.from_uri
        db_cdr.to_uri = cdr.to_uri if cdr.to_uri else db_cdr.to_uri
        db_cdr.call_id = cdr.call_id if cdr.call_id else db_cdr.call_id
        db_cdr.call_start = cdr.call_start if cdr.call_start else db_cdr.call_start
        db_cdr.duration = cdr.duration if cdr.duration else db_cdr.duration
        db.commit()
        db.refresh(db_cdr)
    return db_cdr


def delete_cdr(db: Session, cdr_id: int) -> CDR:
    db_cdr = db.query(CDR).filter(CDR.id == cdr_id).first()
    if db_cdr is not None:
        db.delete(db_cdr)
        db.commit()
    return db_cdr
