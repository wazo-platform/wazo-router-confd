# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .base import Base

if TYPE_CHECKING:  # pragma: no cover
    from .tenant import Tenant  # noqa


class Domain(Base):
    __tablename__ = "domains"
    __table_args__ = (
        UniqueConstraint('tenant_uuid', 'id'),
        UniqueConstraint('tenant_uuid', 'domain'),
    )

    id = Column(Integer, primary_key=True, index=True)
    tenant_uuid = Column(
        UUIDType(), ForeignKey('tenants.uuid', ondelete='CASCADE'), nullable=False
    )
    tenant = relationship('Tenant')
    domain = Column(String(64))
