# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from typing import List, Optional

from sqlalchemy.orm import Session

from wazo_router_confd.models.normalization import (
    NormalizationProfile,
    NormalizationRule,
)
from wazo_router_confd.schemas import normalization as schema


re_clean_number = re.compile('[^0-9,]').sub
re_match_prefix_from_regex = re.compile('[^0-9]')


def get_match_prefix_from_regex(match_regex: Optional[str] = None) -> str:
    did_prefix = (
        re_match_prefix_from_regex.split(match_regex.lstrip('^'))[0]
        if match_regex is not None
        else ''
    )
    return did_prefix


def get_normalization_profile(
    db: Session, normalization_profile_id: int
) -> NormalizationProfile:
    return (
        db.query(NormalizationProfile)
        .filter(NormalizationProfile.id == normalization_profile_id)
        .first()
    )


def get_normalization_profile_by_name(
    db: Session, name: Optional[str]
) -> NormalizationProfile:
    return (
        db.query(NormalizationProfile).filter(NormalizationProfile.name == name).first()
    )


def get_normalization_profiles(
    db: Session, offset: int = 0, limit: int = 100
) -> List[NormalizationProfile]:
    return db.query(NormalizationProfile).offset(offset).limit(limit).all()


def create_normalization_profile(
    db: Session, normalization_profile: schema.NormalizationProfileCreate
) -> NormalizationProfile:
    db_normalization_profile = NormalizationProfile(
        name=normalization_profile.name,
        tenant_id=normalization_profile.tenant_id,
        country_code=normalization_profile.country_code,
        area_code=normalization_profile.area_code,
        intl_prefix=normalization_profile.intl_prefix,
        ld_prefix=normalization_profile.ld_prefix,
        always_ld=normalization_profile.always_ld,
        always_intl_prefix_plus=normalization_profile.always_intl_prefix_plus,
    )
    db.add(db_normalization_profile)
    db.commit()
    db.refresh(db_normalization_profile)
    return db_normalization_profile


def update_normalization_profile(
    db: Session,
    normalization_profile_id: int,
    normalization_profile: schema.NormalizationProfileUpdate,
) -> NormalizationProfile:
    db_normalization_profile = (
        db.query(NormalizationProfile)
        .filter(NormalizationProfile.id == normalization_profile_id)
        .first()
    )
    if db_normalization_profile is not None:
        db_normalization_profile.tenant_id = (
            normalization_profile.tenant_id
            if normalization_profile.tenant_id is not None
            else db_normalization_profile.tenant_id
        )
        db_normalization_profile.country_code = (
            normalization_profile.country_code
            if normalization_profile.country_code is not None
            else db_normalization_profile.country_code
        )
        db_normalization_profile.name = (
            normalization_profile.name
            if normalization_profile.name is not None
            else db_normalization_profile.name
        )
        db_normalization_profile.area_code = (
            normalization_profile.area_code
            if normalization_profile.area_code is not None
            else db_normalization_profile.area_code
        )
        db_normalization_profile.intl_prefix = (
            normalization_profile.intl_prefix
            if normalization_profile.intl_prefix is not None
            else db_normalization_profile.intl_prefix
        )
        db_normalization_profile.ld_prefix = (
            normalization_profile.ld_prefix
            if normalization_profile.ld_prefix is not None
            else db_normalization_profile.ld_prefix
        )
        db_normalization_profile.always_ld = (
            normalization_profile.always_ld
            if normalization_profile.always_ld is not None
            else db_normalization_profile.always_ld
        )
        db_normalization_profile.always_intl_prefix_plus = (
            normalization_profile.always_intl_prefix_plus
            if normalization_profile.always_intl_prefix_plus is not None
            else db_normalization_profile.always_intl_prefix_plus
        )
        db.commit()
        db.refresh(db_normalization_profile)
    return db_normalization_profile


def delete_normalization_profile(
    db: Session, normalization_profile_id: int
) -> NormalizationProfile:
    db_normalization_profile = (
        db.query(NormalizationProfile)
        .filter(NormalizationProfile.id == normalization_profile_id)
        .first()
    )
    if db_normalization_profile is not None:
        db.delete(db_normalization_profile)
        db.commit()
    return db_normalization_profile


def get_normalization_rule(
    db: Session, normalization_rule_id: int
) -> NormalizationRule:
    return (
        db.query(NormalizationRule)
        .filter(NormalizationRule.id == normalization_rule_id)
        .first()
    )


