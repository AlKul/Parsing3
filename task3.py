# 3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pprint import pprint
import pandas as pd
from tqdm import tqdm

from task1 import salary_string_parser, get, get_data_by_params


load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST", None)
MONGO_PORT = int(os.getenv("MONGO_PORT", None))
MONGO_DB = os.getenv("MONGO_DB", None)
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", None)


def update_MDB(info):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        vacancies = db[MONGO_COLLECTION]
        for record in info:
            # ПРоверяем, существует ли запись с текущим урлом. Если нет - апдейт
            vacancies.update_one(
                {"url": record['url']}, 
                {'$set': record}, 
                upsert = True
                )
    return 0

def count_MDB():
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        vacancies = db[MONGO_COLLECTION]
        cursor = vacancies.find()
        return len(list(cursor))

def update_data(vacancy, pages = 40):
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
    return update_MDB(df_res.to_dict('records'))

def main():
    res = update_data(vacancy='программист', pages = 20)
    if res == 0:
        print(f"DB successfully updated: {count_MDB()} records now")

if __name__ == '__main__':
    main()