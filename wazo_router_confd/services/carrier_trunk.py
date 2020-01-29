# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy.orm import Session

from wazo_router_confd.auth import Principal
from wazo_router_confd.models.carrier_trunk import CarrierTrunk
from wazo_router_confd.schemas import carrier_trunk as schema
from wazo_router_confd.services import password as password_service
from wazo_router_confd.services import tenant as tenant_service


def get_carrier_trunk(
    db: Session, principal: Principal, carrier_trunk_id: int
) -> CarrierTrunk:
    db_carrier_trunk = db.query(CarrierTrunk).filter(
        CarrierTrunk.id == carrier_trunk_id
    )
    if principal is not None and principal.tenant_uuids:
        db_carrier_trunk = db_carrier_trunk.filter(
            CarrierTrunk.tenant_uuid.in_(principal.tenant_uuids)
        )
    return db_carrier_trunk.first()


def get_carrier_trunk_by_name(
    db: Session, principal: Principal, name: str
) -> CarrierTrunk:
    return db.query(CarrierTrunk).filter(CarrierTrunk.name == name).first()


def get_carrier_trunks(
    db: Session, principal: Principal, offset: int = 0, limit: int = 100
) -> schema.CarrierTrunkList:
    items = db.query(CarrierTrunk)
    if principal is not None and principal.tenant_uuid:
        items = items.filter(CarrierTrunk.tenant_uuid == principal.tenant_uuid)
    items = items.offset(offset).limit(limit).all()
    return schema.CarrierTrunkList(items=items)


def create_carrier_trunk(
    db: Session, principal: Principal, carrier_trunk: schema.CarrierTrunkCreate
) -> CarrierTrunk:
    carrier_trunk.tenant_uuid = tenant_service.get_uuid(
        principal, db, carrier_trunk.tenant_uuid
    )
    db_carrier_trunk = CarrierTrunk(
        tenant_uuid=carrier_trunk.tenant_uuid,
        carrier_id=carrier_trunk.carrier_id,
        name=carrier_trunk.name,
        normalization_profile_id=carrier_trunk.normalization_profile_id,
        sip_proxy=carrier_trunk.sip_proxy,
        sip_proxy_port=carrier_trunk.sip_proxy_port,
        ip_address=carrier_trunk.ip_address,
        registered=carrier_trunk.registered,
        auth_username=carrier_trunk.auth_username,
        auth_password=password_service.hash(carrier_trunk.auth_password),
        realm=carrier_trunk.realm,
        registrar_proxy=carrier_trunk.registrar_proxy,
        from_domain=carrier_trunk.from_domain,
        expire_seconds=carrier_trunk.expire_seconds,
        retry_seconds=carrier_trunk.retry_seconds,
    )
    db.add(db_carrier_trunk)
    db.commit()
    db.refresh(db_carrier_trunk)
    return db_carrier_trunk


def update_carrier_trunk(
    db: Session,
    principal: Principal,
    carrier_trunk_id: int,
    carrier_trunk: schema.CarrierTrunkUpdate,
) -> CarrierTrunk:
    db_carrier_trunk = get_carrier_trunk(db, principal, carrier_trunk_id)
    if db_carrier_trunk is not None:
        db_carrier_trunk.name = (
            carrier_trunk.name
            if carrier_trunk.name is not None
            else db_carrier_trunk.name
        )
        db_carrier_trunk.normalization_profile_id = (
            carrier_trunk.normalization_profile_id
            if carrier_trunk.normalization_profile_id is not None
            else db_carrier_trunk.normalization_profile_id
        )
        db_carrier_trunk.sip_proxy = (
            carrier_trunk.sip_proxy
            if carrier_trunk.sip_proxy is not None
            else db_carrier_trunk.sip_proxy
        )
        db_carrier_trunk.sip_proxy_port = (
            carrier_trunk.sip_proxy_port
            if carrier_trunk.sip_proxy_port is not None
            else db_carrier_trunk.sip_proxy_port
        )
        db_carrier_trunk.ip_address = (
            carrier_trunk.ip_address
            if carrier_trunk.ip_address is not None
            else db_carrier_trunk.ip_address
        )
        db_carrier_trunk.registered = (
            carrier_trunk.registered
            if carrier_trunk.registered is not None
            else db_carrier_trunk.registered
        )
        db_carrier_trunk.auth_username = (
            carrier_trunk.auth_username
            if carrier_trunk.auth_username is not None
            else db_carrier_trunk.auth_username
        )
        if carrier_trunk.auth_password is not None:
            db_carrier_trunk.auth_password = password_service.hash(
                carrier_trunk.auth_password
            )
        db_carrier_trunk.realm = (
            carrier_trunk.realm
            if carrier_trunk.realm is not None
            else db_carrier_trunk.realm
        )
        db_carrier_trunk.registrar_proxy = (
            carrier_trunk.registrar_proxy
            if carrier_trunk.registrar_proxy is not None
            else db_carrier_trunk.registrar_proxy
        )
        db_carrier_trunk.from_domain = (
            carrier_trunk.from_domain
            if carrier_trunk.from_domain is not None
            else db_carrier_trunk.from_domain
        )
        db_carrier_trunk.expire_seconds = (
            carrier_trunk.expire_seconds
            if carrier_trunk.expire_seconds is not None
            else db_carrier_trunk.expire_seconds
        )
        db_carrier_trunk.retry_seconds = (
            carrier_trunk.retry_seconds
            if carrier_trunk.retry_seconds is not None
            else db_carrier_trunk.retry_seconds
        )
        db.commit()
        db.refresh(db_carrier_trunk)
    return db_carrier_trunk


def delete_carrier_trunk(
    db: Session, principal: Principal, carrier_trunk_id: int
) -> CarrierTrunk:
    db_carrier_trunk = get_carrier_trunk(db, principal, carrier_trunk_id)
    if db_carrier_trunk is not None:
        db.delete(db_carrier_trunk)
        db.commit()
    return db_carrier_trunk
