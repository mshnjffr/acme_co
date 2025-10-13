from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar

T = TypeVar('T')

class IRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, id: int, entity: T) -> Optional[T]:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
