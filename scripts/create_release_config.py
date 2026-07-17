#!/usr/bin/env python3
"""Create an ephemeral ESPHome config with a release version override."""

import argparse
import os
from pathlib import Path
import re

RELEASE_TAG_PATTERN = re.compile(r"^htgdo-v2\.2-esphome-[0-9]+$")


def create_release_config(source: Path, output: Path, release_tag: str) -> None:
    """Write a package wrapper that overrides the firmware version."""
    if not RELEASE_TAG_PATTERN.fullmatch(release_tag):
        raise ValueError(
            f"Release tag must match htgdo-v2.2-esphome-N: {release_tag}"
        )
    if not source.is_file():
        raise FileNotFoundError(f"Firmware config does not exist: {source}")
    if source.suffix not in {".yaml", ".yml"}:
        raise ValueError(f"Firmware config must be YAML: {source}")
    if output.resolve() == source.resolve():
        raise ValueError("Release config output must differ from the source config")

    output.parent.mkdir(parents=True, exist_ok=True)
    include_path = Path(
        os.path.relpath(source.resolve(), output.parent.resolve())
    ).as_posix()
    output.write_text(
        "---\n"
        "substitutions:\n"
        f'  firmware_version: "{release_tag}"\n'
        "\n"
        "packages:\n"
        f"  release_target: !include {include_path}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--release-tag", required=True)
    args = parser.parse_args()

    create_release_config(args.source, args.output, args.release_tag)
    print(f"Created {args.output} for {args.release_tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
