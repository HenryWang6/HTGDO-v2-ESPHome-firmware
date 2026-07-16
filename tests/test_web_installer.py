from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_protocol_switch_updates_install_button_manifest_attribute():
    installer = (REPO_ROOT / "static/index.html").read_text()

    assert 'installButton.setAttribute("manifest", firmware.manifest)' in installer
    assert "installButton.manifest =" not in installer
