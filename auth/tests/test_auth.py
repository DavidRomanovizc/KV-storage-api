import pytest
from starlette.testclient import (
    TestClient,
)

from auth.main import (
    application,
)

client = TestClient(application)


def test_login_success():
    response = client.post("/api/login", json={"username": "admin", "password": "presale"})
    assert response.status_code == 200
    assert "token" in response.json()


def test_login_invalid_credentials():
    response = client.post("/api/login", json={"username": "invalid_username", "password": "invalid_password"})
    assert response.status_code == 401


def test_login_missing_fields():
    response = client.post("/api/login", json={"username": "your_username"})
    assert response.status_code == 422


def test_invalid_token():
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/api/some-secure-endpoint", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"access_granted": False}


@pytest.mark.parametrize("token_header", [
    {"Authorization": "Bearer valid_token"},
    {"Authorization": "Bearer another_valid_token"},
])
def test_valid_token(token_header):
    response = client.post("/api/some-secure-endpoint", headers=token_header)
    assert response.status_code == 200
    assert response.json() == {"access_granted": True}


def test_verify_access():
    login_response = client.post("/api/login", json={"username": "admin", "password": "presale"})
    assert login_response.status_code == 200
    assert "token" in login_response.json()

    token = login_response.json()["token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    verify_response = client.post("/api/verify-access", headers=headers)

    assert verify_response.status_code == 200
    assert verify_response.json() == {"access_granted": True}
