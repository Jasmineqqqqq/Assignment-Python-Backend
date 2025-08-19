"""Basic unit tests for authentication."""

from fastapi.testclient import TestClient

from app.main import create_app


def test_registration_and_login() -> None:
    app = create_app()
    client = TestClient(app)
    register_data = {
        "name": "Dr. Alice",
        "email": "alice@example.com",
        "password": "strongpassword",
        "role": "doctor",
    }
    response = client.post("/auth/register", json=register_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == register_data["email"]

    login_data = {"username": register_data["email"], "password": register_data["password"]}
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    me = response.json()
    assert me["email"] == register_data["email"]