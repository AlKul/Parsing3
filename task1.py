# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, 
# записывающую собранные вакансии в созданную БД.

import pickle
import os
from pprint import pprint
import pandas as pd
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs
from tqdm import tqdm

from pymongo import MongoClient

def get(url, headers, params, proxies=None):
    r = requests.get(url, headers=headers, params=params, proxies=proxies)
    return r

# Фнукция для быстрого добавления записи в mongoDB

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST", None)
MONGO_PORT = int(os.getenv("MONGO_PORT", None))
MONGO_DB = os.getenv("MONGO_DB", None)
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", None)

# MONGO_HOST = "localhost"
# MONGO_PORT = 27017
# MONGO_DB = "vacancies"
# MONGO_COLLECTION = "vacancies_collection"

def insert_into_MDB(info):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        vacancies = db[MONGO_COLLECTION]
        vacancies.insert_many(info)
    return 0
    

# Напишем функцию для определения зп
import numpy as np
def salary_string_parser(string):
    data = {}
    items = string.split(' ')
    if len(items) == 4: # x.000 - y.000 $
        min, max = int(items[0].replace("\u202f", '')), int(items[2].replace("\u202f", ''))
        currency = items[3]
    elif len(items) == 3: # от (до)
        if items[0] == 'от':
            min = int(items[1].replace("\u202f", ''))
            max = np.inf # ну пусть пока так будет
            currency = items[2]
        elif items[0] == 'до':
            min = 0
            max = int(items[1].replace("\u202f", ''))
            currency = items[2]
        else:
            return None
    else:
        return None
    data['min'] = min
    data['max'] = max
    data['currency'] = currency
    return data


def get_data_by_params(params):
    url = "https://hh.ru/search/vacancy?"
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
    }
    proxies = { # Наверное, по-хорошему, надо также парсить сайт для списка прокси, но пока так
        'http': 'http://78.28.152.111:80',
        #'https': 'https://165.227.223.19:3128',
    }

    r = get(url, headers, params)
    if r.status_code >= 400:
        print(f'{__name__} returned error {r.status_code}')
        return None
    soup = bs(r.text, "html.parser")
    vacancies = soup.find_all('div', attrs={"class": "serp-item"})
    df = pd.DataFrame()
    for vacancy in vacancies:
        data = {}
        description = vacancy.find('a', attrs={"class": "bloko-link"})
        employer = vacancy.find('a', attrs={"data-qa": "vacancy-serp__vacancy-employer"})
        try:
            salary = salary_string_parser(vacancy.find('span', attrs={"class": "bloko-header-section-3"}).text)
        except:
            salary = None
        data['url'] = [description.attrs['href']]  # url to vacancy
        data['name'] = [description.text]
        try:
            data['empoyer_url'] = ['https://hh.ru/' + employer.attrs['href']]  # url to empoyer
        except:
            data['empoyer_url'] = None
        data['salary'] = [salary]
        df = pd.concat([df, pd.DataFrame(data)])
    return df


# Функция для сохранения в pkl

def res_2_pkl(res, name='vacancies'):
    dir_path = os.path.join('results')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    filename = f"{name}.pkl"
    file_path = os.path.join(dir_path, filename)
    with open(file_path, 'wb') as f:
        pickle.dump(res, f)
    print(f'Data dumped successfully to {file_path}')
    return 0

# Итоговая функция
# На вход строка для поиска и количесвто страниц (опционально)

def get_data(vacancy, pages = 40):
    df_res = pd.DataFrame()
    url = "https://hh.ru/search/vacancy?"  # vacancy?text=программист+аналитик&from=suggest_post&salary=&clusters=true&area=1&ored_clusters=true&enable_snippets=true"
    for page in tqdm(range(pages)):
        params = {
            'text': vacancy,
            'snippets': 'false',
            'page': page
        }
        df = get_data_by_params(params)
        if df is None:
            print('Nothing left')
            break
        #print(f'Page: {page}\n-loaded: {df.shape[0]}')
        if df.shape[0] == 0:
            break
        df_res = pd.concat([df_res, df], ignore_index=True)
    insert_into_MDB(df_res.to_dict('records'))
#        df_res.to_csv('./results/df_res.csv')

    # и сохраним результат в pkl
    # res_2_pkl(df_res, vacancy)


    return df_res






def main():
    return get_data(vacancy='программист консультант', pages = 20)

if __name__ == '__main__':
    print(f'{main().shape[0]} records found')
