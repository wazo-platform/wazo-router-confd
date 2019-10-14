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

if TYPE_CHECKING:
    from .tenant import Tenant  # noqa
    from .domain import Domain  # noqa


class IPBX(Base):
    __tablename__ = "ipbx"
    __table_args__ = (
        UniqueConstraint('tenant_id', 'id'),
        ForeignKeyConstraint(
            ['tenant_id', 'domain_id'],
            ['domains.tenant_id', 'domains.id'],
            ondelete='CASCADE',
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(
        Integer, ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False
    )
    tenant = relationship("Tenant")
    domain_id = Column(Integer, nullable=False)
    domain = relationship("Domain")
    customer = Column(Integer, nullable=True)
    ip_fqdn = Column(String, nullable=False)
    port = Column(Integer, nullable=False, default=5060)
    registered = Column(Boolean, default=False, nullable=False)
    username = Column(String(50), nullable=True)
    sha1 = Column(String(128), nullable=True)
    sha1b = Column(String(128), nullable=True)
