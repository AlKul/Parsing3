#1) Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
# Для парсинга использовать xpath. Структура данных должна содержать: 
# - название источника,
# - наименование новости,
# - ссылку на новость,
# - дата публикации
# Нельзя использовать BeautifulSoup


 # 2) Сложить все новости в БД(Mongo); без дубликатов, с обновлениями

import requests
from datetime import datetime
import pandas as pd
from pprint import pprint
from datetime import datetime
from fp.fp import FreeProxy
from string import whitespace
from dotenv import load_dotenv
from lxml.html import fromstring
from tqdm import tqdm
import os

#CUSTOM_WHITESPACE = (whitespace + "\xa0").replace(" ", "")

# t = datetime.today().date()
# t.strftime("%Y-%m-%d")
#
# "19:25 вчера"
proxies = FreeProxy().get_proxy_list()

proxies_iterator = iter(proxies)
print("1")

# def clear_string(s, whitespaces=CUSTOM_WHITESPACE):
#     for space in whitespaces:
#         s = s.replace(space, " ")
#     return s

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}


class mail_news_parser:
    url = "https://news.mail.ru/"

    def __init__(self) -> None:
        self.df = pd.DataFrame()
    
    # Get all info from main page
    def get_main_page_content(self):

        # proxies = FreeProxy().get_proxy_list()
        # proxies_iterator = iter(proxies)
        for proxy in proxies:
            try:
                response = requests.get(self.url, headers=headers, proxies={"http": next(proxies_iterator)})
                return response
            except:
                print('Failed: bad proxy')
                pass
            return None

    def get_top_news(self, response):
        items_xpath = '//a[contains(@class, "js-topnews__item")]'
        dom = fromstring(response.text)
        items = dom.xpath(items_xpath)

        data_list = []
        for item in tqdm(items, desc = 'Top News'):
            data = {}
            data['source'] = self.url.split('/')[2]
            news_header = item.xpath('./span/span/text()')
            if len(news_header) == 0:
                data['news_header'] = None
            else:    
                data['news_header'] = news_header[0] 
        # Link
            data['url'] = item.xpath('./@href')[0]
        # Datetime
            date1 = fromstring(requests.get(item.xpath('.//@href')[0],headers=headers, proxies={"http": next(proxies_iterator)}).text).xpath("//*/span[contains(@class, 'js-ago')]/@datetime")
            date2 = datetime.strptime(date1[0], '%Y-%m-%dT%H:%M:%S%z')
            data['date'] = date2
            data_list.append(data)
        self.df = pd.concat([self.df, pd.DataFrame.from_records(data_list)])
        return 0

    def get_non_top_news(self, response):
        items_xpath = '//ul/li[contains(@class, "list__item") and not(contains(@class, "hidden_large"))]'
        dom = fromstring(response.text)
        items = dom.xpath(items_xpath)

        data_list = []
        count = 0
        for item in tqdm(items, desc = 'Other News'):
            data = {}
            data['source'] = self.url.split('/')[2]
            news_header = item.xpath('.//text()')
            if len(news_header) == 0:
                data['news_header'] = None
            else:    
                data['news_header'] = news_header[0] 
        # Link
            data['url'] = item.xpath('.//@href')[0]
        # Datetime
            date1 = fromstring(requests.get(item.xpath('.//@href')[0],headers=headers, proxies={"http": next(proxies_iterator)}).text).xpath("//*/span[contains(@class, 'js-ago')]/@datetime")
            date2 = datetime.strptime(date1[0], '%Y-%m-%dT%H:%M:%S%z')
            data['date'] = date2
            data_list.append(data)
        self.df = pd.concat([self.df, pd.DataFrame.from_records(data_list)])
        return 0
    
    def get_all_news(self):
        response = self.get_main_page_content()
        if response is None:
            print('Failed to load main page')
            return -1
        res1 = self.get_top_news(response)
        res2 = self.get_non_top_news(response)

