# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from time import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from wazo_router_confd.database import get_db
from wazo_router_confd.schemas import normalization as schema
from wazo_router_confd.services import normalization as service


router = APIRouter()


@router.post("/normalization-profiles", response_model=schema.NormalizationProfile)
def create_normalization_profile(
    normalization_profile: schema.NormalizationProfileCreate,
    db: Session = Depends(get_db),
):
    db_normalization_profile = service.get_normalization_profile_by_name(
        db, name=normalization_profile.name
    )
    if db_normalization_profile:
        raise HTTPException(
            status_code=409,
            detail={
                "error_id": "invalid-data",
                "message": "Duplicated match_regex",
                "resource": "normalization_profile",
                "timestamp": time(),
                "details": {
                    "config": {
                        "match_regex": {
                            "constraing_id": "match_regex",
                            "constraint": {"unique": True},
                            "message": "Duplicated match_regex",
                        }
                    }
                },
            },
        )
    return service.create_normalization_profile(
        db=db, normalization_profile=normalization_profile
    )


@router.get("/normalization-profiles", response_model=schema.NormalizationProfileList)
def read_normalization_profiles(
    offset: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    normalization_profiles = service.get_normalization_profiles(
        db, offset=offset, limit=limit
    )
    return normalization_profiles


@router.get(
    "/normalization-profiles/{normalization_profile_id}",
    response_model=schema.NormalizationProfile,
)
def read_normalization_profile(
    normalization_profile_id: int, db: Session = Depends(get_db)
):
    db_normalization_profile = service.get_normalization_profile(
        db, normalization_profile_id=normalization_profile_id
    )
    if db_normalization_profile is None:
        raise HTTPException(status_code=404, detail="Normalization profile not found")
    return db_normalization_profile


@router.put(
    "/normalization-profiles/{normalization_profile_id}",
    response_model=schema.NormalizationProfile,
)
def update_normalization_profile(
    normalization_profile_id: int,
    normalization_profile: schema.NormalizationProfileUpdate,
    db: Session = Depends(get_db),
):
    db_normalization_profile = service.update_normalization_profile(
        db,
        normalization_profile=normalization_profile,
        normalization_profile_id=normalization_profile_id,
    )
    if db_normalization_profile is None:
        raise HTTPException(status_code=404, detail="Normalization profile not found")
    return db_normalization_profile


@router.delete(
    "/normalization-profiles/{normalization_profile_id}",
    response_model=schema.NormalizationProfile,
)
def delete_normalization_profile(
    normalization_profile_id: int, db: Session = Depends(get_db)
):
    db_normalization_profile = service.delete_normalization_profile(
        db, normalization_profile_id=normalization_profile_id
    )
    if db_normalization_profile is None:
        raise HTTPException(status_code=404, detail="Normalization profile not found")
    return db_normalization_profile


@router.post("/normalization-rules", response_model=schema.NormalizationRule)
def create_normalization_rule(
    normalization_rule: schema.NormalizationRuleCreate, db: Session = Depends(get_db)
):
    db_normalization_rule = service.get_normalization_rule_by_match_regex(
        db, match_regex=normalization_rule.match_regex
    )
    if db_normalization_rule:
        raise HTTPException(
            status_code=409,
            detail={
                "error_id": "invalid-data",
                "message": "Duplicated match_regex",
                "resource": "normalization_rule",
                "timestamp": time(),
                "details": {
                    "config": {
                        "match_regex": {
                            "constraing_id": "match_regex",
                            "constraint": {"unique": True},
                            "message": "Duplicated match_regex",
                        }
                    }
                },
            },
        )
    return service.create_normalization_rule(
        db=db, normalization_rule=normalization_rule
    )


@router.get("/normalization-rules", response_model=schema.NormalizationRuleList)
def read_normalization_rules(
    offset: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    normalization_rules = service.get_normalization_rules(
        db, offset=offset, limit=limit
    )
    return normalization_rules


@router.get(
    "/normalization-rules/{normalization_rule_id}",
    response_model=schema.NormalizationRule,
)
def read_normalization_rule(normalization_rule_id: int, db: Session = Depends(get_db)):
    db_normalization_rule = service.get_normalization_rule(
        db, normalization_rule_id=normalization_rule_id
    )
    if db_normalization_rule is None:
        raise HTTPException(status_code=404, detail="Normalization rule not found")
    return db_normalization_rule


@router.put(
    "/normalization-rules/{normalization_rule_id}",
    response_model=schema.NormalizationRule,
)
def update_normalization_rule(
    normalization_rule_id: int,
    normalization_rule: schema.NormalizationRuleUpdate,
    db: Session = Depends(get_db),
):
    db_normalization_rule = service.update_normalization_rule(
        db,
        normalization_rule=normalization_rule,
        normalization_rule_id=normalization_rule_id,
    )
    if db_normalization_rule is None:
        raise HTTPException(status_code=404, detail="Normalization rule not found")
    return db_normalization_rule


@router.delete(
    "/normalization-rules/{normalization_rule_id}",
    response_model=schema.NormalizationRule,
)
def delete_normalization_rule(
    normalization_rule_id: int, db: Session = Depends(get_db)
):
    db_normalization_rule = service.delete_normalization_rule(
        db, normalization_rule_id=normalization_rule_id
    )
    if db_normalization_rule is None:
        raise HTTPException(status_code=404, detail="Normalization rule not found")
    return db_normalization_rule
