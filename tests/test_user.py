import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.main import app
from app.dependencies import get_db
from app.models.user_model import User
from app.services.user_service import UserService


## mangage database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

## test case for user/auth elements

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
        "/v1/users/",
        json={"username": "testuser2", "email": "testuser2@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200

    response = client.post(
        "/v1/users/",
        json={"username": "testuser2", "email": "testuser2@example.com", "password": "testpassword"}
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Email already registered"

