import pytest

from app.main import app
from app.auth.user_service import get_password_hash
from app.models.user_model import User

def test_create_duplicate_user(test_client, db_session):
    response = test_client.post(
        "/v1/register/",
        json={"username": "testuser2", "email": "testuser2@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200

    response = test_client.post(
        "/v1/register/",
        json={"username": "testuser2", "email": "testuser2@example.com", "password": "testpassword"}
    )
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Email already registered"

def test_create_user(test_client, db_session):
    response = test_client.post(
        "/v1/register/",
        json={"username": "testuser3", "email": "test3@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test3@example.com"

def test_login(test_client, db_session):
    response = test_client.post(
        "/v1/token/",
        data={"username": "testuser3", "password": "password"}
    )
    assert response.status_code == 200

def test_invalid_login(test_client, db_session):
    response = test_client.post(
        "/v1/token/",
        data={"username": "testuser3", "email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"

def test_user_me(test_client, db_session):
    login_response = test_client.post(
        "/v1/token/",
        data={"username": "testuser3", "password": "password"}
    )
    assert login_response.status_code == 200
    data = login_response.json()
    assert "token" in data
    assert data["token_type"] == "bearer"

    token = data["token"]
    response = test_client.get(
        "/v1/users/me/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_unauthorized_user_me(test_client, db_session):
    response = test_client.get(
        "/v1/users/me/"
    )
    assert response.status_code == 401
