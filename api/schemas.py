from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime

class OrganisationBase(BaseModel):
    name: str
    details: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    url: Optional[str] = None

class OrganisationCreate(OrganisationBase):
    pass

class OrganisationUpdate(BaseModel):
    name: Optional[str] = None
    details: Optional[str] = None
    tags: Optional[List[str]] = None
    url: Optional[str] = None

class OrganisationResponse(OrganisationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
