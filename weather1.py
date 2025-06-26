import requests
import json

state = "MD"

response = requests.get(f'https://api.weather.gov/alerts/active?area={state}').json()

for x in response['features']:
    print(x['properties']['areaDesc'])
    print(x['properties']['headline'])
    print(x['properties']['description'])
    print(x['\n******\n'])