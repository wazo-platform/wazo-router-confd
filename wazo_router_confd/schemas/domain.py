# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List, Optional

from pydantic import BaseModel, constr, UUID4


class Domain(BaseModel):
    id: int
    domain: constr(max_length=64)  # type: ignore
    tenant_uuid: Optional[UUID4]

    class Config:
        orm_mode = True


class DomainCreate(BaseModel):
    domain: constr(max_length=64)  # type: ignore
    tenant_uuid: Optional[UUID4]


class DomainUpdate(BaseModel):
    domain: constr(max_length=64)  # type: ignore
    tenant_uuid: Optional[UUID4]


class DomainList(BaseModel):
    items: List[Domain]
