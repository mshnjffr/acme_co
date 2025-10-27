from repositories.organisation_repository import OrganisationRepository
from repositories.employee_repository import EmployeeRepository
from services.organisation_service import OrganisationService
from services.employee_service import EmployeeService

DB_PATH = "organisations.db"

def get_organisation_service() -> OrganisationService:
    repository = OrganisationRepository(DB_PATH)
    return OrganisationService(repository)

def get_employee_service() -> EmployeeService:
    repository = EmployeeRepository(DB_PATH)
    return EmployeeService(repository)
