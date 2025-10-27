from datetime import date
from repositories.employee_repository import EmployeeRepository
from services.employee_service import EmployeeService

DB_PATH = "organisations.db"

def seed_employees():
    repository = EmployeeRepository(DB_PATH)
    service = EmployeeService(repository)
    
    sample_employees = [
        {
            "name": "John",
            "last_name": "Doe",
            "age": 32,
            "date_of_birth": date(1992, 5, 15),
            "location": "New York",
            "organisation_id": 1
        },
        {
            "name": "Sarah",
            "last_name": "Johnson",
            "age": 28,
            "date_of_birth": date(1996, 8, 22),
            "location": "San Francisco",
            "organisation_id": 1
        },
        {
            "name": "Michael",
            "last_name": "Chen",
            "age": 35,
            "date_of_birth": date(1989, 11, 3),
            "location": "Seattle",
            "organisation_id": 2
        },
        {
            "name": "Emma",
            "last_name": "Williams",
            "age": 29,
            "date_of_birth": date(1995, 3, 18),
            "location": "Boston",
            "organisation_id": 3
        },
        {
            "name": "David",
            "last_name": "Martinez",
            "age": 41,
            "date_of_birth": date(1983, 7, 9),
            "location": "Austin",
            "organisation_id": 4
        }
    ]
    
    for employee_data in sample_employees:
        service.create_employee(**employee_data)
    
    print(f"Successfully seeded {len(sample_employees)} employees!")

if __name__ == "__main__":
    seed_employees()
