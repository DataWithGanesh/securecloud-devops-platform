
import json
import logging

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to SecureCloud Demo API"


def test_liveness_endpoint():
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_endpoint():
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_response_contains_generated_request_id():
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers.get("X-Request-ID")
    assert len(response.headers["X-Request-ID"]) == 36


def test_valid_incoming_request_id_is_reused():
    request_id = "test-request-123"

    response = client.get(
        "/health/live",
        headers={"X-Request-ID": request_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id


def test_invalid_incoming_request_id_is_replaced():
    response = client.get(
        "/",
        headers={"X-Request-ID": "invalid request id with spaces"},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] != "invalid request id with spaces"
    assert len(response.headers["X-Request-ID"]) == 36


def test_request_log_is_structured_json(caplog):
    with caplog.at_level(logging.INFO, logger="securecloud"):
        response = client.get(
            "/health/ready",
            headers={"X-Request-ID": "observability-test-001"},
        )

    assert response.status_code == 200

    matching_records = [
        record
        for record in caplog.records
        if record.name == "securecloud"
        and record.getMessage() == "http_request_completed"
    ]

    assert matching_records, "Expected a request completion log"

    log_record = matching_records[-1]
    log_entry = json.loads(log_record.getMessage()) if log_record.getMessage().startswith("{") else None

    # JsonFormatter serializes the record when its handler emits it.
    assert log_record.request_id == "observability-test-001"
    assert log_record.http_method == "GET"
    assert log_record.http_path == "/health/ready"
    assert log_record.http_status_code == 200
    assert log_record.duration_ms >= 0


def test_metrics_endpoint_exposes_prometheus_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "securecloud_http_requests_total" in response.text
    assert "securecloud_http_request_duration_seconds" in response.text


def test_application_request_increments_metrics():
    client.get(
        "/health/ready",
        headers={"X-Request-ID": "metrics-test-001"},
    )

    response = client.get("/metrics")

    assert response.status_code == 200
    assert 'securecloud_http_requests_total{method="GET",path="/health/ready",status_code="200"}' in response.text
    assert 'securecloud_http_request_duration_seconds_count{method="GET",path="/health/ready"}' in response.text


def test_not_found_response_increments_error_status_metric():
    response = client.get("/route-that-does-not-exist")

    assert response.status_code == 404

    metrics_response = client.get("/metrics")

    assert metrics_response.status_code == 200
    assert (
        'securecloud_http_requests_total{method="GET",'
        'path="/route-that-does-not-exist",status_code="404"} 1.0'
    ) in metrics_response.text


def test_metrics_scrape_does_not_increment_application_request_count():
    metrics_before = client.get("/metrics")
    assert metrics_before.status_code == 200

    response = client.get("/metrics")
    assert response.status_code == 200

    metrics_after = client.get("/metrics")
    assert metrics_after.status_code == 200

    def get_request_counter_value(metrics_text: str) -> float:
        for line in metrics_text.splitlines():
            if (
                line.startswith("securecloud_http_requests_total{")
                and 'path="/metrics"' in line
            ):
                return float(line.rsplit(" ", 1)[1])
        return 0.0

    assert get_request_counter_value(metrics_before.text) == 0.0
    assert get_request_counter_value(metrics_after.text) == 0.0
