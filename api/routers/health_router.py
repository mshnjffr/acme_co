from fastapi import APIRouter
from api.config import APP_VERSION, API_VERSION

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    return {
        "status": "healthy",
        "service": "Organisation API",
        "service_version": APP_VERSION,
        "api_version": API_VERSION
    }
