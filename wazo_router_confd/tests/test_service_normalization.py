# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import get_app_and_client


@get_app_and_client
def test_normalize_local_number_to_e164(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    normalization_profile = NormalizationProfile(
        name='profile 1',
        tenant=tenant,
        country_code='39',
        area_code='11',
        intl_prefix='00',
        ld_prefix='0',
        always_ld=False,
        always_intl_prefix_plus=False,
    )
    normalization_rule = NormalizationRule(
        profile=normalization_profile,
        rule_type=1,
        priority=0,
        match_regex=r'^39(.+)',
        match_prefix='39',
        replace_regex=r'36\1',
    )
    session.add_all([tenant, normalization_profile, normalization_rule])
    session.commit()
    #
    from wazo_router_confd.services.normalization import normalize_local_number_to_e164

    assert '36011625234' == normalize_local_number_to_e164(
        session, '+39 011 625234', profile=normalization_profile
    )


@get_app_and_client
def test_normalize_e164_to_local_number(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    normalization_profile = NormalizationProfile(
        name='profile 1',
        tenant=tenant,
        country_code='39',
        area_code='11',
        intl_prefix='00',
        ld_prefix='0',
        always_ld=False,
        always_intl_prefix_plus=True,
    )
    normalization_rule = NormalizationRule(
        profile=normalization_profile,
        rule_type=2,
        priority=0,
        match_regex=r'^39(.+)',
        match_prefix='39',
        replace_regex=r'36\1',
    )
    session.add_all([tenant, normalization_profile, normalization_rule])
    session.commit()
    #
    from wazo_router_confd.services.normalization import normalize_e164_to_local_number

    assert '+36011625234' == normalize_e164_to_local_number(
        session, '39011625234', profile=normalization_profile
    )
