# Bulgarian Utility Outage Checker - Home Assistant Add-on

<p align="center">
  <img src="example/logo.png" alt="Bulgarian Utility Outage Checker" width="200"/>
</p>

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

- 🔄 **Automatic updates** - Home Assistant checks for new versions daily
- 📊 Periodic checking for utility outages
- ⏱️ Configurable check interval (1 minute to 1 hour)
- 🔍 Support for custom identifiers (subscriber number, location, street)
- 🌐 Bilingual interface (Bulgarian/English)
- ⚙️ Auto-generated configuration for easy dashboard integration
- 📁 JSON status file for Home Assistant sensors
- 🔔 Binary sensor for automation triggers

## Installation / Инсталация

### Step 1: Add Repository / Стъпка 1: Добавяне на Repository

1. Open Home Assistant / Отворете Home Assistant
2. Go to **Settings** → **Add-ons** → **Add-on Store**
3. Click **⋮** (three dots) in top right corner
4. Select **Repositories**
5. Add this URL:
   ```
   https://github.com/reminchev/bulgarian_utility_outage_checker
   ```
6. Click **Add** → **Close**
7. Refresh the page (F5)

Or click this button:

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Freminchev%2Fbulgarian_utility_outage_checker)

### Step 2: Install Add-on / Стъпка 2: Инсталиране на добавката

1. Find "Bulgarian Utility Outage Checker" in the add-on store
2. Click on it and press **Install**
3. Wait for installation to complete

### Step 3: Configure / Стъпка 3: Конфигурация

1. Go to **Configuration** tab
2. Enter your identifier (examples):
   - Subscriber number / Номер на абонат: `12345678`
   - Location / Населено място: `София`, `Перник`, `Враца`
   - Street / Улица: `София, ул. Витоша`
   - Address / Адрес: `София, ул. Витоша 25`
3. (Optional) Adjust check interval (default: 3600 seconds = 60 minutes)
4. Click **Save**
5. Go to **Info** tab and click **Start**

### Step 4: Add to Dashboard / Стъпка 4: Добавяне към таблото

#### Automatic Configuration / Автоматична конфигурация

The add-on automatically generates a ready-to-use configuration file!

1. After starting the add-on, open **File Editor** add-on (or access via SSH/Samba)
2. Navigate to `/share/utility_outage_config.yaml`
3. **Copy the entire content** of this file
4. Open your `configuration.yaml` file
5. **Paste** the copied configuration at the end
6. Go to **Settings** → **System** → **Restart Home Assistant**

#### Manual Configuration / Ръчна конфигурация

Add this to your `configuration.yaml`:

```yaml
sensor:
  - platform: file
    name: "Utility Outage Status"
    file_path: /share/utility_outage_status.json
    value_template: >
      {% if value_json.state == 'ok' %}
        Няма аварии
      {% elif value_json.state == 'problem' %}
        {{ value_json.outage_type }}
      {% else %}
        Неизвестно
      {% endif %}
    json_attributes:
      - identifier
      - has_outage
      - outage_type
      - details
      - last_check
      - timestamp

binary_sensor:
  - platform: template
    sensors:
      utility_outage:
        friendly_name: "Авария на ток"
        device_class: problem
        value_template: >
          {{ states.sensor.utility_outage_status.attributes.has_outage | default(false) }}
        icon_template: >
          {% if states.sensor.utility_outage_status.attributes.has_outage %}
            mdi:power-plug-off
          {% else %}
            mdi:power-plug
          {% endif %}
```

Restart Home Assistant after adding the configuration.

### Step 5: Create Dashboard Card / Стъпка 5: Създаване на карта

1. Go to your dashboard / Отидете на вашето табло
2. Click **Edit Dashboard** → **Add Card**
3. Choose **Entities Card**
4. Add these entities:

```yaml
type: entities
title: Статус на Електрозахранването
entities:
  - entity: binary_sensor.utility_outage
    name: Авария
  - entity: sensor.utility_outage_status
    name: Статус
  - type: attribute
    entity: sensor.utility_outage_status
    attribute: last_check
    name: Последна проверка
```

Or use a **Glance Card** for compact view:

```yaml
type: glance
title: Електрозахранване
entities:
  - entity: binary_sensor.utility_outage
    name: Авария
  - entity: sensor.utility_outage_status
    name: Статус
```

## Troubleshooting / Отстраняване на проблеми

### Updates / Актуализации
- Home Assistant automatically checks for updates daily
- When a new version is available, you'll see an **Update** button in the add-on
- Click **Update** to install the latest version
- Home Assistant автоматично проверява за актуализации всеки ден
- Когато има нова версия, ще видите бутон **Update** в добавката
- Кликнете **Update** за да инсталирате най-новата версия

### Add-on not starting / Добавката не стартира
- Check that you entered a valid identifier
- Review logs in the **Log** tab

### Sensors not appearing / Сензорите не се показват
- Ensure you added configuration to `configuration.yaml`
- Restart Home Assistant after adding configuration
- Check that file `/share/utility_outage_status.json` exists

### No data updates / Данните не се обновяват
- Check add-on logs for errors
- Verify your identifier is correct for ERM West system
- Ensure add-on is running (check **Info** tab)

## Support / Поддръжка

For issues and questions:
- GitHub Issues: https://github.com/reminchev/bulgarian_utility_outage_checker/issues
- Home Assistant Community: https://community.home-assistant.io/

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
