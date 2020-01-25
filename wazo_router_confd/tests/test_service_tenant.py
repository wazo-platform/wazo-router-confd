# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest  # type: ignore

from uuid import uuid4

from fastapi.exceptions import HTTPException

from wazo_router_confd.auth import Principal
from wazo_router_confd.database import SessionLocal
from wazo_router_confd.services.tenant import get_uuid


def test_get_uuid_with_principal(app):
    uuid = uuid4()

    session = SessionLocal(bind=app.engine)
    principal = Principal(
        auth_id="auth_id",
        uuid="uuid",
        tenant_uuid=str(uuid),
        tenant_uuids=[str(uuid)],
        token="token",
    )
    res = get_uuid(principal, session, None)
    assert res == uuid


def test_get_uuid_with_principal_none(app):
    uuid = uuid4()

    session = SessionLocal(bind=app.engine)
    principal = None
    res = get_uuid(principal, session, uuid)
    assert res == uuid


def test_get_uuid_mismatch_with_principal(app):
    uuid = uuid4()

    session = SessionLocal(bind=app.engine)
    session = SessionLocal(bind=app.engine)

    uuid_principal = str(uuid4())
    principal = Principal(
        auth_id="auth_id",
        uuid="uuid",
        tenant_uuid=uuid_principal,
        tenant_uuids=[uuid_principal],
        token="token",
    )
    with pytest.raises(HTTPException):
        get_uuid(principal, session, uuid)


def test_get_uuid_with_principal_none_and_empty_field(app):
    uuid = None

    session = SessionLocal(bind=app.engine)
    principal = None
    with pytest.raises(HTTPException):
        get_uuid(principal, session, uuid)
