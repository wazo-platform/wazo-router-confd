from .common import get_app_and_client


@get_app_and_client
def test_kamailio_routing_outbound_with_single_ipbx(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk
    from wazo_router_confd.models.ipbx import IPBX

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    carrier = Carrier(name='carrier1', tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='trunk1', carrier=carrier, sip_proxy='192.168.1.1'
    )

    ipbx = IPBX(
        customer=1,
        ip_fqdn='10.0.0.1',
        domain=domain,
        registered=True,
        username='user',
        sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709',
        sha1b='f10e2821bbbea527ea02200352313bc059445190',
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx, carrier, carrier_trunk])
    session.commit()
    #
    request_from_name = "From name"
    request_from_uri = "100@sourcedomain.com"
    request_from_tag = "from_tag"
    request_to_name = "to name"
    request_to_uri = "200@destinationdomain.com"
    request_to_tag = "to_tag"
    #
    response = client.post(
        "/kamailio/routing",
        json={
            "event": "sip-routing",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "call_id": "call-id",
            "from_name": request_from_name,
            "from_uri": request_from_uri,
            "from_tag": request_from_tag,
            "to_uri": request_to_uri,
            "to_name": request_to_name,
            "to_tag": request_to_tag,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "rtjson": {
            "version": "1.0",
            "routing": "serial",
            "routes": [
                {
                    "uri": "sip:%s:%s"
                    % (carrier_trunk.sip_proxy, carrier_trunk.sip_proxy_port),
                    "path": "",
                    "socket": "",
                    "headers": {
                        "from": {"display": request_from_name, "uri": request_from_uri},
                        "to": {"display": request_to_name, "uri": request_to_uri},
                        "extra": "",
                    },
                    "branch_flags": 8,
                    "fr_timer": 5000,
                    "fr_inv_timer": 30000,
                }
            ],
        },
    }


@get_app_and_client
def test_kamailio_routing_outbound_with_no_matching_ipbx(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.ipbx import IPBX

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        customer=1,
        ip_fqdn='10.0.0.2',
        domain=domain,
        registered=True,
        username='user',
        sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709',
        sha1b='f10e2821bbbea527ea02200352313bc059445190',
        tenant=tenant,
    )
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    request_from_name = "From name"
    request_from_uri = "100@sourcedomain.com"
    request_from_tag = "from_tag"
    request_to_name = "to name"
    request_to_uri = "200@anotherdomain.com"
    request_to_tag = "to_tag"
    #
    response = client.post(
        "/kamailio/routing",
        json={
            "event": "sip-routing",
            "source_ip": "10.0.0.1",
            "source_port": 5060,
            "call_id": "call-id",
            "from_name": request_from_name,
            "from_uri": request_from_uri,
            "from_tag": request_from_tag,
            "to_uri": request_to_uri,
            "to_name": request_to_name,
            "to_tag": request_to_tag,
        },
    )
    assert response.status_code == 200
    assert response.json() == {"success": False, "rtjson": None}
