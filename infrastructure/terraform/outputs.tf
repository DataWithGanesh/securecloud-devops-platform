output "aws_region" {
  description = "AWS region configured for SecureCloud"
  value       = var.aws_region
}

output "project_name" {
  description = "SecureCloud project name"
  value       = var.project_name
}

output "environment" {
  description = "Configured deployment environment"
  value       = var.environment
}
