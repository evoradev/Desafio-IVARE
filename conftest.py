import pytest
from rest_framework.test import APIClient
from pet.tests.factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory(password="Senha@123")


@pytest.fixture
def auth_client(api_client, user):
    res = api_client.post(
        "/api/login/",
        {"username": user.username, "password": "Senha@123"},
        format="json",
    )
    assert res.status_code == 200, res.data
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {res.data['access']}")
    return api_client
