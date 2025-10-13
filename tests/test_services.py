import pytest
from models.entity import Organisation
from services.organisation_service import OrganisationService

class TestOrganisationService:
    def test_create_organisation(self, service, sample_org_data):
        """Test creating an organisation through the service."""
        created_org = service.create_organisation(**sample_org_data)
        
        assert created_org.id is not None
        assert created_org.name == sample_org_data["name"]
        assert created_org.details == sample_org_data["details"]
        assert created_org.tags == sample_org_data["tags"]
        assert created_org.url == sample_org_data["url"]
    
    def test_create_organisation_with_defaults(self, service):
        """Test creating an organisation with default values."""
        created_org = service.create_organisation(name="Test Company")
        
        assert created_org.id is not None
        assert created_org.name == "Test Company"
        assert created_org.details is None
        assert created_org.tags == []
        assert created_org.url is None
    
    def test_get_organisation_by_id(self, service, sample_org_data):
        """Test retrieving an organisation by ID."""
        created_org = service.create_organisation(**sample_org_data)
        retrieved_org = service.get_organisation_by_id(created_org.id)
        
        assert retrieved_org is not None
        assert retrieved_org.id == created_org.id
        assert retrieved_org.name == created_org.name
    
    def test_get_organisation_by_id_not_found(self, service):
        """Test retrieving a non-existing organisation."""
        retrieved_org = service.get_organisation_by_id(999)
        assert retrieved_org is None
    
    def test_get_all_organisations_empty(self, service):
        """Test getting all organisations when none exist."""
        orgs = service.get_all_organisations()
        assert orgs == []
    
    def test_get_all_organisations(self, service):
        """Test getting all organisations."""
        service.create_organisation(name="Company A")
        service.create_organisation(name="Company B")
        service.create_organisation(name="Company C")
        
        all_orgs = service.get_all_organisations()
        
        assert len(all_orgs) == 3
        assert all_orgs[0].name == "Company A"
        assert all_orgs[1].name == "Company B"
        assert all_orgs[2].name == "Company C"
    
    def test_update_organisation_all_fields(self, service, sample_org_data):
        """Test updating all fields of an organisation."""
        created_org = service.create_organisation(**sample_org_data)
        
        updated_org = service.update_organisation(
            id=created_org.id,
            name="Updated Name",
            details="Updated details",
            tags=["new", "tags"],
            url="https://updated.com"
        )
        
        assert updated_org is not None
        assert updated_org.name == "Updated Name"
        assert updated_org.details == "Updated details"
        assert updated_org.tags == ["new", "tags"]
        assert updated_org.url == "https://updated.com"
    
    def test_update_organisation_partial(self, service, sample_org_data):
        """Test partial update of an organisation."""
        created_org = service.create_organisation(**sample_org_data)
        
        updated_org = service.update_organisation(
            id=created_org.id,
            name="New Name Only"
        )
        
        assert updated_org is not None
        assert updated_org.name == "New Name Only"
        assert updated_org.details == sample_org_data["details"]
        assert updated_org.tags == sample_org_data["tags"]
        assert updated_org.url == sample_org_data["url"]
    
    def test_update_organisation_not_found(self, service):
        """Test updating a non-existing organisation."""
        updated_org = service.update_organisation(id=999, name="Test")
        assert updated_org is None
    
    def test_update_organisation_preserves_unspecified_fields(self, service):
        """Test that unspecified fields are preserved during update."""
        created_org = service.create_organisation(
            name="Original",
            details="Original details",
            tags=["tag1", "tag2"],
            url="https://original.com"
        )
        
        updated_org = service.update_organisation(
            id=created_org.id,
            name="Updated Name"
        )
        
        assert updated_org.name == "Updated Name"
        assert updated_org.details == "Original details"
        assert updated_org.tags == ["tag1", "tag2"]
        assert updated_org.url == "https://original.com"
    
    def test_delete_organisation(self, service, sample_org_data):
        """Test deleting an organisation."""
        created_org = service.create_organisation(**sample_org_data)
        
        deleted = service.delete_organisation(created_org.id)
        assert deleted is True
        
        retrieved_org = service.get_organisation_by_id(created_org.id)
        assert retrieved_org is None
    
    def test_delete_organisation_not_found(self, service):
        """Test deleting a non-existing organisation."""
        deleted = service.delete_organisation(999)
        assert deleted is False
    
    def test_service_operations_are_isolated(self, service):
        """Test that service operations don't interfere with each other."""
        org1 = service.create_organisation(name="Org 1", tags=["tag1"])
        org2 = service.create_organisation(name="Org 2", tags=["tag2"])
        
        service.update_organisation(id=org1.id, tags=["updated"])
        
        retrieved_org2 = service.get_organisation_by_id(org2.id)
        assert retrieved_org2.tags == ["tag2"]
