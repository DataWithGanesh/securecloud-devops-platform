variable "aws_region" {
  description = "AWS region for SecureCloud infrastructure"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name used for resource naming and tagging"
  type        = string
  default     = "SecureCloud"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
