# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def test_api_status(client):
    response = client.get("/status")
    assert response.status_code == 204
