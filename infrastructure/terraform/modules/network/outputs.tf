output "vpc_id" {
  description = "ID of the SecureCloud VPC"
  value       = aws_vpc.this.id
}

output "vpc_cidr" {
  description = "IPv4 CIDR range of the SecureCloud VPC"
  value       = aws_vpc.this.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.this.id
}


output "alb_security_group_id" {
  description = "ID of the application load balancer security group"
  value       = try(aws_security_group.alb[0].id, null)
}

output "application_security_group_id" {
  description = "ID of the application security group"
  value       = try(aws_security_group.application[0].id, null)
}
