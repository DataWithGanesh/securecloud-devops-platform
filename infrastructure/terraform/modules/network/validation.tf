locals {
  all_subnet_cidrs = concat(
    var.public_subnet_cidrs,
    var.private_subnet_cidrs
  )
}

check "subnet_cidr_layout" {
  assert {
    condition = alltrue([
      for cidr in local.all_subnet_cidrs :
      can(cidrhost(var.vpc_cidr, 0)) &&
      can(cidrhost(cidr, 0))
    ])

    error_message = "The VPC and all subnet CIDRs must be valid CIDR ranges."
  }
}
