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

## Features / Възможности

- 🔄 **Automatic updates** - Home Assistant checks for new versions daily / Автоматични актуализации
- 📊 **Periodic monitoring** - Checks for outages based on your interval / Периодична проверка за аварии
- ⏱️ **Configurable interval** - From 1 minute to 1 hour / Конфигурируем интервал от 1 минута до 1 час
- 🔍 **Custom identifiers** - Subscriber number, location, or street / Поддръжка на идентификатори
- 🌐 **Bilingual interface** - Bulgarian and English / Двуезичен интерфейс (БГ/EN)
- ⚙️ **Auto-configuration** - Generates ready-to-use YAML files / Автоматично генериране на конфигурация
- 📁 **JSON status file** - For advanced integrations / JSON файл със статус за сензори
- 🔔 **Binary sensor** - For automation triggers / Binary sensor за автоматизации
- 📈 **Detailed attributes** - Outage type, last check time, details / Детайлни атрибути
- 🎨 **Dashboard ready** - Multiple card examples included / Готови примери за dashboard карти

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

### Step 4: Configure Home Assistant / Стъпка 4: Конфигурация на Home Assistant

#### ✨ Automatic Configuration (Recommended) / ✨ Автоматична конфигурация (Препоръчително)

The add-on **automatically generates** ready-to-use configuration files!

1. **Start the add-on** - it will create two files:
   - `/config/utility_outage_sensors.yaml` - File sensor configuration
   - `/config/utility_outage_templates.yaml` - Binary sensor template configuration

2. **Open your `configuration.yaml`** (Settings → Add-ons → File Editor)

3. **Add these two lines** to your `configuration.yaml`:
   ```yaml
   sensor: !include utility_outage_sensors.yaml
   template: !include utility_outage_templates.yaml
   ```

   **Note:** If you already have `sensor:` or `template:` sections in your configuration, see the logs for instructions on how to merge them.

4. **Save** and go to **Settings** → **System** → **Restart Home Assistant**

5. After restart, check **Developer Tools** → **States** for:
   - `sensor.utility_outage_status` 
   - `binary_sensor.avaria_na_tok_XXXXXXXXX` (where X is your identifier)

#### 📝 Manual Configuration / 📝 Ръчна конфигурация

If you prefer to add sensors manually or need to customize:

**File Sensor** (monitors status file):
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
```

**Binary Sensor Template** (for automations):
```yaml
template:
  - binary_sensor:
      - name: "Авария на ток - 300062153834"
        device_class: problem
        state: >-
          {{ state_attr('sensor.utility_outage_status', 'has_outage') == true }}
        icon: >-
          {% if state_attr('sensor.utility_outage_status', 'has_outage') == true %}
            mdi:power-plug-off
          {% else %}
            mdi:power-plug
          {% endif %}
        attributes:
          outage_type: >-
            {{ state_attr('sensor.utility_outage_status', 'outage_type') | default('Unknown') }}
          last_check: >-
            {{ state_attr('sensor.utility_outage_status', 'last_check') | default('Never') }}
          details: >-
            {{ state_attr('sensor.utility_outage_status', 'details') | default([]) }}
```

**Important:** Replace `300062153834` with your identifier.

Restart Home Assistant after adding the configuration.

### Step 5: Create Dashboard Card / Стъпка 5: Създаване на карта за таблото

After sensors are created, add them to your dashboard. Here are several card examples:

#### 🎴 Simple Entities Card / Проста Entities карта

Shows all information in a clean list format.

```yaml
type: entities
title: Статус на Електрозахранването
entities:
  - entity: sensor.utility_outage_status
    name: Статус
    icon: mdi:transmission-tower
  - type: attribute
    entity: sensor.utility_outage_status
    attribute: last_check
    name: Последна проверка
    icon: mdi:clock-outline
  - entity: binary_sensor.avaria_na_tok_300062153834
    name: Авария детектирана
