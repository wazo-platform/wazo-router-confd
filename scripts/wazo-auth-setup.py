import requests


response = requests.post(
    "http://localhost:9497/api/auth/_set_token",
    json={
        "auth_id": "uuid-multitenant",
        "metadata": {
            "pbx_user_uuid": "uuid-multitenant",
            "tenant_uuid": "ffffffff-ffff-4c1c-ad1c-ffffffffffff",
            "uuid": "uuid-multitenant"
        },
        "token": "valid-token-multitenant"
    },
    verify=False,
)
assert response.status_code == 204

response = requests.post(
    "http://localhost:9497/api/auth/_set_tenants",
    json=[
        {
            "name": "valid-tenant1",
            "parent_uuid": "ffffffff-ffff-4c1c-ad1c-ffffffffffff",
            "uuid": "ffffffff-ffff-4c1c-ad1c-ffffffffffff"
        },
        {
            "name": "valid-tenant2",
            "parent_uuid": "ffffffff-ffff-4c1c-ad1c-ffffffffffff",
            "uuid": "ffffffff-ffff-4c1c-ad1c-eeeeeeeeeee2"
        },
        {
            "name": "valid-tenant3",
            "parent_uuid": "ffffffff-ffff-4c1c-ad1c-ffffffffffff",
            "uuid": "ffffffff-ffff-4c1c-ad1c-eeeeeeeeeee3"
        }
    ],
    verify=False,
)
assert response.status_code == 204
