# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:  # pragma: no cover
    from .carrier import Carrier  # noqa


class CarrierTrunk(Base):
    __tablename__ = "carrier_trunks"
    __table_args__ = ()

    id = Column(Integer, primary_key=True, index=True)
    carrier_id = Column(
        Integer,
        ForeignKey('carriers.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    carrier = relationship('Carrier')
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
