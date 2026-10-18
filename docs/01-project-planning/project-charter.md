# SecureCloud — Project Charter

**Document Type:** Project Charter  
**Project:** SecureCloud — Production-Grade DevOps + SRE Platform on AWS  
**Version:** 1.0  
**Status:** Draft — Planning and validation  
**Target Duration:** 60 days  
**Target Effort:** Approximately 3 hours per day  
**Cloud Provider:** Amazon Web Services (AWS)  
**Primary Region:** Asia Pacific (Mumbai), `ap-south-1`  
**Cloud Budget Constraint:** Maximum target spend of ₹1,000

---

## 1. Project Overview

SecureCloud is a portfolio engineering project designed to demonstrate how a secure, observable, automated, and reliable cloud-native application platform can be designed, implemented, tested, documented, and operated using modern DevOps and Site Reliability Engineering practices.

The platform will use Infrastructure as Code, automated CI/CD, GitOps, Kubernetes on Amazon EKS, security scanning, software supply-chain controls, observability, reliability engineering, and operational automation.

The implementation will prioritize verifiable engineering evidence, reproducibility, security, cost awareness, and clear technical documentation.

## 2. Problem Statement

Cloud-native platforms require more than a successful application deployment. Engineering teams must also manage infrastructure consistency, deployment safety, security risks, operational visibility, reliability objectives, incident response, and cloud expenditure.

This project will demonstrate a practical approach to addressing these concerns through an integrated platform with automated workflows, measurable validation, and documented operational procedures.

## 3. Project Objectives

1. Build and test a containerized application with automated tests.
2. Implement CI workflows for code quality, testing, and security validation.
3. Define AWS infrastructure using Terraform.
4. Implement Kubernetes deployment on Amazon EKS, subject to the approved cost plan.
5. Configure deployment automation using Helm and Argo CD.
6. Integrate appropriate source-code, infrastructure, dependency, container-image, and Kubernetes security controls.
7. Implement metrics, dashboards, logs, traces, and actionable alerts where feasible.
8. Define service-level indicators, service-level objectives, error budgets, and operational runbooks.
9. Develop automation for diagnostics, reliability calculations, resource inventory, and cost reporting.
10. Document architecture, design decisions, testing evidence, operational procedures, and known limitations.
11. Produce a reproducible Git repository suitable for technical review and portfolio demonstration.

## 4. Scope

### In Scope

- Python/FastAPI demonstration application and automated tests
- Docker image build and local application validation
- Git and GitHub-based source control
- GitHub Actions CI/CD workflows
- AWS IAM and GitHub OpenID Connect federation
- Terraform infrastructure definitions and remote-state design
- AWS networking, Amazon ECR, and Amazon EKS, subject to budget approval
- Helm deployment packaging and Argo CD GitOps
- DevSecOps scanning and software supply-chain security
- Prometheus, Grafana, logging, and distributed tracing components where feasible
- SLI/SLO definitions, error-budget tracking, alerts, and runbooks
- Load testing and recovery validation appropriate to the available infrastructure
- Python automation and cost-management reporting
- Architecture diagrams, decision records, testing reports, and implementation documentation

### Out of Scope for the Initial Release

- A production service offered to external customers
- Guaranteed production-grade availability or a claimed 99.9% achieved SLO without supporting measurements
- A full internal developer portal such as Backstage
- Uncontrolled cloud provisioning or indefinite infrastructure operation
- Expensive managed services that violate the approved budget
- Unverified claims of enterprise-scale performance or security certification

Platform Engineering capabilities may be added in a later phase using reusable deployment templates and documented workflows.

## 5. Architecture Principles

