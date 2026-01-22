from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..logger import log


def _parse_date(driver: webdriver.Chrome): 
    """ПАРСИТ ВСЕ актуальные ДАТЫ из выпадающего меню """
    
    try: 
        log.info('Parsing dates...')
        wait = WebDriverWait(driver, 0.1)
        css_selector = '.column[style*="width: 220px"] .select-wrap' 
        log.debug('CSS selector: %s', css_selector)
        option_box = driver.find_element(By.CSS_SELECTOR, css_selector)
        option_box.click()    
        log.debug('Option box clicked')
        # Ждем появления списка опций ul
        options_list = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        ) 
        log.debug('Options list found')
        # Парсим все доступные группы
        dates_dict = {}
        dates_options = options_list.find_elements(By.TAG_NAME, "option")
        log.debug('Dates options found: %s', len(dates_options))
        for date in dates_options:
            
            data_value = date.get_attribute("value")
            date = date.text.strip()
            log.debug('Current date: %s', date)
            for word in ['(текущая)', 'знам.', 'числ.']:
                date = date.replace(word, '').strip(' ,')

            if data_value and date:
                dates_dict[date] = data_value 

        return dates_dict

    except Exception as e: 
        log.error('Error parsing dates: %s', e)
        raise 


def parse_dates():
    """parses all dates.
    user_date:data_value"""

    log.info("Starting date parser")


    driver = webdriver.Chrome()
    driver.get('https://rasp.rsreu.ru/schedule-frame/group?faculty=1&group=1640&date=')
    try:
        dates = _parse_date(driver)
        log.info("Parsed %d dates", len(dates))
        return dates 
    finally:
        driver.quit()
        log.info("Dates parsing successful.")



