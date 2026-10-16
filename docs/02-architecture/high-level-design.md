# SecureCloud — High-Level Design (HLD)

**Document ID:** SC-HLD-001  
**Version:** 1.0  
**Status:** Draft  
**Related Documents:** SC-ARCH-001, SC-REQ-001, SC-COST-001

---

## 1. Purpose

Describe SecureCloud's logical architecture, major components, responsibilities, and primary interactions without prescribing every implementation detail.

## 2. Architecture Goals

- Reproducible infrastructure and application delivery.
- Secure automation with least-privilege access.
- Automated testing and security validation.
- Kubernetes deployment on Amazon EKS when approved by the cost plan.
- Observable application behavior and measurable reliability.
- Controlled cloud expenditure and safe resource cleanup.
- Documentation and evidence suitable for technical review.

## 3. Logical Architecture Layers

### Layer 1 — Source and Change Management

**Components:** Git, GitHub repository, pull requests, review controls.

**Responsibilities:**
- Store application, infrastructure, and deployment code.
- Track changes and architectural decisions.
- Provide an auditable history of changes.

### Layer 2 — Continuous Integration and Security

**Components:** GitHub Actions, automated tests, code checks, secret scanning, image scanning, infrastructure scanning.

**Responsibilities:**
- Validate changes before release.
- Build application images.
- Report security and quality findings.
- Prevent an approved release from proceeding when required checks fail.

### Layer 3 — Cloud Infrastructure

**Components:** AWS IAM, GitHub OIDC federation, Terraform, VPC, Amazon ECR, Amazon EKS.

**Responsibilities:**
- Provide controlled cloud access.
- Define infrastructure declaratively.
- Store approved container images.
- Host Kubernetes workloads when deployment is authorized.

**Constraint:** AWS resources are conditional on a verified cost estimate and approval.

### Layer 4 — Deployment and GitOps

**Components:** Helm, Argo CD, Kubernetes workloads.

**Responsibilities:**
- Package application configuration.
- Keep deployment definitions version-controlled.
- Reconcile approved configuration with the running cluster.
- Support repeatable deployments and documented rollback procedures.

### Layer 5 — Security Controls

**Components:** Secret scanning, static analysis, Trivy, Checkov, SBOM generation, Cosign, and Kyverno where feasible.

**Responsibilities:**
- Identify exposed secrets and vulnerable dependencies.
- Inspect container images and infrastructure definitions.
- Record software-component information.
- Verify artifact integrity and apply selected workload policies.

### Layer 6 — Observability and Reliability

**Components:** Prometheus, Grafana, Loki, OpenTelemetry, Tempo, and Alertmanager where feasible.

**Responsibilities:**
- Collect and inspect metrics, logs, and traces.
- Present service health and performance.
- Alert on selected failure conditions.
- Support SLI/SLO evaluation and incident investigation.

### Layer 7 — Operations and Cost Management

**Components:** Python automation, runbooks, test reports, resource inventory, cost reviews, and cleanup procedures.

**Responsibilities:**
- Automate selected diagnostic tasks.
- Calculate reliability indicators and error budgets.
- Record test and recovery evidence.
- Track resource lifecycle and cloud spending.

## 4. Primary Delivery Flow

1. A developer submits a source change.
2. GitHub Actions runs tests and configured quality/security checks.
3. A successful workflow builds the container image.
4. An authorized workflow may use OIDC to access AWS.
5. The image may be published to Amazon ECR.
6. Helm and Argo CD manage the deployment to Amazon EKS when approved.
7. Observability components collect application telemetry.
8. Operational checks validate service health, alerts, and reliability behavior.
9. The engineer records evidence and safely removes temporary infrastructure when appropriate.

## 5. Security Design Principles

- Use short-lived federated AWS credentials for supported automation.
- Apply least privilege to users, workflows, and workloads.
- Keep secrets out of Git and container images.
- Review network exposure before provisioning.
- Scan source, infrastructure, and container artifacts.
- Protect Terraform state and deployment configuration.
- Record and remediate security findings.

## 6. Reliability Design Principles

- Define measurable SLIs and proposed SLOs.
- Use health probes and resource limits for Kubernetes workloads.
- Collect relevant telemetry.
- Maintain actionable runbooks.
- Test controlled failure and recovery scenarios.
- Record actual test results rather than assuming production-level reliability.

## 7. Cost Design Principles

- Develop and validate locally whenever possible.
- Estimate complete infrastructure costs before deployment.
- Create EKS resources only for approved testing windows.
- Preserve reusable code and state while removing temporary infrastructure.
- Inspect for leftover compute, networking, storage, and logging resources.
- Review actual charges after cloud tests.

## 8. Major Architecture Decisions

| Decision | Current Direction | Reason |
|---|---|---|
| Cloud provider | AWS | Project requirement |
| Kubernetes target | Amazon EKS | Required deployment environment |
| Infrastructure as Code | Terraform | Reproducible infrastructure definitions |
| CI | GitHub Actions | Repository-integrated automation |
| Container registry | Amazon ECR | AWS image storage |
| Deployment packaging | Helm | Reusable Kubernetes configuration |
| GitOps | Argo CD | Declarative deployment reconciliation |
| Application | Python/FastAPI | Lightweight demonstration service |
| Cost policy | Ephemeral cloud testing | Reduce unnecessary runtime expenditure |

These are planned choices; implementation status must be tracked separately.

## 9. Architecture Boundaries

This HLD defines the logical structure. Exact subnet design, CIDR allocation, security-group rules, IAM policy details, Terraform module interfaces, Kubernetes resource specifications, and component sizing belong in the Low-Level Design.

## 10. Current Limitations

- AWS credits and billing conditions have not yet been verified.
- The full deployment cost has not yet been approved.
- EKS and observability components have not yet been deployed.
- No production availability or performance result is claimed at this stage.

## 11. Review Status

Draft HLD. Validate the detailed design, cost assumptions, and security boundaries before implementation.
