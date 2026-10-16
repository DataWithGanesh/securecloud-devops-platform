# SecureCloud — Low-Level Design (LLD)

**Document ID:** SC-LLD-001  
**Version:** 1.0  
**Status:** Draft  
**Parent Design:** SC-HLD-001

---

## 1. Purpose

Define the intended implementation boundaries, interfaces, security controls, and validation points for SecureCloud. Exact resource settings must be confirmed during implementation and cost review.

## 2. Application Component

**Technology:** Python and FastAPI.

Responsibilities:
- Serve a small demonstration API.
- Provide a health endpoint.
- Expose predictable behavior suitable for automated tests.
- Emit useful application logs.
- Support container execution.

Validation:
- Automated unit and API tests.
- Health endpoint test.
- Container build and startup test.
- Negative-path tests for expected errors.

## 3. Source Control and CI

**Planned components:** Git, GitHub, GitHub Actions.

Workflow stages:
1. Checkout source.
2. Install dependencies.
3. Run automated tests.
4. Run formatting and quality checks.
5. Scan for secrets and source-code issues.
6. Validate Terraform and scan infrastructure definitions.
7. Build the container image.
8. Scan the image and generate applicable artifact reports.
9. Publish an approved image only when deployment prerequisites are satisfied.

Security controls:
- Use minimum required workflow permissions.
- Pin third-party actions to reviewed versions or commit SHAs where practical.
- Do not expose secrets to untrusted pull-request workflows.
- Prefer OIDC for supported AWS authentication instead of long-lived access keys.

## 4. AWS Identity Design

Planned identity flow:

GitHub Actions → OIDC identity token → AWS IAM role assumption → authorized AWS API calls.

Controls:
- Restrict the role trust policy to the intended GitHub organization or owner, repository, and approved workflow context.
- Apply least-privilege permissions.
- Separate read-only validation from infrastructure modification permissions where practical.
- Avoid embedding AWS credentials in source, images, or Terraform files.
- Review and test the trust policy before enabling cloud deployment.

Exact IAM policies remain to be designed and validated.

## 5. Terraform and State

Responsibilities:
- Define infrastructure in version-controlled Terraform.
- Separate reusable modules from environment configuration.
- Validate formatting and configuration in CI.
- Review plans before applying changes.
- Protect state from unauthorized access and concurrent modification.

Remote-state design:
- Use a dedicated S3 state location if approved.
- Enable appropriate encryption and access controls.
- Enable versioning and recovery protections where appropriate.
- Restrict state access because it may contain sensitive values.
- Configure locking using a currently supported Terraform state-locking approach.

The state bucket and related resources must be costed and approved before creation.

## 6. AWS Network Design

The detailed network design will document:
- VPC CIDR and subnet allocation.
- Availability Zone selection.
- Public and private subnet purpose.
- Routing and outbound connectivity.
- EKS control-plane access requirements.
- Worker-node connectivity.
- Security-group rules and required traffic paths.
- Administrative access and logging.

Design principles:
- Expose only endpoints that are required.
- Avoid broad inbound access rules.
- Review public IPv4, NAT, and load-balancer costs.
- Prefer private workload placement where practical and affordable.
- Do not provision networking resources until the cost plan is approved.

Exact CIDRs and traffic rules are intentionally deferred until the network diagram is reviewed.

## 7. Container Registry

**Planned service:** Amazon ECR.

Responsibilities:
- Store approved container images.
- Identify released artifacts by immutable digest.
- Apply repository access controls and a deliberate retention policy.
- Scan images and retain relevant scan evidence.

Image storage and data-transfer costs must be included in the AWS estimate.

## 8. Kubernetes and EKS

**Required deployment target:** Amazon EKS.

Planned workload controls:
- Kubernetes Deployment and Service resources.
- Readiness and liveness probes.
- CPU and memory requests and limits.
- Non-root execution where supported.
- Restricted Linux capabilities and appropriate security contexts.
- Service-account permissions scoped to workload needs.
- Network and admission policies where implemented.

