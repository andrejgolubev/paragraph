from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from api.parser.parser_conf import init


def _parse_group(driver: webdriver.Chrome): 
    """ПАРСИТ ВСЕ актуальные ГРУППЫ из выпадающего меню """

    wait = WebDriverWait(driver, 0.1)

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
        group_number = option.text.strip()
        
        if data_value!='0' and group_number:
            groups_dict[group_number] = data_value 

    return groups_dict


def parse_groups():
    """parses all groups.
    group_number:data-value pairs"""
    driver = init()
    gr = _parse_group(driver=driver)
    return gr



if __name__ == '__main__': 
    print(f'{parse_groups() = }')

