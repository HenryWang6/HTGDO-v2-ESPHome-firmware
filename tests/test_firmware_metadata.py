from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("directory", "filename", "project_name"),
    [
        (Path(), "htgdo_v2_2_secplus2.yaml", "htgdo.secplus2"),
        (Path(), "htgdo_v2_2_secplus1.yaml", "htgdo.secplus1"),
        (Path("static"), "htgdo_v2_2_secplus2.yaml", "htgdo.secplus2"),
        (Path("static"), "htgdo_v2_2_secplus1.yaml", "htgdo.secplus1"),
    ],
)
def test_htgdo_configs_use_stable_identity_and_dev_version(
    directory, filename, project_name
):
    config = yaml.safe_load((REPO_ROOT / directory / filename).read_text())

    assert config["substitutions"]["firmware_version"] == "dev"
    assert config["esphome"]["project"] == {
        "name": project_name,
        "version": "${firmware_version}",
    }


def test_esphome_version_sensor_is_not_labeled_as_firmware_release():
    base_config = (REPO_ROOT / "base_htgdo.yaml").read_text()

    assert 'name: "ESPHome Version"' in base_config
    assert 'name: "Firmware Version"' not in base_config
