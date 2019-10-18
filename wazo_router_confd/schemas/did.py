# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel, constr


class DID(BaseModel):
    id: int
    tenant_id: int
    ipbx_id: int
    carrier_trunk_id: int
    did_regex: Optional[constr(max_length=256)] = None

    class Config:
        orm_mode = True


class DIDCreate(BaseModel):
    tenant_id: int
    ipbx_id: int
    carrier_trunk_id: int
    did_regex: Optional[constr(max_length=256)] = None


class DIDUpdate(BaseModel):
    tenant_id: int
    ipbx_id: int
    carrier_trunk_id: int
    did_regex: Optional[constr(max_length=256)] = None
