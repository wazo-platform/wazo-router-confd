# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from pydantic import BaseModel, constr


class Domain(BaseModel):
    id: int
    domain: constr(max_length=64)
    tenant_id: int

    class Config:
        orm_mode = True


class DomainCreate(BaseModel):
    domain: constr(max_length=64)
    tenant_id: int


class DomainUpdate(BaseModel):
    domain: constr(max_length=64)
    tenant_id: int
