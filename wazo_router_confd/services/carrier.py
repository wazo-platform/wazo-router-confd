from typing import List

from sqlalchemy.orm import Session

from wazo_router_confd.models.carrier import Carrier
from wazo_router_confd.schemas import carrier as schema


def get_carrier(db: Session, carrier_id: int) -> Carrier:
    return db.query(Carrier).filter(Carrier.id == carrier_id).first()


def get_carrier_by_name(db: Session, name: str) -> Carrier:
    return db.query(Carrier).filter(Carrier.name == name).first()


def get_carriers(db: Session, offset: int = 0, limit: int = 100) -> List[Carrier]:
    return db.query(Carrier).offset(offset).limit(limit).all()


def get_carriers_by_tenant(
    db: Session, tenant_id: int, offset: int = 0, limit: int = 100
) -> List[Carrier]:
    return (
        db.query(Carrier)
        .filter(Carrier.tenant_id == tenant_id)
        .offset(offset)
        .limit(limit)
        .all()
    )


def create_carrier(db: Session, carrier: schema.CarrierCreate) -> Carrier:
    db_carrier = Carrier(name=carrier.name, tenant_id=carrier.tenant_id)
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
        db_carrier.tenant_id = (
            carrier.tenant_id if carrier.tenant_id is not None else db_carrier.tenant_id
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
