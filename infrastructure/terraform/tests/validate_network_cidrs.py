import ipaddress
import re
import sys
from pathlib import Path

TERRAFORM_FILE = (
    Path(__file__).resolve().parents[1] / "main.tf"
)


def read_cidr_list(content: str, variable_name: str) -> list[str]:
    pattern = (
        rf'{re.escape(variable_name)}\s*=\s*\[(.*?)\]'
    )
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        raise ValueError(
            f"Could not find {variable_name} in {TERRAFORM_FILE}"
        )

    return re.findall(r'"([^"]+)"', match.group(1))


def read_vpc_cidr(content: str) -> str:
    match = re.search(
        r'vpc_cidr\s*=\s*"([^"]+)"',
        content,
    )

    if not match:
        raise ValueError(
            f"Could not find vpc_cidr in {TERRAFORM_FILE}"
        )

    return match.group(1)


def validate_network(vpc_cidr: str, subnet_cidrs: list[str]) -> None:
    vpc = ipaddress.ip_network(vpc_cidr, strict=True)
    subnets = [
        ipaddress.ip_network(cidr, strict=True)
        for cidr in subnet_cidrs
    ]

    if not subnets:
        raise ValueError("At least one subnet must be configured.")

    for subnet in subnets:
        if not subnet.subnet_of(vpc):
            raise ValueError(
                f"Subnet {subnet} is not fully contained in VPC {vpc}"
            )

    for index, subnet in enumerate(subnets):
        for other in subnets[index + 1:]:
            if subnet.overlaps(other):
                raise ValueError(
                    f"Subnet ranges overlap: {subnet} and {other}"
                )

    print(f"PASS: All subnets are contained in VPC {vpc}.")
    print("PASS: No subnet CIDR ranges overlap.")


def main() -> int:
    try:
        content = TERRAFORM_FILE.read_text(encoding="utf-8")

        vpc_cidr = read_vpc_cidr(content)
        public_cidrs = read_cidr_list(
            content, "public_subnet_cidrs"
        )
        private_cidrs = read_cidr_list(
            content, "private_subnet_cidrs"
        )

        validate_network(
            vpc_cidr,
            public_cidrs + private_cidrs,
        )
        return 0

    except (OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())