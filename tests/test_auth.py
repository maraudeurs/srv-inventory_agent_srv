import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.main import app
from app.dependencies import get_db
from app.auth.user_service import get_password_hash
from app.models.user_model import User
from app.models.database import init_db, purge_db

## mangage database for testing

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

User.metadata.drop_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        User.metadata.create_all(bind=engine)
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

## test case for user/auth elements

# @pytest.fixture(scope="module")
# def setup_database():
#     db = TestingSessionLocal()
#     test_user = User(
#         username="testuser",
#         email="test@example.com",
#         hashed_password=get_password_hash("password"),
#         disabled=False
#     )
#     db.add(test_user)
#     db.commit()
#     db.refresh(test_user)
#     yield db
#     db.delete(test_user)
#     db.query(User).delete()
#     db.commit()
#     db.close()

@pytest.fixture(scope="module")
def setup_database():
    db = TestingSessionLocal()
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    yield db
    db.delete(test_user)
    db.query(User).delete()
    db.commit()
    db.close()

def test_create_duplicate_user():
    response = client.post(
        "/v1/register/",
        json={"username": "testuser2", "email": "testuser2@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200

    response = client.post(
        "/v1/register/",
        json={"username": "testuser2", "email": "testuser2@example.com", "password": "testpassword"}
    )
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Email already registered"

def test_create_user():
    response = client.post(
        "/v1/register/",
        json={"username": "testuser3", "email": "test3@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test3@example.com"

def test_login():
    response = client.post(
        "/v1/token/",
        data={"username": "testuser3", "password": "password"}
    )
    assert response.status_code == 200

def test_invalid_login():
    response = client.post(
        "/v1/token/",
        data={"username": "testuser3", "email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"

def test_user_me():
    login_response = client.post(
        "/v1/token/",
        data={"username": "testuser3", "password": "password"}
    )
    assert login_response.status_code == 200
    data = login_response.json()
    assert "token" in data
    assert data["token_type"] == "bearer"

    token = data["token"]
    response = client.get(
        "/v1/users/me/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_unauthorized_user_me():
    response = client.get(
        "/v1/users/me/"
    )
    assert response.status_code == 401
