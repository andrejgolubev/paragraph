from selenium import webdriver


def init():
    driver=webdriver.Chrome()
    driver.get('https://rasp.rsreu.ru')  

    return driver
    


