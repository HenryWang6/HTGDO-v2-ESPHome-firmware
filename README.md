
# HTGDO ESPHome firmware

ESPHome firmware for HTGDO-v2, based on the upstream ratgdo ESPHome component.
The active HTGDO-v2.4.2 configs target the upstream ratgdo32 v32board pin
mapping and support Security+ 1.0 and Security+ 2.0 openers.

## Web Installer

Flashable release artifacts will be published from this fork after hardware
validation.

## First use after adding to Home Assistant

The ESPHome firmware will allow you to open the door to any position after calibration. To calibrate the door, open and close it once without stopping.

<img width="560" alt="position_demo" src="https://github.com/RATGDO/esphome-ratgdo/assets/663432/22a9873e-67bb-4b2f-bb32-70047cfe666d">

## ESPHome configs

| Board | Chip | Protocol | Config |
|-------|------|----------|--------|
| HTGDO-v2.4.2 | ESP32 | Security+ 2.0 | [htgdo_v2_4_2_secplus2.yaml](static/htgdo_v2_4_2_secplus2.yaml) |
| HTGDO-v2.4.2 | ESP32 | Security+ 1.0 | [htgdo_v2_4_2_secplus1.yaml](static/htgdo_v2_4_2_secplus1.yaml) |
| Upstream v32board | ESP32 | Security+ 2.0 | [v32board.yaml](static/v32board.yaml) |
| Upstream v32board | ESP32 | Security+ 1.0 | [v32board_secplusv1.yaml](static/v32board_secplusv1.yaml) |

Archived upstream example configs are kept under `archive/`.

![Home Assistant Screen Shot](static/hass.png)

## ESP32 Framework

The active HTGDO-v2.4.2 and upstream v32board configs use the ESP-IDF
framework.
