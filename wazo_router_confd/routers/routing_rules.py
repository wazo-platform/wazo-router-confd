# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import routing_rule as schema
from wazo_router_confd.services import routing_rule as service


router = APIRouter()


@router.post("/routing-rules", response_model=schema.RoutingRule)
def create_routing_rule(
    routing_rule: schema.RoutingRuleCreate, db: Session = Depends(get_db)
):
    return service.create_routing_rule(db=db, routing_rule=routing_rule)


@router.get("/routing-rules", response_model=schema.RoutingRuleList)
def read_routing_rules(
    offset: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    routing_rules = service.get_routing_rules(db, offset=offset, limit=limit)
    return routing_rules


@router.get("/routing-rules/{routing_rule_id}", response_model=schema.RoutingRule)
def read_routing_rule(routing_rule_id: int, db: Session = Depends(get_db)):
    db_routing_rule = service.get_routing_rule(db, routing_rule_id=routing_rule_id)
    if db_routing_rule is None:
        raise HTTPException(status_code=404, detail="RoutingRule not found")
    return db_routing_rule


@router.put("/routing-rules/{routing_rule_id}", response_model=schema.RoutingRule)
def update_routing_rule(
    routing_rule_id: int,
    routing_rule: schema.RoutingRuleUpdate,
    db: Session = Depends(get_db),
):
    db_routing_rule = service.update_routing_rule(
        db, routing_rule_id=routing_rule_id, routing_rule=routing_rule
    )
    if db_routing_rule is None:
        raise HTTPException(status_code=404, detail="RoutingRule not found")
    return db_routing_rule


@router.delete("/routing-rules/{routing_rule_id}", response_model=schema.RoutingRule)
def delete_routing_rule(routing_rule_id: int, db: Session = Depends(get_db)):
    db_routing_rule = service.delete_routing_rule(db, routing_rule_id=routing_rule_id)
    if db_routing_rule is None:
        raise HTTPException(status_code=404, detail="RoutingRule not found")
    return db_routing_rule
