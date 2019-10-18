# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel, constr


class Carrier(BaseModel):
    id: int
    name: constr(max_length=256)  # type: ignore
    tenant_id: int

    class Config:
        orm_mode = True


class CarrierCreate(BaseModel):
    name: constr(max_length=256)  # type: ignore
    tenant_id: int


class CarrierUpdate(BaseModel):
    name: Optional[constr(max_length=256)] = None  # type: ignore
    tenant_id: int
