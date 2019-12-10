# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from sqlalchemy import Column, String
from sqlalchemy_utils import UUIDType

from .base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    name = Column(String(256), unique=True, index=True)
    uuid = Column(UUIDType(), primary_key=True, index=True)