class lenta_news_parser:
    url = "https://lenta.ru/"

    def __init__(self) -> None:
        self.df = pd.DataFrame()
    
    # Get all info from main page
    def get_main_page_content(self):

        # proxies = FreeProxy().get_proxy_list()
        # proxies_iterator = iter(proxies)
        for proxy in proxies:
            try:
                response = requests.get(self.url, headers=headers, proxies={"http": next(proxies_iterator)})
                return response
            except:
                print('Failed: bad proxy')
                pass
            return None

    def get_top_news(self, response):
        items_xpath = "//a[contains(@class, '_topnews') or contains(@class, '_compact')]"
        dom = fromstring(response.text)
        items = dom.xpath(items_xpath)

        data_list = []
        for item in tqdm(items, desc = 'Lenta News'):
            data = {}
            data['source'] = self.url.split('/')[2]
            news_header = item.xpath("./div/span[contains(@class, 'card-mini__title')]/text()")
            if len(news_header) == 0:
                data['news_header'] = None
            else:    
                data['news_header'] = news_header[0] 
        # Link
            data['url'] = self.url + item.xpath('./@href')[0][1:]
        # Datetime
            try:
                date1 = item.xpath(".//time")[0].text
                now = datetime.now()
                date2 = datetime(year = now.year, month = now.month, day = now.day, hour = int(date1.split(':')[0]), minute = int(date1.split(':')[1]), second = 0)
                data['date'] = date2
            except:
                data['date'] = None
                
            data_list.append(data)

        self.df = pd.concat([self.df, pd.DataFrame.from_records(data_list)])
        return 0
    
    def get_all_news(self):
        response = self.get_main_page_content()
        if response is None:
            print('Failed to load main page')
            return -1
        res1 = self.get_top_news(response)

class yandex_news_parser:
    url = "https://yandex.ru/news"

    def __init__(self) -> None:
        self.df = pd.DataFrame()
    
    # Get all info from main page
    def get_main_page_content(self):

        # proxies = FreeProxy().get_proxy_list()
        # proxies_iterator = iter(proxies)
        for proxy in proxies:
            try:
                response = requests.get(self.url, headers=headers, proxies={"http": next(proxies_iterator)})
                return response
            except:
                print('Failed: bad proxy')
                pass
            return None

    def get_top_news(self, response):
        items_xpath = '//div[contains(.//a/@class, "mg-card__link") and contains(@class, "mg-grid__item")]'
        dom = fromstring(response.text)
        items = dom.xpath(items_xpath)

        data_list = []
        for item in tqdm(items, desc = 'Yandex News'):
            data = {}
            data['source'] = self.url.split('/')[2]
            news_header = item.xpath("./div/div/h2/a/text()")
            if len(news_header) == 0:
                data['news_header'] = None
            else:    
                data['news_header'] = news_header[0] 
        # Link
            data['url'] = item.xpath('.//a[contains(@class, "mg-card__link")]/@href')[0]
        # Datetime
            try:
                date1 = item.xpath(".//span[contains(@class, 'mg-card-source__time')]/text()")[0]
                now = datetime.now()
                date2 = datetime(year = now.year, month = now.month, day = now.day, hour = int(date1.split(':')[0]), minute = int(date1.split(':')[1]), second = 0)
                data['date'] = date2
            except:
                data['date'] = None
                
            data_list.append(data)

        self.df = pd.concat([self.df, pd.DataFrame.from_records(data_list)])
        return 0
    
    def get_all_news(self):
        response = self.get_main_page_content()
        if response is None:
            print('Failed to load main page')
            return -1
        res1 = self.get_top_news(response)

# yandex_news = yandex_news_parser()
# yandex_news.get_all_news()

# lenta_news = lenta_news_parser()
# lenta_news.get_all_news()

# mail_news = mail_news_parser()
# mail_news.get_all_news()


print()

# 2) Сложить все новости в БД(Mongo); без дубликатов, с обновлениями

from pymongo import MongoClient

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST", None)
MONGO_PORT = int(os.getenv("MONGO_PORT", None))
MONGO_DB = os.getenv("MONGO_DB", None)
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", None)


def update_MDB(info: pd.DataFrame):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        news = db[MONGO_COLLECTION]
        info 
        info.fillna('',inplace=True)
        records = info.to_dict('records')
        for record in records:
            # Проверяем, существует ли запись с текущим урлом. Если нет - апдейт
            news.update_one(
                {"url": record['url']}, 
                {'$set': record}, 
                upsert = True
                )
    return 0

def main():
    yandex_news = yandex_news_parser()
    yandex_news.get_all_news()

    lenta_news = lenta_news_parser()
    lenta_news.get_all_news()

    mail_news = mail_news_parser()
    mail_news.get_all_news()

    print("All news collected")
    df = pd.concat([mail_news.df, lenta_news.df, yandex_news.df], ignore_index=True)

    update_MDB(df)
    print('All news updated in MDB')
    return 0
    

if __name__ == '__main__':
    main()