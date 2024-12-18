from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from .database import engine
from .models import Base
from .routers import plans
from .routers import permissions
from .routers import subscriptions
from .routers import access_control
from .routers import usage_tracking
from .routers import auth
from .routers import cloud_services
from fastapi.openapi.utils import get_openapi


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the router
app.include_router(plans.router, prefix="/api", tags=["Subscription Plans"])

app.include_router(permissions.router, prefix="/api", tags=["Permissions"])

app.include_router(subscriptions.router, prefix="/api", tags=["User Subscriptions"])

app.include_router(access_control.router, prefix="/api", tags=["Access Control"])

app.include_router(usage_tracking.router, prefix="/api", tags=["Usage Tracking"])

app.include_router(auth.router, prefix="/api", tags=["Authentication"])

app.include_router(cloud_services.router, prefix="/api", tags=["Cloud Services"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Cloud Service Access Management System",
        version="1.0.0",
        description="This is a project for managing cloud service access based on subscription plans.",
        routes=app.routes,
    )
    # Define the security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Apply security globally
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {"message": "Welcome to the Cloud Service Access Management System"}


