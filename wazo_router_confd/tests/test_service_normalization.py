# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import aiopg  # type: ignore

from wazo_router_confd.database import from_database_uri_to_dsn


def test_normalize_local_number_to_e164(app, database_uri, event_loop):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
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

    async def test():
        dsn = from_database_uri_to_dsn(database_uri)
        pool = await aiopg.create_pool(dsn=dsn)
        async with pool.acquire() as conn:
            return await normalize_local_number_to_e164(
                conn, '+39 011 625234', profile=normalization_profile
            )
        pool.close()
        await pool.wait_closed()

    ret = event_loop.run_until_complete(test())
    assert '36011625234' == ret


def test_normalize_e164_to_local_number(app, database_uri, event_loop):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
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

    async def test():
        dsn = from_database_uri_to_dsn(database_uri)
        pool = await aiopg.create_pool(dsn=dsn)
        async with pool.acquire() as conn:
            return await normalize_e164_to_local_number(
                conn, '39011625234', profile=normalization_profile
            )
        pool.close()
        await pool.wait_closed()

    ret = event_loop.run_until_complete(test())
    assert '+36011625234' == ret
