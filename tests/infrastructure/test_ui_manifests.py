from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "deploy/kustomize/base"


def documents(path):
    return [item for item in yaml.safe_load_all(path.read_text()) if item]


def test_ui_container_uses_ubi_and_non_root_user():
    containerfile = (ROOT / "src/Containerfile").read_text()

    assert containerfile.startswith("FROM registry.access.redhat.com/ubi9/python-312:")
    assert "USER 1001" in containerfile
    assert "EXPOSE 7860" in containerfile


def test_base_deploys_routable_ui_with_gateway_only_configuration():
    all_documents = [item for path in BASE.glob("*.yaml") for item in documents(path)]
    deployment = next(item for item in all_documents if item.get("kind") == "Deployment" and item["metadata"]["name"] == "praxis-ui")
    service = next(item for item in all_documents if item.get("kind") == "Service" and item["metadata"]["name"] == "praxis-ui")
    route = next(item for item in all_documents if item.get("kind") == "Route" and item["metadata"]["name"] == "praxis-ui")
    container = deployment["spec"]["template"]["spec"]["containers"][0]
    env = {item["name"]: item["value"] for item in container["env"]}

    assert env == {"PRAXIS_BASE_URL": "http://praxis-ai:8080", "PRAXIS_MODEL": "lab-model"}
    assert container["image"].startswith("quay.io/redhat-gpte/praxis-ai-gateway-ui@sha256:")
    assert service["spec"]["ports"][0]["port"] == 7860
    assert route["spec"]["to"]["name"] == "praxis-ui"
    assert route["spec"]["tls"]["insecureEdgeTerminationPolicy"] == "Redirect"
    assert container["securityContext"]["readOnlyRootFilesystem"] is True
    assert container["securityContext"]["allowPrivilegeEscalation"] is False


def test_rhpds_keeps_ui_route_but_removes_direct_gateway_route():
    overlay = (ROOT / "deploy/kustomize/overlays/rhpds/remove-lab-resources.yaml").read_text()
    oauth = (ROOT / "deploy/kustomize/overlays/rhpds/ui-oauth-patch.yaml").read_text()
    resources = (ROOT / "deploy/kustomize/overlays/rhpds/ui-oauth-resources.yaml").read_text()

    assert "name: praxis-ai\n" in overlay
    assert "name: praxis-ui\n" not in overlay
    assert "termination: reencrypt" in oauth
    assert "openshift-service-account=praxis-ui" in oauth
    assert "cookie-secret-file" in oauth
    assert "system:auth-delegator" in resources
