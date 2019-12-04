# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def test_kamailio_cdr(app, client):
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
        did_regex=r'^39[0-9]+$',
        did_prefix='39',
        tenant=tenant,
        ipbx=ipbx,
        carrier_trunk=carrier_trunk,
    )
    session.add_all([tenant, domain, ipbx, carrier, carrier_trunk, did])
    session.commit()
    #
    request_from_uri = "100@testdomain.com"
    request_to_uri = "39123456789@dummy.com"
    call_start = 1570752000
    duration = 60
    #
    response = client.post(
        "/kamailio/cdr",
        json={
            "tenant_uuid": str(tenant.uuid),
            "event": "sip-routing",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "call_id": "call-id",
            "from_uri": request_from_uri,
            "to_uri": request_to_uri,
            "call_start": call_start,
            "duration": duration,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "cdr": {
            "tenant_uuid": str(tenant.uuid),
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "call_id": "call-id",
            "from_uri": request_from_uri,
            "to_uri": request_to_uri,
            "call_start": '2019-10-11T00:00:00+00:00',
            "duration": duration,
        },
    }


def test_kamailio_cdr_failed_no_domain(app, client):
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
        did_regex=r'^39[0-9]+$',
        did_prefix='39',
        tenant=tenant,
        ipbx=ipbx,
        carrier_trunk=carrier_trunk,
    )
    session.add_all([tenant, domain, ipbx, carrier, carrier_trunk, did])
    session.commit()
    #
    request_from_uri = "100@dummy.com"
    request_to_uri = "39123456789@dummy.com"
    call_start = 1570752000
    duration = 60
    #
    response = client.post(
        "/kamailio/cdr",
        json={
            # FIXME(sileht): Fail for the wrong reason, it should be because
            # domain is wrong, but it fails because tenant uuid is wrong.
            # With correct tenant uuid, the cdr is created
            "tenant_uuid": "5ecdf9dd-36d3-4735-a5e8-99bd297bc325",
            # "tenant_uuid": str(tenant.uuid),
            "event": "sip-routing",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "call_id": "call-id",
            "from_uri": request_from_uri,
            "to_uri": request_to_uri,
            "call_start": call_start,
            "duration": duration,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"success": False, "cdr": None}
