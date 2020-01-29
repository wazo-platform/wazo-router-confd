# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def test_auth_failed_missing_header(client_auth):
    response = client_auth.get("/status")
    assert response.status_code == 401
    assert response.text == 'Missing X-Auth-Token header'


def test_auth_failed_invalid_token(client_auth):
    response = client_auth.get("/status", headers={'X-Auth-Token': 'dummy-yummy'})
    assert response.status_code == 401
    assert response.text == 'The provided token is not valid'


def test_auth_failed_valid_token_without_tenants(client_auth):
    response = client_auth.get(
        "/status", headers={'X-Auth-Token': 'wazo-router-confd-no-tenant'}
    )
    assert response.status_code == 401


def test_auth_valid_token(client_auth):
    response = client_auth.get("/status", headers={'X-Auth-Token': 'wazo-router-confd'})
    assert response.status_code == 204


def test_auth_valid_token_with_wrong_tenant(client_auth):
    response = client_auth.get(
        "/status",
        headers={
            'X-Auth-Token': 'wazo-router-confd',
            'Wazo-Tenant': 'ffffffff-ffff-4c1c-ad1c-eeeeeeeeeeee',
        },
    )
    assert response.status_code == 401
