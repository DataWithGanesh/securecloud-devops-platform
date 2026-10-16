# SecureCloud — Security Architecture

**Document ID:** SC-SEC-ARCH-001  
**Version:** 1.0  
**Status:** Draft — Review required

---

## 1. Purpose

Define the security principles, trust boundaries, and planned controls for SecureCloud. Controls are considered implemented only after configuration and validation evidence exist.

## 2. Security Objectives

- Apply least privilege to human, workflow, and workload identities.
- Prevent accidental exposure of credentials and sensitive information.
- Validate source code, infrastructure configuration, and container artifacts.
- Reduce unnecessary network exposure.
- Protect Terraform state and deployment configuration.
- Record security findings and remediation decisions.
- Support repeatable, auditable deployment workflows.

## 3. Identity and Access Management

### Human Access

- Use individual AWS identities and approved access methods.
- Avoid unnecessary administrator permissions.
- Review permissions before provisioning infrastructure.
- Do not share or commit credentials.

### GitHub Actions to AWS

Planned flow:

GitHub Actions → GitHub OIDC token → AWS IAM role assumption → authorized AWS API calls.

Controls:
- Restrict the OIDC trust policy to the intended repository and approved workflow context.
- Scope permissions to the required AWS resources and actions.
- Separate read-only validation and infrastructure-changing permissions where practical.
- Prefer short-lived credentials over long-lived access keys.
- Never print credentials or sensitive tokens in workflow logs.

### Kubernetes Workload Access

Where implemented:
- Use dedicated service accounts for workloads requiring AWS access.
- Grant only the permissions required by each workload.
- Avoid embedding AWS credentials in container images or Kubernetes manifests.
- Review Kubernetes RBAC permissions and namespace boundaries.

## 4. Secrets Management

- Keep secrets out of Git.
- Exclude local secret files from version control.
- Use approved secret-management mechanisms for any required runtime secrets.
- Do not put credentials in Dockerfiles, image layers, Helm values, or logs.
- Run secret scanning in CI.
- If a credential is exposed, revoke or rotate it and assess potential impact immediately.

Secret scanning helps detect mistakes but does not replace safe credential handling.

## 5. Source Code and CI/CD Security

Planned controls:
- Review code and workflow changes.
- Run automated tests and selected security checks.
- Limit workflow permissions.
- Protect deployment credentials from untrusted pull-request code.
- Pin third-party workflow actions to reviewed versions or commit SHAs where practical.
- Restrict image publishing and deployment to approved workflow conditions.
- Preserve relevant scan reports and workflow evidence.

## 6. Software Supply-Chain Security

Planned tools:
- Gitleaks for secret detection.
- Semgrep for selected source-code security analysis.
- Trivy for container and supported artifact scanning.
- Checkov for Infrastructure as Code checks.
- Syft for Software Bill of Materials generation.
- Cosign for image signing and verification.

Controls:
- Review findings rather than automatically ignoring failures.
- Identify released images by digest.
- Record the relationship between source revision, image digest, scan results, and release.
- Document accepted residual risks.
- Protect signing keys or identities according to the chosen signing method.

## 7. Infrastructure Security

- Manage supported infrastructure through Terraform.
- Review Terraform plans before applying changes.
- Use least-privilege IAM permissions.
- Protect remote state with appropriate access controls and encryption.
- Review public exposure, routes, and security-group rules.
- Avoid unrestricted administrative ingress.
- Record infrastructure security scan results.
- Separate reusable configuration from environment-specific settings.

## 8. Kubernetes Security

Where EKS is provisioned:
- Use supported Kubernetes and EKS configurations.
- Define resource requests and limits.
- Use non-root execution and restricted capabilities where supported.
- Configure health probes.
- Apply appropriate RBAC and service-account permissions.
- Restrict network traffic where feasible.
- Evaluate Kyverno policies for selected admission controls.
- Review image provenance and vulnerability findings.
- Keep cluster access restricted to authorized identities.

## 9. Data and Observability Security

- Do not log credentials, tokens, or unnecessary sensitive payloads.
- Restrict access to logs, metrics, traces, dashboards, and reports.
- Define retention according to operational needs and cost constraints.
- Protect Terraform state and any artifacts that may contain sensitive values.
- Review exported reports before publishing them in a public repository.

## 10. Network Security

- Document approved inbound and outbound traffic.
- Expose only necessary endpoints.
- Review public endpoint configuration.
- Use appropriately scoped security groups and network controls.
- Avoid deploying a NAT Gateway or load balancer without a demonstrated requirement and cost approval.
- Record network-related security decisions.

## 11. Security Validation

Before release:
1. Run secret scanning.
2. Run relevant source-code and dependency checks.
3. Scan the container image.
4. Scan Terraform and infrastructure configuration.
5. Review IAM and OIDC trust policies.
6. Validate network exposure.
7. Review security findings and remediation.
8. Record test results and unresolved limitations.

## 12. Incident Response

If a potential security incident occurs:
- Stop the affected workflow or deployment when safe.
- Revoke exposed credentials or restrict affected access.
- Identify affected resources and assess impact.
- Preserve relevant logs and evidence.
- Remediate the cause.
- Verify recovery and document preventive actions.

## 13. Security Acceptance Criteria

- No known exposed credentials remain unresolved.
- Required security scans have been executed.
- Findings are reviewed and their disposition is documented.
- IAM and OIDC permissions are reviewed before deployment.
- Network exposure is reviewed before public access is enabled.
- Security controls have supporting validation evidence.
- Known limitations and residual risks are disclosed.

## 14. Status

Draft security architecture. These controls describe the intended design; they are not claims that the controls have already been implemented or independently audited.
