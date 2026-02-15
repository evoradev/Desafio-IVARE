import pytest
from pet.tests.factories import PetFactory, VaccineFactory


@pytest.mark.django_db
def test_create_vaccination_requires_published_pet_and_vaccine(auth_client, user):
    pet = PetFactory(user=user, is_published=True)
    vaccine = VaccineFactory(is_published=True)

    payload = {
        "pet": pet.id,
        "vaccine": vaccine.id,
        "number_of_aplications": 1,
        "batch_number": "Lote-123",
        "veterinarian_name": "Dra. Silva",
        "observations": "Ok",
    }

    created = auth_client.post("/api/pet-vaccinations/", payload, format="json")
    assert created.status_code == 201, created.data

    listed = auth_client.get("/api/pet-vaccinations/")
    assert listed.status_code == 200
    assert len(listed.data) >= 1


@pytest.mark.django_db
def test_create_vaccination_fails_if_pet_not_published(auth_client, user):
    pet = PetFactory(user=user, is_published=False)
    vaccine = VaccineFactory(is_published=True)

    payload = {"pet": pet.id, "vaccine": vaccine.id}
    res = auth_client.post("/api/pet-vaccinations/", payload, format="json")
    assert res.status_code == 400
    assert "pet" in res.data


@pytest.mark.django_db
def test_create_vaccination_fails_if_vaccine_not_published(auth_client, user):
    pet = PetFactory(user=user, is_published=True)
    vaccine = VaccineFactory(is_published=False)

    payload = {"pet": pet.id, "vaccine": vaccine.id}
    res = auth_client.post("/api/pet-vaccinations/", payload, format="json")
    assert res.status_code == 400
    assert "vaccine" in res.data
