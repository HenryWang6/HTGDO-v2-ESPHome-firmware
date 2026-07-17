from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).parents[2] / "scripts"))

from create_release_config import create_release_config


def test_create_release_config_injects_release_tag(tmp_path):
    source = tmp_path / "firmware.yaml"
    source.write_text("substitutions:\n  firmware_version: dev\n")
    output = tmp_path / "release.yaml"

    create_release_config(source, output, "htgdo-v2.2-esphome-4")

    assert output.read_text() == (
        "---\n"
        "substitutions:\n"
        '  firmware_version: "htgdo-v2.2-esphome-4"\n'
        "\n"
        "packages:\n"
        "  release_target: !include firmware.yaml\n"
    )


@pytest.mark.parametrize(
    "release_tag",
    ["htgdo-v2.2-esphome", "htgdo-v2-esphome-4", "release-4"],
)
def test_create_release_config_rejects_invalid_tags(tmp_path, release_tag):
    source = tmp_path / "firmware.yaml"
    source.write_text("esphome:\n")

    with pytest.raises(ValueError, match="Release tag must match"):
        create_release_config(source, tmp_path / "release.yaml", release_tag)


def test_create_release_config_requires_existing_yaml_source(tmp_path):
    with pytest.raises(FileNotFoundError, match="does not exist"):
        create_release_config(
            tmp_path / "missing.yaml",
            tmp_path / "release.yaml",
            "htgdo-v2.2-esphome-4",
        )


def test_create_release_config_does_not_overwrite_source(tmp_path):
    source = tmp_path / "firmware.yaml"
    source.write_text("esphome:\n")

    with pytest.raises(ValueError, match="must differ"):
        create_release_config(source, source, "htgdo-v2.2-esphome-4")
