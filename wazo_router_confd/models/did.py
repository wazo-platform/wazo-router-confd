# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:
    from .tenant import Tenant  # noqa
    from .ipbx import IPBX  # noqa
    from .carrier_trunk import CarrierTrunk  # noqa


class DID(Base):
    __tablename__ = "dids"
    __table_args__ = (
        Index('tenant_id', 'did_prefix'),
        UniqueConstraint('tenant_id', 'did_regex'),
        ForeignKeyConstraint(
            ['tenant_id', 'ipbx_id'], ['ipbx.tenant_id', 'ipbx.id'], ondelete='CASCADE'
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(
        Integer, ForeignKey('tenants.id', ondelete='CASCADE'), nullable=False
    )
    tenant = relationship('Tenant')
    ipbx_id = Column(Integer, nullable=False)
    ipbx = relationship('IPBX')
    carrier_trunk_id = Column(
        Integer, ForeignKey('carrier_trunks.id', ondelete='CASCADE'), nullable=False
    )
    carrier_trunk = relationship('CarrierTrunk')
    did_regex = Column(String(256))
    did_prefix = Column(String(128))
