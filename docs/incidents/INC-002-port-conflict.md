# INC-002 — Docker Port Conflict and API Routing Failure

**Project:** AWS Systems Engineering Lab  
**Date:** October 11, 2026  
**Severity:** SEV-4 (Development Environment)  
**Status:** Resolved  
**Technology:** Docker Compose, FastAPI, Uvicorn, PostgreSQL, PowerShell

## Incident Summary

During migration from a standalone FastAPI container to a multi-container Docker Compose environment, requests to the `/ready` endpoint returned HTTP 404 despite the endpoint existing in the application code.

Investigation revealed that an older standalone container was still publishing host port 8000. The newer Compose-managed API was running without a published host port.

## Impact

Requests from Windows reached an outdated application container rather than the intended Compose application. Database readiness could not initially be verified through the host endpoint.

No production systems were affected.

## Detection

The following command returned HTTP 404:

```powershell
curl.exe -i http://localhost:8000/ready
```

However, route inspection inside the Compose API confirmed `/ready` existed:

```powershell
docker compose exec api python -c "from main import app; print([route.path for route in app.routes])"
```

## Root Cause

A legacy standalone Docker container named `systems-api` continued publishing port 8000.

The Compose API container exposed port 8000 internally but did not have a working host port mapping.

The host request therefore reached the older application version.

## Investigation

1. Verified that FastAPI was running.
2. Confirmed the `/ready` route existed inside the Compose container.
3. Inspected container status and published ports.
4. Identified the legacy container occupying port 8000.
5. Tested readiness inside the Compose container and observed a separate HTTP 503 database connectivity failure.
6. Corrected container routing and subsequently verified database connectivity.

## Resolution

Removed the legacy container:

```powershell
docker stop systems-api
docker rm systems-api
```

Configured localhost-only port publishing:

```yaml
ports:
  - "127.0.0.1:8000:8000"
```

Recreated the Compose API:

```powershell
docker compose up -d --force-recreate api
```

## Validation

Both endpoints subsequently returned HTTP 200:

```text
GET /health -> 200 OK
GET /ready  -> 200 OK
```

Readiness response:

```json
{
  "status": "ready",
  "database": "connected"
}
```

## Lessons Learned

- A running container does not guarantee that host traffic reaches it.
- Docker's exposed ports and published host ports serve different purposes.
- HTTP 404 can indicate an outdated application version or incorrect request destination.
- Verify port ownership before changing application code.
- Application health and dependency readiness should be monitored separately.

## Preventive Actions

- [x] Remove the legacy container.
- [x] Configure localhost-only port publishing.
- [x] Verify both application endpoints.
- [ ] Add automated integration tests.
- [ ] Add deployment checks for port conflicts.
- [ ] Implement CI/CD validation.
