from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime, date

class EmployeeBase(BaseModel):
    name: str
    last_name: str
    age: int
    date_of_birth: date
    location: str
    organisation_id: int

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    date_of_birth: Optional[date] = None
    location: Optional[str] = None
    organisation_id: Optional[int] = None

class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
