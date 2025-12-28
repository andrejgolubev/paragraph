from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def debug_wait(driver, selector, timeout=10):
    """Функция отладки для ожидания элемента"""
    print(f"⌛ Ожидаем элемент: {selector}")
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        print(f"✅ Элемент найден: {selector}")
        return element
    except Exception as e:
        print(f"❌ Не удалось найти элемент {selector}: {e}")
        # Попробуем найти альтернативные селекторы
        alternative_selectors = [
            "input.select-autocomplete",
            "#field-group", 
            "input[type='text']",
            ".select-autocomplete",
            "input[name='group']"
        ]
        
        for alt_selector in alternative_selectors:
            if alt_selector != selector:
                try:
                    print(f"🔄 Пробуем альтернативный селектор: {alt_selector}")
                    element = driver.find_element(By.CSS_SELECTOR, alt_selector)
                    print(f"✅ Нашли по альтернативному селектору: {alt_selector}")
                    return element
                except:
                    continue
        
        raise e

def parse_group(group_name, driver=webdriver.Chrome): 
    print("🚀 Начало парсинга групп...")
    
    try:
        # Ждем поле ввода с отладкой
        input_field = debug_wait(driver, "input.select-autocomplete#field-group")
        
        print("🖱️ Кликаем на поле ввода...")
        input_field.click()
        
        if group_name:
            print(f"⌨️ Вводим название группы: {group_name}")
            input_field.clear()
            input_field.send_keys(group_name)
        
        # Ждем появления списка опций
        print("📋 Ожидаем список групп...")
        options_list = debug_wait(driver, "ul[role='listbox']")
        
        # Парсим все доступные группы
        groups_dict = {}
        group_options = options_list.find_elements(By.TAG_NAME, "li")
        
        print(f"📊 Найдено элементов li: {len(group_options)}")
        
        for i, option in enumerate(group_options):
            data_value = option.get_attribute("data-value")
            group_text = option.text.strip()
            
            # print(f"  {i+1}. data-value: '{data_value}', text: '{group_text}'")
            
            if data_value and data_value != "0" and group_text:
                groups_dict[group_text] = data_value 

        print(f"✅ Парсинг завершен. Найдено групп: {len(groups_dict)}")
        return groups_dict
        
    except Exception as e:
        return {}


# Основной код с улучшенной обработкой ошибок
if __name__ == '__main__': 
    try:
        print("🌐 Запускаем браузер...")
        driver = webdriver.Chrome()
        
        print("🔗 Переходим на сайт...")
        driver.get('https://rasp.rsreu.ru') 
        
        # Даем время на загрузку
        print("⏳ Ждем загрузки страницы...")
        time.sleep(3)
        
        # Проверяем, что страница загрузилась
        print(f"📄 Заголовок страницы: {driver.title}")
        print(f"🔗 Текущий URL: {driver.current_url}")
        
        gr = parse_group(group_name="5413")
        

        print('Результат:', gr, sep='\n')
    
    except Exception as e:
        print(f"💥 Ошибка в основном потоке: {e}")
        
    finally:
        driver.quit()
        print("👋 Браузер закрыт")







def parse_all_groups():
    try:
        print("🌐 Запускаем браузер...")
        driver = webdriver.Chrome()
        
        print("🔗 Переходим на сайт...")
        driver.get('https://rasp.rsreu.ru') 
        
        # Даем время на загрузку
        print("⏳ Ждем загрузки страницы...")
        time.sleep(3)
        
        # Проверяем, что страница загрузилась
        print(f"📄 Заголовок страницы: {driver.title}")
        print(f"🔗 Текущий URL: {driver.current_url}")
        
        gr = parse_group(group_name="5413")
        
        return gr
    
    except Exception as e:
        print(f"💥 Ошибка в основном потоке: {e}")
        
    finally:
        driver.quit()
        print("👋 Браузер закрыт") 