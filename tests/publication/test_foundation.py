from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_required_foundation_artifacts_exist():
    required = [
        "DESIGN.md",
        "docs/capability-matrix.md",
        "docs/ui-observability.md",
        "docs/decisions/0005-publication-shape.md",
        "tests/validation_matrix.yaml",
        "tests/competency_rubric.yaml",
        "tests/claim_registry.yaml",
        "tests/benchmark_rubric.yaml",
    ]

    missing = [path for path in required if not (ROOT / path).is_file()]
    assert not missing, f"Missing foundation artifacts: {missing}"


def test_every_feature_has_a_scenario():
    features = sorted((ROOT / "features").glob("*.feature"))

    assert features
    for feature in features:
        content = feature.read_text()
        assert "Feature:" in content, feature
        assert "Scenario" in content, feature


def test_learner_evidence_bundle_is_sanitized_by_design():
    collector = (ROOT / "tools/collect_evidence.py").read_text()

    assert "SAFE_RESOURCES" in collector
    assert "secret/" not in collector.lower()
    assert '"Secret values"' in collector
    assert '"prompt content"' in collector
    assert "assessment.md" in collector
    assert ".tar.gz" in collector
