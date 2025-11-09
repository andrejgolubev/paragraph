# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# import time


# def garb_remove(string: str): 
#     return ' '.join(string.split())

# HEADERS = {
#    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36'
# }

# def parse_group(driver, group_name): 
#     wait = WebDriverWait(driver, 10)
#     input_field = wait.until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "input.select-autocomplete#field-group"))
#     )
    
#     # Кликаем на поле ввода чтобы открыть список
#     input_field.click()
#     time.sleep(1)
    
#     # Очищаем поле и вводим название группы
#     input_field.clear()
#     input_field.send_keys(group_name)
#     time.sleep(1)
    
#     # Ждем появления списка опций ul
#     options_list = wait.until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "ul[role='listbox']"))
#     ) # options_list это ul со всеми группами
    
#     # Парсим все доступные группы
#     groups_dict = {}
#     group_options = options_list.find_elements(By.TAG_NAME, "li")

#     for option in group_options:
#         data_value = option.get_attribute("data-value")
#         group_text = option.text.strip()
        
#         if data_value and group_text:
#             groups_dict[group_text] = data_value 

#     return groups_dict
    
# def parse_all_groups(driver):
#     """Парсит все группы с сайта"""
#     return parse_group(driver, "") 

# driver = webdriver.Chrome()
# driver.get('https://rasp.rsreu.ru') 

# gr = parse_group(driver=driver, group_name=5413)


# print(gr)

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

def parse_group(driver, group_name): 
    print("🚀 Начало парсинга групп...")
    
    try:
        # Ждем поле ввода с отладкой
        input_field = debug_wait(driver, "input.select-autocomplete#field-group")
        
        print("🖱️ Кликаем на поле ввода...")
        input_field.click()
        time.sleep(2)
        
        if group_name:
            print(f"⌨️ Вводим название группы: {group_name}")
            input_field.clear()
            input_field.send_keys(group_name)
            time.sleep(2)
        
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
        print(f"💥 Критическая ошибка в parse_group: {e}")
        # Сохраняем скриншот для отладки
        driver.save_screenshot("error_screenshot.png")
        print("📸 Скриншот сохранен как 'error_screenshot.png'")
        return {}

# def parse_all_groups(driver):
#     """Парсит все группы с сайта"""
#     return parse_group(driver, "") 

# Основной код с улучшенной обработкой ошибок
try:
    print("🌐 Запускаем браузер...")
    driver = webdriver.Chrome()
    
    print("🔗 Переходим на сайт...")
    driver.get('https://rasp.rsreu.ru') 
    
    # Даем время на загрузку
    print("⏳ Ждем загрузки страницы...")
    time.sleep(5)
    
    # Проверяем, что страница загрузилась
    print(f"📄 Заголовок страницы: {driver.title}")
    print(f"🔗 Текущий URL: {driver.current_url}")
    
    gr = parse_group(driver=driver, group_name="5413")
    
    print("\n📋 РЕЗУЛЬТАТ:")
    print(gr)
    
except Exception as e:
    print(f"💥 Ошибка в основном потоке: {e}")
    
finally:
    input("⏸️ Нажмите Enter для закрытия браузера...")
    driver.quit()
    print("👋 Браузер закрыт")