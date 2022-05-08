# Зарегистрироваться на https://openweathermap.org/api и написать функцию,
# которая получает погоду в данный момент для города, название которого получается через input.
# https://openweathermap.org/current
import pprint

import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_key = os.getenv("API_KEY", None)
city_name = 'Moscow'

url1 = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_key}'
result1 = requests.get(url1)
pprint.pprint(result1.json())


print('ok1')