```

**Screenshot:**
```
┌─────────────────────────────────────┐
│ Статус на Електрозахранването       │
├─────────────────────────────────────┤
│ 🗼 Статус: Няма аварии              │
│ 🕐 Последна проверка: 11:30         │
│ ⚡ Авария детектирана: off          │
└─────────────────────────────────────┘
```

#### 📊 Detailed Entities Card with Attributes / Детайлна карта с атрибути

Shows more information including outage type.

```yaml
type: entities
title: 🔌 ЕРМ Запад - Мониторинг
entities:
  - entity: binary_sensor.avaria_na_tok_300062153834
    name: Статус на електрозахранването
    secondary_info: last-changed
  - type: attribute
    entity: binary_sensor.avaria_na_tok_300062153834
    attribute: outage_type
    name: Тип на аварията
  - type: attribute
    entity: binary_sensor.avaria_na_tok_300062153834
    attribute: last_check
    name: Последна проверка
  - type: divider
  - entity: sensor.utility_outage_status
    name: Детайлен статус
```

#### 🎯 Glance Card (Compact) / Компактна Glance карта

Perfect for small spaces or mobile view.

```yaml
type: glance
title: Електрозахранване
columns: 2
entities:
  - entity: binary_sensor.avaria_na_tok_300062153834
    name: Авария
  - entity: sensor.utility_outage_status
    name: Статус
```

**Screenshot:**
```
┌───────────────────────────┐
│  Електрозахранване        │
├─────────────┬─────────────┤
│    ⚡       │    ✓        │
│  Авария    │  Статус     │
│    off     │ Няма аварии │
└─────────────┴─────────────┘
```

#### 🚨 Alert Card (Conditional) / Карта за предупреждения

Only shows when there's an outage.

```yaml
type: conditional
conditions:
  - condition: state
    entity: binary_sensor.avaria_na_tok_300062153834
    state: 'on'
card:
  type: markdown
  content: >
    ## ⚠️ АВАРИЯ НА ЕЛЕКТРОЗАХРАНВАНЕТО!

    **Тип:** {{ state_attr('binary_sensor.avaria_na_tok_300062153834', 'outage_type') }}

    **Последна проверка:** {{ state_attr('binary_sensor.avaria_na_tok_300062153834', 'last_check') }}
    
    ---
    
    _Информацията се обновява автоматично всеки час._
  title: 🔴 Внимание!
  theme: red
```

#### 📈 Markdown Card with Status / Markdown карта със статус

Customizable card with formatted information.

```yaml
type: markdown
content: >
  ## 🔌 Статус на Електрозахранването


  {% if is_state('binary_sensor.avaria_na_tok_300062153834', 'on') %}

  ### ⚠️ {{ state_attr('binary_sensor.avaria_na_tok_300062153834', 'outage_type') }}

  **Статус:** 🔴 Има авария

  {% else %}

  ### ✅ Няма аварии

  **Статус:** 🟢 Нормално захранване

  {% endif %}


  ---

  **Последна проверка:** {{ state_attr('binary_sensor.avaria_na_tok_300062153834', 'last_check') | default('Никога') }}

  **Идентификатор:** {{ state_attr('sensor.utility_outage_status', 'identifier') }}
title: ЕРМ Запад - Мониторинг
```

#### 🎨 Button Card (Custom) / Персонализирана Button карта

Requires [button-card](https://github.com/custom-cards/button-card) custom component.

```yaml
type: custom:button-card
entity: binary_sensor.avaria_na_tok_300062153834
name: Електрозахранване
show_state: true
show_last_changed: true
state:
  - value: 'on'
    color: red
    icon: mdi:power-plug-off
    name: АВАРИЯ
  - value: 'off'
    color: green
    icon: mdi:power-plug
    name: Нормално
styles:
  card:
    - font-size: 14px
    - height: 120px
  name:
    - font-weight: bold
    - font-size: 16px
tap_action:
  action: more-info
