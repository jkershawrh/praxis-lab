import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "deploy/rhpds/render_config.py"


def load_module():
    spec = importlib.util.spec_from_file_location("render_config", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def filters_by_name(config):
    return {
        item["filter"]: item
        for chain in config["filter_chains"]
        for item in chain["filters"]
    }


def test_https_backend_sets_endpoint_sni_host_and_secret_reference():
    config = load_module().render("https://models.example.com/v1")
    filters = filters_by_name(config)
    cluster = filters["load_balancer"]["clusters"][0]
    credential = filters["credential_injection"]["clusters"][0]

    assert cluster["endpoints"] == ["models.example.com:443"]
    assert cluster["tls"] == {"sni": "models.example.com"}
    assert filters["headers"]["request_set"] == [{"name": "Host", "value": "models.example.com"}]
    assert credential["env_var"] == "MODEL_API_KEY"
    assert "value" not in credential
    assert "insecure_options" not in config


@pytest.mark.parametrize(
    "url",
    [
        "models.example.com",
        "ftp://models.example.com",
        "https://user:password@models.example.com",
        "https://models.example.com/v2",
        "https://models.example.com/v1?token=secret",
    ],
)
def test_unsafe_or_unsupported_backend_urls_are_rejected(url):
    with pytest.raises(ValueError):
        load_module().render(url)

