# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional, List

from pydantic import BaseModel, constr, UUID4


class DID(BaseModel):
    id: int
    tenant_uuid: UUID4
    ipbx_id: int
    carrier_trunk_id: int
    did_regex: Optional[constr(max_length=256)] = None  # type: ignore

    class Config:
        orm_mode = True


class DIDCreate(BaseModel):
    tenant_uuid: UUID4
    ipbx_id: int
    carrier_trunk_id: int
    did_regex: Optional[constr(max_length=256)] = None  # type: ignore


class DIDUpdate(BaseModel):
    tenant_uuid: UUID4
    ipbx_id: int
    carrier_trunk_id: int
    did_regex: Optional[constr(max_length=256)] = None  # type: ignore


class DIDList(BaseModel):
    items: List[DID]
