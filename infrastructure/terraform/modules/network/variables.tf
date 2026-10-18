
variable "vpc_cidr" {
  description = "IPv4 CIDR range for the SecureCloud VPC"
  type        = string
  default     = "10.20.0.0/16"

  validation {
    condition = (
      can(cidrhost(var.vpc_cidr, 0)) &&
      can(regex("^[0-9.]+/[0-9]+$", var.vpc_cidr))
    )
    error_message = "The VPC CIDR must be a valid IPv4 CIDR range."
  }
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

variable "availability_zones" {
  description = "Two distinct AWS Availability Zones for the network"
  type        = list(string)
  default     = ["ap-south-1a", "ap-south-1b"]

  validation {
    condition = (
      length(var.availability_zones) == 2 &&
      length(distinct(var.availability_zones)) == 2
    )
    error_message = "Provide exactly two distinct Availability Zones."
  }
}

variable "public_subnet_cidrs" {
  description = "CIDR ranges for the two public subnets"
  type        = list(string)
  default     = ["10.20.0.0/20", "10.20.16.0/20"]

  validation {
    condition     = length(var.public_subnet_cidrs) == 2
    error_message = "Exactly two public subnet CIDRs must be provided."
  }

  validation {
    condition = alltrue([
      for cidr in var.public_subnet_cidrs :
      can(cidrhost(cidr, 0)) && can(regex("^[0-9.]+/[0-9]+$", cidr))
    ])
    error_message = "Every public subnet CIDR must be a valid IPv4 CIDR range."
  }
}

variable "private_subnet_cidrs" {
  description = "CIDR ranges for the two private subnets"
  type        = list(string)
  default     = ["10.20.32.0/20", "10.20.48.0/20"]

  validation {
    condition     = length(var.private_subnet_cidrs) == 2
    error_message = "Exactly two private subnet CIDRs must be provided."
  }

  validation {
    condition = alltrue([
      for cidr in var.private_subnet_cidrs :
      can(cidrhost(cidr, 0)) && can(regex("^[0-9.]+/[0-9]+$", cidr))
    ])
    error_message = "Every private subnet CIDR must be a valid IPv4 CIDR range."
  }
}

variable "enable_nat_gateway" {
  description = "Whether to create a NAT Gateway (incurs AWS charges)"
  type        = bool
  default     = false
}
