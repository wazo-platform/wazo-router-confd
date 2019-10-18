# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from pydantic import BaseModel, constr


class Tenant(BaseModel):
    id: int
    name: constr(max_length=256)

    class Config:
        orm_mode = True


class TenantCreate(BaseModel):
    name: str


class TenantUpdate(BaseModel):
    name: str
