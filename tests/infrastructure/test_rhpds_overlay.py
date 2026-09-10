import subprocess
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
OVERLAY = ROOT / "deploy/kustomize/overlays/rhpds"


def render():
    result = subprocess.run(
        ["kubectl", "kustomize", str(OVERLAY)],
        check=True,
        capture_output=True,
        text=True,
    )
    return [item for item in yaml.safe_load_all(result.stdout) if item]


def test_rhpds_overlay_removes_public_route_and_mock_backend():
    resources = render()
    names = {(item["kind"], item["metadata"]["name"]) for item in resources}

    assert ("Route", "praxis-ai") not in names
    assert ("Deployment", "mock-backend") not in names
    assert ("Service", "mock-backend") not in names
    assert ("Deployment", "praxis-ai") in names
    assert ("Service", "praxis-ai") in names


def test_rhpds_overlay_requires_externally_rendered_configmap():
    resources = render()
    names = {(item["kind"], item["metadata"]["name"]) for item in resources}

    assert ("ConfigMap", "praxis-ai-config") not in names
    deployment = next(item for item in resources if item["kind"] == "Deployment")
    config_volume = next(
        volume
        for volume in deployment["spec"]["template"]["spec"]["volumes"]
        if volume["name"] == "config"
    )
    assert config_volume["configMap"]["name"] == "praxis-ai-config"
