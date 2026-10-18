module "network" {
  source = "./modules/network"

  vpc_cidr           = "10.20.0.0/16"
  project_name       = var.project_name
  environment        = var.environment
  availability_zones = ["ap-south-1a", "ap-south-1b"]

  public_subnet_cidrs = [
    "10.20.0.0/20",
    "10.20.16.0/20"
  ]

  private_subnet_cidrs = [
    "10.20.32.0/20",
    "10.20.48.0/20"
  ]

  enable_nat_gateway = false
}
