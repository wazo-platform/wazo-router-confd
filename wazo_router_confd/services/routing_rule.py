# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from sqlalchemy.orm import Session

from wazo_router_confd.models.routing_rule import RoutingRule
from wazo_router_confd.schemas import routing_rule as schema


def get_routing_rule(db: Session, routing_rule_id: int) -> RoutingRule:
    return db.query(RoutingRule).filter(RoutingRule.id == routing_rule_id).first()


def get_routing_rules(
    db: Session, offset: int = 0, limit: int = 100
) -> List[RoutingRule]:
    return db.query(RoutingRule).offset(offset).limit(limit).all()


def create_routing_rule(
    db: Session, routing_rule: schema.RoutingRuleCreate
) -> RoutingRule:
    db_routing_rule = RoutingRule(
        prefix=routing_rule.prefix,
        carrier_trunk_id=routing_rule.carrier_trunk_id,
        ipbx_id=routing_rule.ipbx_id,
        did_regex=routing_rule.did_regex,
        route_type=routing_rule.route_type,
    )
    db.add(db_routing_rule)
    db.commit()
    db.refresh(db_routing_rule)
    return db_routing_rule


def update_routing_rule(
    db: Session, routing_rule_id: int, routing_rule: schema.RoutingRuleUpdate
) -> RoutingRule:
    db_routing_rule = (
        db.query(RoutingRule).filter(RoutingRule.id == routing_rule_id).first()
    )
    if db_routing_rule is not None:
        db_routing_rule.prefix = (
            routing_rule.prefix
            if routing_rule.prefix is not None
            else db_routing_rule.prefix
        )
        db_routing_rule.carrier_trunk_id = (
            routing_rule.carrier_trunk_id
            if routing_rule.carrier_trunk_id is not None
            else db_routing_rule.carrier_trunk_id
        )
        db_routing_rule.ipbx_id = (
            routing_rule.ipbx_id
            if routing_rule.ipbx_id is not None
            else db_routing_rule.ipbx_id
        )
        db_routing_rule.did_regex = (
            routing_rule.did_regex
            if routing_rule.did_regex is not None
            else db_routing_rule.did_regex
        )
        db_routing_rule.route_type = (
            routing_rule.route_type
            if routing_rule.route_type is not None
            else db_routing_rule.route_type
        )
        db.commit()
        db.refresh(db_routing_rule)
    return db_routing_rule


def delete_routing_rule(db: Session, routing_rule_id: int) -> RoutingRule:
    db_routing_rule = (
        db.query(RoutingRule).filter(RoutingRule.id == routing_rule_id).first()
    )
    if db_routing_rule is not None:
        db.delete(db_routing_rule)
        db.commit()
    return db_routing_rule
