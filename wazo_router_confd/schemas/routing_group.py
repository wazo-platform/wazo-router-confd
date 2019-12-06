# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from pydantic import BaseModel, UUID4


class RoutingGroup(BaseModel):
    id: int
    tenant_uuid: UUID4
    routing_rule: Optional[int] = None

    class Config:
        orm_mode = True


class RoutingGroupCreate(BaseModel):
    tenant_uuid: UUID4
    routing_rule: Optional[int] = None


class RoutingGroupUpdate(BaseModel):
    tenant_uuid: UUID4
    routing_rule: Optional[int] = None
