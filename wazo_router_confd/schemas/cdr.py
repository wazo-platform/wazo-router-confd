# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel

from datetime import datetime


class CDR(BaseModel):
    id: int
    tenant_id: int
    source_ip: str
    source_port: int
    from_uri: str
    to_uri: str
    call_id: str
    call_start: Optional[datetime] = None
    duration: Optional[int] = None

    class Config:
        orm_mode = True


class CDRCreate(BaseModel):
    tenant_id: int
    source_ip: str
    source_port: int
    from_uri: str
    to_uri: str
    call_id: str
    call_start: Optional[datetime] = None
    duration: Optional[int] = None


class CDRUpdate(BaseModel):
    tenant_id: int
    source_ip: str
    source_port: int
    from_uri: str
    to_uri: str
    call_id: str
    call_start: Optional[datetime] = None
    duration: Optional[int] = None
