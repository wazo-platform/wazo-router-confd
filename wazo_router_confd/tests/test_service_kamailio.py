# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def test_split_uri_to_parts():
    from wazo_router_confd.services.kamailio import split_uri_to_parts

    assert ('', '', '', '') == split_uri_to_parts('')
