import uuid
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from alembic.command import upgrade
from alembic.config import Config
from app.core.config import get_settings
from app.main import app
from app.models.user import User
from app.models.policy import Policy
from fastapi.testclient import TestClient
from app.db.session import get_db

settings = get_settings()

@pytest.fixture(scope="module")
def module_monkeypatch():
    from _pytest.monkeypatch import MonkeyPatch
    mp = MonkeyPatch()
    yield mp
    mp.undo()

@pytest.fixture(scope="session")
def test_db_name():
    return f"test_db_{uuid.uuid4().hex[:10]}"

@pytest.fixture(scope="session")
def alembic_config():
    return Config("alembic.ini")

@pytest.fixture(scope="session")
def create_test_db(test_db_name):
    if "test_db_" not in test_db_name:
        pytest.fail("Safety check failed - test database name doesn't contain 'test_db_' prefix")

    # Extract base URL and connect to 'postgres' to create the test DB
    base_db_url = settings.DATABASE_URL.rsplit("/", 1)[0]  # Remove DB name
    postgres_url = f"{base_db_url}/postgres"

    default_engine = create_engine(postgres_url, isolation_level="AUTOCOMMIT")

    with default_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE {test_db_name};"))
    
    yield  # Run the tests 

    # Drop the test database after tests complete
    with default_engine.connect() as conn:
        conn.execute(text(f"DROP DATABASE {test_db_name};"))

@pytest.fixture(scope="session")
def apply_migrations(alembic_config, test_db_name):
    base_db_url = settings.DATABASE_URL.rsplit("/", 1)[0]
    test_db_url = f"{base_db_url}/{test_db_name}"
    alembic_config.set_main_option("sqlalchemy.url", test_db_url)
    upgrade(alembic_config, "head")

@pytest.fixture(scope="module")
def db_session(module_monkeypatch, create_test_db, apply_migrations, test_db_name):
    base_db_url = settings.DATABASE_URL.rsplit("/", 1)[0]
    test_db_url = f"{base_db_url}/{test_db_name}"

    # Override settings for the test database
    module_monkeypatch.setattr(settings, "DATABASE_URL", test_db_url)

    engine = create_engine(test_db_url)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()

    yield session  # Run tests using this session

    session.close()
    engine.dispose()

@pytest.fixture(scope="module")
def client(db_session):
    # Override database dependency with test session
    app.dependency_overrides[get_db] = lambda: db_session
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
    db_session.rollback()

@pytest.fixture(scope="function")
def test_user(db_session, email="test@example.com", password="test_hash"):
    user = User(email=email, hashed_password=password)
    db_session.add(user)
    db_session.commit()

    yield user

    db_session.delete(user)
    db_session.commit()

@pytest.fixture(scope="function")
def test_policy(db_session):
    policy = Policy(
        version="v1.0",
        text="Test privacy policy",
        data_purpose="Testing purposes",
        is_active=True
    )
    db_session.add(policy)
    db_session.commit()

    yield policy

    db_session.delete(policy)
    db_session.commit()
