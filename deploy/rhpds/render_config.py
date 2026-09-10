"""Render a Praxis v0.3.0 config from the backend-neutral lab contract."""

import argparse
from pathlib import Path
from urllib.parse import urlparse

import yaml


PRIVATE_SUFFIXES = (".cluster.local", ".svc", ".svc.cluster.local")


def backend_from_url(value: str):
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("MODEL_BASE_URL must use http or https")
    if not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("MODEL_BASE_URL must contain only a scheme, host, optional port, and optional /v1 path")
    if parsed.path not in {"", "/", "/v1", "/v1/"}:
        raise ValueError("MODEL_BASE_URL path must be empty or /v1")

    tls = parsed.scheme == "https"
    port = parsed.port or (443 if tls else 80)
    cluster = {"name": "model-backend", "endpoints": [f"{parsed.hostname}:{port}"]}
    if tls:
        cluster["tls"] = {"sni": parsed.hostname}
    return cluster, parsed.hostname


def render(model_base_url: str):
    cluster, hostname = backend_from_url(model_base_url)
    config = {
        "listeners": [
            {
                "name": "ai-gateway",
                "address": "0.0.0.0:8080",
                "filter_chains": ["access-control", "model-routing", "upstream-credentials"],
            }
        ],
        "filter_chains": [
            {
                "name": "access-control",
                "filters": [
                    {
                        "filter": "ip_acl",
                        "allow": [
                            "10.0.0.0/8",
                            "172.16.0.0/12",
                            "192.168.0.0/16",
                            "127.0.0.1/32",
                        ],
                    }
                ],
            },
            {
                "name": "model-routing",
                "filters": [
                    {
                        "filter": "router",
                        "routes": [{"path_prefix": "/v1/", "cluster": "model-backend"}],
                    },
                    {"filter": "headers", "request_set": [{"name": "Host", "value": hostname}]},
                    {"filter": "load_balancer", "clusters": [cluster]},
                ],
            },
            {
                "name": "upstream-credentials",
                "filters": [
                    {
                        "filter": "credential_injection",
                        "clusters": [
                            {
                                "name": "model-backend",
                                "header": "Authorization",
                                "env_var": "MODEL_API_KEY",
                                "header_prefix": "Bearer ",
                                "strip_client_credential": True,
                            }
                        ],
                    }
                ],
            },
        ],
    }
    if hostname.endswith(PRIVATE_SUFFIXES):
        config["insecure_options"] = {"allow_private_endpoints": True}
    return config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-base-url", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(yaml.safe_dump(render(args.model_base_url), sort_keys=False))


if __name__ == "__main__":
    main()

