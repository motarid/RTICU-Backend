from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
import secrets

# =========================
# Security
# =========================
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


# =========================
# FastAPI App
# =========================
app = FastAPI(
    title="RTICU Clinical API",
    version="1.0.0",
    docs_url=None,     # ⛔ تعطيل Swagger الافتراضي
    redoc_url=None
)


# =========================
# Secure Swagger Endpoint
# =========================
@app.get("/docs", include_in_schema=False)
def secure_docs(_: bool = Depends(swagger_auth)):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="RTICU Secure API Docs"
    )


# =========================
# Basic Test Endpoints
# =========================
@app.get("/")
def root():
    return {"status": "RTICU API running"}


@app.get("/health")
def health():
    return {"status": "ok"}
