from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALLER = (REPO_ROOT / "static/index.html").read_text()


class ProtocolInputParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.protocols: dict[str, dict[str, str | None]] = {}

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = dict(attrs)
        if tag == "input" and attributes.get("name") == "protocol":
            self.protocols[str(attributes["value"])] = attributes


def protocol_inputs() -> dict[str, dict[str, str | None]]:
    parser = ProtocolInputParser()
    parser.feed(INSTALLER)
    return parser.protocols


def accepted_firmware_ids(protocol: str) -> set[str]:
    values = protocol_inputs()[protocol]["data-firmware-ids"]
    assert values is not None
    return {value.lower() for value in values.split(",")}


def test_protocol_cards_define_manifest_and_firmware_identity_mapping():
    protocols = protocol_inputs()

    assert protocols["secplus2"]["data-manifest"] == "secplus2-manifest.json"
    assert protocols["secplus2"]["data-firmware-ids"] == (
        "htgdo.secplus2,htgdo.v2_2_secplus2"
    )
    assert protocols["secplus1"]["data-manifest"] == "secplus1-manifest.json"
    assert protocols["secplus1"]["data-firmware-ids"] == (
        "htgdo.secplus1,htgdo.v2_2_secplus1"
    )
    assert all("disabled" in attributes for attributes in protocols.values())


def test_identity_mapping_accepts_current_and_legacy_but_rejects_wrong_protocol():
    secplus2_ids = accepted_firmware_ids("secplus2")
    secplus1_ids = accepted_firmware_ids("secplus1")

    assert {"htgdo.secplus2", "htgdo.v2_2_secplus2"} <= secplus2_ids
    assert {"htgdo.secplus1", "htgdo.v2_2_secplus1"} <= secplus1_ids
    assert "htgdo.secplus1" not in secplus2_ids
    assert "htgdo.secplus2" not in secplus1_ids
    assert "unknown.firmware" not in secplus2_ids | secplus1_ids


def test_installer_uses_one_protocol_label_source_and_one_release_version_line():
    assert "<title>HTGDO-v2 ESPHome Installer</title>" in INSTALLER
    assert "<h1>HTGDO-v2 ESPHome Installer</h1>" in INSTALLER
    assert INSTALLER.count("Security+ 2.0") == 1
    assert INSTALLER.count("Security+ 1.0") == 1
    assert "Selected:" not in INSTALLER
    assert "const firmwares" not in INSTALLER
    assert 'versionLabel.textContent = "Version: ";' in INSTALLER
    assert "header.png" not in INSTALLER


def test_installer_loads_and_validates_both_manifests_before_enabling_connect():
    assert "await Promise.all" in INSTALLER
    assert "manifest.name !== variant.protocolName" in INSTALLER
    assert "versions.size !== 1" in INSTALLER
    assert 'id="connect-button" type="button" slot="activate" disabled' in INSTALLER
    assert "connectButton.disabled = false" in INSTALLER
    assert "showUnavailable(error)" in INSTALLER
    assert "connectButton.disabled = true" in INSTALLER
    assert "input.disabled = true" in INSTALLER
    assert "Firmware unavailable. Please try again later." in INSTALLER
    assert 'downloadOta.removeAttribute("href")' in INSTALLER


def test_installer_uses_supported_firmware_override_and_pinned_web_tools():
    assert "esp-web-tools@9.4.3" in INSTALLER
    assert "checkSameFirmware(manifest, improvInfo)" in INSTALLER
    assert "variant?.firmwareIds.includes(improvInfo.firmware.toLowerCase())" in INSTALLER
    assert 'installButton.setAttribute("manifest", variant.manifestPath)' in INSTALLER
    assert "installButton.manifest =" not in INSTALLER


def test_installer_uses_concise_manifest_names():
    assert "htgdo-v2-secplus2-manifest.json" not in INSTALLER
    assert "htgdo-v2-secplus1-manifest.json" not in INSTALLER
