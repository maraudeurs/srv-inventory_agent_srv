import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.dependencies import get_db
from app.models.user_model import User
from app.models.instance_model import Instance
from app.models.database import init_db, purge_db

## test parameters
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
DISCOVERY_GENERIC_USER="discovery"
DISCOVERY_GENERIC_PASSWORD="PyGOOKVC83jnIVa4A4NO4bNCeFDkyAifbuX9cQFPGZTDV8rIALotqz21uTOQqAjznO4AQnzcWN5y5DQPnLrdkjyqKuMCnJUl"

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Instance.metadata.drop_all(bind=engine)
User.metadata.drop_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        Instance.metadata.create_all(bind=engine)
        User.metadata.create_all(bind=engine)
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_user():
    response = client.post(
        "/v1/register/",
        json={"username": "testuser", "email": "test@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_read_instance():
    response = client.post(
        "/v1/token/",
        data={"username": "testuser", "password": "password"}
    )
    print(response.json())
    assert response.status_code == 200
    token = response.json()["token"]

    ## Access the protected route
    response = client.get("/v1/instances/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_read_instance_unauthorized():
    response = client.get("/v1/instances/")
    assert response.status_code == 401

def test_post_instance_unauthorized():
    response = client.post("/v1/instances/")
    assert response.status_code == 401

def test_post_instance():
    response = client.post(
        "/v1/instances/",
        json={
            "name": "test",
            "description": "test",
            "ip_v4" : "test",
            "ip_v6" : "test",
            "status" : "test",
            "main_usage" : "test",
            "location" : "test",
            "tag" : "test",
            "cloud_model" : "test",
            "cloud_provider" : "test",
            "provider_uuid" : "test",
            "instance_memory" : "test",
            "instance_cpu" : "test",
            "update_date" : "test",
            "creation_date" : "test"
        },
        auth=(DISCOVERY_GENERIC_USER, DISCOVERY_GENERIC_PASSWORD)
    )
    assert response.status_code == 200

def test_duplicate_post_instance():
    response = client.post(
        "/v1/instances/",
        json={
            "name": "test",
            "description": "test",
            "ip_v4" : "test",
            "ip_v6" : "test",
            "status" : "test",
            "main_usage" : "test",
            "location" : "test",
            "tag" : "test",
            "cloud_model" : "test",
            "cloud_provider" : "test",
            "provider_uuid" : "test",
            "instance_memory" : "test",
            "instance_cpu" : "test",
            "update_date" : "test",
            "creation_date" : "test"
        },
        auth=(DISCOVERY_GENERIC_USER, DISCOVERY_GENERIC_PASSWORD)
    )
    assert response.status_code == 400
    assert response.json() == {"detail" :"Instance already registered"}

def test_post_instance_wrong_auth():
    response = client.post(
        "/v1/instances/",
        json={
            "name": "test2",
            "description": "test2",
            "ip_v4" : "test2",
            "ip_v6" : "test2",
            "status" : "test2",
            "main_usage" : "test2",
            "location" : "test2",
            "tag" : "test2",
            "cloud_model" : "test2",
            "cloud_provider" : "test2",
            "provider_uuid" : "test2",
            "instance_memory" : "test2",
            "instance_cpu" : "test2",
            "update_date" : "test2",
            "creation_date" : "test2"
        },
        auth=("wronglogin", "wrongpassword")
    )
    assert response.status_code == 401

