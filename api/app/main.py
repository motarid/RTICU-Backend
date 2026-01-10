from app.api.routers import hypoxemia
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def swagger_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "rticu")
    correct_password = secrets.compare_digest(credentials.password, "secure123")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

app = FastAPI(
    title="RTICU Clinical API",
    description="RTICU secure clinical API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)


    Clinical decision support APIs for:
    - ICU respiratory workflows
    - Ventilator logic
    - ABG interpretation
    - AI-driven respiratory tools

    Maintained by RTICU Team.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui(credentials: HTTPBasicCredentials = Depends(swagger_auth)):
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="RTICU Secure Docs"
    )
    
