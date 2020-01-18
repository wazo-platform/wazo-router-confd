# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def test_create_carrier_trunk(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    carrier = Carrier(name="carrier", tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier])
    session.commit()

    response = client.post(
        "/1.0/carrier_trunks",
        json={
            "name": "carrier_trunk1",
            "tenant_uuid": str(tenant.uuid),
            "carrier_id": carrier.id,
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
        "id": mock.ANY,
        "name": "carrier_trunk1",
        "tenant_uuid": str(tenant.uuid),
        "carrier_id": carrier.id,
        "normalization_profile_id": None,
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


def test_create_duplicated_carrier_trunk(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    carrier = Carrier(name="carrier", tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1',
        tenant=tenant,
        carrier=carrier,
        sip_proxy='proxy.somedomain.com',
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier, carrier_trunk])
    session.commit()
    #
    response = client.post(
        "/1.0/carrier_trunks",
        json={
            "name": "carrier_trunk1",
            "tenant_uuid": str(tenant.uuid),
            "carrier_id": carrier.id,
            "sip_proxy": "proxy.somedomain.com",
        },
    )
    assert response.status_code == 409


def test_get_carrier_trunk(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    carrier = Carrier(name="carrier", tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1',
        tenant=tenant,
        carrier=carrier,
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
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier, carrier_trunk])
    session.commit()
    #
    response = client.get("/1.0/carrier_trunks/%d" % carrier_trunk.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": carrier_trunk.id,
        "name": "carrier_trunk1",
        "tenant_uuid": str(tenant.uuid),
        "carrier_id": carrier.id,
        "normalization_profile_id": None,
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


def test_get_carrier_trunk_not_found(app, client):
    response = client.get("/1.0/carrier_trunks/1")
    assert response.status_code == 404


def test_get_carrier_trunks(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    carrier = Carrier(name="carrier", tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1',
        tenant=tenant,
        carrier=carrier,
        sip_proxy='proxy.somedomain.com',
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier, carrier_trunk])
    session.commit()
    #
    response = client.get("/1.0/carrier_trunks")
    assert response.status_code == 200
    assert response.json() == [
        {
            'id': carrier_trunk.id,
            'name': 'carrier_trunk1',
            "tenant_uuid": str(tenant.uuid),
            "carrier_id": carrier.id,
            "normalization_profile_id": None,
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


def test_update_carrier_trunk(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    carrier = Carrier(name="carrier", tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1',
        tenant=tenant,
        carrier=carrier,
        sip_proxy='proxy.somedomain.com',
        auth_username='username1',
        auth_password='password1',
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier, carrier_trunk])
    session.commit()
    #
    response = client.put(
        "/1.0/carrier_trunks/%s" % carrier_trunk.id,
        json={
            'name': 'updated_carrier_trunk1',
            "tenant_uuid": str(tenant.uuid),
            "carrier_id": carrier.id,
            "normalization_profile_id": None,
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
        'id': carrier_trunk.id,
        'name': 'updated_carrier_trunk1',
        "tenant_uuid": str(tenant.uuid),
        "carrier_id": carrier.id,
        "normalization_profile_id": None,
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


def test_update_carrier_trunk_not_found(app, client):
    response = client.put(
        "/1.0/carrier_trunks/1",
        json={
            'name': 'updated_carrier_trunk1',
            "tenant_uuid": "acfbc1a7-7ae2-4970-a6a4-0a8eae6a777b",
            "carrier_id": 1,
            "normalization_profile_id": None,
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


def test_delete_carrier_trunk(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.tenant import Tenant

    tenant = Tenant(name="tenant", uuid="3ab844af-8039-45d9-a3aa-bae6f298228f")
    carrier = Carrier(name="carrier", tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1',
        tenant=tenant,
        carrier=carrier,
        sip_proxy='proxy.somedomain.com',
        auth_username='username1',
        auth_password='password1',
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, carrier, carrier_trunk])
    session.commit()
    #
    response = client.delete("/1.0/carrier_trunks/%s" % carrier_trunk.id)
    assert response.status_code == 200
    assert response.json() == {
        'id': carrier_trunk.id,
        'name': 'carrier_trunk1',
        "tenant_uuid": str(tenant.uuid),
        "carrier_id": carrier.id,
        "normalization_profile_id": None,
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


def test_delete_carrier_trunk_not_found(app, client):
    response = client.delete("/1.0/carrier_trunks/1")
    assert response.status_code == 404
