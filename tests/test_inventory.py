import pytest
from fastapi.testclient import TestClient
from app.models.user_model import User

def test_get_inventory(test_client, db_session, test_user):
    ## first get token to access protected route
    response = test_client.post(
        "/v1/token/",
        data={"username": "testuser", "password": "testpassword123"}
    )
    assert response.status_code == 200

    token = response.json()["token"]

    ## Access the protected route
    response = test_client.get("/v1/inventory/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_read_instance_unauthorized(test_client):
    response = test_client.get("/v1/inventory/")
    assert response.status_code == 401