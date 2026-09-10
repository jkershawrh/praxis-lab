from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_track1_automation_exposes_red_solve_green_commands():
    solver = (ROOT / "runtime-automation/track1/solve.sh").read_text()
    validator = (ROOT / "runtime-automation/track1/validate.py").read_text()

    assert "oc apply -k deploy/kustomize/base" in solver
    assert 'state = "green" if all' in validator
    assert 'else "red"' in validator
    assert "sys.exit(0 if state == \"green\" else 1)" in validator


def test_amd64_e2e_proves_gateway_owned_credential_replacement():
    runtime_test = (ROOT / "tests/runtime/amd64-e2e.sh").read_text()

    assert "ghcr.io/praxis-proxy/ai@sha256:" in runtime_test
    assert "caller-supplied-wrong-secret" in runtime_test
    assert "gateway-owned-validation-secret" in runtime_test
    assert "Gateway logs exposed the upstream credential" in runtime_test
    assert "Any HTTP response proves the listener is ready" in runtime_test
