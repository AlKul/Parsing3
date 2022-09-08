#1) Написать программу, которая собирает входящие письма
# из своего или тестового почтового ящика
# и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)

# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#


import os

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from lxml.html import fromstring
import time
import pprint

load_dotenv()

LOGIN = os.getenv("LOGIN", None)
PASSWORD = os.getenv("PASSWORD", None)

chrome_options = Options()
chrome_options.add_argument('start-maximized')

# Инициализируем вебдрайвер
driver = webdriver.Chrome(executable_path="/Users/Alexx/Documents/Geek Brains/Parsing/Lesson5(selenium)/Chrome_driver/chromedriver")#, options=chrome_options)
driver.get('https://account.mail.ru/login?page=https%3A%2F%2Fe.mail.ru%2Fmessages%2Finbox%3Futm_source%3Dportal%26utm_medium%3Dmailbox%26utm_campaign%3De.mail.ru%26mt_click_id%3Dmt-veoz41-1662108620-3928595397&allow_external=1')

time.sleep(1)
elem = driver.find_element(By.NAME, 'username')
elem.send_keys(LOGIN)
elem.send_keys(Keys.ENTER)

# ниже подождем форму для пароля
wait_for_elem = WebDriverWait(driver, timeout=2)
wait_for_elem.until(expected_conditions.presence_of_element_located((By.NAME, 'password')))

# но ждать все равно придется - иначе в половине случаев программа ломается - уже вопрос, почему так
time.sleep(1)

elem = driver.find_element(By.NAME, 'password')
elem.send_keys(PASSWORD)
elem.send_keys(Keys.ENTER)

time.sleep(2)

data_list = []

# Здесь отдельная функция для парсинга информации из письма после его открытия
def get_message_info():
# (от кого, дата отправки, тема письма, текст письма полный)
    print('Reading message: ', end='')
    data = {}
    time.sleep(2)
    print('From...', end='')
# Здесь попробуем достать адресат либо так...
    try:
        data['from'] = driver.find_element(By.XPATH, '//span[contains(@class, "b-contact-informer-target js-contact-informer")][1]').get_attribute(
        'data-contact-informer-email')
# ...либо так
    except Exception as ex:
        try:
            data['from'] = driver.find_elements(By.XPATH, '//span[contains(@class, "letter-contact")]')[0].get_attribute('title')
        except:
            print('Failed getting "from"')
    print('done. ', end='')

# спойлер: этот алгоритм начинает ломаться, начиная где-то с 9-й ссылки
# Но фокус в том, что если проверить вручную, я вижу эти xpaths

    print('Date...', end='')
# Дату пока достанем как есть - в дальнейшем преобразую в datetime
    try:
        data['datetime'] = driver.find_elements(By.XPATH, '//div[contains(@class, "letter__date")]')[0].text
    except Exception as ex:
        print(ex)
    print('done', end='')
    print('Subject...', end='')
    try:
        data['subject'] = driver.find_elements(By.XPATH, '//h2[contains(@class, "thread-subject")]')[0].text#.get_attribute('text')

    except Exception as ex:
        print(ex)
    print('done')
    try:
        data['text'] = driver.find_element(By.XPATH, '//p').text

    except Exception as ex:
        print(ex)
    pprint.pprint(data)
    data_list.append(data)
    return data

# Функция для объединения массивов без дублей
def list_of_unique_elements_union(x: list, y: list):
    return list(set(x+y))

letters = driver.find_elements(By.XPATH, '//a[contains(@class, "llc")]')

letters_list = []
prev_len = len(letters_list)
time.sleep(3)

i = 0
data_list = []
letters_href_list = []

print('Starting the loop')
try:
    while True:
        # Собираем без пересечений все элементы - письма
        letters = driver.find_elements(By.XPATH, '//a[contains(@class, "llc")]')
        letters_list = list_of_unique_elements_union(letters_list, letters)

        i += 1
        # достанем отдельно ссылки
        for letter in letters:
            letters_href_list.append(letter.get_attribute("href"))

        print(f'All {len(set(letters_href_list))} links found')

        if prev_len == len(letters_list):
            print('No new messages added')
            break
        else:
            print(f'{len(letters_list) - prev_len} new messages added')
        prev_len = len(letters_list)

# Пролистнем до последнего письма
        actions = ActionChains(driver)
        actions.move_to_element(letters[-1])
        actions.perform()
        time.sleep(5)

    print(f'All 2gether {len(set(letters_href_list))} found')

    for i, letter_url in enumerate(set(letters_href_list)):
        print(f'№{i} : {letter_url}')


        if letter_url is None:
            print("Empty url u dumb bitch!")
            continue
        # Далее, после открытия письма, достанем из него всю информацию
        try:
            driver.get(letter_url)
            data = get_message_info()
            data_list.append(data)
        except Exception as ex:
            print(ex)

except Exception as ex:
    print(ex)
finally:
    time.sleep(20)
    driver.close()
    driver.quit()


from pymongo import MongoClient

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST", None)
MONGO_PORT = int(os.getenv("MONGO_PORT", None))
MONGO_DB = os.getenv("MONGO_DB", None)
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", None)

# Тут отдельная функция для добавления записей в Монго без дублей (за уникальные ключи я принимаю пару from and datetime)
def update_MDB(info: list):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        mail = db[MONGO_COLLECTION]
        records = info
        print('Updating')
        for record in records:
            # Проверяем, существует ли запись с текущим урлом. Если нет - апдейт
            mail.update_one(
                {'datetime': record['datetime'], 'from': record['from']},
                {'$set': record},
                upsert=True
            )
    return 0

update_MDB(data_list)
