# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def test_create_did(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        password='password',
    )
    carrier = Carrier(name='carrier', tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1', carrier=carrier, sip_proxy='proxy.somedomain.com'
    )
    session.add_all([tenant, domain, ipbx, carrier, carrier_trunk])
    session.commit()
    #
    response = client.post(
        "/1.0/dids",
        json={
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "tenant_uuid": str(tenant.uuid),
            "ipbx_id": ipbx.id,
            "carrier_trunk_id": carrier_trunk.id,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": mock.ANY,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "tenant_uuid": str(tenant.uuid),
        "ipbx_id": ipbx.id,
        "carrier_trunk_id": carrier_trunk.id,
    }


def test_create_duplicated_did(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.did import DID

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        password='password',
    )
    carrier = Carrier(name='carrier', tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1', carrier=carrier, sip_proxy='proxy.somedomain.com'
    )
    did = DID(
        did_regex=r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
        tenant=tenant,
        ipbx=ipbx,
        carrier_trunk=carrier_trunk,
    )
    session.add_all([tenant, domain, ipbx, carrier, carrier_trunk, did])
    session.commit()
    #
    response = client.post(
        "/1.0/dids",
        json={
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "tenant_uuid": str(tenant.uuid),
            "ipbx_id": ipbx.id,
            "carrier_trunk_id": carrier_trunk.id,
        },
    )
    assert response.status_code == 409


def test_get_did(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.did import DID

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        password='password',
    )
    carrier = Carrier(name='carrier', tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1', carrier=carrier, sip_proxy='proxy.somedomain.com'
    )
    did = DID(
        did_regex=r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
        tenant=tenant,
        ipbx=ipbx,
        carrier_trunk=carrier_trunk,
    )
    session.add_all([tenant, domain, ipbx, carrier, carrier_trunk, did])
    session.commit()
    #
    response = client.get("/1.0/dids/%s" % did.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": did.id,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "tenant_uuid": str(tenant.uuid),
        "ipbx_id": ipbx.id,
        "carrier_trunk_id": carrier_trunk.id,
    }


def test_get_did_not_found(app, client):
    response = client.get("/1.0/dids/1")
    assert response.status_code == 404


def test_get_dids(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.did import DID

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        password='password',
    )
    carrier = Carrier(name='carrier', tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1', carrier=carrier, sip_proxy='proxy.somedomain.com'
    )
    did = DID(
        did_regex=r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
        tenant=tenant,
        ipbx=ipbx,
        carrier_trunk=carrier_trunk,
    )
    session.add_all([tenant, domain, ipbx, carrier, carrier_trunk, did])
    session.commit()
    #
    response = client.get("/1.0/dids")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": did.id,
                "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
                "tenant_uuid": str(tenant.uuid),
                "ipbx_id": ipbx.id,
                "carrier_trunk_id": carrier_trunk.id,
            }
        ]
    }


def test_update_did(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.did import DID

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    tenant_b = Tenant(name='fabiob', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff35')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    domain_b = Domain(domain='testdomainb.com', tenant=tenant_b)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        password='password',
    )
    ipbx_b = IPBX(
        tenant=tenant_b,
        domain=domain_b,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        password='password',
    )
    carrier = Carrier(name='carrier', tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1', carrier=carrier, sip_proxy='proxy.somedomain.com'
    )
    carrier_b = Carrier(name='carrier', tenant=tenant_b)
    carrier_trunk_b = CarrierTrunk(
        name='carrier_trunk2', carrier=carrier_b, sip_proxy='proxy.somedomain.com'
    )
    did = DID(
        did_regex=r'^(\+?1)?(800)[2-9]\d{6})$',
        tenant=tenant,
        ipbx=ipbx,
        carrier_trunk=carrier_trunk,
    )
    session.add_all(
        [
            tenant,
            tenant_b,
            domain,
            domain_b,
            ipbx,
            ipbx_b,
            carrier,
            carrier_b,
            carrier_trunk,
            carrier_trunk_b,
            did,
        ]
    )
    session.commit()
    response = client.put(
        "/1.0/dids/%s" % did.id,
        json={
            "id": did.id,
            "did_regex": r"^(\+?1)?(800)[1-9]\d{6})$",
            "tenant_uuid": str(tenant_b.uuid),
            "ipbx_id": ipbx_b.id,
            "carrier_trunk_id": carrier_trunk_b.id,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": did.id,
        "did_regex": r"^(\+?1)?(800)[1-9]\d{6})$",
        "tenant_uuid": str(tenant_b.uuid),
        "ipbx_id": ipbx_b.id,
        "carrier_trunk_id": carrier_trunk_b.id,
    }


def test_update_did_not_found(app, client):
    response = client.put(
        "/1.0/dids/1",
        json={
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "tenant_uuid": "281f5d35-3089-4af3-9773-f8769dfcd878",
            "ipbx_id": 1,
            "carrier_trunk_id": 3,
        },
    )
    assert response.status_code == 404


def test_delete_did(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.did import DID

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        password='password',
    )
    carrier = Carrier(name='carrier', tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1', carrier=carrier, sip_proxy='proxy.somedomain.com'
    )
    did = DID(
        did_regex=r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
        tenant=tenant,
        ipbx=ipbx,
        carrier_trunk=carrier_trunk,
    )
    session.add_all([tenant, domain, ipbx, carrier, carrier_trunk, did])
    session.commit()
    #
    response = client.delete("/1.0/dids/%s" % did.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": did.id,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "carrier_trunk_id": carrier_trunk.id,
        "tenant_uuid": str(tenant.uuid),
        "ipbx_id": ipbx.id,
    }


def test_delete_did_not_found(app, client):
    response = client.delete("/1.0/dids/1")
    assert response.status_code == 404
