# Runbook 5: Missing Logs in Loki

## 1. Purpose

Provide a repeatable procedure for diagnosing missing SecureCloud container logs in Loki and Grafana Explore.

## 2. Scope

This runbook applies to the local Docker Compose observability environment.

- Docker Compose: `apps/demo-api/compose.yaml`
- Grafana: `http://localhost:3000`
- Loki: `http://localhost:3100`
- Loki readiness endpoint: `http://localhost:3100/ready`
- Alloy configuration: `observability/alloy/config.alloy`

AWS and Kubernetes log collection are outside the validated scope of this procedure.

## 3. Symptoms

- Grafana Explore returns no logs for the API container.
- New API log entries do not appear in Loki.
- Alloy reports discovery, processing, or delivery errors.
- Loki is unavailable or reports that it is not ready.

## 4. Initial assessment

### Step 1: Check observability containers

```powershell
docker compose -f apps/demo-api/compose.yaml ps
```

Confirm that the API, Alloy, and Loki containers are running.

### Step 2: Check Loki readiness

```powershell
Invoke-WebRequest http://localhost:3100/ready -UseBasicParsing
```

If Loki is not ready, inspect its logs before investigating the rest of the pipeline.

```powershell
docker compose -f apps/demo-api/compose.yaml logs --tail 100 loki
```

### Step 3: Inspect Alloy logs

```powershell
docker compose -f apps/demo-api/compose.yaml logs --tail 150 alloy
```

Look for container-discovery errors, configuration failures, connection errors, and failed log delivery.

### Step 4: Confirm that the API is generating logs

```powershell
docker compose -f apps/demo-api/compose.yaml logs --tail 50 api
```

If the API is unavailable, follow `api-service-outage.md`.

## 5. Troubleshooting decision process

### Case A: Loki is not ready

1. Inspect Loki logs and the readiness response.
2. Check for startup errors and ingester initialization issues.
3. Allow the configured startup and readiness period to complete.
4. Confirm readiness again before testing log queries.

Do not treat a brief startup delay as a persistent failure without checking the current state.

### Case B: Alloy is stopped or reporting errors

1. Check the Alloy container state.
2. Inspect the Alloy logs for configuration or delivery errors.
3. Review `observability/alloy/config.alloy`.
4. Confirm that the configured Loki endpoint is reachable from the Compose network.
5. Validate the Compose configuration:

```powershell
docker compose -f apps/demo-api/compose.yaml config --quiet
```

6. Correct the identified issue and recheck Alloy logs.

### Case C: API logs exist but are missing from Loki

1. Confirm that the API container is running and generating logs.
2. Inspect Alloy's container-discovery and filtering configuration.
3. Verify that the API container is included by the configured discovery filters.
4. Confirm that Alloy sends logs to the expected Loki push endpoint.
5. Check Loki readiness and Alloy delivery errors.
6. Retry the query in Grafana Explore after correcting the issue.

### Case D: Logs exist in Loki but Grafana Explore returns no results

Open Grafana at `http://localhost:3000`, navigate to Explore, and select the Loki data source.

Start with this query:

```logql
{project="securecloud"}
```

Then narrow the search to the API container:

```logql
{project="securecloud", container="securecloud-demo-api"}
```

If the queries return no results:

1. Confirm that the Loki data source points to the expected Loki service.
2. Check the selected time range.
3. Inspect the actual labels attached to ingested log streams.
4. Adapt the query to match the labels that exist.
5. Check whether the selected time range includes recently ingested logs.

## 6. Recovery validation

- [ ] API container logs are being generated.
- [ ] Alloy is running without recurring configuration or delivery errors.
- [ ] Loki's readiness endpoint succeeds.
- [ ] The broad Loki query returns expected log entries.
- [ ] The API-specific query returns API log entries.
- [ ] Recent structured entries include fields such as `request_id`, `http_method`, `http_path`, `http_status_code`, and `duration_ms` when those fields are emitted by the application.

Do not declare recovery solely because all containers are running. Confirm that recent API logs can be queried from Loki.

## 7. Escalation and evidence

Record the incident period, affected container, Loki readiness result, relevant Alloy and Loki errors, query used, corrective action, and recovery evidence.

Redact credentials, tokens, and sensitive request data before sharing logs.

## 8. Incident closure

Close the incident after the recovery checks pass. Record any follow-up work needed to improve log collection reliability, configuration validation, or alerting.
