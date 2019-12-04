# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel, constr, UUID4


class IPBX(BaseModel):
    id: int
    tenant_uuid: UUID4
    domain_id: int
    normalization_profile_id: Optional[int] = None
    customer: Optional[int] = None
    ip_fqdn: constr(max_length=256)  # type: ignore
    port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None  # type: ignore
    registered: bool = False
    username: Optional[constr(max_length=50)] = None  # type: ignore
    password: Optional[constr(max_length=192)] = None  # type: ignore
    password_ha1: Optional[constr(max_length=64)] = None  # type: ignore
    realm: Optional[constr(max_length=50)] = None  # type: ignore

    class Config:
        orm_mode = True


class IPBXRead(BaseModel):
    id: int
    tenant_uuid: UUID4
    domain_id: int
    normalization_profile_id: Optional[int] = None
    customer: Optional[int] = None
    ip_fqdn: constr(max_length=256)  # type: ignore
    port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None  # type: ignore
    registered: bool = False
    username: Optional[constr(max_length=50)] = None  # type: ignore
    realm: Optional[constr(max_length=50)] = None  # type: ignore

    class Config:
        orm_mode = True


class IPBXCreate(BaseModel):
    tenant_uuid: UUID4
    domain_id: int
    normalization_profile_id: Optional[int] = None
    customer: Optional[int] = None
    ip_fqdn: constr(max_length=256)  # type: ignore
    port: int = 5060
    ip_address: Optional[constr(max_length=256)] = None  # type: ignore
    registered: bool = False
    username: Optional[constr(max_length=50)] = None  # type: ignore
    password: Optional[constr(max_length=192)] = None  # type: ignore
    password_ha1: Optional[constr(max_length=64)] = None  # type: ignore
    realm: Optional[constr(max_length=50)] = None  # type: ignore


class IPBXUpdate(BaseModel):
    tenant_uuid: UUID4
    domain_id: int
    normalization_profile_id: Optional[int] = None
    customer: Optional[int] = None
    ip_fqdn: str
    port: int = 5060
    ip_address: Optional[str] = None  # type: ignore
    registered: bool = False
    username: Optional[str] = None  # type: ignore
    password: Optional[str] = None  # type: ignore
    password_ha1: Optional[str] = None  # type: ignore
    realm: Optional[constr(max_length=50)] = None  # type: ignore
