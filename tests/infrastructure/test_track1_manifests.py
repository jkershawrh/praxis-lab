from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "deploy/kustomize/base"


def documents(path: Path):
    return [document for document in yaml.safe_load_all(path.read_text()) if document]


def test_track1_has_required_openshift_resources():
    kinds = {
        document["kind"]
        for path in BASE.glob("*.yaml")
        for document in documents(path)
    }

    assert {"Deployment", "Service", "Route", "ConfigMap", "NetworkPolicy"} <= kinds


def test_praxis_image_is_pinned_and_pod_uses_restricted_security_context():
    deployment = next(
        document
        for path in BASE.glob("*.yaml")
        for document in documents(path)
        if document.get("kind") == "Deployment"
        and document["metadata"]["name"] == "praxis-ai"
    )
    pod_spec = deployment["spec"]["template"]["spec"]
    container = pod_spec["containers"][0]

    assert container["image"].startswith("ghcr.io/praxis-proxy/ai@sha256:")
    assert pod_spec["securityContext"]["runAsNonRoot"] is True
    assert container["securityContext"]["allowPrivilegeEscalation"] is False
    assert container["securityContext"]["readOnlyRootFilesystem"] is True
    assert container["securityContext"]["capabilities"]["drop"] == ["ALL"]


def test_upstream_credential_comes_from_secret_not_configmap():
    all_documents = [
        document
        for path in BASE.glob("*.yaml")
        for document in documents(path)
    ]
    deployment = next(
        document
        for document in all_documents
        if document.get("kind") == "Deployment" and document["metadata"]["name"] == "praxis-ai"
    )
    configmap = next(
        document
        for document in all_documents
        if document.get("kind") == "ConfigMap" and document["metadata"]["name"] == "praxis-ai-config"
    )
    env = deployment["spec"]["template"]["spec"]["containers"][0]["env"]

    assert any(item.get("valueFrom", {}).get("secretKeyRef", {}).get("key") == "api-key" for item in env)
    assert "api-key" not in str(configmap).lower()
    assert "MODEL_API_KEY" in configmap["data"]["praxis-ai.yaml"]


def test_admin_health_port_is_not_exposed_by_service():
    service = next(
        document
        for path in BASE.glob("*.yaml")
        for document in documents(path)
        if document.get("kind") == "Service" and document["metadata"]["name"] == "praxis-ai"
    )

    assert [port["port"] for port in service["spec"]["ports"]] == [8080]
