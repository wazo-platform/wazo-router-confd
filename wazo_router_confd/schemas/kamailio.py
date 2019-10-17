# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AuthRequest(BaseModel):
    source_ip: Optional[str] = None
    source_port: Optional[int] = 5060
    domain: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class AuthResponse(BaseModel):
    success: bool
    tenant_id: Optional[int] = None
    carrier_trunk_id: Optional[int] = None
    ipbx_id: Optional[int] = None
    domain: Optional[str] = None
    username: Optional[str] = None
    password_ha1: Optional[str] = None


class CDRRequest(BaseModel):
    event: Optional[str] = None
    source_ip: Optional[str] = None
    source_port: Optional[int] = None
    call_id: Optional[str] = None
    from_uri: str
    to_uri: str
    call_start: Optional[datetime] = None
    duration: Optional[int] = None


class RoutingRequest(BaseModel):
    event: Optional[str] = None
    auth: bool = False
    source_ip: Optional[str] = None
    source_port: Optional[int] = None
    domain: Optional[str] = None
    username: Optional[str] = None
    call_id: Optional[str] = None
    from_name: Optional[str] = None
    from_uri: str
    from_tag: Optional[str] = None
    to_uri: str
    to_name: Optional[str] = None
    to_tag: Optional[str] = None


class RoutingResponse(BaseModel):
    rtjson: Optional[dict]
    auth: Optional[AuthResponse] = None
