# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from pydantic import BaseModel


class Tenant(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class TenantCreate(BaseModel):
    name: str


class TenantUpdate(BaseModel):
    name: str
