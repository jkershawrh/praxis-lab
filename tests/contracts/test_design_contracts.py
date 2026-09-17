from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def load_yaml(relative_path: str):
    return yaml.safe_load((ROOT / relative_path).read_text())


def test_validation_matrix_has_all_six_factory_stages():
    matrix = load_yaml("tests/validation_matrix.yaml")
    stage_ids = [stage["id"] for stage in matrix["stages"]]

    assert stage_ids == [
        "stage_0_contracts",
        "stage_1_infrastructure",
        "stage_2_unit",
        "stage_3_integration",
        "stage_4_benchmarks",
        "stage_5_publication",
    ]


def test_backend_contract_uses_neutral_environment_names():
    example = (ROOT / ".env.example").read_text()

    assert "MODEL_BASE_URL=" in example
    assert "MODEL_NAME=" in example
    assert "MODEL_API_KEY=" in example
    assert "MAAS_API_URL=" not in example
    assert "LITELLM" not in example.upper()


def test_competency_release_gate_is_strict():
    rubric = load_yaml("tests/competency_rubric.yaml")

    assert rubric["release_rules"]["no_zero_scores"] is True
    assert rubric["release_rules"]["minimum_total"] == 28
    assert "security_and_secrets" in rubric["release_rules"]["required_score_3"]
    assert "automated_validation" in rubric["release_rules"]["required_score_3"]


def test_rhpds_is_described_as_an_overlay_not_a_dependency():
    decision = (ROOT / "docs/decisions/0001-backend-neutral-contract.md").read_text()

    assert "deployment overlays implementing the same contract" in decision
    assert "not presented as" not in decision  # ADR states the decision directly, without lab prose.


def test_track3_ledger_module_preserves_the_authorization_boundary():
    module = (ROOT / "docs/track3-ppe-ocsf-ledger-preview.md").read_text()
    normalized = " ".join(module.split())

    assert "contract-ready preview" in module
    assert "PPE remains responsible for authorization" in module
    assert "exact same trace identifier" in module
    assert '"latest event" fallback' in module
    assert "does not prove the policy was correct" in normalized


def test_track3_ledger_contract_namespaces_ppe_separately_from_cpex():
    contract = (
        ROOT.parent
        / "are-immutable-ledger/contracts/praxis-ppe-ocsf-ledger-contract.md"
    )

    if not contract.exists():
        # The lab can be cloned independently; its publication contract is
        # still checked above. A sibling checkout enables cross-repo validation.
        return

    content = contract.read_text()
    normalized = " ".join(content.lower().split())
    assert "praxis.ppe.policy.<decision>.v1" in content
    assert "contextforge deployment using cpex" in normalized
    assert "must not inject" in content
    assert "trace_id" in content
