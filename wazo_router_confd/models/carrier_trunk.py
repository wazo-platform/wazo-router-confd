# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    ForeignKeyConstraint,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .base import Base

if TYPE_CHECKING:  # pragma: no cover
    from .carrier import Carrier  # noqa
    from .normalization import NormalizationProfile  # noqa
    from .tenant import Tenant  # noqa


class CarrierTrunk(Base):
    __tablename__ = "carrier_trunks"
    __table_args__ = (
        ForeignKeyConstraint(
            ['tenant_uuid', 'carrier_id'],
            ['carriers.tenant_uuid', 'carriers.id'],
            ondelete='CASCADE',
        ),
        ForeignKeyConstraint(
            ['tenant_uuid', 'normalization_profile_id'],
            ['normalization_profiles.tenant_uuid', 'normalization_profiles.id'],
            ondelete='SET NULL',
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    tenant_uuid = Column(  # type: ignore
        UUIDType(), ForeignKey('tenants.uuid', ondelete='CASCADE'), nullable=False
    )
    tenant = relationship("Tenant")
    carrier_id = Column(Integer, nullable=False)
    carrier = relationship('Carrier')
    normalization_profile_id = Column(Integer, nullable=True)
    normalization_profile = relationship("NormalizationProfile")
    name = Column(String(256), unique=True, index=True)
    sip_proxy = Column(String(128), nullable=False)
    sip_proxy_port = Column(Integer, nullable=False, default=5060)
    ip_address = Column(String(256), nullable=True)
    registered = Column(Boolean, default=False)
    auth_username = Column(String(35), nullable=True)
    auth_password = Column(String(192), nullable=True)
    realm = Column(String(64), nullable=True)
    registrar_proxy = Column(String(128), nullable=True)
    from_domain = Column(String(64), nullable=True)
    expire_seconds = Column(Integer, nullable=False, default=3600)
    retry_seconds = Column(Integer, nullable=False, default=30)
