# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import mock


def test_create_normalization_profile(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    session.add_all([tenant])
    session.commit()
    #
    response = client.post(
        "/normalization-profiles/",
        json={
            "name": "profile 1",
            "tenant_uuid": str(tenant.uuid),
            "country_code": "39",
            "area_code": "11",
            "intl_prefix": "00",
            "ld_prefix": "0",
            "always_ld": True,
            "always_intl_prefix_plus": False,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": mock.ANY,
        "tenant_uuid": str(tenant.uuid),
        "name": "profile 1",
        "country_code": "39",
        "area_code": "11",
        "intl_prefix": "00",
        "ld_prefix": "0",
        "always_ld": True,
        "always_intl_prefix_plus": False,
    }


def test_create_duplicated_normalization_profile(app, client):
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
        "/normalization-profiles/",
        json={"name": "profile 1", "tenant_uuid": str(tenant.uuid)},
    )
    assert response.status_code == 409


def test_get_normalization_profile(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    session.add_all([normalization_profile, tenant])
    session.commit()
    #
    response = client.get("/normalization-profiles/%s" % normalization_profile.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": normalization_profile.id,
        "name": "profile 1",
        "tenant_uuid": str(tenant.uuid),
        "country_code": None,
        "area_code": None,
        "intl_prefix": None,
        "ld_prefix": None,
        "always_ld": False,
        "always_intl_prefix_plus": False,
    }


def test_get_normalization_profile_not_found(app, client):
    response = client.get("/normalization-profiles/1")
    assert response.status_code == 404


def test_get_normalization_profiles(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    session.add_all([normalization_profile, tenant])
    session.commit()
    #
    response = client.get("/normalization-profiles/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": normalization_profile.id,
            "name": "profile 1",
            "tenant_uuid": str(tenant.uuid),
            "country_code": None,
            "area_code": None,
            "intl_prefix": None,
            "ld_prefix": None,
            "always_ld": False,
            "always_intl_prefix_plus": False,
        }
    ]


def test_update_normalization_profile(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='test', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    session.add_all([normalization_profile, tenant])
    session.commit()
    #
    response = client.put(
        "/normalization-profiles/%s" % normalization_profile.id,
        json={'name': 'profile 2', 'tenant_uuid': str(tenant.uuid)},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": normalization_profile.id,
        "name": "profile 2",
        "tenant_uuid": str(tenant.uuid),
        "country_code": None,
        "area_code": None,
        "intl_prefix": None,
        "ld_prefix": None,
        "always_ld": False,
        "always_intl_prefix_plus": False,
    }


def test_update_normalization_profile_not_found(app, client):
    response = client.put(
        "/normalization-profiles/1",
        json={
            'name': 'profile 2',
            'tenant_uuid': "7e614b21-a9c0-4118-a3e8-6748bc24c5ee",
        },
    )
    assert response.status_code == 404


def test_delete_normalization_profile(app, client):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='test', uuid='5a6c0c40-b481-41bb-a41a-75d1cc25ff34')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    session.add_all([normalization_profile, tenant])
    session.commit()
    #
    response = client.delete("/normalization-profiles/%s" % normalization_profile.id)
    assert response.status_code == 200
    assert response.json() == {
        "id": normalization_profile.id,
        "tenant_uuid": str(tenant.uuid),
        "name": "profile 1",
        "country_code": None,
        "area_code": None,
        "intl_prefix": None,
        "ld_prefix": None,
        "always_ld": False,
        "always_intl_prefix_plus": False,
    }


def test_delete_normalization_profile_not_found(app, client):
    response = client.delete("/normalization-profiles/1")
    assert response.status_code == 404
