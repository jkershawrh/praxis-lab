import importlib.util
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "src/ui.py"


def load_module():
    spec = importlib.util.spec_from_file_location("ui", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_traceparent_is_w3c_shaped_and_unique():
    module = load_module()
    first = module.new_traceparent()
    second = module.new_traceparent()

    assert re.fullmatch(r"00-[0-9a-f]{32}-[0-9a-f]{16}-01", first)
    assert first != second


def test_ui_topology_preserves_backend_boundary():
    module = load_module()

    assert "Application client" in module.TOPOLOGY
    assert "Praxis AI Gateway" in module.TOPOLOGY
    assert "Configured model backend" in module.TOPOLOGY
    assert "MaaS" not in module.TOPOLOGY
    assert "LiteLLM" not in module.TOPOLOGY


def test_invoke_does_not_send_authorization(monkeypatch):
    module = load_module()
    captured = {}

    class Response:
        status_code = 200

        @staticmethod
        def json():
            return {"model": "lab-model", "choices": []}

    def fake_post(url, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return Response()

    monkeypatch.setattr(module.httpx, "post", fake_post)
    summary, _ = module.invoke("hello", "lab-model", base_url="https://praxis.example.com")

    assert captured["url"] == "https://praxis.example.com/v1/chat/completions"
    assert "Authorization" not in captured["headers"]
    assert "traceparent" in captured["headers"]
    assert summary["status"] == 200
