# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import get_app_and_client


@get_app_and_client
def test_create_normalization_rule(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    session.add_all([normalization_profile, tenant])
    session.commit()
    #
    response = client.post(
        "/normalization-rules/",
        json={
            "profile_id": normalization_profile.id,
            "match_regex": "^11",
            "replace_regex": "",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "profile_id": normalization_profile.id,
        "match_regex": "^11",
        "replace_regex": "",
    }


@get_app_and_client
def test_create_duplicated_normalization_rule(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    normalization_rule = NormalizationRule(
        match_regex='^11',
        match_prefix='11',
        replace_regex='',
        profile=normalization_profile,
    )
    session.add_all([tenant, normalization_profile, normalization_rule])
    session.commit()
    #
    response = client.post(
        "/normalization-rules/",
        json={
            "profile_id": normalization_profile.id,
            "match_regex": "^11",
            "replace_regex": "",
        },
    )
    assert response.status_code == 409


@get_app_and_client
def test_get_normalization_rule(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    normalization_rule = NormalizationRule(
        match_regex='^11',
        match_prefix='11',
        replace_regex='',
        profile=normalization_profile,
    )
    session.add_all([tenant, normalization_profile, normalization_rule])
    session.commit()
    #
    response = client.get("/normalization-rules/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "profile_id": normalization_profile.id,
        "match_regex": "^11",
        "replace_regex": '',
    }


@get_app_and_client
def test_get_normalization_rule_not_found(app=None, client=None):
    response = client.get("/normalization-rules/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_normalization_rules(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    normalization_rule = NormalizationRule(
        match_regex='^11',
        match_prefix='11',
        replace_regex='',
        profile=normalization_profile,
    )
    session.add_all([tenant, normalization_profile, normalization_rule])
    session.commit()
    #
    response = client.get("/normalization-rules/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "profile_id": normalization_profile.id,
            "match_regex": "^11",
            "replace_regex": '',
        }
    ]


@get_app_and_client
def test_update_normalization_rule(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    normalization_rule = NormalizationRule(
        match_regex='^11',
        match_prefix='11',
        replace_regex='',
        profile=normalization_profile,
    )
    session.add_all([tenant, normalization_profile, normalization_rule])
    session.commit()
    #
    response = client.put(
        "/normalization-rules/1",
        json={
            "match_regex": "^22",
            "replace_regex": "",
            "profile_id": normalization_profile.id,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "profile_id": normalization_profile.id,
        "match_regex": "^22",
        "replace_regex": "",
    }


@get_app_and_client
def test_update_normalization_rule_not_found(app=None, client=None):
    response = client.put(
        "/normalization-rules/1",
        json={"match_regex": "^22", "replace_regex": "", "profile_id": 1},
    )
    assert response.status_code == 404


@get_app_and_client
def test_delete_normalization_rule(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    normalization_rule = NormalizationRule(
        match_regex='^11',
        match_prefix='11',
        replace_regex='',
        profile=normalization_profile,
    )
    session.add_all([tenant, normalization_profile, normalization_rule])
    session.commit()
    #
    response = client.delete("/normalization-rules/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "profile_id": normalization_profile.id,
        "match_regex": "^11",
        "replace_regex": '',
    }


@get_app_and_client
def test_delete_normalization_rule_not_found(app=None, client=None):
    response = client.delete("/normalization-rules/1")
    assert response.status_code == 404
