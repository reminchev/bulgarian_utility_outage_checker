# Home Assistant Add-on: Bulgarian Utility Outage Checker

![Logo](logo.png)

## Description / Описание

This add-on checks for planned and unplanned utility outages in Bulgaria.
Currently supports ERM West EAD. It fetches information from the official website https://info.ermzapad.bg and periodically checks for outages at a specified location.

Този add-on проверява за планирани и непланирани прекъсвания на комунални услуги в България.
В момента поддържа ЕРМ Запад ЕАД. Извлича информация от официалния сайт https://info.ermzapad.bg и периодично проверява за аварии на зададен обект.

## How to use / Как да използвате

1. Install the add-on / Инсталирайте add-on-а
2. Configure the identifier (subscriber number, location, or street) / Конфигурирайте идентификатора (номер на абонат, населено място или улица)
3. (Optional) Set check interval in seconds / (Опционално) Задайте интервал на проверка в секунди
4. Start the add-on / Стартирайте add-on-а
5. Check logs for outage status / Проверете логовете за статус на аварии

## Configuration / Конфигурация

### Option / Опция: `identifier`

The identifier of the object you want to check. This can be:
- Subscriber number / Номер на абонат
- Location / Населено място
- Street / Улица
- Other identifier searchable in ERM West system / Друг идентификатор

**Required option / Задължителна опция**

### Option / Опция: `check_interval`

Check interval in seconds (between 60 and 3600 seconds) / Интервал на проверка в секунди (между 60 и 3600 секунди).

**Default / По подразбиране:** `3600` (60 minutes / минути)

## Configuration example / Пример за конфигурация

```yaml
identifier: "София, ул. Витоша" # Sofia, Vitosha street
check_interval: 3600
```

## How it works / Как работи

The add-on periodically checks the ERM West website for outage information:
- ✅ **No outages / Няма аварии** - No current interruptions / Няма текущи прекъсвания
- ⚠️ **Planned outage / Планирана авария** - Scheduled maintenance / Планирано прекъсване
- ⚠️ **Unplanned outage / Непланирана авария** - Emergency outage / Аварийно прекъсване

The status is displayed in the add-on logs and updates when changes occur.
Статусът се извежда в логовете на add-on-а и се обновява при промяна.
