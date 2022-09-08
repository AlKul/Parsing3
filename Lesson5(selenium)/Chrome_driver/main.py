from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

url = 'https://gb.ru/login/'
driver = webdriver.Chrome(executable_path='/Users/Alexx/Documents/Geek Brains/Parsing/Lesson5(selenium)/Chrome_driver/chromedriver')

try:
    driver.get(url=url)

    elem = driver.find_element('id', 'user_email')
    elem.send_keys('study.ai_172@mail.ru')

    elem = driver.find_element('id', 'user_password')
    elem.send_keys('NextPassword172!?')

    elem.send_keys(Keys.ENTER)

    time.sleep(10)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
print('Done')
