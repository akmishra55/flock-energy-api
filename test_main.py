
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_meters():
    response = client.get("/meters")

    assert response.status_code == 200

    body = response.json()
    assert body["source"] == "mock"
    assert body["total"] == 2
    assert len(body["data"]) == 2


def test_search_meter():
    response = client.get("/meters?search=J100001")

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["data"][0]["meterId"] == "J100001"


def test_energy_for_known_meter():
    response = client.get("/meters/J100001/energy")

    assert response.status_code == 200
    assert len(response.json()["data"]) == 3


def test_second_meter_has_no_sample_energy_readings():
    response = client.get("/meters/J100002/energy")

    assert response.status_code == 200

    body = response.json()
    assert body["meter_id"] == "J100002"
    assert body["source"] == "mock"
    assert body["data"] == []


def test_unknown_meter_returns_404():
    response = client.get("/meters/J999999/energy")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
