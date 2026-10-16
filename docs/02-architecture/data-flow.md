# SecureCloud — Data Flow Design

**Document ID:** SC-DATA-001  
**Version:** 1.0  
**Status:** Draft

---

## 1. Purpose

Describe the principal information flows between the engineer, source control, CI/CD, AWS infrastructure, Kubernetes workloads, and operational tooling.

## 2. Source Code Flow

1. The engineer changes application, Terraform, or deployment code.
2. Changes are committed to Git and pushed to the GitHub repository.
3. A pull request or approved repository event triggers GitHub Actions.
4. CI checks out the relevant source revision.
5. Tests, code checks, secret scanning, and infrastructure validation run as configured.
6. Results are recorded in workflow logs and reports.

**Security controls:** Repository access restrictions, code review, minimum workflow permissions, and secret scanning.

## 3. Container Build and Artifact Flow

1. CI builds the application container image from the approved source revision.
2. The image is checked using the configured security scanner.
3. An SBOM is generated where implemented.
4. Image signing and verification are performed where configured.
5. An approved workflow may publish the image to Amazon ECR.
6. The image digest and related validation evidence are recorded.

**Security controls:** Image scanning, artifact identity, registry permissions, and reviewed release conditions.

## 4. AWS Authentication Flow

1. An approved GitHub Actions workflow requests an OIDC identity token.
2. AWS IAM evaluates the configured trust policy.
3. If the identity and trust conditions match, the workflow assumes the permitted IAM role.
4. The workflow receives temporary credentials.
5. AWS API calls are restricted by the role's permissions and applicable resource policies.

**Security controls:** Narrow trust conditions, least privilege, temporary credentials, and avoidance of secrets in logs.

This flow is planned and must be validated before it is treated as operational.

## 5. Infrastructure Provisioning Flow

1. Terraform configuration is stored in version control.
2. CI or an authorized engineer validates the configuration and reviews the plan.
3. The proposed resource changes and cost implications are reviewed.
4. Provisioning proceeds only after the required approval.
5. Terraform records managed infrastructure in its state.
6. The resulting resources and outputs are checked and documented.

**Security controls:** Protected state, reviewed plans, controlled credentials, and explicit deployment approval.

## 6. Application Deployment Flow

1. An approved image is stored in Amazon ECR.
2. Deployment configuration references the intended image digest or approved image version.
3. Helm renders the Kubernetes resources.
4. Argo CD reconciles approved Git configuration with the EKS cluster when GitOps is enabled.
5. Kubernetes schedules the application workload.
6. Health probes and rollout status are checked.
7. Deployment results and any rollback are recorded.

**Security controls:** Registry permissions, workload identity, Kubernetes access controls, health checks, and reviewed deployment configuration.

## 7. User Request Flow

The intended request path is:

Client → HTTPS ingress endpoint → Kubernetes Service → FastAPI application Pod.

The final ingress component, TLS configuration, and network route remain subject to detailed design and cost approval.

## 8. Observability Flow

1. The application produces metrics, logs, and traces where instrumented.
2. Configured telemetry components collect the relevant signals.
3. Monitoring and logging backends store or process the signals.
4. Dashboards display service health and performance.
5. Alert rules evaluate selected conditions.
6. Operators investigate alerts using dashboards, logs, traces, and runbooks.
7. Findings and corrective actions are documented.

**Security controls:** Access restrictions, appropriate retention, and exclusion of secrets from telemetry.

## 9. Cost and Cleanup Flow

1. The engineer defines the resources required for a planned test.
2. The cost plan and deployment window are reviewed.
3. Approved resources are provisioned.
4. Tests and evidence collection are completed.
5. Temporary resources are removed using the appropriate lifecycle process.
6. Remaining resources are inventoried and checked.
7. Observed costs and cleanup results are recorded.

Terraform state and reusable configuration must be preserved as required for safe future operations.

## 10. Data Classification and Handling

| Data Type | Handling Principle |
|---|---|
| Application source | Version-controlled with appropriate repository access. |
| Workflow configuration | Reviewed and protected against untrusted changes. |
| AWS credentials | Temporary where supported; never committed to source. |
| Terraform state | Restricted because it may contain sensitive values. |
| Container images | Access-controlled and identifiable by digest. |
| Test and scan reports | Retained as evidence and reviewed before publication. |
| Logs and traces | Avoid sensitive payloads and apply appropriate access and retention controls. |
| Cost reports | Review before publication if they expose account-specific details. |

## 11. Open Decisions

- Final artifact retention policy.
- Final image-signing and verification workflow.
- Exact telemetry collection and storage configuration.
- Final ingress and TLS implementation.
- Evidence retention and repository publication policy.

## 12. Status

Draft data-flow design. Actual flows must be verified against the implemented configuration and test evidence.
