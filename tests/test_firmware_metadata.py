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
        (Path(), "htgdo_v2_5_secplus2.yaml", "htgdo.v2_5_secplus2"),
        (Path(), "htgdo_v2_5_secplus1.yaml", "htgdo.v2_5_secplus1"),
        (Path("static"), "htgdo_v2_5_secplus2.yaml", "htgdo.v2_5_secplus2"),
        (Path("static"), "htgdo_v2_5_secplus1.yaml", "htgdo.v2_5_secplus1"),
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
    assert config["esphome"]["min_version"] == "2026.10.2"
    assert config["improv_ble"] == {"authorizer": "none"}
    assert "esp32_improv" not in config


def test_esphome_version_sensor_is_not_labeled_as_firmware_release():
    base_config = (REPO_ROOT / "base_htgdo.yaml").read_text()

    assert 'name: "ESPHome Version"' in base_config
    assert 'name: "Firmware Version"' not in base_config


@pytest.mark.parametrize("protocol", ["secplus1", "secplus2"])
def test_v25_enables_gpio4_while_v22_keeps_message_only(protocol):
    for directory in (Path(), Path("static")):
        v22 = yaml.safe_load((REPO_ROOT / directory / f"htgdo_v2_2_{protocol}.yaml").read_text())
        v25 = yaml.safe_load((REPO_ROOT / directory / f"htgdo_v2_5_{protocol}.yaml").read_text())
        assert "ratgdo" not in v22
        assert v25["ratgdo"] == {"input_obst_pin": "GPIO4"}
        assert v25["substitutions"]["id_prefix"] == v22["substitutions"]["id_prefix"]
        assert v25["esphome"]["name"] == v22["esphome"]["name"]
