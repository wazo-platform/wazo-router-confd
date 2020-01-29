from dataclasses import dataclass
from typing import Optional, List

from aiohttp import ClientSession
from aiohttp import TCPConnector  # type: ignore

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response


X_AUTH_TOKEN_HEADER = 'X-Auth-Token'
WAZO_TENANT = 'Wazo-Tenant'


@dataclass
class Principal:
    auth_id: str
    uuid: str
    tenant_uuid: str
    tenant_uuids: List[str]
    token: str


class AuthClient(object):
    def __init__(self, url: str, cert: bool):
        self._url = url
        self._cert = cert

    async def get_token_data(self, token: str, tenant_uuid: str) -> Optional[Principal]:
        verify_ssl = bool(self._cert)
        connector = TCPConnector(verify_ssl=verify_ssl)
        async with ClientSession(connector=connector) as session:
            token_data = dict()
            # get the token data
            token_url = self._url + '/token/' + token
            async with session.get(token_url) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                if data is not None and data.get('data'):
                    token_data.update(
                        dict(
                            auth_id=data['data']['auth_id'],
                            uuid=data['data']['metadata']['uuid'],
                            tenant_uuid=data['data']['metadata']['tenant_uuid'],
                            tenant_uuids=[data['data']['metadata']['tenant_uuid']],
                            token=data['data']['token'],
                        )
                    )
            # get the list of tenants linked to the token
            tenants_url = self._url + '/tenants'
            async with session.get(
                tenants_url, headers={"X-Auth-Token": token}
            ) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                if data is not None and data.get('items'):
                    token_data['tenant_uuids'] = list(
                        map(lambda x: x['uuid'], data['items'])
                    )
                    if tenant_uuid:
                        if tenant_uuid not in token_data['tenant_uuids']:
                            return None
                        token_data['tenant_uuid'] = tenant_uuid
                        token_data['tenant_uuids'] = [tenant_uuid]
            return Principal(**token_data)


def get_principal(request: Request) -> Optional[Principal]:
    return getattr(request.state, 'principal', None)


def setup_auth(app: FastAPI, config: dict) -> FastAPI:
    config['wazo_auth'] = bool(config.get('wazo_auth'))

    if config['wazo_auth']:
        auth_client = AuthClient(
            url=config['wazo_auth_url'], cert=bool(config['wazo_auth_cert'])
        )

        # pylint: disable= unused-variable
        @app.middleware("http")
        async def auth_middleware(request: Request, call_next):
            header = request.headers.get(X_AUTH_TOKEN_HEADER)
            if header is None:
                return Response(
                    "Missing %s header" % X_AUTH_TOKEN_HEADER, status_code=401
                )
            tenant_uuid = request.headers.get(WAZO_TENANT)
            principal = await auth_client.get_token_data(header, tenant_uuid)
            if principal is None:
                return Response("The provided token is not valid", status_code=401)
            request.state.principal = principal
            response = await call_next(request)
            return response

    return app
