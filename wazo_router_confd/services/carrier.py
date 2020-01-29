# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy.orm import Session

from wazo_router_confd.auth import Principal
from wazo_router_confd.models.carrier import Carrier
from wazo_router_confd.schemas import carrier as schema
from wazo_router_confd.services import tenant as tenant_service


def get_carrier(db: Session, principal: Principal, carrier_id: int) -> Carrier:
    db_carrier = db.query(Carrier).filter(Carrier.id == carrier_id)
    if principal is not None and principal.tenant_uuids:
        db_carrier = db_carrier.filter(Carrier.tenant_uuid.in_(principal.tenant_uuids))
    return db_carrier.first()


def get_carrier_by_name(db: Session, principal: Principal, name: str) -> Carrier:
    db_carrier = db.query(Carrier).filter(Carrier.name == name)
    if principal is not None and principal.tenant_uuids:
        db_carrier = db_carrier.filter(Carrier.tenant_uuid.in_(principal.tenant_uuids))
    return db_carrier.first()


def get_carriers(
    db: Session, principal: Principal, offset: int = 0, limit: int = 100
) -> schema.CarrierList:
    items = db.query(Carrier)
    if principal is not None and principal.tenant_uuid:
        items = items.filter(Carrier.tenant_uuid == principal.tenant_uuid)
    items = items.offset(offset).limit(limit).all()
    return schema.CarrierList(items=items)


def create_carrier(
    db: Session, principal: Principal, carrier: schema.CarrierCreate
) -> Carrier:
    carrier.tenant_uuid = tenant_service.get_uuid(principal, db, carrier.tenant_uuid)
    db_carrier = Carrier(name=carrier.name, tenant_uuid=carrier.tenant_uuid)
    db.add(db_carrier)
    db.commit()
    db.refresh(db_carrier)
    return db_carrier


def update_carrier(
    db: Session, principal: Principal, carrier_id: int, carrier: schema.CarrierUpdate
) -> Carrier:
    db_carrier = get_carrier(db, principal, carrier_id)
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


def delete_carrier(db: Session, principal: Principal, carrier_id: int) -> Carrier:
    db_carrier = get_carrier(db, principal, carrier_id)
    if db_carrier is not None:
        db.delete(db_carrier)
        db.commit()
    return db_carrier
