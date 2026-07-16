from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_ci_manifest_uses_build_action_version_output():
    workflow = (REPO_ROOT / ".github/workflows/ci.yml").read_text()

    assert "steps.esphome-build.outputs.version" in workflow
    assert "steps.esphome-build.outputs.esphome-version" not in workflow


def test_release_manifest_uses_release_tag_as_version():
    workflow = (REPO_ROOT / ".github/workflows/release.yml").read_text()

    assert '--arg version "${{ needs.preflight.outputs.release_tag }}"' in workflow
    assert "steps.esphome-build.outputs.esphome-version" not in workflow
