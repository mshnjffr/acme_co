import pytest
from datetime import datetime, timezone
from models.entity import Organisation

class TestOrganisation:
    def test_create_organisation_with_all_fields(self):
        """Test creating an organisation with all fields."""
        org = Organisation(
            id=1,
            name="Test Company",
            details="A test organisation",
            tags=["test", "sample"],
            url="https://testcompany.com",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        assert org.id == 1
        assert org.name == "Test Company"
        assert org.details == "A test organisation"
        assert org.tags == ["test", "sample"]
        assert org.url == "https://testcompany.com"
        assert isinstance(org.created_at, datetime)
        assert isinstance(org.updated_at, datetime)
    
    def test_create_organisation_minimal_fields(self):
        """Test creating an organisation with only required field."""
        org = Organisation(name="Minimal Company")
        
        assert org.name == "Minimal Company"
        assert org.id is None
        assert org.details is None
        assert org.tags == []
        assert org.url is None
        assert org.created_at is None
        assert org.updated_at is None
    
    def test_create_organisation_default_tags(self):
        """Test that tags default to empty list."""
        org = Organisation(name="Company A")
        assert org.tags == []
        
        org2 = Organisation(name="Company B")
        assert org2.tags == []
        
        org.tags.append("tag1")
        assert org.tags == ["tag1"]
        assert org2.tags == []
    
    def test_to_dict_with_all_fields(self):
        """Test converting organisation to dictionary."""
        now = datetime.now(timezone.utc)
        org = Organisation(
            id=1,
            name="Test Company",
            details="Details",
            tags=["tag1", "tag2"],
            url="https://example.com",
            created_at=now,
            updated_at=now
        )
        
        org_dict = org.to_dict()
        
        assert org_dict["id"] == 1
        assert org_dict["name"] == "Test Company"
        assert org_dict["details"] == "Details"
        assert org_dict["tags"] == ["tag1", "tag2"]
        assert org_dict["url"] == "https://example.com"
        assert org_dict["created_at"] == now.isoformat()
        assert org_dict["updated_at"] == now.isoformat()
    
    def test_to_dict_with_none_values(self):
        """Test converting organisation with None values to dictionary."""
        org = Organisation(name="Test")
        org_dict = org.to_dict()
        
        assert org_dict["id"] is None
        assert org_dict["name"] == "Test"
        assert org_dict["details"] is None
        assert org_dict["tags"] == []
        assert org_dict["url"] is None
        assert org_dict["created_at"] is None
        assert org_dict["updated_at"] is None