def get_normalization_rule_by_match_regex(
    db: Session, match_regex: Optional[str]
) -> NormalizationRule:
    return (
        db.query(NormalizationRule)
        .filter(NormalizationRule.match_regex == match_regex)
        .first()
    )


def get_normalization_rules(
    db: Session, offset: int = 0, limit: int = 100
) -> List[NormalizationRule]:
    return db.query(NormalizationRule).offset(offset).limit(limit).all()


def create_normalization_rule(
    db: Session, normalization_rule: schema.NormalizationRuleCreate
) -> NormalizationRule:
    db_normalization_rule = NormalizationRule(
        profile_id=normalization_rule.profile_id,
        rule_type=normalization_rule.rule_type,
        priority=normalization_rule.priority,
        match_regex=normalization_rule.match_regex,
        match_prefix=get_match_prefix_from_regex(normalization_rule.match_regex),
        replace_regex=normalization_rule.replace_regex,
    )
    db.add(db_normalization_rule)
    db.commit()
    db.refresh(db_normalization_rule)
    return db_normalization_rule


def update_normalization_rule(
    db: Session,
    normalization_rule_id: int,
    normalization_rule: schema.NormalizationRuleUpdate,
) -> NormalizationRule:
    db_normalization_rule = (
        db.query(NormalizationRule)
        .filter(NormalizationRule.id == normalization_rule_id)
        .first()
    )
    if db_normalization_rule is not None:
        db_normalization_rule.profile_id = (
            normalization_rule.profile_id
            if normalization_rule.profile_id is not None
            else db_normalization_rule.profile_id
        )
        db_normalization_rule.rule_type = (
            normalization_rule.rule_type
            if normalization_rule.rule_type is not None
            else db_normalization_rule.rule_type
        )
        db_normalization_rule.priority = (
            normalization_rule.priority
            if normalization_rule.priority is not None
            else db_normalization_rule.priority
        )
        db_normalization_rule.match_regex = (
            normalization_rule.match_regex
            if normalization_rule.match_regex is not None
            else db_normalization_rule.match_regex
        )
        db_normalization_rule.match_prefix = get_match_prefix_from_regex(
            db_normalization_rule.match_regex
        )
        db_normalization_rule.replace_regex = (
            normalization_rule.replace_regex
            if normalization_rule.replace_regex is not None
            else db_normalization_rule.replace_regex
        )
        db.commit()
        db.refresh(db_normalization_rule)
    return db_normalization_rule


def delete_normalization_rule(
    db: Session, normalization_rule_id: int
) -> NormalizationRule:
    db_normalization_rule = (
        db.query(NormalizationRule)
        .filter(NormalizationRule.id == normalization_rule_id)
        .first()
    )
    if db_normalization_rule is not None:
        db.delete(db_normalization_rule)
        db.commit()
    return db_normalization_rule


def normalize_local_number_to_e164(
    db: Session, number: str, profile: Optional[NormalizationProfile] = None
) -> str:
    number = re_clean_number('', number)
    if profile is not None:
        prefixes = [number[:i] for i in range(0, min(10, len(number)))]
        rules = (
            db.query(NormalizationRule)
            .filter(NormalizationRule.profile_id == profile.id)
            .filter(NormalizationRule.match_prefix.in_(prefixes))
            .filter(NormalizationRule.rule_type == 1)
            .order_by(NormalizationRule.priority)
            .order_by(NormalizationRule.id)
        )
        for rule in rules:
            number = re.sub(rule.match_regex, rule.replace_regex, number)
    return number


def normalize_e164_to_local_number(
    db: Session, number: str, profile: Optional[NormalizationProfile] = None
) -> str:
    number = re_clean_number('', number)
    if profile is not None:
        prefixes = [number[:i] for i in range(0, min(10, len(number)))]
        rules = (
            db.query(NormalizationRule)
            .filter(NormalizationRule.profile_id == profile.id)
            .filter(NormalizationRule.match_prefix.in_(prefixes))
            .filter(NormalizationRule.rule_type == 2)
            .order_by(NormalizationRule.priority)
            .order_by(NormalizationRule.id)
        )
        for rule in rules:
            number = re.sub(rule.match_regex, rule.replace_regex, number)
        if profile.always_intl_prefix_plus:
            number = "+%s" % number
    return number
