from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = (ROOT / "README.md").read_text()


def test_readme_is_quickstart_ready():
    required_sections = [
        "# Govern AI Model Access with Praxis",
        "## Customer problem",
        "## Architecture",
        "## How an application uses Praxis",
        "## How a platform team uses Praxis",
        "## Customer adoption path",
        "## Requirements",
        "## Deploy Track 1",
        "## Run the learner UI",
        "## Validate red and green",
        "## Learning tracks",
        "## Project metadata",
    ]

    assert all(section in README for section in required_sections)


def test_readme_leads_with_customer_use_before_demo_platform_details():
    customer_workflow = README.index("## How an application uses Praxis")
    demo_profile = README.index("## Demo-platform profile")

    assert customer_workflow < demo_profile
    assert "RHPDS" not in README[:demo_profile]


def test_readme_preserves_backend_neutrality_and_rhpds_boundary():
    assert "MaaS is not presented as a Praxis dependency" in README
    assert "Red Hat OpenShift AI" in README
    assert "MODEL_BASE_URL" in README
    assert "PRAXIS_BASE_URL" in README


def test_readme_has_required_catalog_metadata():
    for field in [
        "Title",
        "Description",
        "Industry",
        "Product",
        "Use case",
        "Partner",
        "Contributor organization",
    ]:
        assert f"**{field}:**" in README
