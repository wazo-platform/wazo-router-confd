# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel, constr

from datetime import datetime


class CDR(BaseModel):
    id: int
    tenant_id: int
    source_ip: constr(max_length=64)
    source_port: int
    from_uri: constr(max_length=256)
    to_uri: constr(max_length=256)
    call_id: constr(max_length=256)
    call_start: Optional[datetime] = None
    duration: Optional[int] = None

    class Config:
        orm_mode = True


class CDRCreate(BaseModel):
    tenant_id: int
    source_ip: constr(max_length=64)
    source_port: int
    from_uri: constr(max_length=256)
    to_uri: constr(max_length=256)
    call_id: constr(max_length=256)
    call_start: Optional[datetime] = None
    duration: Optional[int] = None


class CDRUpdate(BaseModel):
    tenant_id: int
    source_ip: constr(max_length=64)
    source_port: int
    from_uri: constr(max_length=256)
    to_uri: constr(max_length=256)
    call_id: constr(max_length=256)
    call_start: Optional[datetime] = None
    duration: Optional[int] = None
