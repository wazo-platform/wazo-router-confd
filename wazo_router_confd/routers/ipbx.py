# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_confd.auth import Principal, get_principal
from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import ipbx as schema
from wazo_router_confd.services import ipbx as service


router = APIRouter()


@router.post("/ipbxs", response_model=schema.IPBXRead)
def create_ipbx(
    ipbx: schema.IPBXCreate,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    return service.create_ipbx(db, principal, ipbx=ipbx)


@router.get("/ipbxs", response_model=schema.IPBXList)
def read_ipbxs(
    offset: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    ipbxs = service.get_ipbxs(db, principal, offset=offset, limit=limit)
    return ipbxs


@router.get("/ipbxs/{ipbx_id}", response_model=schema.IPBXRead)
def read_ipbx(
    ipbx_id: int,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_ipbx = service.get_ipbx(db, principal, ipbx_id=ipbx_id)
    if db_ipbx is None:
        raise HTTPException(status_code=404, detail="IPBX not found")
    return db_ipbx


@router.put("/ipbxs/{ipbx_id}", response_model=schema.IPBXRead)
def update_ipbx(
    ipbx_id: int,
    ipbx: schema.IPBXUpdate,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_ipbx = service.update_ipbx(db, principal, ipbx=ipbx, ipbx_id=ipbx_id)
    if db_ipbx is None:
        raise HTTPException(status_code=404, detail="IPBX not found")
    return db_ipbx


@router.delete("/ipbxs/{ipbx_id}", response_model=schema.IPBXRead)
def delete_ipbx(
    ipbx_id: int,
    db: Session = Depends(get_db),
    principal: Principal = Depends(get_principal),
):
    db_ipbx = service.delete_ipbx(db, principal, ipbx_id=ipbx_id)
    if db_ipbx is None:
        raise HTTPException(status_code=404, detail="IPBX not found")
    return db_ipbx
