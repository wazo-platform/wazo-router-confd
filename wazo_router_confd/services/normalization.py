# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from typing import Any, List, Optional

from psycopg2.extras import DictCursor  # type: ignore

from sqlalchemy.orm import Session


from wazo_router_confd.auth import Principal
from wazo_router_confd.models.normalization import (
    NormalizationProfile,
    NormalizationRule,
)
from wazo_router_confd.schemas import normalization as schema
from wazo_router_confd.services import tenant as tenant_service


re_clean_number = re.compile('[^0-9a-zA-Z]').sub
re_match_prefix_from_regex = re.compile('[^0-9a-zA-Z]')


def get_match_prefix_from_regex(match_regex: Optional[str] = None) -> str:
    did_prefix = (
        re_match_prefix_from_regex.split(match_regex.lstrip('^'))[0]
        if match_regex is not None
        else ''
    )
    return did_prefix


def get_normalization_profile(
    db: Session, principal: Principal, normalization_profile_id: int
) -> NormalizationProfile:
    db_normalization_profile = db.query(NormalizationProfile).filter(
        NormalizationProfile.id == normalization_profile_id
    )
    if principal is not None and principal.tenant_uuids:
        db_normalization_profile = db_normalization_profile.filter(
            NormalizationProfile.tenant_uuid.in_(principal.tenant_uuids)
        )
    return db_normalization_profile.first()


def get_normalization_profile_by_name(
    db: Session, principal: Principal, name: Optional[str]
) -> NormalizationProfile:
    db_normalization_profile = db.query(NormalizationProfile).filter(
        NormalizationProfile.name == name
    )
    if principal is not None and principal.tenant_uuids:
        db_normalization_profile = db_normalization_profile.filter(
            NormalizationProfile.tenant_uuid.in_(principal.tenant_uuids)
        )
    return db_normalization_profile.first()


def get_normalization_profiles(
    db: Session, principal: Principal, offset: int = 0, limit: int = 100
) -> schema.NormalizationProfileList:
    items = db.query(NormalizationProfile)
    if principal is not None and principal.tenant_uuid:
        items = items.filter(NormalizationProfile.tenant_uuid == principal.tenant_uuid)
    items = items.offset(offset).limit(limit).all()
    return schema.NormalizationProfileList(items=items)


def create_normalization_profile(
    db: Session,
    principal: Principal,
    normalization_profile: schema.NormalizationProfileCreate,
) -> NormalizationProfile:
    normalization_profile.tenant_uuid = tenant_service.get_uuid(
        principal, db, normalization_profile.tenant_uuid
    )
    db_normalization_profile = NormalizationProfile(
        name=normalization_profile.name,
        tenant_uuid=normalization_profile.tenant_uuid,
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
    principal: Principal,
    normalization_profile_id: int,
    normalization_profile: schema.NormalizationProfileUpdate,
) -> NormalizationProfile:
    db_normalization_profile = get_normalization_profile(
        db, principal, normalization_profile_id
    )
    if db_normalization_profile is not None:
        db_normalization_profile.tenant_uuid = (
            normalization_profile.tenant_uuid
            if normalization_profile.tenant_uuid is not None
            else db_normalization_profile.tenant_uuid
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
    db: Session, principal: Principal, normalization_profile_id: int
) -> NormalizationProfile:
    db_normalization_profile = get_normalization_profile(
        db, principal, normalization_profile_id
    )
    if db_normalization_profile is not None:
        db.delete(db_normalization_profile)
        db.commit()
    return db_normalization_profile


def get_normalization_rule(
    db: Session, principal: Principal, normalization_rule_id: int
) -> NormalizationRule:
    db_normalization_rule = db.query(NormalizationRule).filter(
        NormalizationRule.id == normalization_rule_id
    )
    if principal is not None and principal.tenant_uuids:
        db_normalization_rule = db_normalization_rule.join(NormalizationProfile).filter(
            NormalizationProfile.tenant_uuid.in_(principal.tenant_uuids)
        )
    return db_normalization_rule.first()


def get_normalization_rule_by_match_regex(
    db: Session, principal: Principal, match_regex: Optional[str]
) -> NormalizationRule:
    db_normalization_rule = db.query(NormalizationRule).filter(
        NormalizationRule.match_regex == match_regex
    )
    if principal is not None and principal.tenant_uuids:
        db_normalization_rule = db_normalization_rule.join(NormalizationProfile).filter(
            NormalizationProfile.tenant_uuid.in_(principal.tenant_uuids)
        )
    return db_normalization_rule.first()


def get_normalization_rules(
    db: Session, principal: Principal, offset: int = 0, limit: int = 100
) -> schema.NormalizationRuleList:
    items = db.query(NormalizationRule)
    if principal is not None and principal.tenant_uuid:
        items = items.join(NormalizationProfile).filter(
            NormalizationProfile.tenant_uuid == principal.tenant_uuid
        )
    items = items.offset(offset).limit(limit).all()
    return schema.NormalizationRuleList(items=items)


def create_normalization_rule(
    db: Session,
    principal: Principal,
    normalization_rule: schema.NormalizationRuleCreate,
) -> NormalizationRule:
    profile = get_normalization_profile(db, principal, normalization_rule.profile_id)
    if profile is None:
        return None
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
    principal: Principal,
    normalization_rule_id: int,
    normalization_rule: schema.NormalizationRuleUpdate,
) -> NormalizationRule:
    db_normalization_rule = get_normalization_rule(db, principal, normalization_rule_id)
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
    db: Session, principal: Principal, normalization_rule_id: int
) -> NormalizationRule:
    db_normalization_rule = get_normalization_rule(db, principal, normalization_rule_id)
    if db_normalization_rule is not None:
        db.delete(db_normalization_rule)
        db.commit()
    return db_normalization_rule


async def normalize_local_number_to_e164(
    conn: Any, number: str, profile: Optional[NormalizationProfile] = None
) -> str:
    number = re_clean_number('', number)
    if profile is not None:
        prefixes = [number[:i] for i in range(0, min(10, len(number)))]
        sql = (
            "SELECT match_regex, replace_regex "
            "FROM normalization_rules "
            "WHERE profile_id = %s AND rule_type = 1 AND match_prefix = ANY(%s) "
            "ORDER BY priority, id;"
        )
        rules = []
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(sql, [profile.id, prefixes])
            async for rule in cur:
                rules.append(rule)
        number = normalize_apply_rules(number, rules)
    return number


async def normalize_e164_to_local_number(
    conn: Any, number: str, profile: Optional[NormalizationProfile] = None
) -> str:
    number = re_clean_number('', number)
    if profile is not None:
        prefixes = [number[:i] for i in range(0, min(10, len(number)))]
        sql = (
            "SELECT match_regex, replace_regex "
            "FROM normalization_rules "
            "WHERE profile_id = %s AND rule_type = 2 AND match_prefix = ANY(%s) "
            "ORDER BY priority, id;"
        )
        rules = []
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute(sql, [profile.id, prefixes])
            async for rule in cur:
                rules.append(rule)
        number = normalize_apply_rules(number, rules)
        if profile.always_intl_prefix_plus:
            number = "+%s" % number
    return number


def normalize_apply_rules(number: str, rules: List[dict]) -> str:
    for rule in rules:
        number = re.sub(rule['match_regex'], rule['replace_regex'], number)
    return number
