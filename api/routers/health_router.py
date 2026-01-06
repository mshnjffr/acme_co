from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health_check():
    return {
        "status": "healthy",
        "service": "Organisation API",
        "version": "2.0.0"
    }
