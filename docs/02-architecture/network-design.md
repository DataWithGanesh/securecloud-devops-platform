# SecureCloud — Network Design

**Document ID:** SC-NET-001  
**Version:** 1.0  
**Status:** Draft — Design review required  
**AWS Region:** ap-south-1 (Mumbai)

---

## 1. Purpose

Define the proposed AWS network boundaries and traffic flows for SecureCloud before any network resources are provisioned.

## 2. Network Objectives

- Isolate application workloads within a dedicated VPC.
- Minimize unnecessary public exposure.
- Support the Amazon EKS deployment requirement.
- Document ingress, egress, and administrative access paths.
- Keep network costs within the approved project budget.
- Make network configuration reproducible through Terraform.

## 3. Proposed VPC

| Setting | Proposed Value | Status |
|---|---|---|
| AWS Region | ap-south-1 | Selected |
| VPC CIDR | 10.0.0.0/16 | Proposed |
| Public subnet example | 10.0.1.0/24 | Proposed |
| Private subnet example A | 10.0.2.0/24 | Proposed |
| Private subnet example B | 10.0.3.0/24 | Proposed |
| Availability Zones | To be selected during detailed design | Pending |

The CIDRs are planning examples, not provisioned resources. Check for overlap with any networks used by the engineer before finalizing them.

## 4. Subnet Responsibilities

### Public Subnets

Potential uses:
- Internet-facing load-balancer resources, if required.
- Internet Gateway routing for explicitly approved public resources.

Public subnets must not automatically expose worker nodes or application management interfaces.

### Private Subnets

Potential uses:
- EKS worker nodes.
- Application workloads.
- Internal services.

Private subnet placement does not by itself guarantee that a workload is secure. Security groups, IAM, routing, endpoint access, and workload policies must also be reviewed.

## 5. Ingress Design

The proposed application ingress path is:

Client → HTTPS endpoint → approved ingress/load-balancing component → Kubernetes Service → application Pod.

The final ingress implementation depends on the selected EKS design and the budget assessment.

Before deployment:
- Select the required ingress component.
- Determine whether a public endpoint is necessary.
- Restrict administrative access.
- Document TLS certificate handling.
- Estimate load-balancer and public IPv4 charges.

## 6. Egress Design

EKS nodes and workloads may need outbound access to retrieve images, download dependencies, or call approved services.

Evaluate these options before deployment:
- NAT Gateway.
- NAT instance or other supported network architecture.
- Relevant AWS service endpoints.
- A controlled alternative appropriate to the workload.

Do not create a NAT Gateway by default. Its hourly and data-processing charges may consume a significant portion of the budget.

## 7. EKS Network Considerations

The detailed EKS design must specify:
- Cluster endpoint access mode.
- Control-plane and node communication requirements.
- Node subnet placement.
- Security-group rules.
- Required DNS and outbound connectivity.
- Pod networking and available IP capacity.
- Administrative access and audit requirements.

Exact rules must be validated against current Amazon EKS requirements before provisioning.

## 8. Security Boundaries

- Permit only required inbound traffic.
- Avoid unrestricted administrative ports.
- Use least-privilege security-group rules.
- Keep credentials out of network configuration files.
- Review public endpoint exposure.
- Record required traffic between CI, AWS services, EKS, and observability components.
- Enable relevant network logging only after reviewing its storage and ingestion cost.

## 9. Cost Controls

Before creating network resources:
1. Estimate public IPv4 and load-balancer charges.
2. Estimate NAT hourly and data-processing charges.
3. Evaluate service endpoints and their costs.
4. Define the deployment window.
5. Document the cleanup plan.
6. Verify that the complete deployment remains within the approved budget.

## 10. Cleanup Requirements

After temporary testing:
- Remove temporary load balancers and network resources when safe.
- Verify that temporary NAT resources have been removed.
- Review public IP addresses, elastic network interfaces, and associated resources.
- Check for remaining billable components.
- Preserve reusable Terraform code and required state.

## 11. Open Decisions

- Final VPC and subnet CIDRs.
- Number of Availability Zones.
- EKS endpoint access configuration.
- Public versus private ingress.
- Outbound connectivity approach.
- Whether a NAT Gateway is necessary.
- Whether an Application Load Balancer is necessary.
- Network logging configuration and retention.

## 12. Status

Draft network design. No AWS network resources are implied to exist. Finalize after cost, security, and EKS feasibility reviews.
