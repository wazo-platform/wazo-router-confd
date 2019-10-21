# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:  # pragma: no cover
    from .tenant import Tenant  # noqa


class NormalizationProfile(Base):
    __tablename__ = "normalization_profiles"
    __table_args__ = (UniqueConstraint('tenant_id', 'id'),)

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(
        Integer, ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False
    )
    tenant = relationship('Tenant')
    name = Column(String(256), nullable=False, unique=True)
    country_code = Column(String(64), nullable=True)
    area_code = Column(String(64), nullable=True)
    intl_prefix = Column(String(64), nullable=True)
    ld_prefix = Column(String(64), nullable=True)
    always_ld = Column(Boolean, nullable=False, default=False)


class NormalizationRule(Base):
    __tablename__ = "normalization_rules"
    __table_args__ = (UniqueConstraint('profile_id', 'match_regex'),)

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(
        Integer,
        ForeignKey('normalization_profiles.id', ondelete='CASCADE'),
        nullable=False,
    )
    profile = relationship('NormalizationProfile')
    match_regex = Column(String(256), nullable=False)
    match_prefix = Column(String(256), nullable=False)
    replace_regex = Column(String(256), nullable=False)
