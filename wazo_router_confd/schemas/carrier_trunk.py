# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, List

from pydantic import BaseModel, constr, UUID4


class CarrierTrunk(BaseModel):
    id: int
    carrier_id: int
    normalization_profile_id: Optional[int] = None
    name: constr(max_length=256)  # type: ignore
    sip_proxy: constr(max_length=128)  # type: ignore
    sip_proxy_port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None  # type: ignore
    registered: bool = False
    auth_username: Optional[constr(max_length=35)] = None  # type: ignore
    auth_password: Optional[constr(max_length=192)] = None  # type: ignore
    realm: Optional[constr(max_length=64)] = None  # type: ignore
    registrar_proxy: Optional[constr(max_length=128)] = None  # type: ignore
    from_domain: Optional[constr(max_length=64)] = None  # type: ignore
    expire_seconds: int = 3600
    retry_seconds: int = 30

    class Config:
        orm_mode = True


class CarrierTrunkRead(BaseModel):
    id: int
    tenant_uuid: Optional[UUID4]
    carrier_id: int
    normalization_profile_id: Optional[int] = None
    name: constr(max_length=256)  # type: ignore
    sip_proxy: constr(max_length=128)  # type: ignore
    sip_proxy_port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None  # type: ignore
    registered: bool = False
    auth_username: Optional[constr(max_length=35)] = None  # type: ignore
    realm: Optional[constr(max_length=64)] = None  # type: ignore
    registrar_proxy: Optional[constr(max_length=128)] = None  # type: ignore
    from_domain: Optional[constr(max_length=64)] = None  # type: ignore
    expire_seconds: int = 3600
    retry_seconds: int = 30

    class Config:
        orm_mode = True


class CarrierTrunkCreate(BaseModel):
    tenant_uuid: Optional[UUID4]
    carrier_id: int
    normalization_profile_id: Optional[int] = None
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
    normalization_profile_id: Optional[int] = None
    name: constr(max_length=256)  # type: ignore
    sip_proxy: constr(max_length=128)  # type: ignore
    sip_proxy_port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None  # type: ignore
    registered: bool = False
    auth_username: Optional[constr(max_length=35)] = None  # type: ignore
    auth_password: Optional[constr(max_length=192)] = None  # type: ignore
    realm: Optional[constr(max_length=64)] = None  # type: ignore
    registrar_proxy: Optional[constr(max_length=128)] = None  # type: ignore
    from_domain: Optional[constr(max_length=64)] = None  # type: ignore
    expire_seconds: int = 3600
    retry_seconds: int = 30


class CarrierTrunkList(BaseModel):
    items: List[CarrierTrunkRead]
