from typing import List, Optional
from datetime import date
from repositories.base import IRepository
from models.employee import Employee

class EmployeeService:
    def __init__(self, repository: IRepository[Employee]):
        self._repository = repository
    
    def get_all_employees(self) -> List[Employee]:
        return self._repository.get_all()
    
    def get_employee_by_id(self, id: int) -> Optional[Employee]:
        return self._repository.get_by_id(id)
    
    def create_employee(
        self,
        name: str,
        last_name: str,
        age: int,
        date_of_birth: date,
        location: str,
        organisation_id: int
    ) -> Employee:
        employee = Employee(
            name=name,
            last_name=last_name,
            age=age,
            date_of_birth=date_of_birth,
            location=location,
            organisation_id=organisation_id
        )
        return self._repository.create(employee)
    
    def update_employee(
        self,
        id: int,
        name: Optional[str] = None,
        last_name: Optional[str] = None,
        age: Optional[int] = None,
        date_of_birth: Optional[date] = None,
        location: Optional[str] = None,
        organisation_id: Optional[int] = None
    ) -> Optional[Employee]:
        existing = self._repository.get_by_id(id)
        if not existing:
            return None
        
        updated_employee = Employee(
            name=name if name is not None else existing.name,
            last_name=last_name if last_name is not None else existing.last_name,
            age=age if age is not None else existing.age,
            date_of_birth=date_of_birth if date_of_birth is not None else existing.date_of_birth,
            location=location if location is not None else existing.location,
            organisation_id=organisation_id if organisation_id is not None else existing.organisation_id
        )
        
        return self._repository.update(id, updated_employee)
    
    def delete_employee(self, id: int) -> bool:
        return self._repository.delete(id)
