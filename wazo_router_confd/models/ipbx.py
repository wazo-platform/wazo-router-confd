# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey,
    ForeignKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:  # pragma: no cover
    from .tenant import Tenant  # noqa
    from .domain import Domain  # noqa
    from .normalization import NormalizationProfile  # noqa


class IPBX(Base):
    __tablename__ = "ipbx"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'id'),
        UniqueConstraint('tenant_id', 'domain_id', 'username'),
        ForeignKeyConstraint(
            ['tenant_id', 'domain_id'],
            ['domains.tenant_id', 'domains.id'],
            ondelete='CASCADE',
        ),
        ForeignKeyConstraint(
            ['tenant_id', 'normalization_profile_id'],
            ['normalization_profiles.tenant_id', 'normalization_profiles.id'],
            ondelete='SET NULL',
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(
        Integer, ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False
    )
    tenant = relationship("Tenant")
    domain_id = Column(Integer, nullable=False)
    domain = relationship("Domain")
    normalization_profile_id = Column(Integer, nullable=True)
    normalization_profile = relationship("NormalizationProfile")
    customer = Column(Integer, nullable=True)
    ip_fqdn = Column(String(256), nullable=False)
    ip_address = Column(String(256), nullable=True)
    port = Column(Integer, nullable=False, default=5060)
    registered = Column(Boolean, default=False, nullable=False)
    username = Column(String(50), nullable=True)
    password = Column(String(192), nullable=True)
    password_ha1 = Column(String(64), nullable=True)
    realm = Column(String(64), nullable=True)
