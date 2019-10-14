# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from time import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import did as schema
from wazo_router_confd.services import did as service


router = APIRouter()


@router.post("/dids/", response_model=schema.DID)
def create_did(did: schema.DIDCreate, db: Session = Depends(get_db)):
    db_did = service.get_did_by_regex(db, regex=did.did_regex)
    if db_did:
        raise HTTPException(
            status_code=409,
            detail={
                "error_id": "invalid-data",
                "message": "Duplicated did_regex",
                "resource": "did",
                "timestamp": time(),
                "details": {
                    "config": {
                        "did_regex": {
                            "constraing_id": "did_regex",
                            "constraint": {"unique": True},
                            "message": "Duplicated did_regex",
                        }
                    }
                },
            },
        )
    return service.create_did(db=db, did=did)


@router.get("/dids/", response_model=List[schema.DID])
def read_dids(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    dids = service.get_dids(db, offset=offset, limit=limit)
    return dids


@router.get("/dids/{did_id}", response_model=schema.DID)
def read_did(did_id: int, db: Session = Depends(get_db)):
    db_did = service.get_did(db, did_id=did_id)
    if db_did is None:
        raise HTTPException(status_code=404, detail="DID not found")
    return db_did


@router.put("/dids/{did_id}", response_model=schema.DID)
def update_carrier(did_id: int, did: schema.DIDUpdate, db: Session = Depends(get_db)):
    db_did = service.update_did(db, did=did, did_id=did_id)
    if db_did is None:
        raise HTTPException(status_code=404, detail="DID not found")
    return db_did


@router.delete("/dids/{did_id}", response_model=schema.DID)
def delete_carrier(did_id: int, db: Session = Depends(get_db)):
    db_did = service.delete_did(db, did_id=did_id)
    if db_did is None:
        raise HTTPException(status_code=404, detail="DID not found")
    return db_did
