
# HTGDO ESPHome firmware

ESPHome firmware for HTGDO-v2, based on the upstream ratgdo ESPHome component.
The active HTGDO-v2.2 configs target the upstream ratgdo32 v32board pin
mapping and support Security+ 1.0 and Security+ 2.0 openers.

## Web Installer

Official release artifacts are published from manual releases tagged
`htgdo-v2.2-esphome-N`, for example `htgdo-v2.2-esphome-1`.

The Web Installer is deployed from the latest official release:

https://henrywang6.github.io/HTGDO-v2-ESPHome-firmware/

## First use after adding to Home Assistant

The ESPHome firmware will allow you to open the door to any position after calibration. To calibrate the door, open and close it once without stopping.

<img width="560" alt="position_demo" src="https://github.com/RATGDO/esphome-ratgdo/assets/663432/22a9873e-67bb-4b2f-bb32-70047cfe666d">

## ESPHome configs

| Board | Chip | Protocol | Config |
|-------|------|----------|--------|
| HTGDO-v2.2 | ESP32 | Security+ 2.0 | [htgdo_v2_2_secplus2.yaml](static/htgdo_v2_2_secplus2.yaml) |
| HTGDO-v2.2 | ESP32 | Security+ 1.0 | [htgdo_v2_2_secplus1.yaml](static/htgdo_v2_2_secplus1.yaml) |

Upstream reference configs are kept in this repo for comparison, but CI and
official HTGDO releases only build the two HTGDO-v2 configs above.

![Home Assistant Screen Shot](static/hass.png)

## ESP32 Framework

The active HTGDO-v2.2 and upstream v32board configs use the ESP-IDF
framework.
