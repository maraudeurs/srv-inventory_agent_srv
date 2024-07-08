import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime

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

## global vars
current_datetime = datetime.now().isoformat()

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
            "ip_v4" : "127.0.0.1",
            "ip_v6" : "test",
            "status" : "test",
            "main_usage" : "test",
            "location" : "test",
            "tag" : "test",
            "cloud_model" : "test",
            "cloud_provider" : "test",
            "provider_uuid" : "test",
            "instance_memory" : 60,
            "instance_cpu" : 8,
            "in_bandwidth" : "test",
            "out_bandwidth" : "test",
            "cloud_service_type" : "test",
            "inventory_source_method" : "test",
            "system_os" : "test",
            "system_release" : "test",
            "system_architecture" : "test",
            "hostname" : "test",
            "python_version" : "test",
            "virtualization_method" : ["docker"],
            "update_date" : current_datetime,
            "creation_date" : current_datetime
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
            "ip_v4" : "127.0.0.1",
            "ip_v6" : "test",
            "status" : "test",
            "main_usage" : "test",
            "location" : "test",
            "tag" : "test",
            "cloud_model" : "test",
            "cloud_provider" : "test",
            "provider_uuid" : "test",
            "instance_memory" : 60,
            "instance_cpu" : 8,
            "in_bandwidth" : "test",
            "out_bandwidth" : "test",
            "cloud_service_type" : "test",
            "inventory_source_method" : "test",
            "system_os" : "test",
            "system_release" : "test",
            "system_architecture" : "test",
            "hostname" : "test",
            "python_version" : "test",
            "virtualization_method" : [],
            "update_date" : current_datetime,
            "creation_date" : current_datetime
        },
        auth=(DISCOVERY_GENERIC_USER, DISCOVERY_GENERIC_PASSWORD)
    )
    assert response.status_code == 400
    assert "Instance already registered" in response.text

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
            "instance_memory" : 60,
            "instance_cpu" : 8,
            "in_bandwidth" : "test2",
            "out_bandwidth" : "test2",
            "cloud_service_type" : "test2",
            "inventory_source_method" : "test2",
            "system_os" : "test2",
            "system_release" : "test2",
            "system_architecture" : "test2",
            "hostname" : "test2",
            "python_version" : "test2",
            "virtualization_method" : [],
            "update_date" : current_datetime,
            "creation_date" : current_datetime
        },
        auth=("wronglogin", "wrongpassword")
    )
    assert response.status_code == 401

