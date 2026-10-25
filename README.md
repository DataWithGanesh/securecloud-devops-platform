# SecureCloud — Production-Grade DevOps & SRE Platform

A security-focused, observable cloud platform demonstrating Infrastructure as Code (IaC), container security, Kubernetes deployment configuration, GitOps, CI/CD automation, and Site Reliability Engineering (SRE) practices.

> **Project status:** Core application, CI workflows, infrastructure configuration, and local observability components have been implemented and validated. AWS infrastructure and a live Kubernetes deployment have not yet been provisioned.

## Overview

SecureCloud demonstrates how DevOps and SRE practices can be combined to build, validate, monitor, and prepare an application for reliable deployment.

The project includes a FastAPI demo service, Terraform infrastructure definitions, hardened container and Kubernetes configurations, Helm packaging, Argo CD GitOps configuration, automated image supply-chain checks, and a local observability stack.

## Architecture

The platform follows this high-level workflow:

1. **Application:** A FastAPI service exposes health endpoints, structured JSON logs, and Prometheus metrics.
2. **Continuous integration:** GitHub Actions runs automated tests and configuration, security, and deployment-manifest checks.
3. **Container supply chain:** The image workflow builds and scans the container, generates an SBOM, publishes the image to GitHub Container Registry (GHCR), and automates Helm digest promotion.
4. **Infrastructure as Code:** Terraform defines the AWS network and supporting infrastructure configuration.
5. **Deployment configuration:** Helm packages the Kubernetes workload, while an Argo CD Application defines the GitOps deployment target.
6. **Observability:** Prometheus collects metrics, Grafana visualizes them, Grafana Alloy collects container logs, and Loki stores and serves those logs.

See the architecture diagrams:

- [SecureCloud architecture](docs/02-architecture/diagrams/securecloud-architecture.png)
- [Deployment architecture](docs/02-architecture/diagrams/deployment-architecture.png)

## Technology Stack

| Area                   | Technologies                                                             |
| ---------------------- | ------------------------------------------------------------------------ |
| Application            | Python, FastAPI, Uvicorn                                                 |
| Containers             | Docker, Docker Compose                                                   |
| Infrastructure as Code | Terraform                                                                |
| Cloud configuration    | AWS VPC, subnets, security groups and related infrastructure definitions |
| Kubernetes packaging   | Kubernetes manifests, Helm                                               |
| GitOps                 | Argo CD configuration                                                    |
| CI/CD                  | GitHub Actions                                                           |
| Image security         | Trivy, Gitleaks, Bandit                                                  |
| Supply-chain evidence  | SPDX SBOM                                                                |
| Metrics and dashboards | Prometheus, Grafana                                                      |
| Logs                   | Grafana Alloy, Loki                                                      |
| Testing                | Pytest, configuration and manifest validation                            |

## Repository Structure

```text
.
├── .github/workflows/          # CI and image supply-chain workflows
├── apps/
│   └── demo-api/               # FastAPI service and local Compose stack
├── deployment/
│   ├── argocd/                 # Argo CD Application configuration
│   └── helm/                   # Helm chart
├── infrastructure/
│   └── terraform/              # AWS infrastructure definitions
├── observability/
│   ├── alloy/                  # Container log collection
│   ├── grafana/                # Datasource provisioning
│   └── loki/                   # Loki configuration
├── docs/
│   ├── 01-project-planning/
│   ├── 02-architecture/
│   └── 09-evidence-and-reports/
├── runbooks/                   # Operational procedures
├── security/                   # Security-related project materials
└── testing/                    # Testing-related project materials
```

## Local Observability Quick Start

### Prerequisites

- Docker Desktop with Docker Compose
- Git
- Python 3.13 for local application tests

Clone the repository and enter the project directory:

```powershell
git clone https://github.com/DataWithGanesh/securecloud-devops-platform.git
cd securecloud-devops-platform
```

Start the local observability stack:

```powershell
docker compose -f apps/demo-api/compose.yaml up -d --build
```

Check container status:

```powershell
docker compose -f apps/demo-api/compose.yaml ps
```

Validate the Compose configuration:

```powershell
docker compose -f apps/demo-api/compose.yaml config --quiet
```

### Local Endpoints

