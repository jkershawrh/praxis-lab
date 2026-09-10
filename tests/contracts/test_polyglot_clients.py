from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
CLIENTS = {
    "python": ROOT / "clients/python/client.py",
    "typescript": ROOT / "clients/typescript/client.ts",
    "java": ROOT / "clients/java/src/main/java/com/redhat/praxis/PraxisClient.java",
}


def test_all_clients_use_only_the_praxis_endpoint_contract():
    for language, path in CLIENTS.items():
        source = path.read_text()
        assert "PRAXIS_BASE_URL" in source, language
        assert "/v1/chat/completions" in source, language
        assert "MODEL_BASE_URL" not in source, language
        assert "MODEL_API_KEY" not in source, language
        assert "maas" not in source.lower(), language
        assert "litellm" not in source.lower(), language


def test_shared_openapi_contract_is_backend_neutral():
    contract = yaml.safe_load((ROOT / "contracts/openapi/praxis-client.yaml").read_text())

    assert contract["paths"]["/v1/chat/completions"]["post"]
    serialized = str(contract).lower()
    assert "maas" not in serialized
    assert "litellm" not in serialized

