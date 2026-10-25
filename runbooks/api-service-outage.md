# Runbook 1: API Service Outage

## 1. Purpose

Provide a repeatable procedure to diagnose and recover the SecureCloud FastAPI service when health checks fail or the API becomes unavailable.

## 2. Scope

This runbook applies to the local Docker Compose observability environment.

- API service: `securecloud-demo-api`
- API base URL: `http://localhost:8001`
- Liveness endpoint: `/health/live`
- Readiness endpoint: `/health/ready`
- Metrics endpoint: `/metrics`

**Environment limitation:** These procedures are validated against the local Compose setup. AWS, Kubernetes, and production recovery procedures must be adapted and tested before use in those environments.

## 3. Symptoms

- The API does not respond on port `8001`.
- The liveness or readiness endpoint returns an error.
- Docker reports that the API container has exited or is repeatedly restarting.
- Prometheus reports the API scrape target as down.

## 4. Initial assessment

Run these commands from the repository root.

### Step 1: Check container status

```powershell
docker compose -f apps/demo-api/compose.yaml ps
```

Look for an exited, restarting, or unhealthy API container.

### Step 2: Check API liveness

```powershell
Invoke-RestMethod http://localhost:8001/health/live
```

Expected response:

```json
{
  "status": "ok"
}
```

### Step 3: Check API readiness

```powershell
Invoke-RestMethod http://localhost:8001/health/ready
```

Expected response:

```json
{
  "status": "ready"
}
```

### Step 4: Inspect API logs

```powershell
docker compose -f apps/demo-api/compose.yaml logs --tail 100 api
```

Look for startup failures, Python exceptions, configuration errors, and repeated restarts.

## 5. Troubleshooting decision process

### Case A: API container is stopped

1. Inspect the container status and recent logs.
2. Identify the reported startup or runtime failure.
3. Correct the underlying configuration or application issue.
4. Restart only the affected service:

```powershell
docker compose -f apps/demo-api/compose.yaml up -d api
```

5. Repeat the liveness and readiness checks.

### Case B: API is running but requests fail

1. Check the API logs for exceptions.
2. Confirm port `8001` is mapped correctly in Compose.
3. Validate the Compose configuration:

```powershell
docker compose -f apps/demo-api/compose.yaml config --quiet
```

4. Check liveness and readiness again.

### Case C: API works but Prometheus reports it as down

1. Open `http://localhost:9090/targets`.
2. Locate the API scrape target.
3. Inspect the target's error message and scrape URL.
4. Confirm the API metrics endpoint responds:

```powershell
Invoke-WebRequest http://localhost:8001/metrics -UseBasicParsing
```

5. Correct the scrape configuration or connectivity issue indicated by the evidence.

## 6. Recovery validation

After applying a fix, verify:

- [ ] The API container is running.
- [ ] `/health/live` returns `status: ok`.
- [ ] `/health/ready` returns `status: ready`.
- [ ] `/metrics` responds successfully.
- [ ] Prometheus reports the API target as `UP`.
- [ ] Recent API logs contain no recurring startup or runtime errors.

Do not declare recovery based solely on the container running; verify the application endpoints as well.

## 7. Escalation and evidence

If the service remains unavailable:

1. Preserve the relevant container logs and error messages.
2. Record the time the incident started and the affected endpoints.
3. Document the troubleshooting actions and their results.
4. Escalate unresolved application or infrastructure issues to the responsible engineer.

Avoid recording secrets, tokens, passwords, or sensitive request payloads in incident evidence.

## 8. Incident closure

Close the incident only after the recovery checks pass. Record the root cause, corrective action, and any follow-up work required to prevent recurrence.
