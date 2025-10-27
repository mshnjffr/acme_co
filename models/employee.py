from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional

@dataclass
class Employee:
    name: str
    last_name: str
    age: int
    date_of_birth: date
    location: str
    organisation_id: int
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'age': self.age,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'location': self.location,
            'organisation_id': self.organisation_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
