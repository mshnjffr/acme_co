from repositories.organisation_repository import OrganisationRepository
from services.organisation_service import OrganisationService

DB_PATH = "organisations.db"

def get_organisation_service() -> OrganisationService:
    repository = OrganisationRepository(DB_PATH)
    return OrganisationService(repository)
