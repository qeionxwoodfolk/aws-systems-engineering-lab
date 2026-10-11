# INC-001: Docker Build Context Failure

**Project:** AWS Systems Engineering Lab  
**Incident ID:** INC-001  
**Date:** October 10, 2026  
**Severity:** SEV-4 — Development Environment  
**Status:** Resolved  
**Category:** Containerization / Deployment Failure  
**Environment:** Windows 11, PowerShell, Docker Desktop 29.8.2

---

## 1. Executive Summary

During the initial containerization of a Python FastAPI application, a Docker image build failed because the specified build context referenced a nonexistent directory.

Further investigation identified an additional configuration issue: the Dockerfile had been saved with a `.txt` extension rather than the expected `Dockerfile` filename.

Both issues were corrected, and the application was successfully built, deployed, and verified through its HTTP health endpoint.

**Impact:** Local development and deployment were temporarily blocked. No production systems or customer workloads were affected.

## 2. System Architecture

The application consists of:

- **FastAPI:** Python web framework providing application endpoints.
- **Uvicorn:** ASGI web server handling HTTP requests.
- **Docker:** Container runtime used to package and execute the application.
- **Windows PowerShell:** Command-line environment used to manage builds and deployments.

Application directory structure:

```text
aws-systems-engineering/
└── app/
    ├── main.py
    ├── requirements.txt
    └── Dockerfile
```

## 3. Incident Detection

The incident was detected when the following Docker build command failed:

```powershell
docker build -t systems-lab-api:1.0 ./app
```

### Error Message

```text
ERROR: failed to build:
unable to prepare context:
path "./app" not found
```

The error indicated that Docker could not locate the requested build context.

## 4. Root Cause Analysis

### Primary Root Cause — Incorrect Build Context

The terminal was already positioned inside:

```text
C:\Users\qeion\aws-systems-engineering\app
```

The command referenced `./app`, which instructed Docker to search for another `app` directory within the current directory.

That nested directory did not exist.

### Secondary Configuration Issue — Incorrect Dockerfile Extension

Directory inspection revealed that the Dockerfile had been saved as:

```text
Dockerfile.txt
```

Docker expects a file named `Dockerfile` by default unless an alternative filename is explicitly specified.

This issue would have prevented the corrected build command from locating its build instructions.

## 5. Troubleshooting and Resolution

### Step 1 — Inspect Working Directory

Used PowerShell to determine the current directory:

```powershell
pwd
```

### Step 2 — Inspect Application Files

Listed the contents of the directory:

```powershell
ls
```

Identified the incorrectly named `Dockerfile.txt`.

### Step 3 — Correct Dockerfile Naming

Executed:

```powershell
Rename-Item Dockerfile.txt Dockerfile
```

### Step 4 — Correct Build Context

Rebuilt the image using the current directory:

```powershell
docker build -t systems-lab-api:1.0 .
```

The `.` specifies the current directory as Docker's build context.

### Step 5 — Deploy the Application

Started the container:

```powershell
docker run -d --name systems-api -p 8000:8000 systems-lab-api:1.0
```

### Step 6 — Verify Service Health

Executed:

```powershell
curl.exe http://localhost:8000/health
```

Observed response:

```json
{
  "status": "healthy",
  "timestamp": "2026-10-11T02:22:41.228349+00:00"
}
```

The HTTP response confirmed that the FastAPI application was responding successfully.

## 6. Resolution Validation

| Validation | Result |
|---|---|
| Dockerfile renamed | Passed |
| Build context corrected | Passed |
| Docker image successfully built | Passed |
| Container started | Passed |
| Application health endpoint | Passed |

**Final Status:** Resolved

## 7. Preventive Measures

The following improvements were identified to reduce similar deployment failures:

1. Verify the current working directory before executing commands that use relative paths.
2. Validate required application files before initiating container builds.
3. Standardize Dockerfile naming conventions.
4. Add automated Docker build checks through GitHub Actions.
5. Maintain deployment and troubleshooting documentation.

## 8. Key Engineering Lessons

**Docker Build Context:** Docker resolves relative build paths from the shell's current working directory.

**Configuration Validation:** Incorrect filenames and directory structures can cause deployment failures independently of application code.

**Root Cause Analysis:** Investigating the error message and filesystem state helped isolate the problem without unnecessary changes to Docker Engine configuration.

**Health Verification:** A successful image build does not guarantee that an application works. Runtime checks are necessary to confirm successful deployment.

## 9. Follow-Up Actions

- [x] Correct Dockerfile extension.
- [x] Correct Docker build context.
- [x] Successfully build container image.
- [x] Start FastAPI container.
- [x] Verify application health endpoint.
- [ ] Implement automated build validation in GitHub Actions.
- [ ] Add container security scanning.
- [ ] Extend the environment with PostgreSQL and Docker Compose.

---

## Incident Conclusion

The deployment failure resulted from incorrect local filesystem references and Dockerfile naming.

After correcting both configuration issues, the application was successfully containerized and verified.

This incident demonstrates practical experience with Docker troubleshooting, PowerShell filesystem inspection, container deployment, and structured root cause analysis.
