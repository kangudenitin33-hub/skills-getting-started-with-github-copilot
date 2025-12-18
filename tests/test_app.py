import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data

def test_signup_for_activity():
    email = "testuser@example.com"
    activity = "Basketball"
    # Remove if already present
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json().get("message", "")
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response2.status_code == 400
    # Unregister
    response3 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response3.status_code in (200, 404)
    if response3.status_code == 200:
        assert email not in client.get("/activities").json()[activity]["participants"]

def test_unregister_not_found():
    response = client.delete("/activities/Basketball/unregister", params={"email": "notfound@example.com"})
    assert response.status_code == 404

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "user@example.com"})
    assert response.status_code == 404