```

#### 📱 Stack Card (Combined Layout) / Комбинирана карта

Combines multiple card types in one.

```yaml
type: vertical-stack
cards:
  - type: glance
    title: 🔌 ЕРМ Запад
    entities:
      - entity: binary_sensor.avaria_na_tok_300062153834
        name: Статус
  - type: conditional
    conditions:
      - condition: state
        entity: binary_sensor.avaria_na_tok_300062153834
        state: 'on'
    card:
      type: markdown
      content: >
        ⚠️ **{{ state_attr('binary_sensor.avaria_na_tok_300062153834', 'outage_type') }}**
        
        Проверено: {{ state_attr('binary_sensor.avaria_na_tok_300062153834', 'last_check') }}
  - type: entities
    entities:
      - entity: sensor.utility_outage_status
        name: Детайлен статус
```

---

**💡 Tips / Съвети:**
- Replace `300062153834` with your actual identifier in the entity names
- You can customize colors, icons, and text in any card
- For automations, use `binary_sensor.avaria_na_tok_XXXXXXXXX` as trigger
- Check [Home Assistant card documentation](https://www.home-assistant.io/dashboards/cards/) for more options

---

## Automations / Автоматизации

Use the binary sensor to create automations that react to power outages.

### 📱 Send notification on outage / Изпращане на нотификация при авария

```yaml
automation:
  - alias: "Notify on Power Outage"
    description: "Send notification when power outage is detected"
    trigger:
      - platform: state
        entity_id: binary_sensor.avaria_na_tok_300062153834
        to: "on"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "⚠️ Авария на тока!"
          message: >
            {{ state_attr('binary_sensor.avaria_na_tok_300062153834', 'outage_type') }}
            
            Проверено: {{ state_attr('binary_sensor.avaria_na_tok_300062153834', 'last_check') }}
          data:
            priority: high
            ttl: 0
```

### 🔔 Persistent notification / Постоянна нотификация

```yaml
automation:
  - alias: "Persistent Notification on Outage"
    trigger:
      - platform: state
        entity_id: binary_sensor.avaria_na_tok_300062153834
        to: "on"
    action:
      - service: persistent_notification.create
        data:
          title: "🔴 Авария на електрозахранването"
          message: >
            **Тип:** {{ state_attr('binary_sensor.avaria_na_tok_300062153834', 'outage_type') }}
            
            **Проверено:** {{ state_attr('binary_sensor.avaria_na_tok_300062153834', 'last_check') }}
          notification_id: power_outage
          
  - alias: "Clear Notification on Recovery"
    trigger:
      - platform: state
        entity_id: binary_sensor.avaria_na_tok_300062153834
        to: "off"
    action:
      - service: persistent_notification.dismiss
        data:
          notification_id: power_outage
```

### 💡 Turn off devices on planned outage / Изключване на устройства при планирана авария

```yaml
automation:
  - alias: "Turn off devices on planned outage"
    trigger:
      - platform: state
        entity_id: binary_sensor.avaria_na_tok_300062153834
        to: "on"
    condition:
      - condition: template
        value_template: >
          {{ 'Планирана' in state_attr('binary_sensor.avaria_na_tok_300062153834', 'outage_type') }}
    action:
      - service: light.turn_off
        target:
          entity_id: all
      - service: switch.turn_off
        target:
          entity_id: 
            - switch.ac_unit
            - switch.water_heater
      - service: notify.mobile_app_your_phone
        data:
          message: "Устройствата са изключени поради планирана авария."
```

### 🚨 Flash lights on unplanned outage / Мигане на светлини при непланирана авария

```yaml
automation:
  - alias: "Alert on Unplanned Outage"
    trigger:
      - platform: state
        entity_id: binary_sensor.avaria_na_tok_300062153834
        to: "on"
    condition:
      - condition: template
        value_template: >
          {{ 'Непланирана' in state_attr('binary_sensor.avaria_na_tok_300062153834', 'outage_type') }}
    action:
      - repeat:
          count: 3
          sequence:
            - service: light.turn_on
              target:
                entity_id: light.living_room
              data:
                brightness: 255
                rgb_color: [255, 0, 0]
            - delay:
                seconds: 1
            - service: light.turn_off
              target:
                entity_id: light.living_room
            - delay:
                seconds: 1
      - service: notify.mobile_app_your_phone
        data:
          title: "🚨 НЕПЛАНИРАНА АВАРИЯ!"
          message: "Непланирана авария на електрозахранването!"
