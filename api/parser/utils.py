from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from api.parser.parser_conf import init



def convert_date(date: str): 
    """date подаётся в формате в таком, в котором юзер ее выбирает из списка на фронтенде для последующей конвертации 
    в пригодную для вставки в ссылку и парсинга сайта ргрту. т.е. (10.11.2025, числ.) -> 2025-11-10  """
    return '-'.join(reversed(date[:10].split('.'))) 











# def _parse_date_v2(driver: webdriver.Chrome): 
#     """ПАРСИТ ВСЕ актуальные ДАТЫ из выпадающего меню """

#     wait = WebDriverWait(driver, 10)
#     css_selector = '.column[style*="width: 152px"] .select-wrap' 

#     option_box = wait.until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
#     )
#     option_box.click()    


#     options_list = wait.until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, 'select[name="date"]'))
#     ) 
    
#     # Парсим все доступные группы
#     dates_dict = {}
#     dates_options = options_list.find_elements(By.TAG_NAME, "option")

#     for user_date in dates_options:
#         data_value = user_date.get_attribute("value")
#         user_date = user_date.text.strip()
        
#         if data_value and user_date:
#             dates_dict[user_date] = data_value 

#     return dates_dict 

# driver = init() 