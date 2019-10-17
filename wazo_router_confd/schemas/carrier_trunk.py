# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel


class CarrierTrunk(BaseModel):
    id: int
    carrier_id: int
    name: str
    sip_proxy: str
    sip_proxy_port: int = 5060
    ip_address: Optional[str] = None
    registered: bool = False
    auth_username: Optional[str] = None
    auth_password: Optional[str] = None
    realm: Optional[str] = None
    registrar_proxy: Optional[str] = None
    from_domain: Optional[str] = None
    expire_seconds: int = 3600
    retry_seconds: int = 30

    class Config:
        orm_mode = True


class CarrierTrunkRead(BaseModel):
    id: int
    carrier_id: int
    name: str
    sip_proxy: str
    sip_proxy_port: int = 5060
    ip_address: Optional[str] = None
    registered: bool = False
    auth_username: Optional[str] = None
    realm: Optional[str] = None
    registrar_proxy: Optional[str] = None
    from_domain: Optional[str] = None
    expire_seconds: int = 3600
    retry_seconds: int = 30

    class Config:
        orm_mode = True


class CarrierTrunkCreate(BaseModel):
    carrier_id: int
    name: str
    sip_proxy: str
    sip_proxy_port: int = 5060
    ip_address: Optional[str] = None
    registered: bool = False
    auth_username: Optional[str] = None
    auth_password: Optional[str] = None
    realm: Optional[str] = None
    registrar_proxy: Optional[str] = None
    from_domain: Optional[str] = None
    expire_seconds: int = 3600
    retry_seconds: int = 30


class CarrierTrunkUpdate(BaseModel):
    name: str
    sip_proxy: str
    sip_proxy_port: int = 5060
    ip_address: Optional[str] = None
    registered: bool = False
    auth_username: Optional[str] = None
    auth_password: Optional[str] = None
    realm: Optional[str] = None
    registrar_proxy: Optional[str] = None
    from_domain: Optional[str] = None
    expire_seconds: int = 3600
    retry_seconds: int = 30
