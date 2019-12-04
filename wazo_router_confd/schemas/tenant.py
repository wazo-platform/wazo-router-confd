# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from pydantic import BaseModel, constr, UUID4


class Tenant(BaseModel):
    name: constr(max_length=256)  # type: ignore
    uuid: UUID4

    class Config:
        orm_mode = True


class TenantCreate(BaseModel):
    name: str
    uuid: UUID4


class TenantUpdate(BaseModel):
    name: str
