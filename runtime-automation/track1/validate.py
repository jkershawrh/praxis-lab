"""Return machine-readable Track 1 RED/GREEN evidence from OpenShift."""

import json
import os
import subprocess
import sys


PROJECT = os.environ.get("PROJECT_NAME", "praxis-ai-gateway")


def oc(*args):
    return subprocess.run(
        ["oc", "-n", PROJECT, *args],
        capture_output=True,
        text=True,
    )


def check(name, *args):
    result = oc(*args)
    return {
        "name": name,
        "passed": result.returncode == 0,
        "evidence": (result.stdout or result.stderr).strip()[:500],
    }


checks = [
    check("praxis deployment exists", "get", "deployment/praxis-ai", "-o", "name"),
    check("praxis rollout is available", "rollout", "status", "deployment/praxis-ai", "--timeout=5s"),
    check("model credential secret exists", "get", "secret/model-backend-credentials", "-o", "name"),
    check("praxis service exists", "get", "service/praxis-ai", "-o", "name"),
    check("learner UI rollout is available", "rollout", "status", "deployment/praxis-ui", "--timeout=5s"),
    check("learner UI route exists", "get", "route/praxis-ui", "-o", "name"),
    check("network isolation exists", "get", "networkpolicy/praxis-ai-default-deny", "-o", "name"),
]
state = "green" if all(item["passed"] for item in checks) else "red"
print(json.dumps({"track": 1, "project": PROJECT, "state": state, "checks": checks}, indent=2))
sys.exit(0 if state == "green" else 1)
