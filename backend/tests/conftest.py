import pytest
import os
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from typing import Generator

# Use PostgreSQL for tests if available, otherwise SQLite
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if TEST_DATABASE_URL:
    # Use PostgreSQL for tests
    SQLALCHEMY_DATABASE_URL = TEST_DATABASE_URL
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True
    )
    USE_SQLITE = False
else:
    # Fallback to SQLite (with spatialite disabled for basic tests)
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )
    USE_SQLITE = True
    
    # Disable spatialite for SQLite tests
    @event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_record):
        pass  # Skip spatialite initialization

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator:
    """Create a fresh database session for each test."""
    if USE_SQLITE:
        # For SQLite, only create non-geometry tables
        # Import only models that don't use Geometry columns
        from app.models.source import Source
        from app.models.user import User
        
        # Create only these tables
        Base.metadata.create_all(bind=engine, tables=[Source.__table__, User.__table__])
    else:
        # Create all tables for PostgreSQL
        Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables
        if USE_SQLITE:
            from app.models.source import Source
            from app.models.user import User
            Base.metadata.drop_all(bind=engine, tables=[Source.__table__, User.__table__])
        else:
            Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Generator):
    """Create a test client with database dependency override."""
    from fastapi.testclient import TestClient
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
