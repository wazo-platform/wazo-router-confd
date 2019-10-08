# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import get_app_and_client


@get_app_and_client
def test_create_did(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709',
        sha1b='f10e2821bbbea527ea02200352313bc059445190',
    )
    carrier = Carrier(name='carrier', tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='carrier_trunk1', carrier=carrier, sip_proxy='proxy.somedomain.com'
    )
    session.add_all([tenant, domain, ipbx, carrier, carrier_trunk])
    session.commit()
    #
    response = client.post(
        "/dids/",
        json={
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "tenant_id": tenant.id,
            "ipbx_id": ipbx.id,
            "carrier_trunk_id": carrier_trunk.id,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "tenant_id": 1,
        "ipbx_id": 1,
        "carrier_trunk_id": 1,
    }


@get_app_and_client
def test_create_duplicated_did(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.did import DID

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709',
        sha1b='f10e2821bbbea527ea02200352313bc059445190',
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
        "/dids/",
        json={
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "tenant_id": 1,
            "ipbx_id": 1,
            "carrier_trunk_id": 1,
        },
    )
    assert response.status_code == 409


@get_app_and_client
def test_get_did(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.did import DID

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709',
        sha1b='f10e2821bbbea527ea02200352313bc059445190',
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
    response = client.get("/dids/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "tenant_id": 1,
        "ipbx_id": 1,
        "carrier_trunk_id": 1,
    }


@get_app_and_client
def test_get_did_not_found(app=None, client=None):
    response = client.get("/dids/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_dids(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.did import DID

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709',
        sha1b='f10e2821bbbea527ea02200352313bc059445190',
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
    response = client.get("/dids/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "tenant_id": 1,
            "ipbx_id": 1,
            "carrier_trunk_id": 1,
        }
    ]


@get_app_and_client
def test_update_did(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.did import DID

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709',
        sha1b='f10e2821bbbea527ea02200352313bc059445190',
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
    response = client.put(
        "/dids/1",
        json={
            "id": 1,
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "tenant_id": 2,
            "ipbx_id": 1,
            "carrier_trunk_id": 2,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "tenant_id": 2,
        "ipbx_id": 1,
        "carrier_trunk_id": 2,
    }


@get_app_and_client
def test_update_did_not_found(app=None, client=None):
    response = client.put(
        "/dids/1",
        json={
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "tenant_id": 1,
            "ipbx_id": 1,
            "carrier_trunk_id": 3,
        },
    )
    assert response.status_code == 404


@get_app_and_client
def test_delete_did(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.ipbx import IPBX
    from wazo_router_confd.models.did import DID

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709',
        sha1b='f10e2821bbbea527ea02200352313bc059445190',
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
    response = client.delete("/dids/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "carrier_trunk_id": 1,
        "tenant_id": 1,
        "ipbx_id": 1,
    }


@get_app_and_client
def test_delete_did_not_found(app=None, client=None):
    response = client.delete("/dids/1")
    assert response.status_code == 404
