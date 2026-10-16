# SecureCloud — Risk Register

**Document ID:** SC-RISK-001  
**Version:** 1.0  
**Status:** Draft  
**Review Frequency:** At each milestone and before cloud provisioning

---

## 1. Risk Rating

- **Likelihood:** Low, Medium, or High.
- **Impact:** Low, Medium, or High.
- **Priority:** Determined by likelihood, impact, and the need for immediate controls.

## 2. Identified Risks

| ID | Risk | Likelihood | Impact | Priority | Mitigation and Response |
|---|---|---|---|---|---|
| R-001 | EKS and supporting services exceed the ₹1,000 budget. | High | High | Critical | Estimate all relevant charges, verify credits, minimize deployment duration, and prohibit provisioning before approval. |
| R-002 | AWS resources continue generating charges after testing. | Medium | High | High | Maintain a resource inventory, define cleanup steps, and verify resources after every deployment session. |
| R-003 | AWS permissions are broader than required. | Medium | High | High | Review IAM permissions, use least privilege, and scope GitHub OIDC trust to the intended repository and workflow context. |
| R-004 | AWS credentials or application secrets are committed to Git. | Medium | High | High | Use secret scanning, exclude sensitive files, avoid hardcoded secrets, and rotate any exposed credentials immediately. |
| R-005 | Terraform state is exposed, corrupted, or changed unexpectedly. | Medium | High | High | Restrict state access, enable appropriate encryption and recovery controls, and protect state operations from concurrent changes. |
| R-006 | Infrastructure changes create unexpected network exposure. | Medium | High | High | Review network paths, security groups, public endpoints, and inbound rules before applying changes. |
| R-007 | Local memory limits interrupt testing or builds. | Medium | Medium | Medium | Keep containers lightweight, run one major workload at a time, and inspect Docker resource consumption. |
| R-008 | GitOps configuration drifts from the intended deployment state. | Medium | Medium | Medium | Use version-controlled manifests, inspect Argo CD synchronization status, and document reconciliation and rollback procedures. |
| R-009 | Security scans report vulnerabilities that block delivery. | High | Medium | High | Review severity and exploitability, update affected components, document accepted residual risks, and avoid hiding scan failures. |
| R-010 | Observability services consume excessive compute, storage, or memory. | Medium | High | High | Start with a minimal stack, constrain resource usage, limit retention, and verify costs before deploying. |
| R-011 | Performance tests overload resources or generate unnecessary charges. | Medium | High | High | Use bounded test duration and concurrency, define stop conditions, and avoid uncontrolled load or fault injection. |
| R-012 | Project scope expands beyond the 60-day target. | Medium | Medium | Medium | Prioritize essential requirements, defer optional extensions, and record scope changes explicitly. |
| R-013 | Tests pass locally but fail in CI or on EKS. | Medium | Medium | Medium | Keep test commands reproducible, validate container behavior, and record environment-specific differences. |
| R-014 | Cleanup removes a resource still needed by another workload. | Low | High | Medium | Inventory resources, identify dependencies, review Terraform state, and verify ownership before deletion. |
| R-015 | The project claims production readiness without sufficient evidence. | Medium | High | High | Trace claims to test results, document limitations, and distinguish a portfolio demonstration from a production service. |

## 3. Immediate Controls

Before any AWS provisioning:

1. Confirm the applicable AWS billing method, credits, and current spend.
2. Prepare a service-by-service cost estimate.
3. Define the proposed deployment window and cleanup procedure.
4. Review IAM permissions and authentication design.
5. Confirm that no credentials or secrets are stored in the repository.
6. Record the approval decision and remaining uncertainties.

## 4. Incident and Escalation Approach

If unexpected AWS charges, credential exposure, or unintended public access are detected:

- Stop the relevant deployment or automation where safe.
- Revoke or rotate exposed credentials if necessary.
- Identify affected resources and assess impact.
- Remove unintended exposure or stop unnecessary chargeable resources.
- Preserve relevant logs and evidence.
- Document the cause, remediation, and preventive actions.

## 5. Review Record

| Review | Trigger | Status |
|---|---|---|
| Initial review | Planning phase | Draft |
| Cost review | Before AWS provisioning | Pending |
| Security review | Before external deployment | Pending |
| Final review | Project completion | Pending |

## 6. Residual Risk

Risk ratings are initial assessments, not verified measurements. Reassess them when implementation details, AWS prices, test results, or project constraints change.
