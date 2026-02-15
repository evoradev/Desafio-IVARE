import pytest

@pytest.mark.django_db
def test_create_vaccine(auth_client):
    payload = {
        "name": "Antirrábica",
        "manufacturer": "Lab X",
        "disease_prevented": "Raiva",
        "is_published": True,
    }
    res = auth_client.post("/api/vaccines/", payload, format="json")
    assert res.status_code == 201, res.data
