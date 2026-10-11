# AWS Systems Engineering Lab

A hands-on cloud infrastructure and reliability engineering project focused on secure deployments, containerization, database operations, automation, and incident response.

## Technology Stack

- **Cloud:** AWS (planned EC2, IAM, S3, Systems Manager)
- **Infrastructure as Code:** Terraform (planned)
- **Containers:** Docker and Docker Compose
- **Backend:** Python, FastAPI, Uvicorn
- **Database:** PostgreSQL 17
- **Development:** Windows PowerShell, Git, GitHub

## Architecture

```text
Windows Host
    |
    | localhost:8000
    v
FastAPI Container
    |
    | Docker internal network
    | db:5432
    v
PostgreSQL Container
    |
    v
Persistent Docker Volume
```

## Implemented Features

- Containerized FastAPI application
- PostgreSQL database integration
- Docker Compose orchestration
- Localhost-only API port publishing
- Database health checks
- Application health and readiness endpoints
- Persistent database storage
- Incident ticket table
- Incident creation and retrieval API endpoints

## Getting Started

### Requirements

- Docker Desktop with Linux container support
- Docker Compose v2
- Git

### Configuration

Create a `.env` file in the repository root containing:

```dotenv
POSTGRES_PASSWORD=your_unique_random_password
```

Never commit this file.

### Start the Application

```powershell
docker compose up -d --build
docker compose ps
```

### Verify Health

```powershell
curl.exe http://localhost:8000/health
curl.exe http://localhost:8000/ready
```

### View Incidents

```powershell
Invoke-RestMethod http://localhost:8000/incidents
```

The incident API requires an initialized `incident_tickets` table. Database schema automation is planned.

## Validation Completed

- FastAPI health endpoint returned HTTP 200.
- Database readiness endpoint returned HTTP 200.
- PostgreSQL initialized successfully.
- Database records survived container recreation.
- Docker host port conflict was diagnosed and corrected.

## Incident Reports

- [INC-001: Docker Build Context Failure](docs/incidents/INC-001-docker-build-failure.md)
- [INC-002: Docker Port Conflict](docs/incidents/INC-002-port-conflict.md)

## Security

- PostgreSQL is not published to the host.
- FastAPI is bound to the local host interface.
- Local secrets are excluded through `.gitignore`.
- Database queries use parameterized SQL.
- AWS infrastructure will use least-privilege IAM and protected Terraform state.

**Note:** The incident API is currently a local development application without authentication. It must not be publicly exposed without additional security controls.

## Roadmap

- [x] Containerize FastAPI
- [x] Deploy PostgreSQL with Docker Compose
- [x] Configure database persistence
- [x] Implement application readiness checks
- [x] Document Docker incidents
- [ ] Automate database schema initialization
- [ ] Implement automated tests
- [ ] Build Python diagnostic CLI
- [ ] Deploy AWS infrastructure using Terraform
- [ ] Implement automated backups and recovery
- [ ] Add CI/CD and security scanning
