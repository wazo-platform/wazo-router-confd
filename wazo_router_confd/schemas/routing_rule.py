# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel, constr


class RoutingRule(BaseModel):
    id: int
    carrier_trunk_id: int
    ipbx_id: int
    prefix: Optional[constr(max_length=128)] = None  # type: ignore
    did_regex: Optional[constr(max_length=256)] = None  # type: ignore
    route_type: constr(max_length=10)  # type: ignore

    class Config:
        orm_mode = True


class RoutingRuleCreate(BaseModel):
    carrier_trunk_id: int
    ipbx_id: int
    prefix: Optional[constr(max_length=128)] = None  # type: ignore
    did_regex: Optional[constr(max_length=256)] = None  # type: ignore
    route_type: constr(max_length=10)  # type: ignore


class RoutingRuleUpdate(BaseModel):
    carrier_trunk_id: int
    ipbx_id: int
    prefix: Optional[constr(max_length=128)] = None  # type: ignore
    did_regex: Optional[constr(max_length=256)] = None  # type: ignore
    route_type: constr(max_length=10)  # type: ignore
