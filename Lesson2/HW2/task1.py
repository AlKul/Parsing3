# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность)
# с сайтов Superjob(по желанию) и HH(обязательно).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#
# 1) Наименование вакансии.
# 2) Предлагаемую зарплату (отдельно минимальную и максимальную).
# 3) Ссылку на саму вакансию.
# 4) Сайт, откуда собрана вакансия.

import json
import time
import pickle
import os
from pprint import pprint
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

def get(url, headers, params, proxies=None):
    r = requests.get(url, headers=headers, params=params, proxies=proxies)
    return r

# Напишем функцию для определения зп
# (нашел строчку - '150\u202f000 – 180\u202f000 руб.', в которой зп указывается, но не более, буду ее парсить)
# Если можно было проще и элегантнее, простите, надеюсь, укажете

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
        'http': 'http://3.88.169.225:80',
        # 'https': 'https://165.227.223.19:3128',
    }

    r = get(url, headers, params)
    if r.status_code >= 400:
        return None
    soup = bs(r.text, "html.parser")
    vacancies = soup.find_all('div', attrs={"class": "vacancy-serp-item"})
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
        #df = df.append(data, ignore_index=True)
        df = pd.concat([df, pd.DataFrame(data)])
    return df

print('ok2')


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

    for page in range(pages):
        params = {
            'text': vacancy,
            'snippets': 'false',
            'page': page
        }
        df = get_data_by_params(params)
        if df is None:
            print('Nothing left')
            break
        print(f'Page: {page}\n-loaded: {df.shape[0]}')
        if df.shape[0] == 0:
            break
        df_res = pd.concat([df_res, df], ignore_index=True)
        df_res.to_csv('./results/df_res.csv')

    # и сохраним результат в pkl
    res_2_pkl(df_res, vacancy)


    return df_res

print('Done')

def main():
    return get_data(vacancy='программист какой-то', pages = 5)

if __name__ == '__main__':
    print(main().shape)
