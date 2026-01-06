from fastapi import FastAPI
from api.routers import organisation_router, employee_router, health_router

API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

app = FastAPI(title="Organisation API", version="2.0.0")

app.include_router(organisation_router, prefix=API_PREFIX)
app.include_router(employee_router, prefix=API_PREFIX)
app.include_router(health_router, prefix=API_PREFIX)


@app.get("/")
def root():
    return {
        "message": "Organisation API",
        "version": "2.0.0",
        "api_version": API_VERSION,
        "endpoints": {
            "health": f"GET {API_PREFIX}/health",
            "docs": "GET /docs",
            "organisations": {
                "list": f"GET {API_PREFIX}/organisation",
                "get": f"GET {API_PREFIX}/organisation/{{id}}",
                "create": f"PUT {API_PREFIX}/organisation",
                "update": f"PUT {API_PREFIX}/organisation/{{id}}",
                "delete": f"DELETE {API_PREFIX}/organisation/{{id}}"
            },
            "employees": {
                "list": f"GET {API_PREFIX}/employee"
            }
        }
    }
