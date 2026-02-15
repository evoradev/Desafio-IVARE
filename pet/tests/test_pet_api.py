import pytest
from pet.models import Pet


@pytest.mark.django_db
def test_pet_crud_flow(auth_client, user):
    # CREATE
    payload = {
        "name": "Thor",
        "owner_name": "Évora Rafael",
        "pet_type": "DOG",
        "description": "Cachorro saudável",
        "is_published": True,
    }
    created = auth_client.post("/api/pets/", payload, format="json")
    assert created.status_code == 201, created.data
    pet_id = created.data["id"]

    # LIST (só os do usuário)
    listed = auth_client.get("/api/pets/")
    assert listed.status_code == 200
    assert any(p["id"] == pet_id for p in listed.data)

    # RETRIEVE
    got = auth_client.get(f"/api/pets/{pet_id}/")
    assert got.status_code == 200
    assert got.data["id"] == pet_id

    # PATCH
    patched = auth_client.patch(f"/api/pets/{pet_id}/", {"name": "Thor 2"}, format="json")
    assert patched.status_code == 200
    assert patched.data["name"] == "Thor 2"

    # DELETE
    deleted = auth_client.delete(f"/api/pets/{pet_id}/")
    assert deleted.status_code in (204, 200)

    # RETRIEVE novamente
    again = auth_client.get(f"/api/pets/{pet_id}/")
    assert again.status_code == 404
