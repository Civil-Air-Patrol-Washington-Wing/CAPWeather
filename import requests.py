import requests
import json
from datetime import datetime
import pytz

state = "MD"

# Timezones
utc = pytz.utc
eastern = pytz.timezone('US/Eastern')

response = requests.get(f'https://api.weather.gov/alerts/active?area={state}').json()

for x in response['features']:
    sent_time_utc_str = x['properties']['sent']
    
    # Convert string to datetime object in UTC
    sent_time_utc = datetime.strptime(sent_time_utc_str, "%Y-%m-%dT%H:%M:%S%z")
    
    # Convert to Eastern Time
    sent_time_est = sent_time_utc.astimezone(eastern)
    
    # Format as readable string
    readable_time = sent_time_est.strftime("%Y-%m-%d %I:%M %p %Z")

    print("Area:", x['properties']['areaDesc'])
    print("Headline:", x['properties']['headline'])
    print("Description:", x['properties']['description'])
    print("Sent Time:", readable_time)
    print('\n******\n')
