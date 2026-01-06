from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import organisation_router, employee_router, health_router
from api.config import APP_VERSION, API_VERSION, API_PREFIX

app = FastAPI(title="Organisation API", version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(organisation_router, prefix=API_PREFIX)
app.include_router(employee_router, prefix=API_PREFIX)
app.include_router(health_router, prefix=API_PREFIX)


@app.get("/")
def root():
    return {
        "message": "Organisation API",
        "service_version": APP_VERSION,
        "api_version": API_VERSION,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }
