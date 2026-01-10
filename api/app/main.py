from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
import secrets

# Routers
from app.api.routers import health, patients
# لاحقًا: from app.api.routers import hypoxemia

# =========================
# Security (Swagger Login)
# =========================
security = HTTPBasic()

SWAGGER_USERNAME = "admin"
SWAGGER_PASSWORD = "rticu123"


def swagger_auth(
    credentials: HTTPBasicCredentials = Depends(security),
):
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
    description="Secure ICU Clinical Decision Support API",
    version="1.0.0",
    docs_url=None,   # ❌ disable default docs
    redoc_url=None   # ❌ disable default redoc
)

# =========================
# CORS (optional but safe)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Routers Registration ✅
# =========================
app.include_router(health.router, tags=["Health"])
app.include_router(patients.router, tags=["Patients"])
# لاحقًا:
# app.include_router(hypoxemia.router, prefix="/clinical", tags=["Hypoxemia & ARDS"])


# =========================
# Protected Swagger Docs 🔐
# =========================
@app.get("/docs", include_in_schema=False)
def secure_docs(auth: bool = Depends(swagger_auth)):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="RTICU Secure API Docs",
    )
