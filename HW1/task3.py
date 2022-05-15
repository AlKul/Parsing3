import requests

url = 'https://www.cbr-xml-daily.ru/latest.js'
res1 = requests.get(url)

print('ok1')

url2 = 'https://soundcloud.com/atlanticrecords/shinedown'#-bully-1?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing'
res2 = requests.get(url2)
print('ok4')

url3 = 'http://map.aviasales.ru/supported_directions.json?origin_iata=LED&one_way=false&locale=ru'
res3 = requests.get(url3)
print('ok2')



## Let's try to get the cheapest ticket price for current time just anywhere
from datetime import datetime
today = datetime.now().strftime("%Y-%m-%d")

current_params = {
    'period':str(today)+':season',
    'no_viza':'true',
    'shengen':'false',
    'need_viza':'false'
}

url4 = 'http://map.aviasales.ru/prices.json?'#?origin_iata=LED&period=2017-02-01:season&direct=true&one_way=false&no_visa=true&schengen=true&need_visa=true&locale=ru&min_trip_duration_in_days=13&max_trip_duration_in_days=15'
res4 = requests.get(url4, params=current_params)

print('Tickets found')

print('Done')