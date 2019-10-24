# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import get_app_and_client


@get_app_and_client
def test_kamailio_dbtext_uacreg(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant
    from wazo_router_confd.models.domain import Domain
    from wazo_router_confd.models.carrier import Carrier
    from wazo_router_confd.models.carrier_trunk import CarrierTrunk

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    carrier = Carrier(name='carrier1', tenant=tenant)
    carrier_trunk = CarrierTrunk(
        name='trunk1',
        carrier=carrier,
        sip_proxy='192.168.1.1',
        registered=True,
        auth_username='username',
        auth_password='password',
        realm='realm',
        registrar_proxy='registrar',
        from_domain='domain.com',
        expire_seconds=300,
        retry_seconds=10,
    )
    session.add_all([tenant, domain, carrier, carrier_trunk])
    session.commit()
    #
    response = client.get("/kamailio/dbtext/uacreg")
    assert response.status_code == 200
    assert response.json() == {
        "content": "l_uuid(string) l_username(string) l_domain(string) r_username(string) r_domain(string) realm(string) auth_username(string) auth_password(string) auth_proxy(string) expires(int) flags(int) reg_delay(int)\n1:username:domain.com:username:domain.com:realm:username:password:registrar:300:4:10\n"
    }
