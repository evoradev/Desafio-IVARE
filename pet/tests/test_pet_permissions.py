import pytest
from rest_framework.test import APIClient
from pet.tests.factories import UserFactory, PetFactory


@pytest.mark.django_db
def test_user_cannot_access_other_users_pet():
    user_a = UserFactory(password="Senha@123")
    user_b = UserFactory(password="Senha@123")

    pet_b = PetFactory(user=user_b)

    client = APIClient()
    login = client.post("/api/login/", {"username": user_a.username, "password": "Senha@123"}, format="json")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

    res = client.get(f"/api/pets/{pet_b.id}/")
    assert res.status_code in (404, 403)

    patch = client.patch(f"/api/pets/{pet_b.id}/", {"name": "hack"}, format="json")
    assert patch.status_code in (404, 403)
