# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, List

from pydantic import BaseModel, constr, UUID4

from datetime import datetime


class CDR(BaseModel):
    id: int
    tenant_uuid: Optional[UUID4]
    source_ip: constr(max_length=64)  # type: ignore
    source_port: int
    from_uri: constr(max_length=256)  # type: ignore
    to_uri: constr(max_length=256)  # type: ignore
    call_id: constr(max_length=256)  # type: ignore
    call_start: Optional[datetime] = None
    duration: Optional[int] = None

    class Config:
        orm_mode = True


class CDRCreate(BaseModel):
    tenant_uuid: Optional[UUID4]
    source_ip: constr(max_length=64)  # type: ignore
    source_port: int
    from_uri: constr(max_length=256)  # type: ignore
    to_uri: constr(max_length=256)  # type: ignore
    call_id: constr(max_length=256)  # type: ignore
    call_start: Optional[datetime] = None
    duration: Optional[int] = None


class CDRUpdate(BaseModel):
    tenant_uuid: Optional[UUID4]
    source_ip: constr(max_length=64)  # type: ignore
    source_port: int
    from_uri: constr(max_length=256)  # type: ignore
    to_uri: constr(max_length=256)  # type: ignore
    call_id: constr(max_length=256)  # type: ignore
    call_start: Optional[datetime] = None
    duration: Optional[int] = None


class CDRList(BaseModel):
    items: List[CDR]
