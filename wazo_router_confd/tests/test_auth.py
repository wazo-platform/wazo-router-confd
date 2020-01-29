# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_router_confd.auth import Principal


def test_auth_principal():
    principal = Principal(
        auth_id="auth_id",
        uuid="uuid",
        tenant_uuid="tenant_uuid",
        tenant_uuids=["tenant_uuid"],
        token="token",
    )
    assert (
        str(principal)
        == "Principal(auth_id='auth_id', uuid='uuid', tenant_uuid='tenant_uuid', tenant_uuids=['tenant_uuid'], token='token')"
    )
