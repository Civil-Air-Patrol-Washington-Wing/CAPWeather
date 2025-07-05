import requests
from datetime import datetime, timedelta, timezone
import os

# === Constants ===
API_KEY = 'yBESXp2E0mkxktSh6tXJAo2GmAgGnt2pYk08EWxu'
API_URL = 'https://api.nasa.gov/neo/rest/v1/feed'
OUTPUT_FILE = 'neo_report.html'

# === Date Setup ===
end_date = datetime.now(timezone.utc).date()
start_date = end_date - timedelta(days=7)

# === Fetch Data ===
params = {
    'start_date': start_date.isoformat(),
    'end_date': end_date.isoformat(),
    'api_key': API_KEY
}

response = requests.get(API_URL, params=params)
data = response.json()

# === HTML Generator ===
def create_html(data):
    html = '''
    <html>
    <head>
        <meta charset="UTF-8">
        <title>NEO Report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                background-color: #111;
                color: #fff;
                margin: 0;
                padding: 0 2em;
                overflow: hidden;
            }
            .scroll-container {
                height: 100vh;
                overflow-y: hidden;
                animation: scroll 60s linear infinite;
            }
            @keyframes scroll {
                0% { transform: translateY(100%); }
                100% { transform: translateY(-100%); }
            }
            h1, h2 { color: #ffcc00; }
            .neo {
                border-bottom: 1px solid #444;
                margin-bottom: 1em;
                padding-bottom: 1em;
            }
        </style>
    </head>
    <body>
    <div class="scroll-container">
    <h1>NASA Near-Earth Object Report</h1>
    '''

    for date, neos in data.get('near_earth_objects', {}).items():
        html += f"<h2>{date}</h2>"
        for neo in neos:
            name = neo['name']
            url = neo['nasa_jpl_url']
            hazard = "Yes" if neo['is_potentially_hazardous_asteroid'] else "No"
            diameter = neo['estimated_diameter']['meters']
            dia_min = diameter['estimated_diameter_min']
            dia_max = diameter['estimated_diameter_max']
            close_data = neo['close_approach_data'][0]
            approach_time = close_data['close_approach_date_full']
            distance_km = close_data['miss_distance']['kilometers']
            velocity_kph = close_data['relative_velocity']['kilometers_per_hour']

            html += f'''
            <div class="neo">
                <strong><a href="{url}" target="_blank" style="color: #9cf;">{name}</a></strong><br>
                Hazardous: {hazard}<br>
                Diameter: {dia_min:.1f}m - {dia_max:.1f}m<br>
                Close Approach: {approach_time}<br>
                Distance: {float(distance_km):,.0f} km<br>
                Velocity: {float(velocity_kph):,.0f} km/h<br>
            </div>
            '''

    html += '''
    </div>
    </body>
    </html>
    '''
    return html

# === Write to File ===
html_content = create_html(data)
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"NEO report generated: {os.path.abspath(OUTPUT_FILE)}")
