# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import cdr as schema
from wazo_router_confd.services import cdr as service


router = APIRouter()


@router.post("/cdrs/", response_model=schema.CDR)
def create_cdr(cdr: schema.CDRCreate, db: Session = Depends(get_db)):
    return service.create_cdr(db=db, cdr=cdr)


@router.get("/cdrs/", response_model=List[schema.CDR])
def read_cdrs(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cdrs = service.get_cdrs(db, offset=offset, limit=limit)
    return cdrs


@router.get("/cdrs/{cdr_id}", response_model=schema.CDR)
def read_cdr(cdr_id: int, db: Session = Depends(get_db)):
    db_cdr = service.get_cdr(db, cdr_id=cdr_id)
    if db_cdr is None:
        raise HTTPException(status_code=404, detail="CDR not found")
    return db_cdr


@router.put("/cdrs/{cdr_id}", response_model=schema.CDR)
def update_cdr(cdr_id: int, cdr: schema.CDRUpdate, db: Session = Depends(get_db)):
    db_cdr = service.update_cdr(db, cdr=cdr, cdr_id=cdr_id)
    if db_cdr is None:
        raise HTTPException(status_code=404, detail="CDR not found")
    return db_cdr


@router.delete("/cdrs/{cdr_id}", response_model=schema.CDR)
def delete_cdr(cdr_id: int, db: Session = Depends(get_db)):
    db_cdr = service.delete_cdr(db, cdr_id=cdr_id)
    if db_cdr is None:
        raise HTTPException(status_code=404, detail="CDR not found")
    return db_cdr
