# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy.orm import Session

from wazo_router_confd.models.carrier import Carrier
from wazo_router_confd.schemas import carrier as schema


def get_carrier(db: Session, carrier_id: int) -> Carrier:
    return db.query(Carrier).filter(Carrier.id == carrier_id).first()


def get_carrier_by_name(db: Session, name: str) -> Carrier:
    return db.query(Carrier).filter(Carrier.name == name).first()


def get_carriers(db: Session, offset: int = 0, limit: int = 100) -> schema.CarrierList:
    return schema.CarrierList(items=db.query(Carrier).offset(offset).limit(limit).all())


def create_carrier(db: Session, carrier: schema.CarrierCreate) -> Carrier:
    db_carrier = Carrier(name=carrier.name, tenant_uuid=carrier.tenant_uuid)
    db.add(db_carrier)
    db.commit()
    db.refresh(db_carrier)
    return db_carrier


def update_carrier(
    db: Session, carrier_id: int, carrier: schema.CarrierUpdate
) -> Carrier:
    db_carrier = db.query(Carrier).filter(Carrier.id == carrier_id).first()
    if db_carrier is not None:
        db_carrier.name = carrier.name if carrier.name is not None else db_carrier.name
        db_carrier.tenant_uuid = (
            carrier.tenant_uuid
            if carrier.tenant_uuid is not None
            else db_carrier.tenant_uuid
        )
        db.commit()
        db.refresh(db_carrier)
    return db_carrier


def delete_carrier(db: Session, carrier_id: int) -> Carrier:
    db_carrier = db.query(Carrier).filter(Carrier.id == carrier_id).first()
    if db_carrier is not None:
        db.delete(db_carrier)
        db.commit()
    return db_carrier
