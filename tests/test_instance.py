import pytest

from datetime import datetime

from app.main import app
from app.models.user_model import User
from app.models.instance_model import Instance

## test parameters
DISCOVERY_GENERIC_USER="discovery"
DISCOVERY_GENERIC_PASSWORD="PyGOOKVC83jnIVa4A4NO4bNCeFDkyAifbuX9cQFPGZTDV8rIALotqz21uTOQqAjznO4AQnzcWN5y5DQPnLrdkjyqKuMCnJUl"

## global vars
current_datetime = datetime.now().isoformat()

def test_read_instance(test_client, db_session, test_user):
    ## first get token
    response = test_client.post(
        "/v1/token/",
        data={"username": "testuser", "password": "testpassword123"}
    )
    assert response.status_code == 200
    token = response.json()["token"]

    ## then access the protected route
    response = test_client.get("/v1/instances/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_read_instance_unauthorized(test_client, db_session):
    response = test_client.get("/v1/instances/")
    assert response.status_code == 401

def test_post_instance_unauthorized(test_client, db_session):
    response = test_client.post("/v1/instances/")
    assert response.status_code == 401

def test_post_instance(test_client, db_session):
    response = test_client.post(
        "/v1/instances/",
        json={
            "name": "test",
            "description": "test",
            "main_ipv4" : "127.0.0.1",
            "ip_v4_list": [],
            "ip_v6_list" : [],
            "status" : "active",
            "main_group": "test",
            "environment": "test",
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
            "virtualization_method" : ["docker", "proxmox"],
            "update_date" : current_datetime
        },
        auth=(DISCOVERY_GENERIC_USER, DISCOVERY_GENERIC_PASSWORD)
    )
    assert response.status_code == 200

def test_duplicate_post_instance(test_client, db_session):
    response = test_client.post(
        "/v1/instances/",
        json={
            "name": "test",
            "description": "test",
            "main_ipv4" : "127.0.0.2",
            "ip_v4_list": [],
            "ip_v6_list" : [],
            "status" : "active",
            "main_group": "test",
            "environment": "test",
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
            "update_date" : current_datetime
        },
        auth=(DISCOVERY_GENERIC_USER, DISCOVERY_GENERIC_PASSWORD)
    )
    assert response.status_code == 400
    assert "Instance already registered" in response.text

def test_post_instance_wrong_auth(test_client, db_session):
    response = test_client.post(
        "/v1/instances/",
        json={
            "name": "test",
            "description": "test",
            "main_ipv4" : "127.0.0.1",
            "ip_v4_list": [],
            "ip_v6_list" : [],
            "status" : "active",
            "main_group": "test",
            "environment": "test",
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
            "update_date" : current_datetime
        },
        auth=("wronglogin", "wrongpassword")
    )
    assert response.status_code == 401

