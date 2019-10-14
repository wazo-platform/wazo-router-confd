# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel


class Carrier(BaseModel):
    id: int
    name: str
    tenant_id: int

    class Config:
        orm_mode = True


class CarrierCreate(BaseModel):
    name: str
    tenant_id: int


class CarrierUpdate(BaseModel):
    name: Optional[str] = None
    tenant_id: int
