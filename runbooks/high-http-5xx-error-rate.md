# Runbook 2: High HTTP 5xx Error Rate

## 1. Purpose

Provide a consistent procedure for investigating elevated HTTP 5xx responses from the SecureCloud FastAPI service.

## 2. Scope

This runbook applies to the local Docker Compose environment.

- API: `http://localhost:8001`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- Loki: `http://localhost:3100`

This procedure covers local diagnostics. Production incident-response processes must be adapted and tested before operational use.

## 3. Symptoms

- The Prometheus high-5xx alert becomes active.
- Grafana shows an increase in server-error responses.
- Users receive HTTP 500–599 responses.
- API logs contain repeated server-side errors.

## 4. Initial assessment

### Step 1: Check API availability

```powershell
Invoke-RestMethod http://localhost:8001/health/live
Invoke-RestMethod http://localhost:8001/health/ready
```

If the service is unavailable, follow `api-service-outage.md`.

### Step 2: Inspect API container logs

```powershell
docker compose -f apps/demo-api/compose.yaml logs --tail 200 api
```

Look for Python exceptions, failed dependencies, configuration problems, and repeated errors around the incident time.

### Step 3: Inspect Prometheus

Open `http://localhost:9090/alerts` and inspect the high-5xx alert.

In the Prometheus query interface, inspect the available HTTP request counter:

```promql
http_requests_total
```

Check the actual metric labels before constructing a filtered query. If the application exposes a `status_code` label, a possible error-rate query is:

```promql
sum(rate(http_requests_total{status_code=~"5.."}[5m]))
/
clamp_min(sum(rate(http_requests_total[5m])), 1)
```

**Metric verification:** Use this query only if `http_requests_total` and its `status_code` label match the running application's `/metrics` output. Otherwise, adapt the query to the actual metric name and labels.

## 5. Investigate structured logs

Open Grafana at `http://localhost:3000`, navigate to Explore, and select the Loki data source.

Start with:

```logql
{project="securecloud", container="securecloud-demo-api"}
```

Narrow the search to the relevant incident period and inspect:

- `request_id`
- `http_method`
- `http_path`
- `http_status_code`
- `duration_ms`

Use the request ID to correlate log entries for a specific request when available. Do not assume that every failure produces a Python exception; inspect the recorded status code as well.

## 6. Troubleshooting decision process

### Case A: A specific endpoint returns 5xx responses

1. Identify the affected path and HTTP method.
2. Correlate the request with structured logs.
3. Inspect the relevant exception or application code path.
4. Reproduce the failure locally if safe.
5. Correct the underlying cause and run the relevant tests.

### Case B: Errors occur across multiple endpoints

1. Check container health and startup logs.
2. Inspect recent application or configuration changes.
3. Check whether shared application components are failing.
4. Review available resource and dependency evidence.
5. Avoid restarting services repeatedly without collecting diagnostic evidence.

### Case C: The alert fires but no corresponding logs appear

1. Confirm the Loki data source is healthy.
2. Verify that Alloy is running.
3. Inspect Alloy logs for discovery or delivery errors.
4. Confirm the API container is included in log collection.
5. Follow `missing-logs-in-loki.md` once that runbook is available.

## 7. Recovery validation

- [ ] API liveness and readiness checks pass.
- [ ] The identified failure has been corrected.
- [ ] Relevant automated tests pass.
- [ ] The observed error rate returns to its expected baseline.
- [ ] Prometheus alert state is checked after the evaluation window.
- [ ] Logs show successful requests and no recurring instances of the identified failure.

Do not declare recovery solely because an alert is inactive; verify API behavior and relevant metrics.

## 8. Escalation and incident evidence

Record the incident start and end times, affected endpoints, representative request IDs, relevant error messages, root cause, corrective action, and follow-up tasks.

Remove or redact secrets and sensitive request data before sharing evidence.

## 9. Incident closure

Close the incident after the recovery checks pass. Document prevention measures such as regression tests, improved validation, or additional monitoring where appropriate.
