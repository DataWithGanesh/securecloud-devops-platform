# SecureCloud - Argo CD GitOps Configuration

## 1. Overview

This directory contains the Argo CD Application manifest for the SecureCloud demo API.

The configuration describes how Argo CD can track the Git repository, read the Helm chart, and reconcile the application's desired state in a Kubernetes cluster.

**Scope:** Configuration and repository validation only. No Kubernetes cluster deployment or AWS resource provisioning is performed as part of this milestone.

## 2. Repository Structure

```text
deployment/
|-- argocd/
|   |-- application.yaml
|   `-- README.md
`-- helm/
    `-- securecloud-demo-api/
        |-- Chart.yaml
        |-- values.yaml
        `-- templates/
```

## 3. Application Configuration

| Setting                   | Configured value                       |
| ------------------------- | -------------------------------------- |
| Resource kind             | `Application`                          |
| Argo CD namespace         | `argocd`                               |
| Application name          | `securecloud-demo-api`                 |
| Git branch                | `main`                                 |
| Helm chart path           | `deployment/helm/securecloud-demo-api` |
| Destination namespace     | `securecloud`                          |
| Helm release name         | `securecloud-demo-api`                 |
| Automated sync            | Enabled                                |
| Self-healing              | Enabled                                |
| Automated pruning         | Disabled                               |
| Namespace creation option | `CreateNamespace=true`                 |

The destination server is configured as `https://kubernetes.default.svc`, the Kubernetes API service address used from within a cluster.

## 4. Synchronization Behavior

### Automated synchronization

Automated synchronization is enabled in the manifest. When Argo CD is installed and configured with repository access and a destination cluster, it can reconcile the application's live state with the desired state stored in Git.

### Self-healing

`selfHeal: true` requests reconciliation when the live application state drifts from the desired state.

### Pruning

`prune: false` disables automated pruning during automated synchronization. Resources removed from Git are not automatically deleted by that automated pruning behavior.

This setting does not prohibit every possible deletion. Actual behavior also depends on the action, resource, and Argo CD configuration.

### Namespace creation

`CreateNamespace=true` requests creation of the destination namespace during synchronization if it does not exist.

These behaviors are configured in the manifest. They have not been tested against a running Argo CD installation in this project milestone.

## 5. CI Validation

The GitHub Actions workflow includes an `argocd-validation` job that:

- Parses `deployment/argocd/application.yaml` using PyYAML.
- Checks the API version and resource kind.
- Checks the application name and Argo CD namespace.
- Verifies the repository URL, branch, and Helm chart path.
- Checks the destination namespace.
- Verifies that self-healing is enabled and automated pruning is disabled.

This job validates YAML syntax and selected configuration values. It does not perform full validation against the Argo CD Application CRD schema or test synchronization with a live cluster.

## 6. Security and Operational Considerations

Before any future deployment:

- Review repository access and authentication requirements.
- Review Argo CD AppProject source and destination restrictions.
- Review automated synchronization and deletion behavior.
- Review Kubernetes RBAC and workload security settings.
- Assess AWS costs and security implications separately.
- Obtain explicit approval before provisioning infrastructure or deploying workloads.

## 7. Current Status

**Status:** Reference configuration and CI validation completed.

**Not performed:** Argo CD installation, Kubernetes synchronization, application deployment, and AWS resource provisioning.

A successful CI run confirms that the checks defined in the workflow passed for the tested commit. It does not establish that a live deployment works or that the complete system is production-ready.
