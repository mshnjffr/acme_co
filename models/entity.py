from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Organisation:
    name: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    details: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    url: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'details': self.details,
            'tags': self.tags,
            'url': self.url
        }
