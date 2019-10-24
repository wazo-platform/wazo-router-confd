# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from pydantic import BaseModel, constr
from typing import Optional


class Tenant(BaseModel):
    id: int
    name: constr(max_length=256)  # type: ignore
    uuid: Optional[constr(max_length=32)]  # type: ignore

    class Config:
        orm_mode = True


class TenantCreate(BaseModel):
    name: str
    uuid: Optional[constr(max_length=32)]  # type: ignore


class TenantUpdate(BaseModel):
    name: str
