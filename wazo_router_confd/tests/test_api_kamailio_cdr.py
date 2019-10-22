from .common import get_app_and_client


@get_app_and_client
def test_kamailio_cdr(app=None, client=None):
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
            "tenant_id": tenant.id,
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
            "tenant_id": tenant.id,
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "call_id": "call-id",
            "from_uri": request_from_uri,
            "to_uri": request_to_uri,
            "call_start": '2019-10-11T00:00:00+00:00',
            "duration": duration,
        },
    }


@get_app_and_client
def test_kamailio_cdr_failed_no_domain(app=None, client=None):
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
            "tenant_id": 0,
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