| Component              | URL                                |
| ---------------------- | ---------------------------------- |
| Demo API               | http://localhost:8001              |
| API liveness           | http://localhost:8001/health/live  |
| API readiness          | http://localhost:8001/health/ready |
| API Prometheus metrics | http://localhost:8001/metrics      |
| Prometheus             | http://localhost:9090              |
| Prometheus targets     | http://localhost:9090/targets      |
| Grafana                | http://localhost:3000              |
| Loki                   | http://localhost:3100              |

The API, Prometheus, Grafana, and Loki HTTP ports are bound to localhost in the local Compose configuration.

### Grafana

The local Grafana instance has a provisioned Loki datasource. Use the local credentials configured for your development environment; do not reuse local development credentials in production.

In Grafana Explore, select Loki and query:

```logql
{project="securecloud"}
```

To view demo API logs specifically:

```logql
{project="securecloud", container="securecloud-demo-api"}
```

### Stop the Local Stack

```powershell
docker compose -f apps/demo-api/compose.yaml down
```

This stops and removes the Compose containers and network. Named or external data volumes, if configured, may have a different lifecycle.

## Application Validation

Check API liveness:

```powershell
Invoke-RestMethod http://localhost:8001/health/live
```

Check API readiness:

```powershell
Invoke-RestMethod http://localhost:8001/health/ready
```

Check Prometheus metrics availability:

```powershell
(Invoke-WebRequest -UseBasicParsing http://localhost:8001/metrics).StatusCode
```

Expected HTTP status: `200`.

## CI/CD and Security

The GitHub Actions workflows implement automated validation across application code, infrastructure configuration, Kubernetes manifests, Helm, and image supply-chain tasks.

Configured checks include:

- Automated application tests
- Terraform formatting and validation
- Terraform security scanning
- Secret scanning with Gitleaks
- Python security analysis with Bandit
- Container vulnerability scanning with Trivy
- Kubernetes manifest and schema validation
- Helm linting and rendered-manifest validation
- Image publication to GHCR
- SPDX SBOM generation
- Automated Helm image-digest promotion

Workflow success demonstrates that the configured checks passed for the relevant commit. It does not, by itself, establish that the application has been deployed to AWS or tested under production load.

## Reliability and Observability

The demo API exposes health endpoints and Prometheus metrics. The local observability configuration includes:

- API request rate
- HTTP 5xx error rate
- P95 request latency
- Prometheus target availability
- Structured API request logs
- Log collection through Alloy and querying through Loki
- Prometheus alert rules for API availability, elevated 5xx errors, and high P95 latency

The local metrics and log pipeline has been exercised in the development environment. Alert firing under controlled failure conditions and production alert delivery require separate verification.

## Infrastructure and GitOps

Terraform defines the AWS infrastructure configuration, while Helm and Argo CD files describe the intended Kubernetes deployment and GitOps workflow.

**Important:** Terraform validation and Kubernetes/Helm manifest validation do not mean AWS resources or a Kubernetes cluster exist. Provisioning, live deployment, cloud IAM integration, and end-to-end cloud validation are outside the completed local validation unless explicitly recorded otherwise.

No AWS resources should be provisioned without reviewing the cost plan and obtaining approval.

## Documentation

- [Project charter](docs/01-project-planning/project-charter.md)
- [Requirements specification](docs/01-project-planning/requirements-specification.md)
- [Implementation plan](docs/01-project-planning/implementation-plan.md)
- [Scope and exclusions](docs/01-project-planning/scope-and-exclusions.md)
- [Cost plan](docs/01-project-planning/cost-plan.md)
- [Definition of done](docs/01-project-planning/definition-of-done.md)
- [Risk register](docs/01-project-planning/risk-register.md)
- [High-level design](docs/02-architecture/high-level-design.md)
- [Low-level design](docs/02-architecture/low-level-design.md)
- [Network design](docs/02-architecture/network-design.md)
- [Security architecture](docs/02-architecture/security-architecture.md)
- [Data flow](docs/02-architecture/data-flow.md)
- [CI validation report](docs/09-evidence-and-reports/ci-validation-report.md)

## Project Goals

SecureCloud is designed to demonstrate practical DevOps and SRE skills:

- Repeatable infrastructure configuration through IaC
- Automated build, test, and security validation
- Immutable container image references and supply-chain evidence
- Kubernetes deployment hardening
- GitOps configuration and image promotion
- Metrics, dashboards, structured logging, and alerting
- Operational documentation and repeatable validation

## License

Add a license file before treating this repository as an openly licensed project. Until then, no open-source license is specified.



