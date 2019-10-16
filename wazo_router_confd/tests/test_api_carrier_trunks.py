# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import get_app_and_client


@get_app_and_client
def test_create_carrier_trunk(app=None, client=None):
    response = client.post(
        "/carrier_trunks/",
        json={
            "name": "carrier_trunk1",
            "carrier_id": 1,
            "sip_proxy": "proxy.somedomain.com",
            "ip_address": "10.0.0.1",
            "registered": True,
            "auth_username": "user",
            "auth_password": "pass",
            "realm": "somerealm.com",
            "registrar_proxy": "registrar-proxy.com",
            "from_domain": "gw.somedomain.com",
            "expire_seconds": 1800,
            "retry_seconds": 10,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "carrier_trunk1",
        "carrier_id": 1,
        "sip_proxy": "proxy.somedomain.com",
        "sip_proxy_port": 5060,
        "ip_address": "10.0.0.1",
        "registered": True,
        "auth_username": "user",
        "realm": "somerealm.com",
        "registrar_proxy": "registrar-proxy.com",
        "from_domain": "gw.somedomain.com",
        "expire_seconds": 1800,
        "retry_seconds": 10,
    }


@get_app_and_client
def test_create_duplicated_carrier_trunk(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk

    session = SessionLocal(bind=app.engine)
    session.add(
        CarrierTrunk(
            name='carrier_trunk1', carrier_id=1, sip_proxy='proxy.somedomain.com'
        )
    )
    session.commit()
    #
    response = client.post(
        "/carrier_trunks/",
        json={
            "name": "carrier_trunk1",
            "carrier_id": 1,
            "sip_proxy": "proxy.somedomain.com",
        },
    )
    assert response.status_code == 409


@get_app_and_client
def test_get_carrier_trunk(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk

    session = SessionLocal(bind=app.engine)
    session.add(
        CarrierTrunk(
            name='carrier_trunk1',
            carrier_id=1,
            sip_proxy='proxy.somedomain.com',
            registered=True,
            ip_address="10.0.0.1",
            auth_username='user',
            auth_password='pass',
            realm='somerealm.com',
            registrar_proxy='registrar-proxy.com',
            from_domain='gw.somedomain.com',
            expire_seconds=1800,
            retry_seconds=10,
        )
    )
    session.commit()
    #
    response = client.get("/carrier_trunks/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "carrier_trunk1",
        "carrier_id": 1,
        "sip_proxy": "proxy.somedomain.com",
        "sip_proxy_port": 5060,
        "ip_address": "10.0.0.1",
        "registered": True,
        "auth_username": "user",
        "realm": "somerealm.com",
        "registrar_proxy": "registrar-proxy.com",
        "from_domain": "gw.somedomain.com",
        "expire_seconds": 1800,
        "retry_seconds": 10,
    }


@get_app_and_client
def test_get_carrier_trunk_not_found(app=None, client=None):
    response = client.get("/carrier_trunks/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_carrier_trunks(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk

    session = SessionLocal(bind=app.engine)
    session.add(
        CarrierTrunk(
            name='carrier_trunk1', carrier_id=1, sip_proxy='proxy.somedomain.com'
        )
    )
    session.commit()
    #
    response = client.get("/carrier_trunks/")
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': 1,
            'name': 'carrier_trunk1',
            'carrier_id': 1,
            'sip_proxy': 'proxy.somedomain.com',
            "sip_proxy_port": 5060,
            "ip_address": None,
            'registered': False,
            'auth_username': None,
            'realm': None,
            'registrar_proxy': None,
            'from_domain': None,
            'expire_seconds': 3600,
            'retry_seconds': 30,
        }
    ]


@get_app_and_client
def test_update_carrier_trunk(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk

    session = SessionLocal(bind=app.engine)
    session.add(
        CarrierTrunk(
            name='carrier_trunk1',
            carrier_id=1,
            sip_proxy='proxy.somedomain.com',
            auth_username='username1',
            auth_password='password1',
        )
    )
    session.commit()
    #
    response = client.put(
        "/carrier_trunks/1",
        json={
            'name': 'updated_carrier_trunk1',
            "carrier_id": 1,
            "sip_proxy": "proxy.somedomain.com",
            "sip_proxy_port": 5061,
            "ip_address": "10.0.0.1",
            "registered": True,
            'auth_username': 'username2',
            'auth_password': 'password2',
            "realm": "somerealm.com",
            "registrar_proxy": "registrar-proxy.com",
            "from_domain": "gw.somedomain.com",
            "expire_seconds": 1800,
            "retry_seconds": 10,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'name': 'updated_carrier_trunk1',
        'carrier_id': 1,
        'sip_proxy': 'proxy.somedomain.com',
        "sip_proxy_port": 5061,
        "ip_address": "10.0.0.1",
        'auth_username': 'username2',
        'expire_seconds': 1800,
        'retry_seconds': 10,
        'from_domain': "gw.somedomain.com",
        'realm': "somerealm.com",
        'registered': True,
        'registrar_proxy': "registrar-proxy.com",
    }


@get_app_and_client
def test_update_carrier_trunk_not_found(app=None, client=None):
    response = client.put(
        "/carrier_trunks/1",
        json={
            'name': 'updated_carrier_trunk1',
            "carrier_id": 1,
            "sip_proxy": "proxy.somedomain.com",
            "registered": True,
            'auth_username': 'username2',
            'auth_password': 'password2',
            "realm": "somerealm.com",
            "registrar_proxy": "registrar-proxy.com",
            "from_domain": "gw.somedomain.com",
            "expire_seconds": 1800,
            "retry_seconds": 10,
        },
    )
    assert response.status_code == 404


@get_app_and_client
def test_delete_carrier_trunk(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk

    session = SessionLocal(bind=app.engine)
    session.add(
        CarrierTrunk(
            name='carrier_trunk1',
            carrier_id=1,
            sip_proxy='proxy.somedomain.com',
            auth_username='username1',
            auth_password='password1',
        )
    )
    session.commit()
    #
    response = client.delete("/carrier_trunks/1")
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'name': 'carrier_trunk1',
        'carrier_id': 1,
        'sip_proxy': 'proxy.somedomain.com',
        'sip_proxy_port': 5060,
        "ip_address": None,
        'auth_username': 'username1',
        'expire_seconds': 3600,
        'retry_seconds': 30,
        'from_domain': None,
        'realm': None,
        'registered': False,
        'registrar_proxy': None,
    }


@get_app_and_client
def test_delete_carrier_trunk_not_found(app=None, client=None):
    response = client.delete("/carrier_trunks/1")
    assert response.status_code == 404
