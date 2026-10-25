# Runbook 4: Missing Prometheus Metrics

## 1. Purpose

Provide a repeatable procedure for diagnosing missing SecureCloud API metrics in Prometheus.

## 2. Scope

This runbook applies to the local Docker Compose observability stack.

- API metrics endpoint: `http://localhost:8001/metrics`
- Prometheus UI: `http://localhost:9090`
- Prometheus targets: `http://localhost:9090/targets`
- Prometheus alerts: `http://localhost:9090/alerts`

Live AWS and Kubernetes monitoring are outside the validated scope of this procedure.

## 3. Symptoms

- API metrics are missing from Prometheus queries.
- The API scrape target is down.
- Grafana panels show no data.
- A monitoring alert indicates that the API is unavailable or its metrics are missing.

## 4. Initial assessment

### Step 1: Verify the API metrics endpoint

```powershell
Invoke-WebRequest http://localhost:8001/metrics -UseBasicParsing
```

Confirm that the endpoint responds successfully and includes the expected metric names.

### Step 2: Inspect Prometheus targets

Open `http://localhost:9090/targets`.

1. Locate the API target.
2. Check whether its state is `UP` or `DOWN`.
3. If it is down, inspect the last scrape error and scrape URL.
4. Confirm that the configured target address matches the Docker Compose network and service configuration.

### Step 3: Query a known metric

In the Prometheus expression browser, query a metric that actually appears in the API's `/metrics` output.

For example, use `http_requests_total` only if that exact metric exists.

If a metric exists at the API endpoint but not in Prometheus, investigate scraping and target configuration before changing application instrumentation.

## 5. Troubleshooting decision process

### Case A: The API metrics endpoint fails

1. Check API container status:

```powershell
docker compose -f apps/demo-api/compose.yaml ps
```

2. Inspect API logs:

```powershell
docker compose -f apps/demo-api/compose.yaml logs --tail 100 api
```

3. Check the API health endpoints.
4. Correct any application startup or runtime error.
5. Retry the metrics request.

If the API is unavailable, follow `api-service-outage.md`.

### Case B: The API endpoint works but the Prometheus target is down

1. Open the targets page and capture the scrape error.
2. Inspect the Prometheus scrape configuration.
3. Confirm the target hostname, port, and metrics path.
4. Verify that Prometheus can reach the API service over the Compose network.
5. Validate the Compose configuration:

```powershell
docker compose -f apps/demo-api/compose.yaml config --quiet
```

6. Apply a correction only after identifying the cause, then recheck the target.

### Case C: The target is up but a query returns no data

1. Verify the exact metric name in `/metrics`.
2. Inspect the metric's available labels.
3. Remove filters temporarily to determine whether the label selector is too restrictive.
4. Check whether the application has received requests that would produce the metric.
5. Confirm that the selected time range includes recent samples.

A missing time series does not always mean that Prometheus scraping is broken.

### Case D: Grafana shows no data but Prometheus has metrics

1. Run the same query in Prometheus.
2. Confirm that Grafana uses the intended Prometheus data source.
3. Inspect dashboard query expressions and label filters.
4. Check the dashboard time range.
5. Correct the query or data-source configuration as indicated by the evidence.

## 6. Recovery validation

- [ ] The API `/metrics` endpoint responds successfully.
- [ ] The API target is `UP` in Prometheus.
- [ ] A known metric returns data in Prometheus.
- [ ] Relevant Grafana panels display data when their queries are valid.
- [ ] No recurring scrape errors remain.

Do not declare recovery solely because the target is `UP`; confirm that the expected metrics are queryable.

## 7. Escalation and evidence

Record the affected metric names, scrape URL, target state, error message, diagnostic steps, and corrective action.

Do not include secrets or sensitive request data in shared evidence.

## 8. Incident closure

Close the incident after the recovery checks pass. Document any follow-up work, including instrumentation changes, scrape-configuration corrections, or dashboard improvements.
