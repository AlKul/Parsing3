from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.get('https://gb.ru/login')

elem = driver.find_element_by_id('user_email')
elem.send_keys('study.ai_172@mail.ru')

elem = driver.find_element_by_id('user_password')
elem.send_keys('Password172')

check = driver.find_element_by_id('user_remember_me')
check.click()

elem.send_keys(Keys.ENTER)

profile = driver.find_element_by_xpath("//span[@class='arrow top']/../a")
driver.get(profile.get_attribute('href'))

profile = driver.find_element_by_class_name("text-sm")
driver.get(profile.get_attribute('href'))

gender = driver.find_element_by_name('user[gender]')
select = Select(gender)
select.select_by_value('male')

gender.submit()

driver.back()
driver.forward()
driver.refresh()

driver.close()



