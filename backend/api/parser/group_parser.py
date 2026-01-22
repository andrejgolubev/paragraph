from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..logger import log


def _parse_group(driver: webdriver.Chrome): 
    """ПАРСИТ ВСЕ актуальные ГРУППЫ из выпадающего меню """
    try:
        log.info("Parsing groups...")
        wait = WebDriverWait(driver, 0.1)

        icon = driver.find_element(By.CSS_SELECTOR, "i.mdi")
        icon.click()    

        # Ждем появления списка опций ul
        options_list = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul[role='listbox']"))
        ) # options_list это ul со всеми группами

        groups_dict = {}
        group_options = options_list.find_elements(By.TAG_NAME, "li")

        for option in group_options:
            data_value = option.get_attribute("data-value")
            group_number = option.text.strip()

            if data_value!='0' and group_number:
                groups_dict[group_number] = data_value 

        return groups_dict
    except Exception as exc:
        log.error("Error parsing groups: %s", exc, exc_info=True)
        raise


def parse_groups():
    """parses all groups.
    group_number:data-value pairs"""
    log.info("Starting group parser")
    driver = webdriver.Chrome()
    driver.get('https://rasp.rsreu.ru')

    try:
        groups = _parse_group(driver=driver)
        log.info("Parsed %d groups", len(groups))
        return groups
    finally:
        driver.quit()
        log.info("Groups parsing successful.")