Validation:
- Helm chart validation.
- Kubernetes manifest validation.
- Successful EKS deployment test when approved.
- Health and rollout checks.
- Controlled failure and rollback test where feasible.

EKS, worker compute, load balancing, and supporting services must pass the budget approval gate first.

## 9. Helm and Argo CD

Helm:
- Package the application resources.
- Separate defaults from environment-specific values.
- Avoid placing secrets in plain-text values files.
- Validate chart templates before deployment.

Argo CD:
- Track approved deployment configuration in Git.
- Reconcile the intended state with the EKS cluster.
- Record synchronization and health status.
- Document drift correction and rollback procedures.

The GitOps repository and deployment permissions must be reviewed before enabling automated synchronization.

## 10. Security Tooling

Planned tools and responsibilities:

- **Gitleaks:** detect exposed secrets.
- **Semgrep:** inspect source code for selected security issues.
- **Trivy:** scan container images and supported artifacts.
- **Checkov:** inspect Terraform and infrastructure configuration.
- **Syft:** generate a Software Bill of Materials.
- **Cosign:** sign and verify supported container artifacts.
- **Kyverno:** enforce selected Kubernetes admission policies.

Tool versions, configuration, severity thresholds, and remediation policy will be documented during implementation. Findings must not be hidden simply to obtain a passing pipeline.

## 11. Observability

Planned components, subject to resource feasibility:
- Prometheus for metrics.
- Grafana for dashboards.
- Loki for logs.
- OpenTelemetry instrumentation and collection.
- Tempo for distributed traces.
- Alertmanager for alert routing.

Design requirements:
- Define telemetry sources and destinations.
- Use consistent service identifiers.
- Avoid recording secrets or sensitive payloads.
- Limit retention and resource consumption.
- Test alerts and document the associated runbooks.

The full stack may be too resource-intensive for a small temporary cluster. The final component selection must reflect the approved deployment budget and available capacity.

## 12. Reliability Engineering

Planned capabilities:
- Define availability and latency SLIs.
- Select proposed SLO targets and measurement windows.
- Calculate error budgets.
- Test application health and selected failure conditions.
- Record load-test configuration and results.
- Maintain troubleshooting, recovery, and cleanup runbooks.
- Document simulated exercises separately from real incidents.

SLO values will not be represented as achieved production results without supporting measurements.

## 13. Cost and Cleanup

Before provisioning:
- Estimate all selected resources.
- Record the approved deployment window.
- Identify dependencies and persistent resources.
- Define a safe cleanup plan.

After testing:
- Save evidence and relevant state.
- Remove temporary resources using the appropriate lifecycle workflow.
- Verify compute, networking, storage, and load-balancer cleanup.
- Inspect retained images, logs, snapshots, and state resources.
- Record observed charges and remaining risks.

Terraform destroy must not be run without reviewing its plan, resource ownership, dependencies, and state.

## 14. Validation Gates

1. Application tests pass before image release.
2. Security checks run before approved publishing.
3. Terraform validation passes before infrastructure review.
4. Cost approval precedes chargeable resource creation.
5. AWS access policies are reviewed before deployment.
6. EKS behavior is tested on Amazon EKS when provisioned.
7. Observability and recovery claims require recorded test evidence.
8. Cleanup is verified before the deployment session is considered complete.

## 15. Open Design Decisions

- Final VPC and subnet CIDRs.
- EKS endpoint access configuration.
- Node type and capacity.
- NAT versus alternative outbound connectivity.
- Load-balancer and ingress design.
- Terraform state resource configuration.
- Observability component sizing and retention.
- Exact cost and feasibility of the complete EKS deployment.

These decisions remain open until the detailed architecture and cost review.

## 16. Status

Draft LLD. No AWS infrastructure is implied to be deployed by this document.