```

### 📊 Log outages to file / Запис на аварии във файл

```yaml
automation:
  - alias: "Log Power Outages"
    trigger:
      - platform: state
        entity_id: binary_sensor.avaria_na_tok_300062153834
        to: "on"
    action:
      - service: notify.outage_log
        data:
          message: >
            {{ now().strftime('%Y-%m-%d %H:%M:%S') }} - 
            {{ state_attr('binary_sensor.avaria_na_tok_300062153834', 'outage_type') }}
```

---

## Troubleshooting / Отстраняване на проблеми

### 🔄 Updates / Актуализации
- Home Assistant automatically checks for updates daily / HA автоматично проверява за актуализации
- When a new version is available, you'll see an **Update** button / При нова версия ще видите бутон **Update**
- Click **Update** to install the latest version / Кликнете **Update** за инсталиране
- Current version: **1.3.2** (January 2026)

### ❌ Add-on not starting / Добавката не стартира
- Check that you entered a valid identifier / Проверете дали сте въвели валиден идентификатор
- Review logs in the **Log** tab / Прегледайте логовете в раздел **Log**
- Ensure identifier exists in ERM West system / Уверете се че идентификаторът съществува

### 🔍 Sensors not appearing / Сензорите не се показват
1. **Check configuration files exist:**
   - Open File Editor → navigate to `/config/`
   - Look for `utility_outage_sensors.yaml` and `utility_outage_templates.yaml`
   - If missing, restart the add-on

2. **Verify configuration.yaml:**
   ```yaml
   sensor: !include utility_outage_sensors.yaml
   template: !include utility_outage_templates.yaml
   ```

3. **Restart Home Assistant:**
   - Settings → System → Restart
   - Wait 2-3 minutes for full restart

4. **Check Developer Tools:**
   - Go to Developer Tools → States
   - Search for `sensor.utility_outage_status`
   - Search for `binary_sensor.avaria_na_tok_`

5. **Check logs for errors:**
   - Settings → System → Logs
   - Look for configuration errors

### 🔧 Configuration conflicts / Конфликти в конфигурацията

**If you already have `sensor:` section in configuration.yaml:**

Option 1 - Use include_dir_merge_list:
```yaml
sensor: !include_dir_merge_list sensors/
```
Then move `utility_outage_sensors.yaml` to `/config/sensors/` folder.

Option 2 - Merge manually:
Open `utility_outage_sensors.yaml`, copy its content, and paste it under your existing `sensor:` section.

**If you already have `template:` section:**

Option 1 - Use include_dir_merge_list:
```yaml
template: !include_dir_merge_list templates/
```
Then move `utility_outage_templates.yaml` to `/config/templates/` folder.

Option 2 - Merge manually:
Open `utility_outage_templates.yaml`, copy its content, and paste it under your existing `template:` section.

### 📊 No data updates / Данните не се обновяват
- Check add-on logs for errors / Проверете логовете за грешки
- Verify your identifier is correct for ERM West / Проверете идентификатора
- Ensure add-on is running / Уверете се че добавката работи
- Check if `/share/utility_outage_status.json` file exists and updates / Проверете дали файлът се обновява
- Try restarting the add-on / Опитайте да рестартирате добавката

### 🌐 Website connectivity issues / Проблеми със свързването към сайта
- The add-on needs internet access to reach `info.ermzapad.bg`
- Check your Home Assistant network settings
- Verify firewall settings allow outbound connections
- ERM West website may be temporarily down

## Support / Поддръжка

For issues and questions:
- GitHub Issues: https://github.com/reminchev/bulgarian_utility_outage_checker/issues
- Home Assistant Community: https://community.home-assistant.io/

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
