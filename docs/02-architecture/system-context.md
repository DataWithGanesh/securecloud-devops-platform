# SecureCloud — System Context

**Document ID:** SC-ARCH-001  
**Version:** 1.0  
**Status:** Draft  
**Architecture Level:** System Context

---

## 1. Purpose

Describe SecureCloud's external actors, systems, trust boundaries, and principal information flows before defining detailed infrastructure.

## 2. System Overview

SecureCloud is a demonstration platform for building, validating, deploying, observing, and operating a containerized application using DevOps and Site Reliability Engineering practices.

The platform combines source control, automated workflows, AWS infrastructure, Kubernetes deployment, security validation, observability, and operational documentation.

## 3. External Actors

| Actor | Responsibility |
|---|---|
| Project Engineer | Develops code, reviews changes, operates approved deployment workflows, and maintains documentation. |
| Repository Reviewer | Reviews implementation, pull requests, security findings, architecture, and test evidence. |
| CI Workflow | Executes automated tests, builds, validations, and approved publishing or deployment steps. |
| AWS Account | Provides cloud infrastructure and identity services for approved deployments. |
| Platform Operator | Reviews health, telemetry, incidents, costs, and cleanup results. |

These are logical roles; one person may perform multiple roles in this portfolio project.

## 4. External Systems

| System | Purpose | Trust Consideration |
|---|---|---|
| GitHub repository | Stores source code, workflows, infrastructure definitions, and deployment configuration. | Protect repository access and review changes. |
| GitHub Actions | Runs automated build, test, scan, and approved deployment workflows. | Use scoped permissions and avoid long-lived AWS credentials. |
| AWS IAM and OIDC | Federates an approved GitHub workflow to AWS. | Restrict trust to the intended repository and workflow context. |
| Amazon ECR | Stores container images when AWS publishing is enabled. | Restrict push/pull permissions and identify images by digest. |
| Amazon EKS | Hosts Kubernetes workloads when cloud deployment is approved. | Apply least privilege, network controls, and workload security policies. |
| Observability components | Collect and present metrics, logs, traces, and alerts. | Protect telemetry and avoid exposing sensitive data. |
| Local development environment | Supports coding, tests, and container builds. | Do not store credentials in source files or container images. |

## 5. Primary Information Flows

1. The engineer changes code and opens a reviewed repository change.
2. GitHub Actions checks out the code and runs configured tests and security checks.
3. The workflow builds a container image when the required checks pass.
4. An approved workflow may authenticate to AWS using OIDC.
5. The workflow may publish the image to Amazon ECR.
6. When EKS deployment is approved, Helm and Argo CD manage the Kubernetes deployment workflow.
7. The running application emits telemetry to configured monitoring and logging systems.
8. The engineer reviews test results, dashboards, alerts, costs, and operational evidence.
9. Temporary cloud resources are removed according to the approved cleanup procedure.

Flows 4–8 depend on the corresponding AWS resources and integrations being implemented and approved. This document does not imply that those integrations are already deployed.

## 6. Trust Boundaries

- **Developer workstation:** Source editing and local builds; AWS access must be controlled.
- **Source-control boundary:** Repository and workflow changes require appropriate review and permissions.
- **CI execution boundary:** Workflow jobs execute code and must receive only necessary permissions.
- **AWS identity boundary:** OIDC trust and IAM permissions control cloud access.
- **AWS infrastructure boundary:** Network rules and service identities limit access to deployed resources.
- **Workload boundary:** Kubernetes namespaces, service accounts, policies, and network controls separate workloads where implemented.
- **Observability boundary:** Logs, metrics, and traces must be protected against unauthorized access and sensitive-data leakage.

## 7. Architectural Assumptions

- AWS Mumbai (`ap-south-1`) is the intended deployment region.
- Amazon EKS is the required Kubernetes target.
- GitHub and GitHub Actions are the planned source-control and automation systems.
- Terraform is the planned Infrastructure as Code tool.
- Helm and Argo CD are the planned Kubernetes packaging and GitOps tools.
- AWS provisioning is conditional on cost and permission reviews.
- Local Kubernetes is not a substitute for the EKS requirement.

## 8. Out of Scope for This View

This context diagram specification does not define subnet CIDRs, security-group rules, node sizes, Kubernetes manifests, IAM policy JSON, or exact service costs. Those belong in the Low-Level Design and cost assessment.

## 9. Status

Draft system context. Confirm the final architecture and information flows as implementation details are validated.
