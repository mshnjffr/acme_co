import pytest
from models.entity import Organisation
from repositories.organisation_repository import OrganisationRepository

class TestOrganisationRepository:
    def test_create_organisation(self, repository, sample_org_data):
        """Test creating an organisation."""
        org = Organisation(**sample_org_data)
        created_org = repository.create(org)
        
        assert created_org.id is not None
        assert created_org.name == sample_org_data["name"]
        assert created_org.details == sample_org_data["details"]
        assert created_org.tags == sample_org_data["tags"]
        assert created_org.url == sample_org_data["url"]
        assert created_org.created_at is not None
        assert created_org.updated_at is not None
    
    def test_create_organisation_minimal(self, repository, sample_org_data_minimal):
        """Test creating an organisation with minimal data."""
        org = Organisation(**sample_org_data_minimal)
        created_org = repository.create(org)
        
        assert created_org.id is not None
        assert created_org.name == sample_org_data_minimal["name"]
        assert created_org.details is None
        assert created_org.tags == []
        assert created_org.url is None
    
    def test_get_by_id_existing(self, repository, sample_org_data):
        """Test retrieving an existing organisation by ID."""
        org = Organisation(**sample_org_data)
        created_org = repository.create(org)
        
        retrieved_org = repository.get_by_id(created_org.id)
        
        assert retrieved_org is not None
        assert retrieved_org.id == created_org.id
        assert retrieved_org.name == created_org.name
        assert retrieved_org.details == created_org.details
        assert retrieved_org.tags == created_org.tags
        assert retrieved_org.url == created_org.url
    
    def test_get_by_id_non_existing(self, repository):
        """Test retrieving a non-existing organisation."""
        retrieved_org = repository.get_by_id(999)
        assert retrieved_org is None
    
    def test_get_all_empty(self, repository):
        """Test getting all organisations when none exist."""
        orgs = repository.get_all()
        assert orgs == []
    
    def test_get_all_multiple(self, repository):
        """Test getting all organisations."""
        org1 = Organisation(name="Company A", tags=["tag1"])
        org2 = Organisation(name="Company B", tags=["tag2"])
        org3 = Organisation(name="Company C", tags=["tag3"])
        
        repository.create(org1)
        repository.create(org2)
        repository.create(org3)
        
        all_orgs = repository.get_all()
        
        assert len(all_orgs) == 3
        assert all_orgs[0].name == "Company A"
        assert all_orgs[1].name == "Company B"
        assert all_orgs[2].name == "Company C"
    
    def test_update_organisation(self, repository, sample_org_data):
        """Test updating an organisation."""
        org = Organisation(**sample_org_data)
        created_org = repository.create(org)
        
        updated_data = Organisation(
            name="Updated Company",
            details="Updated details",
            tags=["updated"],
            url="https://updated.com"
        )
        
        updated_org = repository.update(created_org.id, updated_data)
        
        assert updated_org is not None
        assert updated_org.id == created_org.id
        assert updated_org.name == "Updated Company"
        assert updated_org.details == "Updated details"
        assert updated_org.tags == ["updated"]
        assert updated_org.url == "https://updated.com"
        assert updated_org.created_at == created_org.created_at
        assert updated_org.updated_at != created_org.updated_at
    
    def test_update_non_existing(self, repository):
        """Test updating a non-existing organisation."""
        org = Organisation(name="Test")
        updated_org = repository.update(999, org)
        assert updated_org is None
    
    def test_delete_existing(self, repository, sample_org_data):
        """Test deleting an existing organisation."""
        org = Organisation(**sample_org_data)
        created_org = repository.create(org)
        
        deleted = repository.delete(created_org.id)
        assert deleted is True
        
        retrieved_org = repository.get_by_id(created_org.id)
        assert retrieved_org is None
    
    def test_delete_non_existing(self, repository):
        """Test deleting a non-existing organisation."""
        deleted = repository.delete(999)
        assert deleted is False
    
    def test_tags_are_stored_and_retrieved_correctly(self, repository):
        """Test that tags array is properly stored and retrieved."""
        org = Organisation(
            name="Test",
            tags=["python", "fastapi", "testing"]
        )
        created_org = repository.create(org)
        retrieved_org = repository.get_by_id(created_org.id)
        
        assert retrieved_org.tags == ["python", "fastapi", "testing"]
    
    def test_empty_tags_handled_correctly(self, repository):
        """Test that empty tags are handled correctly."""
        org = Organisation(name="Test", tags=[])
        created_org = repository.create(org)
        retrieved_org = repository.get_by_id(created_org.id)
        
        assert retrieved_org.tags == []
