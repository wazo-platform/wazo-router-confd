# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .common import get_app_and_client


@get_app_and_client
def test_create_normalization_profile(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    session.add_all([tenant])
    session.commit()
    #
    response = client.post(
        "/normalization-profiles/",
        json={
            "name": "profile 1",
            "tenant_id": tenant.id,
            "country_code": "39",
            "area_code": "11",
            "intl_prefix": "00",
            "ld_prefix": "0",
            "always_ld": True,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "tenant_id": tenant.id,
        "name": "profile 1",
        "country_code": "39",
        "area_code": "11",
        "intl_prefix": "00",
        "ld_prefix": "0",
        "always_ld": True,
    }


@get_app_and_client
def test_create_duplicated_normalization_profile(app=None, client=None):
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
        "/normalization-profiles/", json={"name": "profile 1", "tenant_id": tenant.id}
    )
    assert response.status_code == 409


@get_app_and_client
def test_get_normalization_profile(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    session.add_all([normalization_profile, tenant])
    session.commit()
    #
    response = client.get("/normalization-profiles/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "profile 1",
        "tenant_id": tenant.id,
        "country_code": None,
        "area_code": None,
        "intl_prefix": None,
        "ld_prefix": None,
        "always_ld": False,
    }


@get_app_and_client
def test_get_normalization_profile_not_found(app=None, client=None):
    response = client.get("/normalization-profiles/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_normalization_profiles(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    session.add_all([normalization_profile, tenant])
    session.commit()
    #
    response = client.get("/normalization-profiles/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "profile 1",
            "tenant_id": tenant.id,
            "country_code": None,
            "area_code": None,
            "intl_prefix": None,
            "ld_prefix": None,
            "always_ld": False,
        }
    ]


@get_app_and_client
def test_update_normalization_profile(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='test')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    session.add_all([normalization_profile, tenant])
    session.commit()
    #
    response = client.put(
        "/normalization-profiles/1", json={'name': 'profile 2', 'tenant_id': tenant.id}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "profile 2",
        "tenant_id": tenant.id,
        "country_code": None,
        "area_code": None,
        "intl_prefix": None,
        "ld_prefix": None,
        "always_ld": False,
    }


@get_app_and_client
def test_update_normalization_profile_not_found(app=None, client=None):
    response = client.put(
        "/normalization-profiles/1", json={'name': 'profile 2', 'tenant_id': 1}
    )
    assert response.status_code == 404


@get_app_and_client
def test_delete_normalization_profile(app=None, client=None):
    from wazo_router_confd.database import SessionLocal
    from wazo_router_confd.models.normalization import NormalizationProfile
    from wazo_router_confd.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='test')
    normalization_profile = NormalizationProfile(name='profile 1', tenant=tenant)
    session.add_all([normalization_profile, tenant])
    session.commit()
    #
    response = client.delete("/normalization-profiles/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "tenant_id": tenant.id,
        "name": "profile 1",
        "country_code": None,
        "area_code": None,
        "intl_prefix": None,
        "ld_prefix": None,
        "always_ld": False,
    }


@get_app_and_client
def test_delete_normalization_profile_not_found(app=None, client=None):
    response = client.delete("/normalization-profiles/1")
    assert response.status_code == 404
