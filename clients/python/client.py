"""Minimal Python client for the stable Praxis-facing contract."""

import json
import os
from urllib.request import Request, urlopen


def invoke(prompt: str):
    base_url = os.environ["PRAXIS_BASE_URL"].rstrip("/")
    payload = json.dumps(
        {
            "model": os.environ.get("PRAXIS_MODEL", "lab-model"),
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")
    request = Request(
        f"{base_url}/v1/chat/completions",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


if __name__ == "__main__":
    print(json.dumps(invoke("Explain the role of an AI gateway in one sentence."), indent=2))

