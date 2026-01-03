from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from api.parser.parser_conf import init



def _parse_date(driver: webdriver.Chrome): 
    """ПАРСИТ ВСЕ актуальные ДАТЫ из выпадающего меню """

    wait = WebDriverWait(driver, 0.1)
    css_selector = '.column[style*="width: 220px"] .select-wrap' 

    option_box = driver.find_element(By.CSS_SELECTOR, css_selector)
    option_box.click()    
    
    # Ждем появления списка опций ul
    options_list = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
    ) 
    
    # Парсим все доступные группы
    dates_dict = {}
    dates_options = options_list.find_elements(By.TAG_NAME, "option")

    for user_date in dates_options:
        
        data_value = user_date.get_attribute("value")
        user_date = user_date.text.strip()

        if ' (текущая)' in user_date: 
            user_date = user_date.replace(' (текущая)', '')

        if data_value and user_date:
            dates_dict[user_date] = data_value 

    return dates_dict


def parse_dates():
    """parses all dates.
    user_date:data_value"""
    
    driver = init()
    driver.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=1&group=1640&date=')

    dates = _parse_date(driver=driver)
    return dates 



if __name__ == '__main__': 
    print(f'{parse_dates() = }')