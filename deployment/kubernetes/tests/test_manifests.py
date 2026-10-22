import unittest
from pathlib import Path

import yaml


BASE = Path(__file__).resolve().parent.parent / "demo-api"


def load_manifest(filename):
    with (BASE / filename).open(encoding="utf-8-sig") as file:
        return yaml.safe_load(file)


class TestKubernetesManifests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.namespace = load_manifest("namespace.yaml")
        cls.deployment = load_manifest("deployment.yaml")
        cls.service = load_manifest("service.yaml")
        cls.pod = cls.deployment["spec"]["template"]
        cls.container = cls.pod["spec"]["containers"][0]

    def test_namespace(self):
        self.assertEqual(self.namespace["kind"], "Namespace")
        self.assertEqual(self.namespace["metadata"]["name"], "securecloud")

    def test_deployment_namespace_and_replicas(self):
        self.assertEqual(self.deployment["kind"], "Deployment")
        self.assertEqual(self.deployment["metadata"]["namespace"], "securecloud")
        self.assertEqual(self.deployment["spec"]["replicas"], 2)

    def test_service_namespace_and_type(self):
        self.assertEqual(self.service["kind"], "Service")
        self.assertEqual(self.service["metadata"]["namespace"], "securecloud")
        self.assertEqual(self.service["spec"]["type"], "ClusterIP")

    def test_service_selector_matches_pod_labels(self):
        labels = self.pod["metadata"]["labels"]
        selector = self.service["spec"]["selector"]
        self.assertTrue(all(labels.get(key) == value for key, value in selector.items()))

    def test_http_port(self):
        self.assertTrue(any(
            port.get("name") == "http" and port.get("containerPort") == 8000
            for port in self.container["ports"]
        ))

    def test_health_probes(self):
        self.assertEqual(
            self.container["livenessProbe"]["httpGet"]["path"], "/health/live"
        )
        self.assertEqual(
            self.container["readinessProbe"]["httpGet"]["path"], "/health/ready"
        )

    def test_non_root_security(self):
        security = self.pod["spec"]["securityContext"]
        self.assertTrue(security["runAsNonRoot"])
        self.assertEqual(security["runAsUser"], 10001)
        self.assertEqual(security["runAsGroup"], 10001)

    def test_container_security(self):
        security = self.container["securityContext"]
        self.assertFalse(security["allowPrivilegeEscalation"])
        self.assertTrue(security["readOnlyRootFilesystem"])
        self.assertEqual(security["capabilities"]["drop"], ["ALL"])

    def test_resource_requests_and_limits(self):
        resources = self.container["resources"]
        for section in ("requests", "limits"):
            for resource in ("cpu", "memory"):
                with self.subTest(section=section, resource=resource):
                    self.assertIn(resource, resources[section])

    def test_service_targets_named_http_port(self):
        self.assertEqual(self.service["spec"]["ports"][0]["targetPort"], "http")


if __name__ == "__main__":
    unittest.main(verbosity=2)
