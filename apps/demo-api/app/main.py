
import json
import logging
import re
import sys
import time
import uuid
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


SERVICE_NAME = "securecloud-demo-api"
SERVICE_VERSION = "0.1.0"

request_id_context: ContextVar[str] = ContextVar(
    "request_id",
    default="-",
)

HTTP_REQUESTS_TOTAL = Counter(
    "securecloud_http_requests_total",
    "Total number of completed HTTP requests.",
    ["method", "path", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "securecloud_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ["method", "path"],
)


class JsonFormatter(logging.Formatter):
    """Format application logs as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": SERVICE_NAME,
            "message": record.getMessage(),
            "request_id": getattr(
                record,
                "request_id",
                request_id_context.get(),
            ),
        }

        for field in (
            "http_method",
            "http_path",
            "http_status_code",
            "duration_ms",
        ):
            if hasattr(record, field):
                log_entry[field] = getattr(record, field)

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)


logger = logging.getLogger("securecloud")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)


class RequestContextFilter(logging.Filter):
    """Attach the current request ID to log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = request_id_context.get()
        return True


logger.addFilter(RequestContextFilter())


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Track request IDs, latency, metrics, and request logs."""

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        supplied_id = request.headers.get("X-Request-ID", "")

        if re.fullmatch(r"[A-Za-z0-9._-]{1,64}", supplied_id):
            request_id = supplied_id
        else:
            request_id = str(uuid.uuid4())

        context_token = request_id_context.set(request_id)
        started_at = time.perf_counter()

        try:
            response = await call_next(request)
            duration_seconds = time.perf_counter() - started_at
            duration_ms = round(duration_seconds * 1000, 2)

            response.headers["X-Request-ID"] = request_id

            # Exclude /metrics to avoid monitoring traffic inflating
            # application request metrics.
            if request.url.path != "/metrics":
                HTTP_REQUESTS_TOTAL.labels(
                    method=request.method,
                    path=request.url.path,
                    status_code=str(response.status_code),
                ).inc()

                HTTP_REQUEST_DURATION_SECONDS.labels(
                    method=request.method,
                    path=request.url.path,
                ).observe(duration_seconds)

            logger.info(
                "http_request_completed",
                extra={
                    "request_id": request_id,
                    "http_method": request.method,
                    "http_path": request.url.path,
                    "http_status_code": response.status_code,
                    "duration_ms": duration_ms,
                },
            )

            return response

        except Exception:
            duration_seconds = time.perf_counter() - started_at
            duration_ms = round(duration_seconds * 1000, 2)

            # Record unexpected application failures as HTTP 500s.
            if request.url.path != "/metrics":
                HTTP_REQUESTS_TOTAL.labels(
                    method=request.method,
                    path=request.url.path,
                    status_code="500",
                ).inc()

                HTTP_REQUEST_DURATION_SECONDS.labels(
                    method=request.method,
                    path=request.url.path,
                ).observe(duration_seconds)

            logger.exception(
                "http_request_failed",
                extra={
                    "request_id": request_id,
                    "http_method": request.method,
                    "http_path": request.url.path,
                    "http_status_code": 500,
                    "duration_ms": duration_ms,
                },
            )
            raise

        finally:
            request_id_context.reset(context_token)


app = FastAPI(
    title="SecureCloud Demo API",
    description="A demo API for the SecureCloud DevOps and SRE platform.",
    version=SERVICE_VERSION,
)

app.add_middleware(RequestLoggingMiddleware)


class HealthResponse(BaseModel):
    status: str
    service: str


@app.get("/", tags=["General"])
def root() -> dict[str, str]:
    return {
        "message": "Welcome to SecureCloud Demo API",
        "version": SERVICE_VERSION,
    }


@app.get("/health/live", response_model=HealthResponse, tags=["Health"])
def liveness() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=SERVICE_NAME,
    )


@app.get("/health/ready", response_model=HealthResponse, tags=["Health"])
def readiness() -> HealthResponse:
    return HealthResponse(
        status="ready",
        service=SERVICE_NAME,
    )


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
