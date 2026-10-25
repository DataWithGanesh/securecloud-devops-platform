# Runbook 3: High API Latency

## 1. Purpose

Provide a repeatable procedure for diagnosing elevated response latency in the SecureCloud FastAPI service.

## 2. Scope

This runbook applies to the local Docker Compose environment.

- API: `http://localhost:8001`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- API metrics: `http://localhost:8001/metrics`

AWS and Kubernetes production environments are outside the validated scope of this procedure.

## 3. Symptoms

- The high-P95-latency alert becomes active.
- The API responds successfully but takes longer than expected.
- Grafana shows increasing request duration.
- Structured logs contain elevated `duration_ms` values.

## 4. Initial assessment

### Step 1: Check API health

```powershell
Invoke-RestMethod http://localhost:8001/health/live
Invoke-RestMethod http://localhost:8001/health/ready
```

If either check fails, follow `api-service-outage.md`.

### Step 2: Inspect the latency alert

Open `http://localhost:9090/alerts` and inspect the high-P95-latency alert.

Review the alert expression and configured threshold before interpreting its state.

### Step 3: Inspect available metrics

Open `http://localhost:8001/metrics` or run:

```powershell
Invoke-WebRequest http://localhost:8001/metrics -UseBasicParsing
```

Identify the actual request-duration histogram and its bucket labels.

For a histogram named `http_request_duration_seconds`, a typical P95 query is:

```promql
histogram_quantile(
  0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

**Metric verification:** Use this query only if the histogram and bucket series exist under those names. Otherwise, adapt it to the metric exposed by the application.

## 5. Investigate request latency

Open Grafana at `http://localhost:3000` and review the SecureCloud API dashboard.

In Grafana Explore, query the API logs in Loki:

```logql
{project="securecloud", container="securecloud-demo-api"}
```

Inspect these fields where available:

- `http_method`
- `http_path`
- `http_status_code`
- `duration_ms`
- `request_id`

Look for endpoints with consistently elevated durations and compare slow requests with normal requests.

## 6. Troubleshooting decision process

### Case A: One endpoint is slow

1. Identify the affected path and method.
2. Compare the duration of multiple requests to that endpoint.
3. Inspect application logs and the relevant code path.
4. Reproduce the issue locally if safe.
5. Add or run tests for the suspected cause.

### Case B: Multiple endpoints are slow

1. Check container status and recent API logs.
2. Review available CPU, memory, and container-resource evidence.
3. Check whether the slowdown coincides with application changes or repeated errors.
4. Investigate shared code paths and dependencies.
5. Change one suspected cause at a time and measure the result.

### Case C: The latency alert fires but metrics are missing

1. Confirm that the API metrics endpoint responds.
2. Open `http://localhost:9090/targets`.
3. Verify that the API scrape target is `UP`.
4. Inspect the actual histogram name and labels.
5. Follow `missing-prometheus-metrics.md` once that runbook is available.

## 7. Recovery validation

- [ ] Liveness and readiness checks pass.
- [ ] The suspected latency cause has been addressed.
- [ ] Relevant automated tests pass.
- [ ] Latency metrics return to an acceptable baseline.
- [ ] The alert is checked after its evaluation window.
- [ ] Logs no longer show the same pattern of slow requests.

Do not declare recovery solely because the alert becomes inactive. Verify the measured latency and application behavior.

## 8. Escalation and evidence

Record the incident period, affected endpoints, observed latency, relevant request IDs, diagnostic findings, corrective action, and any remaining risks.

Redact credentials, tokens, and sensitive request data from shared evidence.

## 9. Incident closure

Close the incident after the recovery checks pass. Record any follow-up work, such as performance tests, regression tests, or additional instrumentation.
