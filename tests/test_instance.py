import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

from app.main import app
from app.dependencies import get_db
from app.models.user_model import User
from app.models.instance_model import Instance


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://test:test@infra-test.webdrone.fr:5432/provider_inventory"

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


def test_read_instance():
    # Login the user to get a token
    response = client.post(
        "/v1/token/",
        data={"username": "testuser", "password": "password"}
    )
    assert response.status_code == 200
    token = response.json()["token"]

    # Access the protected route
    response = client.get("/v1/instances/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_read_instance_unauthorized():
    # Attempt to access the protected route without a token
    response = client.get("/v1/instances/")
    assert response.status_code == 401


# @pytest.fixture(scope="module")
# def setup_database():
#     db = TestingSessionLocal()
#     user_service = UserService(db)
#     db_user = User(
#         username="testuser",
#         email="test@example.com",
#         hashed_password=UserService.get_password_hash("password"),
#         is_active=True,
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     db_instance = Instance(
#         name="testinstance",
#         description="test description",
#         owner_id=db_user.id
#     )
#     db.add(db_instance)
#     db.commit()
#     db.refresh(db_instance)
#     yield db
#     db.query(Instance).delete()
#     db.query(User).delete()
#     db.commit()
#     db.close()

# def test_create_user():
#     response = client.post(
#         "/users/",
#         json={"username": "newuser", "email": "newuser@example.com", "password": "password"}
#     )
#     assert response.status_code == 200
#     assert response.json()["email"] == "newuser@example.com"

# def test_login_for_access_token(setup_database):
#     response = client.post(
#         "/token",
#         data={"username": "testuser", "password": "password"}
#     )
#     assert response.status_code == 200
#     assert "access_token" in response.json()

# def test_read_users_me(setup_database):
#     login_response = client.post(
#         "/token",
#         data={"username": "testuser", "password": "password"}
#     )
#     access_token = login_response.json()["access_token"]
#     response = client.get(
#         "/users/me/",
#         headers={"Authorization": f"Bearer {access_token}"}
#     )
#     assert response.status_code == 200
#     assert response.json()["username"] == "testuser"

# def test_get_instances_unauthenticated():
#     response = client.get("/instances/")
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Not authenticated"}

# def test_get_instances_authenticated(setup_database):
#     login_response = client.post(
#         "/token",
#         data={"username": "testuser", "password": "password"}
#     )
#     access_token = login_response.json()["access_token"]
#     response = client.get(
#         "/instances/",
#         headers={"Authorization": f"Bearer {access_token}"}
#     )
#     assert response.status_code == 200
#     instances = response.json()
#     assert len(instances) == 1
#     assert instances[0]["name"] == "testinstance"
#     assert instances[0]["description"] == "test description"
