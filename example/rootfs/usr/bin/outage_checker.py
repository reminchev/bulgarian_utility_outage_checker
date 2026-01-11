#!/usr/bin/env python3
"""
Bulgarian Utility Outage Checker / Проверка за Аварии На комунални услуги в България
Checks for planned and unplanned utility outages / Проверява за планирани и аварийни прекъсвания на комунални услуги
"""
import requests
import time
import json
import logging
import sys
from bs4 import BeautifulSoup
from datetime import datetime

# Настройка на logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OutageChecker:
    """Class for checking outages from ERM West / Клас за проверка на аварии от ЕРМ Запад"""
    
    BASE_URL = "https://info.ermzapad.bg/webint/vok/avplan.php"
    
    def __init__(self, identifier, check_interval=3600):
        """
        Инициализация
        
        Args:
            identifier: Идентификатор на обекта за проверка
            check_interval: Интервал на проверка в секунди (по подразбиране 60 минути)
        """
        self.identifier = identifier
        self.check_interval = check_interval
        self.session = requests.Session()
        self.last_status = None
        
    def check_outage(self):
        """Проверява за аварии на даден идентификатор"""
        try:
            # Първи заявка за получаване на сесия
            response = self.session.get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            
            # Търсене по идентификатор
            search_data = {
                'objid': self.identifier,
                'search': '1'
            }
            
            response = self.session.post(self.BASE_URL, data=search_data, timeout=10)
            response.raise_for_status()
            
            # Парсване на HTML отговора
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Търсене на информация за аварии
            result = {
                'identifier': self.identifier,
                'timestamp': datetime.now().isoformat(),
                'has_outage': False,
                'outage_type': None,
                'details': []
            }
            
            # Търсене на червени маркери (непланирани аварии)
            red_markers = soup.find_all(string=lambda text: text and 'Непланирани прекъсвания' in text)
            if red_markers:
                result['has_outage'] = True
                result['outage_type'] = 'Непланирана авария'
                
            # Търсене на зелени маркери (планирани аварии)
            green_markers = soup.find_all(string=lambda text: text and 'Планирани прекъсвания' in text)
            if green_markers:
                result['has_outage'] = True
                if result['outage_type']:
                    result['outage_type'] = 'Планирана и непланирана авария'
                else:
                    result['outage_type'] = 'Планирана авария'
            
            # Извличане на детайли за аварията
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) > 0:
                        row_text = ' '.join([cell.get_text(strip=True) for cell in cells])
                        if row_text and self.identifier.lower() in row_text.lower():
                            result['details'].append(row_text)
            
            # Проверка дали има резултати от търсенето
            if not result['details']:
                # Проверка за съобщение "Няма намерени записи"
                no_results = soup.find_all(string=lambda text: text and ('Няма' in text or 'няма' in text))
                if no_results:
                    result['has_outage'] = False
                    result['outage_type'] = 'Няма текуща авария'
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Грешка при свързване със сайта: {e}")
            return None
        except Exception as e:
            logger.error(f"Грешка при обработка на данните: {e}")
            return None
    
    def format_status(self, result):
        """Форматира статуса за изход"""
        if not result:
            return "❌ Грешка при проверка"
        
        if result['has_outage']:
            status = f"⚠️ {result['outage_type']}"
            if result['details']:
                status += "\nДетайли:\n" + "\n".join(result['details'])
        else:
            status = "✅ Няма текущи аварии"
        
        return status
    
    def run(self):
        """Main loop for checking / Главен цикъл за проверка"""
        logger.info(f"Starting outage check for identifier / Стартиране на проверка за идентификатор: {self.identifier}")
        logger.info(f"Check interval / Интервал на проверка: {self.check_interval} seconds / секунди")
        
        while True:
            try:
                result = self.check_outage()
                status = self.format_status(result)
                
                # Check if status changed / Проверка дали статусът се е променил
                if status != self.last_status:
                    logger.info(f"\n{'='*60}")
                    logger.info(f"New status for / Нов статус за {self.identifier}:")
                    logger.info(status)
                    logger.info(f"{'='*60}\n")
                    self.last_status = status
                else:
                    logger.debug("No status change / Няма промяна в статуса")
                
                # Изчакване преди следващата проверка
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("Stopping check / Спиране на проверката...")
                break
            except Exception as e:
                logger.error(f"Unexpected error / Неочаквана грешка: {e}")
                time.sleep(self.check_interval)

def main():
    """Main function / Главна функция"""
    try:
        # Read configuration from Home Assistant / Четене на конфигурацията от Home Assistant
        with open('/data/options.json', 'r') as f:
            options = json.load(f)
        
        identifier = options.get('identifier', '')
        check_interval = options.get('check_interval', 3600)
        
        if not identifier:
            logger.error("Identifier not set in configuration! / Идентификаторът не е зададен в конфигурацията!")
            logger.error("Please set an identifier in addon settings. / Моля, задайте идентификатор в настройките на addon-а.")
            sys.exit(1)
        
        # Create and start checker / Създаване и стартиране на checker
        checker = OutageChecker(identifier, check_interval)
        checker.run()
        
    except FileNotFoundError:
        logger.error("Configuration file not found! / Конфигурационният файл не е намерен!")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during startup / Грешка при стартиране: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
