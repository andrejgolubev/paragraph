from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def _parse_group(driver): 
    """ПАРСИТ ВСЕ актуальные ГРУППЫ из выпадающего меню """

    wait = WebDriverWait(driver, 10)
    # input_field = wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "input.select-autocomplete#field-group"))
    # )
    
    # input_field.click()

    # Очищаем поле и вводим название группы
    # input_field.clear()
    # input_field.send_keys('--Не выбрана--')

    icon = driver.find_element(By.CSS_SELECTOR, "i.mdi")
    icon.click()    
    
    
    
    # Ждем появления списка опций ul
    options_list = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul[role='listbox']"))
    ) # options_list это ul со всеми группами
    
    # Парсим все доступные группы
    groups_dict = {}
    group_options = options_list.find_elements(By.TAG_NAME, "li")

    for option in group_options:
        data_value = option.get_attribute("data-value")
        group_text = option.text.strip()
        
        if data_value and group_text:
            groups_dict[group_text] = data_value 

    return groups_dict


driver=webdriver.Chrome()
driver.get('https://rasp.rsreu.ru') #СЮДА МОЖНО СРАЗУ ССЫЛКУ НОРМАЛЬНУЮ СКОМПЛЕЛИРОВАННУЮ
    


def parse_groups():
    """parses all groups.
    group_number:data-value"""
    
    gr = _parse_group(driver=driver)
    return gr



GROUPS_INVERTED = {key: value for value, key in parse_groups().items()}
GROUPS = {key: value for value, key in GROUPS_INVERTED.items()}

if __name__ == '__main__': 
    print(parse_groups())
    print(GROUPS_INVERTED)

