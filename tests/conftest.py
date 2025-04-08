
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import project modules
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your application factory
from main import create_app

# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def app():
    #Create a fresh app instance for each test.
    return create_app()

@pytest.fixture
def client(app):
    #Create a test client using the app fixture.
    return TestClient(app)

@pytest.fixture
def test_db():
    # Setup test database
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    # Teardown
    Base.metadata.drop_all(bind=engine)
