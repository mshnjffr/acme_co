import pytest
from fastapi.testclient import TestClient
from main import app
from api.config import API_PREFIX

client = TestClient(app)

ORGANISATION_ENDPOINT = f"{API_PREFIX}/organisation"


class TestOrganisationAPI:
    def test_create_organisation_full(self):
        """Test creating an organisation with all fields via API."""
        response = client.put(ORGANISATION_ENDPOINT, json={
            "name": "API Test Company",
            "details": "Created via API",
            "tags": ["api", "test"],
            "url": "https://apitest.com"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "API Test Company"
        assert data["details"] == "Created via API"
        assert data["tags"] == ["api", "test"]
        assert data["url"] == "https://apitest.com"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_organisation_minimal(self):
        """Test creating an organisation with only required fields."""
        response = client.put(ORGANISATION_ENDPOINT, json={
            "name": "Minimal Company"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Minimal Company"
        assert data["details"] is None
        assert data["tags"] == []
        assert data["url"] is None
    
    def test_create_organisation_missing_name(self):
        """Test creating an organisation without name (should fail)."""
        response = client.put(ORGANISATION_ENDPOINT, json={
            "details": "No name provided"
        })
        
        assert response.status_code == 422
    
    def test_get_all_organisations_empty(self):
        """Test getting all organisations when none exist."""
        response = client.get(ORGANISATION_ENDPOINT)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_all_organisations(self):
        """Test getting all organisations."""
        client.put(ORGANISATION_ENDPOINT, json={"name": "Company A"})
        client.put(ORGANISATION_ENDPOINT, json={"name": "Company B"})
        
        response = client.get(ORGANISATION_ENDPOINT)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
    
    def test_get_organisation_by_id(self):
        """Test getting a specific organisation by ID."""
        create_response = client.put(ORGANISATION_ENDPOINT, json={
            "name": "Test Company",
            "tags": ["test"]
        })
        created_id = create_response.json()["id"]
        
        response = client.get(f"{ORGANISATION_ENDPOINT}/{created_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_id
        assert data["name"] == "Test Company"
        assert data["tags"] == ["test"]
    
    def test_get_organisation_by_id_not_found(self):
        """Test getting a non-existing organisation."""
        response = client.get(f"{ORGANISATION_ENDPOINT}/999999")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Organisation not found"
    
    def test_update_organisation_full(self):
        """Test updating all fields of an organisation."""
        create_response = client.put(ORGANISATION_ENDPOINT, json={
            "name": "Original Name",
            "details": "Original details"
        })
        created_id = create_response.json()["id"]
        
        update_response = client.put(f"{ORGANISATION_ENDPOINT}/{created_id}", json={
            "name": "Updated Name",
            "details": "Updated details",
            "tags": ["updated"],
            "url": "https://updated.com"
        })
        
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["id"] == created_id
        assert data["name"] == "Updated Name"
        assert data["details"] == "Updated details"
        assert data["tags"] == ["updated"]
        assert data["url"] == "https://updated.com"
    
    def test_update_organisation_partial(self):
        """Test partial update of an organisation."""
        create_response = client.put(ORGANISATION_ENDPOINT, json={
            "name": "Original",
            "details": "Original details",
            "tags": ["tag1"]
        })
        created_id = create_response.json()["id"]
        
        update_response = client.put(f"{ORGANISATION_ENDPOINT}/{created_id}", json={
            "name": "Updated Name Only"
        })
        
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["name"] == "Updated Name Only"
        assert data["details"] == "Original details"
        assert data["tags"] == ["tag1"]
    
    def test_update_organisation_not_found(self):
        """Test updating a non-existing organisation."""
        response = client.put(f"{ORGANISATION_ENDPOINT}/999999", json={
            "name": "Test"
        })
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Organisation not found"
    
    def test_delete_organisation(self):
        """Test deleting an organisation."""
        create_response = client.put(ORGANISATION_ENDPOINT, json={
            "name": "To Be Deleted"
        })
        created_id = create_response.json()["id"]
        
        delete_response = client.delete(f"{ORGANISATION_ENDPOINT}/{created_id}")
        
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Organisation deleted successfully"
        
        get_response = client.get(f"{ORGANISATION_ENDPOINT}/{created_id}")
        assert get_response.status_code == 404
    
    def test_delete_organisation_not_found(self):
        """Test deleting a non-existing organisation."""
        response = client.delete(f"{ORGANISATION_ENDPOINT}/999999")
        
        assert response.status_code == 204
    
    def test_organisation_lifecycle(self):
        """Test complete lifecycle: create, read, update, delete."""
        create_response = client.put(ORGANISATION_ENDPOINT, json={
            "name": "Lifecycle Test",
            "tags": ["test"]
        })
        assert create_response.status_code == 201
        org_id = create_response.json()["id"]
        
        get_response = client.get(f"{ORGANISATION_ENDPOINT}/{org_id}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "Lifecycle Test"
        
        update_response = client.put(f"{ORGANISATION_ENDPOINT}/{org_id}", json={
            "name": "Updated Lifecycle"
        })
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Lifecycle"
        
        delete_response = client.delete(f"{ORGANISATION_ENDPOINT}/{org_id}")
        assert delete_response.status_code == 200
        
        final_get_response = client.get(f"{ORGANISATION_ENDPOINT}/{org_id}")
        assert final_get_response.status_code == 404
    
    def test_tags_array_handling(self):
        """Test that tags are properly handled as arrays."""
        response = client.put(ORGANISATION_ENDPOINT, json={
            "name": "Tag Test",
            "tags": ["tag1", "tag2", "tag3"]
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["tags"] == ["tag1", "tag2", "tag3"]
        assert isinstance(data["tags"], list)
    
    def test_empty_tags_array(self):
        """Test handling of empty tags array."""
        response = client.put(ORGANISATION_ENDPOINT, json={
            "name": "Empty Tags",
            "tags": []
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["tags"] == []
