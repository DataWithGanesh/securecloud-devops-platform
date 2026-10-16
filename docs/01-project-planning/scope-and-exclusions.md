# SecureCloud — Scope and Exclusions

**Document ID:** SC-SCOPE-001  
**Version:** 1.0  
**Status:** Draft

---

## 1. Purpose

Define the boundaries of the initial SecureCloud release, including committed deliverables, conditional deliverables, exclusions, and change-control rules.

## 2. Core Deliverables

### Application and Engineering

- Python/FastAPI demonstration application.
- Automated application tests.
- Dockerfile and reproducible container build.
- Git repository with a clear, documented structure.
- GitHub Actions continuous integration workflow.

### Infrastructure and Deployment

- Terraform infrastructure code and validation.
- AWS IAM and GitHub OIDC design.
- Terraform remote-state design and secure configuration.
- AWS networking and Amazon ECR design.
- Helm deployment configuration.
- Kubernetes deployment on Amazon EKS, subject to cost approval.
- Argo CD GitOps workflow, subject to deployment feasibility.

### Security

- Secret scanning.
- Source-code security analysis.
- Container vulnerability scanning.
- Infrastructure-as-Code security scanning.
- Software Bill of Materials (SBOM).
- Container signing and verification where feasible.
- Kubernetes policy enforcement where feasible.

### Reliability and Operations

- Service-level indicators and objectives.
- Error-budget calculation.
- Metrics and dashboards.
- Centralized logging and distributed tracing where feasible.
- Alerting and operational runbooks.
- Load and recovery testing.
- Python-based diagnostics and cost/resource reporting.

### Documentation

- Project planning documents.
- High-Level Design (HLD) and Low-Level Design (LLD).
- Editable architecture diagrams and rendered exports.
- Architecture Decision Records.
- Setup, testing, deployment, troubleshooting, and cleanup instructions.
- Test results, scan reports, and evidence index.

## 3. Conditional Deliverables

The following require a feasibility review before implementation or deployment:

- Amazon EKS cluster and worker nodes.
- NAT gateway and public load balancer.
- Long-running observability and tracing services.
- Managed databases, caches, and persistent storage.
- Extended performance, resilience, and failure-injection tests.
- Any service that could exceed the approved AWS spending limit.

Conditional does not mean silently omitted. Each item must be implemented, formally deferred, or documented with its cost and feasibility findings.

## 4. Explicit Exclusions from Release 1

- A production service for real external customers.
- A full Backstage-based Internal Developer Portal.
- Multi-account enterprise landing-zone implementation.
- Multi-region disaster recovery.
- A paid monitoring or security subscription.
- Unbounded load tests or uncontrolled fault injection.
- A claim of achieved production availability without sufficient measurements.
- A claim of complete security or compliance certification.
- Local Kubernetes as a substitute for the required Amazon EKS deployment.
- Cloud resource creation before the cost review is approved.

## 5. Budget Boundary

The target maximum AWS spend is ₹1,000.

Before provisioning, evaluate the complete resource plan, including control-plane charges, compute, networking, storage, image storage, logs, load balancing, data transfer, taxes, and available credits.

A budget alert is not a hard spending cap. If the approved EKS configuration cannot fit the budget, stop before provisioning and document the findings. Any proposed change must be reviewed rather than silently changing the platform requirements.

## 6. Change Control

Every proposed scope change must record:

1. The requested change and its purpose.
2. Expected engineering effort.
3. Security and operational impact.
4. AWS cost impact.
5. Dependencies and schedule impact.
6. Approval or deferral decision.

Update the requirements specification and relevant architecture documents when an approved change alters the design.

## 7. Completion Rule

A deliverable is complete only when its implementation status is clear and appropriate validation evidence is available.

Every deliverable must be marked as one of:

- Implemented and tested.
- Implemented but not fully tested.
- Designed but not implemented.
- Deferred with a documented reason.
- Excluded from the initial release.

## 8. Review Status

Draft scope established. Revisit conditional deliverables after the cost assessment and architecture review.
