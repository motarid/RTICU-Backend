from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
import secrets

# ===============================
# Security (Swagger Auth)
# ===============================
security = HTTPBasic()

SWAGGER_USERNAME = "admin"
SWAGGER_PASSWORD = "rticu123"

def swagger_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, SWAGGER_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, SWAGGER_PASSWORD
    )

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


# ===============================
# FastAPI App (Swagger Disabled)
# ===============================
app = FastAPI(
    title="RTICU Clinical API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)


# ===============================
# Routers Import
# ===============================
from app.api.routers import health, patients, hypoxemia


# ===============================
# Routers Registration
# ===============================
app.include_router(
    health.router,
    tags=["Health"]
)

app.include_router(
    patients.router,
    tags=["Patients"]
)

app.include_router(
    hypoxemia.router,
    prefix="/clinical",
    tags=["Hypoxemia & ARDS"]
)


# ===============================
# Secure OpenAPI JSON
# ===============================
@app.get("/openapi.json", include_in_schema=False)
def openapi_json(auth: bool = Depends(swagger_auth)):
    return JSONResponse(app.openapi())


# ===============================
# Secure Swagger UI
# ===============================
@app.get("/docs", include_in_schema=False)
def secure_swagger(auth: bool = Depends(swagger_auth)):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="RTICU Secure API Docs"
    )
