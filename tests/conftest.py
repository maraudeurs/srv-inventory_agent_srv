
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.dependencies import get_db
from app.models.user_model import User
from app.models.instance_model import Instance
from app.core.security import get_password_hash
# from app.models.database import init_db, purge_db

from datetime import datetime

## test parameters
SQLALCHEMY_DATABASE_URL = "sqlite:///./pytest.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
## Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

## Create tables in database
Instance.metadata.create_all(bind=engine)
User.metadata.create_all(bind=engine)

current_datetime = datetime.now()

@pytest.fixture(scope="function")
def test_user(db_session):
    """Add a test user to the database."""
    test_user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        disabled=False
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)
    assert test_user.id is not None
    return test_user

@pytest.fixture(scope="function")
def test_instance(db_session):
    """Add a test instance to the database."""
    test_instance = Instance(
        name="test",
        description="test",
        main_ipv4="127.0.0.2",
        status="test",
        main_group="test",
        environment="test",
        ansible_ssh_user="test",
        main_usage="test",
        location="test",
        tag="test",
        cloud_model="test",
        cloud_provider="test",
        provider_uuid="test",
        instance_memory=1,
        instance_cpu=1,
        in_bandwidth="test",
        out_bandwidth="test",
        cloud_service_type="test",
        inventory_source_method="test",
        system_os="test",
        system_release="test",
        system_architecture="test",
        hostname="test",
        python_version="test",
        update_date=current_datetime,
        creation_date=current_datetime,
    )
    db_session.add(test_instance)
    db_session.commit()
    db_session.refresh(test_instance)
    assert test_instance.id is not None
    return test_instance

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def test_client(db_session, test_instance, test_user):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

