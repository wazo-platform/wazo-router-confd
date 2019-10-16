# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:
    from .tenant import Tenant  # noqa


class CDR(Base):
    __tablename__ = "cdrs"
    __table_args__ = ()

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(
        Integer, ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False
    )
    tenant = relationship('Tenant')
    source_ip = Column(String(64), nullable=False)
    source_port = Column(Integer, nullable=False, default=5060)
    from_uri = Column(String(256), nullable=False)
    to_uri = Column(String(256), nullable=False)
    call_id = Column(String(256), nullable=False)
    call_start = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)
