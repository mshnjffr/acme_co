from .organisation_router import router as organisation_router
from .employee_router import router as employee_router
from .health_router import router as health_router

__all__ = ["organisation_router", "employee_router", "health_router"]
