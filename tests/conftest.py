import pytest
import os
import tempfile
from fastapi.testclient import TestClient
from repositories.organisation_repository import OrganisationRepository
from services.organisation_service import OrganisationService
from main import app

@pytest.fixture
def test_db_path():
    """Create a temporary database file for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    os.unlink(path)

@pytest.fixture
def repository(test_db_path):
    """Create a test repository instance."""
    return OrganisationRepository(test_db_path)

@pytest.fixture
def service(repository):
    """Create a test service instance."""
    return OrganisationService(repository)

@pytest.fixture
def client():
    """Create a test client for API testing."""
    return TestClient(app)

@pytest.fixture
def sample_org_data():
    """Sample organisation data for testing."""
    return {
        "name": "Test Company",
        "details": "A test organisation",
        "tags": ["test", "sample"],
        "url": "https://testcompany.com"
    }

@pytest.fixture
def sample_org_data_minimal():
    """Minimal organisation data for testing."""
    return {
        "name": "Minimal Company"
    }
