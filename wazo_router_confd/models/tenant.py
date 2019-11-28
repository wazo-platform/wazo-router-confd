# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import UUIDType

from .base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), unique=True, index=True)
    uuid = Column(UUIDType(), unique=True, index=True)
