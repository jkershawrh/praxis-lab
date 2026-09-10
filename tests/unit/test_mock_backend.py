import importlib.util
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "backend/mock_server.py"


def load_module():
    spec = importlib.util.spec_from_file_location("mock_server", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_chat_response_preserves_requested_model():
    module = load_module()
    payload = {"model": "test-model", "messages": [{"role": "user", "content": "hello"}]}

    status, response = module.build_response("/v1/chat/completions", payload)

    assert status == 200
    assert response["model"] == "test-model"
    assert response["choices"][0]["message"]["role"] == "assistant"


def test_invalid_path_fails_closed():
    module = load_module()

    status, response = module.build_response("/unknown", {})

    assert status == 404
    assert response == {"error": {"message": "not found", "type": "invalid_request_error"}}


def test_deployed_mock_implements_the_tested_contract():
    documents = yaml.safe_load_all((ROOT / "deploy/kustomize/base/mock-backend.yaml").read_text())
    configmap = next(document for document in documents if document["kind"] == "ConfigMap")
    deployed = configmap["data"]["mock_server.py"]

    assert 'path == "/v1/chat/completions"' in deployed
    assert 'os.environ.get("EXPECTED_API_KEY"' in deployed
    assert '"usage":' in deployed
