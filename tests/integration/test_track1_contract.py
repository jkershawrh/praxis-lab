from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def test_praxis_routes_v1_to_mock_backend_and_injects_secret():
    config = yaml.safe_load((ROOT / "config/praxis/track1-mock.yaml").read_text())
    filters = {
        item["filter"]: item
        for chain in config["filter_chains"]
        for item in chain["filters"]
    }

    route = filters["router"]["routes"][0]
    cluster = filters["load_balancer"]["clusters"][0]
    credential = filters["credential_injection"]["clusters"][0]

    assert route == {"path_prefix": "/v1/", "cluster": "model-backend"}
    assert cluster["name"] == "model-backend"
    assert cluster["endpoints"] == ["mock-backend:8000"]
    assert credential["name"] == "model-backend"
    assert credential["env_var"] == "MODEL_API_KEY"
    assert credential["strip_client_credential"] is True

