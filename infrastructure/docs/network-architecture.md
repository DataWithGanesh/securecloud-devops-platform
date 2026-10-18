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

### 9.1 Application Load Balancer Security Group

The reference configuration defines an ALB security group with
explicit ingress and egress rules.

- Inbound: TCP 443 only from CIDRs listed in `allowed_https_cidrs`.
- Default: `allowed_https_cidrs` is empty, so no HTTPS ingress
  rules are created.
- Outbound: TCP traffic to the application security group on
  `application_port` only.
- Do not use `0.0.0.0/0` as an approved source without an explicit
  security review and justification.

An ALB, HTTPS listener, TLS certificate, and target group are not
created by this security-group configuration.

### 9.2 Application Security Group

- Inbound: TCP traffic on `application_port` only from the ALB
  security group.
- Default application port: 8000, matching the current demo API
  container configuration.
- No direct public ingress rule is defined.
- Outbound: no egress rules are defined initially.

The restrictive outbound policy may prevent access to external APIs,
databases, telemetry backends, or other dependencies. If dependencies
are introduced, document and add only the required outbound rules.

### 9.3 Security-Group Controls

- `enable_application_security_groups` controls whether these
  security groups and their associated rules are defined.
- Security-group IDs are exposed through the network module outputs
  for future infrastructure integration.
- Security groups are stateful; response traffic for permitted
  connections is automatically allowed.
- Keep ingress and egress rules explicit and narrowly scoped.
- Do not introduce direct public access to application workloads.
- Do not hard-code credentials or secrets.

### 9.4 Validation Limitations

Terraform formatting and validation check configuration structure
and syntax; they do not prove runtime reachability or effective
security in AWS.

No AWS-dependent checks have been performed. The security-group
configuration remains a reference design until independently
reviewed and tested in an approved environment.

## 10. Cost and Deployment Guardrails

- This repository is a reference implementation.
- No AWS infrastructure is to be provisioned during development.
- Do not run `terraform apply`.
- Do not create AWS resources for this project.
- Review costs and billing visibility before any future deployment.
- AWS Budgets provides notifications; it is not a hard spending cap.

## 11. Validation

Validate Terraform syntax and formatting locally.
Run the local network CIDR validation test.
Document AWS-dependent checks as unverified until tested in AWS.
