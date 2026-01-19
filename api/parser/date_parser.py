from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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

    for date in dates_options:
        
        data_value = date.get_attribute("value")
        date = date.text.strip()
        for word in ['(текущая)', 'знам.', 'числ.']:
            date = date.replace(word, '').strip(' ,')


        if data_value and date:
            dates_dict[date] = data_value 

    return dates_dict


def parse_dates():
    """parses all dates.
    user_date:data_value"""
    
    driver = webdriver.Chrome()
    driver.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=1&group=1640&date=')

    dates = _parse_date(driver)
    return dates 



