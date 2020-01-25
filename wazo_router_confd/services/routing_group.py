# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy.orm import Session

from wazo_router_confd.auth import Principal
from wazo_router_confd.models.routing_group import RoutingGroup
from wazo_router_confd.schemas import routing_group as schema
from wazo_router_confd.services import tenant as tenant_service


def get_routing_group(
    db: Session, principal: Principal, routing_group_id: int
) -> RoutingGroup:
    db_routing_group = db.query(RoutingGroup).filter(
        RoutingGroup.id == routing_group_id
    )
    if principal is not None and principal.tenant_uuids:
        db_routing_group = db_routing_group.filter(
            RoutingGroup.tenant_uuid.in_(principal.tenant_uuids)
        )
    return db_routing_group.first()


def get_routing_groups(
    db: Session, principal: Principal, offset: int = 0, limit: int = 100
) -> schema.RoutingGroupList:
    items = db.query(RoutingGroup)
    if principal is not None and principal.tenant_uuid:
        items = items.filter(RoutingGroup.tenant_uuid == principal.tenant_uuid)
    items = items.offset(offset).limit(limit).all()
    return schema.RoutingGroupList(items=items)


def create_routing_group(
    db: Session, principal: Principal, routing_group: schema.RoutingGroupCreate
) -> RoutingGroup:
    routing_group.tenant_uuid = tenant_service.get_uuid(
        principal, db, routing_group.tenant_uuid
    )
    db_routing_group = RoutingGroup(
        routing_rule_id=routing_group.routing_rule_id,
        tenant_uuid=routing_group.tenant_uuid,
    )
    db.add(db_routing_group)
    db.commit()
    db.refresh(db_routing_group)
    return db_routing_group


def update_routing_group(
    db: Session,
    principal: Principal,
    routing_group_id: int,
    routing_group: schema.RoutingGroupUpdate,
) -> RoutingGroup:
    db_routing_group = get_routing_group(db, principal, routing_group_id)
    if db_routing_group is not None:
        db_routing_group.routing_rule_id = (
            routing_group.routing_rule_id
            if routing_group.routing_rule_id is not None
            else db_routing_group.routing_rule_id
        )
        db_routing_group.tenant_uuid = (
            routing_group.tenant_uuid
            if routing_group.tenant_uuid is not None
            else db_routing_group.tenant_uuid
        )
        db.commit()
        db.refresh(db_routing_group)
    return db_routing_group


def delete_routing_group(
    db: Session, principal: Principal, routing_group_id: int
) -> RoutingGroup:
    db_routing_group = get_routing_group(db, principal, routing_group_id)
    if db_routing_group is not None:
        db.delete(db_routing_group)
        db.commit()
    return db_routing_group
