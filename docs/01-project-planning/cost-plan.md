# SecureCloud — AWS Cost Plan

**Document ID:** SC-COST-001  
**Version:** 1.0  
**Status:** Draft — Cost verification required  
**Budget Ceiling:** ₹1,000 total AWS spend  
**AWS Region:** ap-south-1 (Mumbai)

---

## 1. Objective

Control AWS expenditure throughout SecureCloud development while preserving Amazon EKS as the required Kubernetes deployment target.

## 2. Cost Management Principles

1. Develop and validate locally wherever possible.
2. Estimate AWS charges before provisioning.
3. Create cloud resources only for planned tests.
4. Capture test evidence before removing temporary infrastructure.
5. Destroy temporary resources safely and verify cleanup.
6. Preserve reusable configuration and Terraform state.
7. Review actual AWS costs throughout the project.
8. Never assume that stopping a laptop stops cloud resources.

## 3. Resources Requiring Cost Review

The estimate must account for:

- Amazon EKS cluster control plane
- EC2 worker nodes or other compute
- NAT gateways and data processing
- Load balancers and public IPv4 addresses
- EBS volumes and snapshots
- Amazon ECR image storage
- S3 storage and requests
- CloudWatch logs and metrics
- Data transfer
- Applicable taxes and currency conversion

Not every service will necessarily be deployed. Include only the resources in the proposed architecture, while accounting for indirect dependencies.

## 4. EKS Runtime Scenarios

For preliminary planning, the standard EKS control-plane rate is assumed to be USD 0.10 per cluster-hour. Verify the current rate and applicable Kubernetes support tier before deployment.

| Runtime | Control-plane estimate |
|---|---:|
| 10 hours | USD 1 |
| 30 hours | USD 3 |
| 100 hours | USD 10 |
| 720 hours | USD 72 |

These figures exclude all supporting resources, taxes, and other charges.

Reference: https://aws.amazon.com/eks/pricing/

## 5. Daily Deployment Workflow

### Before deployment

- Confirm the task requires AWS.
- Review current spend and available credits.
- Estimate the cost of the proposed resources and runtime.
- Confirm the cleanup procedure and resource dependencies.
- Obtain approval against the ₹1,000 budget.

### During testing

- Use only the required resources.
- Capture logs, test reports, image digests, and other evidence.
- Avoid unnecessary runtime and uncontrolled load tests.
- Check for unexpected resource creation or charges.

### After testing

- Preserve test evidence and relevant configuration.
- Destroy temporary resources when appropriate.
- Verify that compute, networking, load balancers, and temporary storage have been removed.
- Inspect remaining billable resources.
- Record the day's deployment and cost observations.

## 6. Resource Lifecycle Policy

| Resource | Default policy |
|---|---|
| EKS cluster and temporary worker nodes | Create for approved integration tests; destroy when no longer needed. |
| NAT gateway and load balancer | Avoid unless required; remove temporary instances after testing. |
| Temporary disks and snapshots | Retain only when needed; verify deletion and dependencies. |
| ECR images | Keep required evidence and useful artifacts; apply deliberate retention rules. |
| Terraform state | Preserve securely for safe infrastructure management. |
| IAM and OIDC configuration | Retain reviewed reusable configuration when appropriate. |
| Logs and test evidence | Retain only as needed, with a documented retention policy. |

Terraform destroy must never be run blindly. Verify resource ownership, dependencies, and state before deletion.

## 7. Budget Approval Gate

Before creating chargeable resources, record:

- Verified available credits and expiry, if applicable
- Current billing status and existing spend
- Estimated cost of every planned resource
- Planned deployment duration
- Estimated taxes and currency assumptions
- Cleanup and verification procedure
- Expected remaining budget

A budget alert is not a hard spending cap. Charges may continue until resources are actually removed, and some resources may persist independently.

## 8. Decision Rule

If the proposed EKS configuration cannot fit the remaining budget:

- Do not provision it.
- Continue application, container, Terraform, and documentation work where possible.
- Record the deployment tests blocked by the constraint.
- Reassess only when verified credits, budget, or architecture feasibility changes.

Do not replace EKS with local Kubernetes without an explicit scope decision.

## 9. Current Status

- Target budget: ₹1,000
- AWS region: ap-south-1
- Docker: verified running
- AWS CLI authentication: verified
- Current credits: not yet verified
- Complete deployment estimate: pending
- AWS infrastructure provisioning: not approved
