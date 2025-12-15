from fastapi import FastAPI, HTTPException, Depends
from typing import List
from api.schemas import OrganisationCreate, OrganisationUpdate, OrganisationResponse
from api.employee_schemas import EmployeeResponse
from api.dependencies import get_organisation_service, get_employee_service
from services.organisation_service import OrganisationService
from services.employee_service import EmployeeService

app = FastAPI(title="Organisation API", version="2.0.0")

@app.get("/")
def root():
    return {
        "message": "Organisation API",
        "version": "2.0.0",
        "endpoints": {
            "health": "GET /health",
            "docs": "GET /docs",
            "organisations": {
                "list": "GET /organisation",
                "get": "GET /organisation/{id}",
                "create": "PUT /organisation",
                "update": "PUT /organisation/{id}",
                "delete": "DELETE /organisation/{id}"
            },
            "employees": {
                "list": "GET /employee"
            }
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Organisation API",
        "version": "2.0.0"
    }

@app.get("/organisation", response_model=List[OrganisationResponse])
def get_organisations(
    service: OrganisationService = Depends(get_organisation_service)
):
    organisations = service.get_all_organisations()
    return [org.to_dict() for org in organisations]

@app.get("/organisation/{id}", response_model=OrganisationResponse)
def get_organisation(
    id: int,
    service: OrganisationService = Depends(get_organisation_service)
):
    org = service.get_organisation_by_id(id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return org.to_dict()

@app.put("/organisation", response_model=OrganisationResponse, status_code=201)
def create_organisation(
    org: OrganisationCreate,
    service: OrganisationService = Depends(get_organisation_service)
):
    created_org = service.create_organisation(
        name=org.name,
        details=org.details,
        tags=org.tags,
        url=org.url
    )
    return created_org.to_dict()

@app.put("/organisation/{id}", response_model=OrganisationResponse)
def update_organisation(
    id: int,
    org: OrganisationUpdate,
    service: OrganisationService = Depends(get_organisation_service)
):
    updated_org = service.update_organisation(
        id=id,
        name=org.name,
        details=org.details,
        tags=org.tags,
        url=org.url
    )
    if not updated_org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return updated_org.to_dict()

@app.delete("/organisation/{id}")
def delete_organisation(
    id: int,
    service: OrganisationService = Depends(get_organisation_service)
):
    deleted = service.delete_organisation(id)
    if not deleted:
        raise HTTPException(status_code=204, detail="Organisation not found")
    return {"message": "Organisation deleted successfully"}

@app.get("/employee", response_model=List[EmployeeResponse])
def get_employees(
    service: EmployeeService = Depends(get_employee_service)
):
    employees = service.get_all_employees()
    return [employee.to_dict() for employee in employees]
