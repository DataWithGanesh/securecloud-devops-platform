
# Application security groups are defined as reference infrastructure.
# No AWS resources are deployed by this code alone.

resource "aws_security_group" "alb" {
  count = var.enable_application_security_groups ? 1 : 0

  name_prefix = "${var.project_name}-${var.environment}-alb-"
  description = "Controls HTTPS ingress to the application load balancer"
  vpc_id      = aws_vpc.this.id

  # Ingress and egress are defined explicitly below.
  ingress = []
  egress  = []

  tags = {
    Name = "${var.project_name}-${var.environment}-alb-sg"
    Tier = "public"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "application" {
  count = var.enable_application_security_groups ? 1 : 0

  name_prefix = "${var.project_name}-${var.environment}-app-"
  description = "Allows application traffic only from the load balancer"
  vpc_id      = aws_vpc.this.id

  # No direct public ingress and no unrestricted default egress.
  ingress = []
  egress  = []

  tags = {
    Name = "${var.project_name}-${var.environment}-app-sg"
    Tier = "private"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Only explicitly approved IPv4 CIDRs can initiate HTTPS connections.
# An empty allowed_https_cidrs list creates no ingress rules.
resource "aws_vpc_security_group_ingress_rule" "alb_https" {
  for_each = var.enable_application_security_groups ? toset(var.allowed_https_cidrs) : toset([])

  security_group_id = aws_security_group.alb[0].id
  description       = "HTTPS from approved client CIDR ${each.value}"

  cidr_ipv4   = each.value
  ip_protocol = "tcp"
  from_port   = 443
  to_port     = 443
}

# The load balancer can send traffic only to the application port
# on the application security group.
resource "aws_vpc_security_group_egress_rule" "alb_to_application" {
  count = var.enable_application_security_groups ? 1 : 0

  security_group_id            = aws_security_group.alb[0].id
  referenced_security_group_id = aws_security_group.application[0].id
  description                  = "Forward traffic to the application port"

  ip_protocol = "tcp"
  from_port   = var.application_port
  to_port     = var.application_port
}

# The application accepts traffic on its configured port only
# when the source is the load balancer security group.
resource "aws_vpc_security_group_ingress_rule" "application_from_alb" {
  count = var.enable_application_security_groups ? 1 : 0

  security_group_id            = aws_security_group.application[0].id
  referenced_security_group_id = aws_security_group.alb[0].id
  description                  = "Application traffic from the load balancer only"

  ip_protocol = "tcp"
  from_port   = var.application_port
  to_port     = var.application_port
}
