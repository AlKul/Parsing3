#2) Написать программу, которая собирает «Новинки» с сайта техники mvideo
# и складывает данные в БД. Магазины можно выбрать свои.
# Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

import os

from dotenv import load_dotenv
load_dotenv()

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path="/Users/Alexx/Documents/Geek Brains/Parsing/Lesson5(selenium)/Chrome_driver/chromedriver", options=chrome_options)

url = 'https://www.mvideo.ru/'

driver.get(url)

# Сюда будем кидать заголовки, как дойдем до новинок - закончим
headers = []

# счетчик "прокручиваний вниз"
i = 0
# флаг - станет 1, когда наткнемся на Новинки
flag = 0

while i < 10:
    time.sleep(1.5)
    i+=1

    headers = list(set((headers + driver.find_elements(By.XPATH, '//h2[contains(@class, "title")]'))))

    for header in headers:
        if header.text.find('овинки') > -1:
            flag = 1
            break
# Листаем вниз
    actions = ActionChains(driver)
    actions.send_keys(Keys.PAGE_DOWN)
    actions.perform()

    if flag:
        break

goods_list = []
if flag == 1:
    goods = driver.find_elements(By.XPATH, '//div[contains(@class, "mvid-carousel-inner")]/a[contains(@class, "story-item ng-star-inserted")]')
    print(f'Found {len(goods)} goods')
    for item in goods:
        goods_list.append(
            {
                'url': item.get_attribute('href')
            }
        )

print('Done collecting new goods')
    # if len(headers) != 0:
    #     print('Found it')
    #     break

from pymongo import MongoClient

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST", None)
MONGO_PORT = int(os.getenv("MONGO_PORT", None))
MONGO_DB = 'MVideo_Goods'
MONGO_COLLECTION = 'Goods_Collection'

def update_MDB(info: list):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        goods = db[MONGO_COLLECTION]
        records = info
        for record in records:
            # Проверяем, существует ли запись с текущим урлом. Если нет - апдейт
            goods.update_one(
                {'url': record['url']},
                {'$set': record},
                upsert=True
            )
    print('Updating complete')
    return 0

update_MDB(goods_list)

time.sleep(10)
driver.close()
driver.quit()

print("Done")

