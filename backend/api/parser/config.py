import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from ..logger import log

def create_driver():
    """Создаём WebDriver с оптимальными настройками для сервера"""

    options = Options()

    # Headless режим (без GUI)
    options.add_argument('--headless')

    # Отключаем GPU (для серверов без видеокарты)
    options.add_argument('--no-gpu')

    # Отключаем песочницу (нужно для запуска от root)
    options.add_argument('--no-sandbox')

    # Отключаем /dev/shm (решает проблемы с памятью)
    options.add_argument('--disable-dev-shm-usage')

    # Отключаем уведомления
    options.add_argument('--disable-notifications')


    chrome_binary = "/backend/chrome-linux64/chrome"
    chromedriver_binary = "/backend/chromedriver-linux64/chromedriver"


    if os.path.exists(chrome_binary) and os.path.exists(chromedriver_binary):
        
        options.binary_location = chrome_binary
        service = Service(chromedriver_binary)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(60)

        log.info('chrome-linux64 driver initialized.')
        return driver
    else:
        # на локалке просто возвращаем т.к. он скачан и драйвер его находит
        log.info('local driver initialized (requires pre-installed driver)')
        return webdriver.Chrome(options=options)

