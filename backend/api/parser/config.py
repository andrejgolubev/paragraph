import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from ..logger import log


# пути к бинарникам
CHROME_BINARY = "/backend/chrome-linux64/chrome"
CHROMEDRIVER_BINARY = "/backend/chromedriver-linux64/chromedriver"


def create_driver():
    """Создаём WebDriver с оптимальными настройками для сервера"""

    options = Options()
    options.add_argument('--headless') # Headless режим (без GUI)
    options.add_argument('--no-gpu') # Откл. GPU (для серверов без видеокарты)
    options.add_argument('--no-sandbox') # Откл. песочницу (нужно для запуска от root)
    options.add_argument('--disable-dev-shm-usage') # Откл. /dev/shm (решает проблемы с памятью)
    options.add_argument('--disable-notifications') # Откл. уведомления

    if os.path.exists(CHROME_BINARY) and os.path.exists(CHROMEDRIVER_BINARY):
        options.binary_location = CHROME_BINARY
        service = Service(CHROMEDRIVER_BINARY)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(60)

        log.info('chrome-linux64 driver initialized.')
        return driver
    else:
        # на локалке просто возвращаем т.к. он скачан и драйвер его находит
        log.info('local driver initialized (requires pre-installed driver)')
        return webdriver.Chrome(options=options)