- **Infrastructure as Code:** Manage supported infrastructure through version-controlled Terraform.
- **Least privilege:** Grant identities only the permissions required for their tasks.
- **Secure by default:** Scan code and artifacts and validate deployment policies.
- **Automation first:** Prefer repeatable pipelines over undocumented manual operations.
- **GitOps:** Keep deployment configuration version-controlled and reconcile changes through the selected GitOps workflow.
- **Observability:** Use metrics, logs, traces, and alerts to support diagnosis.
- **Reliability engineering:** Define measurable indicators and test failure and recovery scenarios.
- **Cost awareness:** Estimate, tag, monitor, and clean up cloud resources.
- **Evidence-based claims:** Report only capabilities that have been implemented and validated.
- **Documentation as code:** Maintain technical documentation alongside the implementation.

## 6. Constraints

1. The project must reside on the D: drive.
2. The target AWS expenditure is ₹1,000 maximum; this must be validated against actual pricing, taxes, credits, and billing before provisioning.
3. Amazon EKS is the required Kubernetes deployment environment. Local Kubernetes distributions are not part of this project.
4. The available Docker environment reports approximately 3.49 GiB of memory; local workloads must be sized accordingly.
5. Cloud resources must not be provisioned until the cost and deployment plan is approved.
6. AWS credentials and secrets must never be committed to the repository.
7. The 60-day schedule is a target, not a guarantee.

## 7. Success Criteria

The project will be considered complete when the applicable criteria below are implemented and supported by evidence:

- Application tests execute successfully.
- The application image builds reproducibly.
- CI workflows validate changes and report failures clearly.
- Terraform configuration passes the selected validation and security checks.
- AWS access for automation uses an appropriately scoped identity and OIDC where implemented.
- The EKS deployment and GitOps workflow are demonstrated if budget approval permits.
- Selected security controls produce reviewable scan results.
- Observability dashboards and alerts are tested with documented outcomes.
- SLO calculations and incident runbooks are exercised using recorded scenarios.
- Recovery and performance tests have documented procedures and results.
- Cloud resources are inventoried and unnecessary resources are cleaned up.
- Architecture, decisions, setup instructions, limitations, and evidence are documented.
- No unimplemented capability is presented as completed.

## 8. Budget and Provisioning Policy

The ₹1,000 limit is a hard project constraint, not an AWS billing guarantee.

Before creating chargeable infrastructure, prepare a cost estimate covering the EKS control plane, worker compute, networking, NAT, load balancing, storage, image storage, logs, data transfer, taxes, and applicable credits.

A budget alert does not automatically prevent additional spending. Prefer avoiding unnecessary resources and deleting temporary infrastructure after approved tests.

If the required EKS deployment cannot be demonstrated within the approved budget, pause provisioning and document the cost findings before proposing any alternative. Do not silently replace EKS with local Kubernetes.

## 9. Delivery Approach

Work will proceed in small milestones:

1. Planning and architecture
2. Application and automated tests
3. CI and containerization
4. AWS identity, Terraform, and cost validation
5. EKS and GitOps, subject to budget approval
6. DevSecOps and supply-chain security
7. Observability and SRE practices
8. Testing, evidence, documentation, and cleanup

Each milestone follows the cycle: **Design → Implement → Test → Document → Review**.

## 10. Current Status

- Project directory: `D:\securecloud-devops-platform`.
- Docker Engine: previously verified running.
- AWS CLI authentication: previously verified successful; no AWS resources have been provisioned for this project.
- Configured AWS region: `ap-south-1`.
- Application: FastAPI demonstration service implemented; all three automated tests passed locally.
- Container: Docker image built successfully; root, liveness, and readiness endpoints responded correctly; container ran as non-root UID `10001` and was removed after testing.
- CI: GitHub Actions workflow includes application testing and security checks. Terraform formatting/validation and infrastructure scanning have been added locally and require workflow execution evidence.
- Terraform infrastructure: reference network and security-group configuration implemented; local formatting and validation passed.
- AWS identity and remote state: design and implementation status require separate verification.
- EKS deployment: not provisioned.
- Cost validation: full deployment estimate not approved; AWS provisioning remains excluded from the current work.
- Documentation and evidence: in progress.

## 11. Approval Gate

No chargeable AWS infrastructure will be provisioned until the proposed configuration, expected cost, cleanup plan, and available credits have been reviewed against the ₹1,000 constraint.
