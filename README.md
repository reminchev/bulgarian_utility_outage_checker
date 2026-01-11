# Bulgarian Utility Outage Checker - Home Assistant Add-on

Home Assistant add-on repository for checking planned and unplanned utility outages in Bulgaria.

Add-on documentation: <https://developers.home-assistant.io/docs/add-ons>

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Freminchev%2Fbulgarian_utility_outage_checker)

## Add-ons

This repository contains the following add-ons:

### [Bulgarian Utility Outage Checker](./example)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

_Проверка за аварии на комунални услуги в България / Check for planned and unplanned utility outages in Bulgaria._

Currently supports:
- **ERM West** (ЕРМ Запад) - Electricity distribution company

## Features

- Periodic checking for utility outages
- Configurable check interval (1 minute to 1 hour)
- Support for custom identifiers (subscriber number, location, street)
- Bilingual interface (Bulgarian/English)

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
