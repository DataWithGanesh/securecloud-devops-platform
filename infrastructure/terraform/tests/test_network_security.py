"""Regression tests for SecureCloud Terraform network security settings.

These tests inspect Terraform source files. They do not connect to AWS
or verify the security of any deployed infrastructure.
"""

import re
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

NETWORK_MODULE = (
    PROJECT_ROOT
    / "infrastructure"
    / "terraform"
    / "modules"
    / "network"
)

MAIN_FILE = NETWORK_MODULE / "main.tf"
SECURITY_GROUPS_FILE = NETWORK_MODULE / "security-groups.tf"
VARIABLES_FILE = NETWORK_MODULE / "variables.tf"


def read_terraform_file(path: Path) -> str:
    """Read a Terraform source file or fail with a useful error."""
    if not path.is_file():
        raise FileNotFoundError(
            f"Required Terraform file not found: {path}"
        )

    return path.read_text(encoding="utf-8")


class TestNetworkSecurity(unittest.TestCase):
    """Check important network security defaults and restrictions."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.main = read_terraform_file(MAIN_FILE)
        cls.security_groups = read_terraform_file(
            SECURITY_GROUPS_FILE
        )
        cls.variables = read_terraform_file(VARIABLES_FILE)

    def test_public_subnets_do_not_auto_assign_public_ips(self):
        """Public subnets must disable automatic public IP assignment."""
        public_subnet = re.search(
            r'resource\s+"aws_subnet"\s+"public"\s*\{(.*?)\n\}',
            self.main,
            re.DOTALL,
        )

        self.assertIsNotNone(
            public_subnet,
            "Could not find the public subnet resource.",
        )

        self.assertRegex(
            public_subnet.group(1),
            r"map_public_ip_on_launch\s*=\s*false",
        )

    def test_private_subnets_do_not_auto_assign_public_ips(self):
        """Private subnets must disable automatic public IP assignment."""
        private_subnet = re.search(
            r'resource\s+"aws_subnet"\s+"private"\s*\{(.*?)\n\}',
            self.main,
            re.DOTALL,
        )

        self.assertIsNotNone(
            private_subnet,
            "Could not find the private subnet resource.",
        )

        self.assertRegex(
            private_subnet.group(1),
            r"map_public_ip_on_launch\s*=\s*false",
        )

    def test_https_ingress_uses_configured_cidr_allowlist(self):
        """ALB HTTPS ingress must use the configured CIDR allowlist."""
        https_rule = re.search(
            r'resource\s+"aws_vpc_security_group_ingress_rule"\s+'
            r'"alb_https"\s*\{(.*?)\n\}',
            self.security_groups,
            re.DOTALL,
        )

        self.assertIsNotNone(
            https_rule,
            "Could not find the alb_https ingress rule.",
        )

        rule = https_rule.group(1)

        self.assertRegex(rule, r"from_port\s*=\s*443")
        self.assertRegex(rule, r"to_port\s*=\s*443")
        self.assertRegex(
            rule,
            r"cidr_ipv4\s*=\s*each\.value",
        )
        self.assertRegex(
            rule,
            r"for_each\s*=.*?var\.allowed_https_cidrs",
        )

    def test_https_allowlist_defaults_to_empty(self):
        """HTTPS ingress must not be opened to the internet by default."""
        variable = re.search(
            r'variable\s+"allowed_https_cidrs"\s*\{(.*?)\n\}',
            self.variables,
            re.DOTALL,
        )

        self.assertIsNotNone(
            variable,
            "Could not find the allowed_https_cidrs variable.",
        )

        self.assertRegex(
            variable.group(1),
            r"default\s*=\s*\[\s*\]",
        )

    def test_application_ingress_is_restricted_to_alb_security_group(self):
        """Application ingress must reference the ALB security group."""
        application_rule = re.search(
            r'resource\s+"aws_vpc_security_group_ingress_rule"\s+'
            r'"application_from_alb"\s*\{(.*?)\n\}',
            self.security_groups,
            re.DOTALL,
        )

        self.assertIsNotNone(
            application_rule,
            "Could not find the application_from_alb ingress rule.",
        )

        self.assertRegex(
            application_rule.group(1),
            r"referenced_security_group_id\s*=\s*"
            r"aws_security_group\.alb\[0\]\.id",
        )

    def test_application_ingress_uses_configured_port(self):
        """Application ingress must use the configured application port."""
        application_rule = re.search(
            r'resource\s+"aws_vpc_security_group_ingress_rule"\s+'
            r'"application_from_alb"\s*\{(.*?)\n\}',
            self.security_groups,
            re.DOTALL,
        )

        self.assertIsNotNone(
            application_rule,
            "Could not find the application_from_alb ingress rule.",
        )

        rule = application_rule.group(1)

        self.assertRegex(
            rule,
            r"from_port\s*=\s*var\.application_port",
        )
        self.assertRegex(
            rule,
            r"to_port\s*=\s*var\.application_port",
        )

    def test_nat_gateway_is_disabled_by_default(self):
        """NAT Gateway creation must remain opt-in."""
        variable = re.search(
            r'variable\s+"enable_nat_gateway"\s*\{(.*?)\n\}',
            self.variables,
            re.DOTALL,
        )

        self.assertIsNotNone(
            variable,
            "Could not find the enable_nat_gateway variable.",
        )

        self.assertRegex(
            variable.group(1),
            r"default\s*=\s*false",
        )

    def test_ingress_does_not_allow_all_ipv4(self):
        """Security group ingress must not allow unrestricted IPv4 access."""
        self.assertNotRegex(
            self.security_groups,
            r'cidr_ipv4\s*=\s*"0\.0\.0\.0/0"',
        )

    def test_ingress_does_not_allow_all_ipv6(self):
        """Security group ingress must not allow unrestricted IPv6 access."""
        self.assertNotRegex(
            self.security_groups,
            r'cidr_ipv6\s*=\s*"::/0"',
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)