# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def test_hash():
    from wazo_router_confd.services import password

    result = password.hash(None)
    assert result is None
    #
    result = password.hash("password")
    assert result is not None


def test_hash_ha1():
    from wazo_router_confd.services import password

    result = password.hash_ha1(None, None, None)
    assert result is None
    #
    result = password.hash_ha1("username", "realm", "password")
    assert result is not None
