# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from .base import Base

if TYPE_CHECKING:  # pragma: no cover
    from .tenant import Tenant  # noqa
    from .carrier_trunk import CarrierTrunk  # noqa
    from .ipbx import IPBX  # noqa


class CDR(Base):
    __tablename__ = "cdrs"
    __table_args__ = ()

    id = Column(Integer, primary_key=True, index=True)
    tenant_uuid = Column(
        UUIDType(), ForeignKey('tenants.uuid', ondelete='CASCADE'), nullable=False
    )
    tenant = relationship('Tenant')
    ipbx_id = Column(Integer, ForeignKey('ipbx.id', ondelete='CASCADE'), nullable=True)
    ipbx = relationship('IPBX')
    carrier_trunk_id = Column(
        Integer, ForeignKey('carrier_trunks.id', ondelete='CASCADE'), nullable=True
    )
    carrier_trunk = relationship('CarrierTrunk')
    source_ip = Column(String(64), nullable=False)
    source_port = Column(Integer, nullable=False, default=5060)
    from_uri = Column(String(256), nullable=False)
    to_uri = Column(String(256), nullable=False)
    call_id = Column(String(256), nullable=False)
    call_start = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)
