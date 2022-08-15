# 2. Написать функцию, которая производит поиск 
# и выводит на экран вакансии с заработной платой больше введённой суммы.

from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

MONGO_HOST = os.getenv("MONGO_HOST", None)
MONGO_PORT = int(os.getenv("MONGO_PORT", None))
MONGO_DB = os.getenv("MONGO_DB", None)
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", None)


def min_salary_input():
    min_salary = input()
    if min_salary == 'q':
        return -1
    try:
        min_salary = float(min_salary)
        show_vacancies(min_salary)
        return 1
    except:
        print("Enter a number")
        return 0

def show_vacancies(min_salary):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        vacancies = db[MONGO_COLLECTION]
        cursor = vacancies.find({
            "salary.max" : {'$gt' : min_salary}
        })
        # Выведем пока только топ 10
        for item in list(cursor)[:10]:
            pprint(item, indent=4, width=1)
        return 0
        
def main():
    print("Enter your minimum salary to find vacancies\nEnter 'q' to quit\n")
    while True:
        res = min_salary_input()
        if res == -1:
            print('Quitting')
            break

if __name__ == '__main__':
    main()