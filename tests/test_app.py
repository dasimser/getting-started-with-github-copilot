import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Ensure user is not already signed up
    client.post(f"/activities/{activity}/unregister?email={email}")

    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]


def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/unregister?email={email}")
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    client.post(f"/activities/{activity}/unregister?email={email}")


def test_unregister_not_registered():
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
