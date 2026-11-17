
# HTGDO ESPHome firmware

ESPHome firmware for HTGDO-v2, based on the upstream ratgdo ESPHome component.
The active HTGDO-v2.2 configs target the upstream ratgdo32 v32board pin
mapping and support Security+ 1.0 and Security+ 2.0 openers.

## Web Installer

Official release artifacts are published from manual releases tagged
`htgdo-v2.2-esphome-N`, for example `htgdo-v2.2-esphome-1`.

The Web Installer is deployed from the latest official release:

https://henrywang6.github.io/HTGDO-v2-ESPHome-firmware/

The installer presents one protocol name and one release version. Official
release versions use the exact GitHub tag, such as
`htgdo-v2.2-esphome-4`. The firmware identities stored on the device are
`htgdo.secplus2` and `htgdo.secplus1`; they remain stable across releases so
the installer can distinguish updates from protocol changes.

ESP Web Tools shows the device node name (for example `garage-door-xxxxxx`) in
the dialog header. Its install/update action and confirmation text use the
friendly protocol name, while the connected firmware row shows the stable
identity and exact release tag.

Each release publishes these customer-facing assets:

- `secplus2-manifest.json` and `secplus1-manifest.json`
- `<release-tag>-secplus2.factory.bin` and `<release-tag>-secplus1.factory.bin`
- `<release-tag>-secplus2.ota.bin` and `<release-tag>-secplus1.ota.bin`
- `SHA256SUMS`

The `ESPHome Version` diagnostic entity reports the ESPHome build-tool version.
It is separate from the hardware-linked firmware release tag above.

## First use after adding to Home Assistant

The ESPHome firmware will allow you to open the door to any position after calibration. To calibrate the door, open and close it once without stopping.

<img width="560" alt="position_demo" src="https://github.com/RATGDO/esphome-ratgdo/assets/663432/22a9873e-67bb-4b2f-bb32-70047cfe666d">

## ESPHome configs

| Board | Chip | Protocol | Config |
|-------|------|----------|--------|
| HTGDO-v2.2 | ESP32 | Security+ 2.0 | [htgdo_v2_2_secplus2.yaml](static/htgdo_v2_2_secplus2.yaml) |
| HTGDO-v2.2 | ESP32 | Security+ 1.0 | [htgdo_v2_2_secplus1.yaml](static/htgdo_v2_2_secplus1.yaml) |
| HTGDO-v2.5 (v2.2 compatibility pending hardware validation) | ESP32 | Security+ 2.0 | [htgdo_v2_5_secplus2.yaml](static/htgdo_v2_5_secplus2.yaml) |
| HTGDO-v2.5 (v2.2 compatibility pending hardware validation) | ESP32 | Security+ 1.0 | [htgdo_v2_5_secplus1.yaml](static/htgdo_v2_5_secplus1.yaml) |

The v2.5 configs enable GPIO4 obstruction input. The v2.2 configs keep message-only
obstruction reporting. The intended v2.5 release must be tested on both board
versions before it is marked compatible with v2.2 hardware.

The v2.5 configs provide a **Factory reset** button in Home Assistant and the
device web interface. Pressing it erases the device's saved Wi-Fi credentials
and other ESPHome preferences, then reboots into the initial provisioning flow
with the `HTGDO Setup` access point. It does not remove the device entry from
Home Assistant or erase any paired remotes, keypads, or wall controls from the
garage door opener. Remove the Home Assistant entry separately when transferring
the device. The current device web interface and native API have no
authentication, so use this control only on a trusted local network.

Upstream reference configs are kept in this repo for comparison. Current official
releases still use the v2.2 configs until v2.5 hardware validation and release
workflow updates are complete.

Pull-request CI runs the Python tests and compiles all four HTGDO configs. It
does not publish firmware or Web Installer artifacts. Official binaries and
the GitHub Pages installer are updated only by the manual release workflow.

![Home Assistant Screen Shot](static/hass.png)

## ESP32 Framework

The active HTGDO-v2.2 and upstream v32board configs use the ESP-IDF
framework.
