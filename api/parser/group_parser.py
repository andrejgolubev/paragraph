from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



def parse_group(group_name, driver): 
    wait = WebDriverWait(driver, 10)
    input_field = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.select-autocomplete#field-group"))
    )
    
    input_field.click()
    
    # Очищаем поле и вводим название группы
    input_field.clear()
    input_field.send_keys(group_name)
    
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
driver.get('https://rasp.rsreu.ru') 
    


def parse_all_groups():
    """for usage in main.py. parses all groups."""
    
    gr = parse_group(driver=driver, group_name=5413)
    return gr

if __name__ == '__main__': 
    gr = parse_group(driver=driver, group_name=5413)
    print(gr)

