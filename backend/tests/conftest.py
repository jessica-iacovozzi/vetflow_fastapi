import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app
from app.models.base import TimeStampedBase as Base

@pytest.fixture(scope="session")
def postgresql_url(request):
    """
    Create a PostgreSQL database URL for testing.
    Uses environment variables if available, otherwise uses pytest-postgresql.
    """
    try:
        import pytest_postgresql
        from pytest_postgresql.executor import PostgresExecutor
    except ImportError:
        pytest.skip("pytest-postgresql is required for PostgreSQL testing")
    
    # Create PostgreSQL executor
    postgresql = PostgresExecutor(
        postgres_options='-p 5433',  # Use a non-standard port to avoid conflicts
        host='localhost',
    )
    
    # Start the PostgreSQL instance
    postgresql.start()
    
    # Construct database URL
    url = (
        f"postgresql://{postgresql.user}:"
        f"{postgresql.password}@{postgresql.host}:"
        f"{postgresql.port}/{postgresql.dbname}"
    )
    
    # Yield the URL and ensure cleanup
    yield url
    
    # Stop the PostgreSQL instance
    postgresql.stop()

@pytest.fixture(scope="session")
def test_database(postgresql_url):
    """
    Create a SQLAlchemy engine for the test database.
    """
    # Create SQLAlchemy engine
    engine = create_engine(postgresql_url)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    yield engine
    
    # Cleanup
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(test_database):
    """
    Create a new database session for each test function.
    """
    # Create a new session maker for testing
    TestingSessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=test_database
    )
    
    try:
        # Create a new database session
        db = TestingSessionLocal()
        yield db
    finally:
        # Close the session and clear data for next test
        db.close()
        Base.metadata.drop_all(bind=test_database)
        Base.metadata.create_all(bind=test_database)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client that uses the test database session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Override the database dependency with test session
    app.dependency_overrides[get_db] = override_get_db
    
    # Create and yield the test client
    yield TestClient(app)
    
    # Clear the dependency overrides after the test
    app.dependency_overrides.clear()