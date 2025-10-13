from typing import List, Optional
from repositories.base import IRepository
from models.entity import Organisation

class OrganisationService:
    def __init__(self, repository: IRepository[Organisation]):
        self._repository = repository
    
    def get_all_organisations(self) -> List[Organisation]:
        return self._repository.get_all()
    
    def get_organisation_by_id(self, id: int) -> Optional[Organisation]:
        return self._repository.get_by_id(id)
    
    def create_organisation(
        self,
        name: str,
        details: Optional[str] = None,
        tags: Optional[List[str]] = None,
        url: Optional[str] = None
    ) -> Organisation:
        organisation = Organisation(
            name=name,
            details=details,
            tags=tags or [],
            url=url
        )
        return self._repository.create(organisation)
    
    def update_organisation(
        self,
        id: int,
        name: Optional[str] = None,
        details: Optional[str] = None,
        tags: Optional[List[str]] = None,
        url: Optional[str] = None
    ) -> Optional[Organisation]:
        existing = self._repository.get_by_id(id)
        if not existing:
            return None
        
        updated_org = Organisation(
            name=name if name is not None else existing.name,
            details=details if details is not None else existing.details,
            tags=tags if tags is not None else existing.tags,
            url=url if url is not None else existing.url
        )
        
        return self._repository.update(id, updated_org)
    
    def delete_organisation(self, id: int) -> bool:
        return self._repository.delete(id)
