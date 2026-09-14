"""Validate a learner-owned Praxis configuration with the pinned OpenShift image."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
import uuid
from pathlib import Path
from typing import Optional


PRAXIS_IMAGE = "ghcr.io/praxis-proxy/ai@sha256:ef1f8e216f3428e15bc5953f5938562658edc9232ebfce5f946f05cddd34a0e6"


def oc(project: str, *args: str, stdin: Optional[str] = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["oc", "-n", project, *args],
        input=stdin,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    if not args.config.is_file():
        parser.error(f"configuration does not exist: {args.config}")

    suffix = uuid.uuid4().hex[:8]
    name = f"praxis-config-check-{suffix}"
    configmap = oc(
        args.project,
        "create",
        "configmap",
        name,
        f"--from-file=praxis-ai.yaml={args.config}",
        "--dry-run=client",
        "-o",
        "json",
    )
    if configmap.returncode:
        print(configmap.stderr)
        return configmap.returncode

    pod = {
        "apiVersion": "v1",
        "kind": "Pod",
        "metadata": {"name": name, "labels": {"app.kubernetes.io/part-of": "praxis-config-validation"}},
        "spec": {
            "restartPolicy": "Never",
            "securityContext": {"runAsNonRoot": True, "seccompProfile": {"type": "RuntimeDefault"}},
            "containers": [{
                "name": "validator",
                "image": PRAXIS_IMAGE,
                "args": ["--validate", "--config", "/config/praxis-ai.yaml"],
                "securityContext": {"allowPrivilegeEscalation": False, "capabilities": {"drop": ["ALL"]}},
                "volumeMounts": [{"name": "config", "mountPath": "/config", "readOnly": True}],
            }],
            "volumes": [{"name": "config", "configMap": {"name": name}}],
        },
    }

    try:
        applied_cm = oc(args.project, "apply", "-f", "-", stdin=configmap.stdout)
        applied_pod = oc(args.project, "apply", "-f", "-", stdin=json.dumps(pod))
        if applied_cm.returncode or applied_pod.returncode:
            print(applied_cm.stderr or applied_pod.stderr)
            return 2

        phase = ""
        for _ in range(60):
            result = oc(args.project, "get", f"pod/{name}", "-o", "jsonpath={.status.phase}")
            phase = result.stdout
            if phase in {"Succeeded", "Failed"}:
                break
            time.sleep(2)
        logs = oc(args.project, "logs", f"pod/{name}")
        print(logs.stdout or logs.stderr)
        print(f"Praxis configuration validation: {phase or 'TimedOut'}")
        return 0 if phase == "Succeeded" else 1
    finally:
        oc(args.project, "delete", "pod,configmap", name, "--ignore-not-found", "--wait=false")


if __name__ == "__main__":
    raise SystemExit(main())
