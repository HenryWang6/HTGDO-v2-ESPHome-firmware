from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD_ACTION = (
    "ratgdo/esphome-build-action@"
    "69cd483b363e218e220cd805ee2fe8a5324c6f77"
)


def test_ci_only_runs_tests_and_two_firmware_builds():
    workflow = (REPO_ROOT / ".github/workflows/ci.yml").read_text()

    assert workflow.count(BUILD_ACTION) == 1
    assert "htgdo_v2_2_secplus1.yaml" in workflow
    assert "htgdo_v2_2_secplus2.yaml" in workflow
    assert "actions/upload-artifact" not in workflow
    assert "manifest_filename" not in workflow
    assert "Prepare CI artifact" not in workflow


def test_release_injects_and_validates_binary_project_metadata():
    workflow = (REPO_ROOT / ".github/workflows/release.yml").read_text()

    assert workflow.count(BUILD_ACTION) == 1
    assert "scripts/create_release_config.py" in workflow
    assert "steps.esphome-build.outputs.project-name" in workflow
    assert "steps.esphome-build.outputs.project-version" in workflow
    assert 'PROJECT_VERSION: ${{ steps.esphome-build.outputs.project-version }}' in workflow
    assert 'if [ "${PROJECT_VERSION}" != "${RELEASE_TAG}" ]' in workflow
    assert '"version": $version' in workflow


def test_release_uses_friendly_manifest_names_and_concise_assets():
    workflow = (REPO_ROOT / ".github/workflows/release.yml").read_text()

    assert "name: Security+ 2.0" in workflow
    assert "name: Security+ 1.0" in workflow
    assert "manifest_filename: secplus2-manifest.json" in workflow
    assert "manifest_filename: secplus1-manifest.json" in workflow
    assert 'factory_name="${RELEASE_TAG}-${SLUG}.factory.bin"' in workflow
    assert 'ota_name="${RELEASE_TAG}-${SLUG}.ota.bin"' in workflow
    assert '"new_install_improv_wait_time": 15' in workflow
    assert '"new_install_prompt_erase": true' in workflow
    assert '"home_assistant_domain": "esphome"' in workflow
    assert ".parts[0].path = $factory" in workflow
    assert ".ota.path = $ota" in workflow
    assert "new_install_skip_erase" not in workflow
    assert "name: ${{ needs.preflight.outputs.release_tag }}" in workflow
    assert "static/header.png" not in workflow


def test_release_is_created_before_pages_are_updated():
    workflow = yaml.load(
        (REPO_ROOT / ".github/workflows/release.yml").read_text(),
        Loader=yaml.BaseLoader,
    )

    assert workflow["jobs"]["release"]["needs"] == ["preflight", "prepare"]
    assert workflow["jobs"]["deploy"]["needs"] == ["prepare", "release"]


def test_release_runs_are_serialized_before_updating_pages():
    workflow = yaml.load(
        (REPO_ROOT / ".github/workflows/release.yml").read_text(),
        Loader=yaml.BaseLoader,
    )

    assert workflow["concurrency"] == {
        "group": "htgdo-v2-esphome-release",
        "cancel-in-progress": "false",
    }


def test_ci_and_release_build_checkout_local_sources():
    ci = (REPO_ROOT / ".github/workflows/ci.yml").read_text()
    release = (REPO_ROOT / ".github/workflows/release.yml").read_text()

    assert "scripts/update_refs_for_ci.py" in ci
    assert "scripts/update_refs_for_ci.py" in release
