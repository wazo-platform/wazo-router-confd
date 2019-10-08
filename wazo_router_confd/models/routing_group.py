# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:
    from .tenant import Tenant  # noqa


class RoutingGroup(Base):
    __tablename__ = "routing_groups"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(
        Integer, ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False
    )
    tenant = relationship('Tenant')
    routing_rule = Column(
        Integer, ForeignKey('routing_rules.id', ondelete='CASCADE'), nullable=True
    )
