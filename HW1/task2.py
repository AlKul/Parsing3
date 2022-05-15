# 2. Зарегистрироваться на https://openweathermap.org/api и написать функцию,
# которая получает погоду в данный момент для города, название которого получается через input.
# https://openweathermap.org/current
import pprint

import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_key = os.getenv("API_KEY", None)
city_name = 'Maliboo'

url1 = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_key}'
result1 = requests.get(url1)

def get_coordinates_by_city_name(city_name):
    concrete_params = {
        'q':city_name,
        'limit':1,
        'appid':API_key
    }
    #url1 = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_key}'
    url1 = 'http://api.openweathermap.org/geo/1.0/direct?'
    result1 = (requests.get(url1, params=concrete_params).json()[0]['lat'], requests.get(url1, params=concrete_params).json()[0]['lon'])
    return result1


#url2 = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}'
def get_weather_by_coordinates(lat, lon):
    url2 = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'
    request2 = requests.get(url2).json()
    temperature = request2.get('main').get('temp')
    weather = request2.get('weather')[0].get('main')
    return str(round(temperature - 273, 2)) + '°C' + ' - ' + str(weather)
def get_weather_by_city_name(city_name):
    return get_weather_by_coordinates(*get_coordinates_by_city_name(city_name))


print(f'The weather in {city_name}:\n' + get_weather_by_city_name(city_name))