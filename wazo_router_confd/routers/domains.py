# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from time import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_confd.auth import Principal, get_principal
from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import domain as schema
from wazo_router_confd.services import domain as service


router = APIRouter()


@router.post("/domains", response_model=schema.Domain)
def create_domain(
    domain: schema.DomainCreate,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_domain = service.get_domain(db, principal, domain=domain.domain)
    if db_domain:
        raise HTTPException(
            status_code=409,
            detail={
                "error_id": "invalid-data",
                "message": "Duplicated name",
                "resource": "domain",
                "timestamp": time(),
                "details": {
                    "config": {
                        "name": {
                            "constraing_id": "name",
                            "constraint": {"unique": True},
                            "message": "Duplicated name",
                        }
                    }
                },
            },
        )
    return service.create_domain(db, principal, domain=domain)


@router.get("/domains", response_model=schema.DomainList)
def read_domains(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    domains = service.get_domains(db, principal, offset=offset, limit=limit)
    return domains


@router.get("/domains/{domain_id}", response_model=schema.Domain)
def read_domain(
    domain_id: int,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_domain = service.get_domain_by_id(db, principal, domain_id=domain_id)
    if db_domain is None:
        raise HTTPException(status_code=404, detail="Domain not found")
    return db_domain


@router.put("/domains/{domain_id}", response_model=schema.Domain)
def update_domain(
    domain_id: int,
    domain: schema.DomainUpdate,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_domain = service.update_domain(db, principal, domain=domain, domain_id=domain_id)
    if db_domain is None:
        raise HTTPException(status_code=404, detail="Domain not found")
    return db_domain


@router.delete("/domains/{domain_id}", response_model=schema.Domain)
def delete_domain(
    domain_id: int,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_domain = service.delete_domain(db, principal, domain_id=domain_id)
    if db_domain is None:
        raise HTTPException(status_code=404, detail="Domain not found")
    return db_domain
