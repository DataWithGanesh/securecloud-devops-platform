# SecureCloud AWS Network Architecture

## 1. Purpose

Define the planned network architecture for the SecureCloud
DevOps and SRE platform. This document describes reference
configuration only; it does not represent deployed AWS resources.

## 2. AWS Region

- Region: ap-south-1
- Availability Zones: two zones selected within the region

## 3. VPC Design

- VPC CIDR: 10.20.0.0/16
- Public subnets: two
- Private subnets: two
- Internet Gateway: included in the design
- Route tables: separate public and private routing
- Security groups: least-privilege traffic rules
- Network ACLs: use defaults initially; customize only when justified

## 3.1 Subnet CIDR Allocation

VPC CIDR: 10.20.0.0/16

| Subnet       | Availability Zone | CIDR          | Purpose                  |
| ------------ | ----------------- | ------------- | ------------------------ |
| Public AZ-A  | AZ-A              | 10.20.0.0/20  | Ingress and optional NAT |
| Public AZ-B  | AZ-B              | 10.20.16.0/20 | Ingress and optional NAT |
| Private AZ-A | AZ-A              | 10.20.32.0/20 | EKS nodes and workloads  |
| Private AZ-B | AZ-B              | 10.20.48.0/20 | EKS nodes and workloads  |

Each subnet uses a /20 IPv4 range. AWS reserves five IPv4 addresses
per subnet, so the usable address count is lower than the total.

These CIDRs are planned values and have not been created in AWS.

## 4. Public Subnets

Intended uses:

- Internet-facing application load balancer, if required
- NAT Gateway, when explicitly enabled

Public subnet placement does not automatically make a resource
publicly accessible. Routing, addressing, and security rules
must also permit the intended traffic.

## 5. Private Subnets

Intended uses:

- EKS worker nodes
- Application workloads
- Internal services

Private workloads should not receive direct inbound internet access.
Required outbound connectivity must be designed explicitly.

## 6. NAT Gateway Strategy

- Disabled by default in the reference configuration.
- Document the required public-subnet placement and route changes.
- Evaluate hourly, data-processing, Elastic IP, and related costs.
- Do not create NAT Gateways in AWS for this project.

## 7. Administrative Access

- Preferred design: Systems Manager Session Manager when supported.
- Traditional bastion host: documented as an alternative only.
- No publicly exposed SSH access is planned by default.
- Do not create a bastion host in AWS for this project.

## 8. VPC Endpoints

Evaluate endpoints for the AWS services required by the workloads.
Compare endpoint charges against NAT Gateway and data-transfer costs.
Do not create endpoints in AWS for this project.

## 9. Security Requirements

- Restrict inbound traffic to explicitly required ports and sources.
- Keep worker nodes in private subnets.
- Apply least-privilege IAM permissions.
- Avoid hard-coded credentials and secrets.
- Enable logging and monitoring in the future reference design.

## 10. Cost and Deployment Guardrails

- This repository is a reference implementation.
- No AWS infrastructure is to be provisioned during development.
- Do not run terraform apply.
- Review costs and billing visibility before any future deployment.
- AWS Budgets provides notifications; it is not a hard spending cap.

## 11. Validation

Validate Terraform syntax and formatting locally.
Document AWS-dependent checks as unverified until tested in AWS.
