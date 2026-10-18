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
