from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="SecureCloud Demo API",
    description="A demo API for the SecureCloud DevOps and SRE platform.",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    status: str
    service: str


@app.get("/", tags=["General"])
def root() -> dict[str, str]:
    return {
        "message": "Welcome to SecureCloud Demo API",
        "version": "0.1.0",
    }


@app.get("/health/live", response_model=HealthResponse, tags=["Health"])
def liveness() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="securecloud-demo-api",
    )


@app.get("/health/ready", response_model=HealthResponse, tags=["Health"])
def readiness() -> HealthResponse:
    return HealthResponse(
        status="ready",
        service="securecloud-demo-api",
    )
