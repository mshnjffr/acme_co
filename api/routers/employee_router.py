from fastapi import APIRouter, Depends
from typing import List
from api.employee_schemas import EmployeeResponse
from api.dependencies import get_employee_service
from services.employee_service import EmployeeService

router = APIRouter(prefix="/employee", tags=["employees"])


@router.get("", response_model=List[EmployeeResponse])
def get_employees(
    service: EmployeeService = Depends(get_employee_service)
):
    employees = service.get_all_employees()
    return [employee.to_dict() for employee in employees]
