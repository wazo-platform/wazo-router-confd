from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

if TYPE_CHECKING:
    from .carrier_trunk import CarrierTrunk  # noqa
    from .ipbx import IPBX  # noqa


class RoutingRule(Base):
    __tablename__ = "routing_rules"

    id = Column(Integer, primary_key=True, index=True)
    prefix = Column(String(15), nullable=True)
    carrier_trunk_id = Column(Integer, ForeignKey('carrier_trunks.id', ondelete='CASCADE'), nullable=False)
    carrier_trunk = relationship('CarrierTrunk')
    ipbx_id = Column(Integer, ForeignKey('ipbx.id', ondelete='CASCADE'), nullable=False)
    ipbx = relationship('IPBX')
    did_regex = Column(String, nullable=True)
    route_type = Column(String(10), nullable=False, default='pstn')
