"""Create a sanitized, portable evidence bundle from a Praxis lab run."""

from __future__ import annotations

import argparse
import json
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path


SAFE_RESOURCES = (
    "deployment/praxis-ai",
    "service/praxis-ai",
    "configmap/praxis-ai-config",
    "networkpolicy",
)


def run(*command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--output", default="artifacts")
    parser.add_argument("--scenario", default="industry-sensitive shared AI access")
    args = parser.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    root = Path(args.output) / f"praxis-evidence-{stamp}"
    root.mkdir(parents=True, exist_ok=False)

    checks = []
    for resource in SAFE_RESOURCES:
        result = run("oc", "-n", args.project, "get", resource, "-o", "yaml")
        filename = resource.replace("/", "-") + ".yaml"
        (root / filename).write_text(result.stdout if result.returncode == 0 else result.stderr)
        checks.append({"resource": resource, "passed": result.returncode == 0})

    identity = run("oc", "whoami")
    summary = {
        "generated_at": stamp,
        "project": args.project,
        "identity": identity.stdout.strip(),
        "scenario": args.scenario,
        "checks": checks,
        "excluded": ["Secret values", "prompt content", "model responses", "access tokens"],
    }
    (root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (root / "assessment.md").write_text(
        f"# Praxis evidence assessment\n\n"
        f"- Scenario: {args.scenario}\n"
        f"- OpenShift project: `{args.project}`\n"
        "- Demonstrated: gateway availability, backend-neutral access, credential ownership, network boundaries, controlled failure and recovery\n"
        "- Not demonstrated: production identity design, sensitive-data policy, retention enforcement, regulatory approval\n"
        "- Decision: complete the missing controls and organizational review before production use\n"
    )

    archive = root.with_suffix(".tar.gz")
    with tarfile.open(archive, "w:gz") as bundle:
        bundle.add(root, arcname=root.name)
    print(archive)
    return 0 if all(check["passed"] for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
