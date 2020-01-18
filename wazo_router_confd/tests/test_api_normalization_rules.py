# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def test_create_normalization_rule(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    session.add_all([normalization_profile, tenant])
    session.commit()
    #
    response = client.post(
        "/1.0/normalization-rules",
        json={
            "profile_id": normalization_profile.id,
            "rule_type": 1,
            "priority": 1,
            "match_regex": "^11",
            "replace_regex": "",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": mock.ANY,
        "profile_id": normalization_profile.id,
        "rule_type": 1,
        "priority": 1,
        "match_regex": "^11",
        "replace_regex": "",
    }


def test_create_duplicated_normalization_rule(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
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
        "/1.0/normalization-rules",
        json={
            "profile_id": normalization_profile.id,
            "match_regex": "^11",
            "replace_regex": "",
        },
    )
    assert response.status_code == 409


def test_get_normalization_rule(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
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
    response = client.get("/1.0/normalization-rules/%s" % normalization_rule.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": normalization_rule.id,
        "rule_type": 1,
        "priority": 0,
        "profile_id": normalization_profile.id,
        "match_regex": "^11",
        "replace_regex": '',
    }


def test_get_normalization_rule_not_found(app, client):
    response = client.get("/1.0/normalization-rules/1")
    assert response.status_code == 404


def test_get_normalization_rules(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
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
    response = client.get("/1.0/normalization-rules")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": normalization_rule.id,
                "profile_id": normalization_profile.id,
                "rule_type": 1,
                "priority": 0,
                "match_regex": "^11",
                "replace_regex": '',
            }
        ]
    }


def test_update_normalization_rule(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
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
        "/1.0/normalization-rules/%s" % normalization_rule.id,
        json={
            "match_regex": "^22",
            "replace_regex": "",
            "profile_id": normalization_profile.id,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": normalization_rule.id,
        "rule_type": 1,
        "priority": 0,
        "profile_id": normalization_profile.id,
        "match_regex": "^22",
        "replace_regex": "",
    }


def test_update_normalization_rule_not_found(app, client):
    response = client.put(
        "/1.0/normalization-rules/1",
        json={"match_regex": "^22", "replace_regex": "", "profile_id": 1},
    )
    assert response.status_code == 404


def test_delete_normalization_rule(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.normalization import NormalizationRule
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
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
    response = client.delete("/1.0/normalization-rules/%s" % normalization_rule.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": normalization_rule.id,
        "rule_type": 1,
        "priority": 0,
        "profile_id": normalization_profile.id,
        "match_regex": "^11",
        "replace_regex": '',
    }


def test_delete_normalization_rule_not_found(app, client):
    response = client.delete("/1.0/normalization-rules/1")
    assert response.status_code == 404
