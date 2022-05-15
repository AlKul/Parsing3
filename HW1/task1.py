# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json; написать функцию, возвращающую список репозиториев.

import requests
import pprint
import pickle
import os
from dotenv import load_dotenv
load_dotenv()

USERNAME = os.getenv("USERNAME", None)
user_login = 'defunkt'

url = f'https://api.github.com/users/{user_login}'

response = requests.get(url)
print('ok')
pprint.pprint(response)

repos_url = response.json()['repos_url']
response2 = requests.get(repos_url).json()

print('ok2')

# Функция ниже достанет JSON с репозитоиями для переданного юзера и сохранит результат в файл ./User_repos.json
def get_repos_json(user_login):
    url = f'https://api.github.com/users/{user_login}'
    response = requests.get(url)
    #pprint.pprint(response)
    repos_url = response.json()['repos_url']

    res = requests.get(repos_url).json()

    dir_path = os.path.join('results')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    filename = f"{user_login}_repositories.json"
    file_path = os.path.join(dir_path, filename)

    with open(file_path, 'wb') as f:
        pickle.dump(res, f)

    return res
print('ok3')

# Функция ниже достанет из JSON'а список ссылок на репозитории
def get_repos_urls(json_file):
    url_list = []
    for item in json_file:
        url_list.append(item['html_url'])
    return url_list
print('ok4')

# Финальная функция, возвращает список репозиториев
def get_user_repositories_list(user_login):
    return get_repos_urls(get_repos_json(user_login))

print('done')

print(get_user_repositories_list(user_login))

