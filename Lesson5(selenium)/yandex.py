from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('headless')


driver = webdriver.Chrome(options=chrome_options)

driver.get('https://market.yandex.ru/catalog--noutbuki-v-izhevske/54544/list?cpa=0&hid=91013&glfilter=7893318%3A152722%2C152981&onstock=1&local-offers-first=0')

time.sleep(3)
priceFrom = driver.find_element_by_id("glpricefrom")
priceFrom.send_keys("10000")

priceTo = driver.find_element_by_id("glpriceto")
priceTo.send_keys("30000")

buttonsPanel = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_8v6CFFrbuZ']")))

button48 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "vLDMfabyVq")))
button48.click()

button12 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Показывать по 12']")))
button12.click()


#
# time.sleep(10)
#
# hpCheck = driver.find_element_by_xpath("//input[@name='Производитель HP']")
# hpCheck.click()
#
# lenovoCheck = driver.find_element_by_xpath("//input[@name='Производитель Lenovo']")
# hpCheck.click()
#
# # goods = driver.find_elements_by_class_name('sku-card-small-container')
# # for good in goods:
# #     print(good.find_element_by_class_name('sku-card-small__title').text)
# #     print(good.find_element_by_class_name('sku-price__integer').text)
