import requests 
from datetime import datetime
import pytz

# Get public IP address
ip_address = requests.get('http://api.ipify.org').text
print("IP Address:", ip_address)

# Get geo info from IP
geo_data = requests.get(f'http://ip-api.com/json/{ip_address}').json()
print("Geo Data:", geo_data)

lat = geo_data['lat']
lon = geo_data['lon']
print("Latitude:", lat)
print("Longitude:", lon)

# Get weather alerts for location
response = requests.get(f'https://api.weather.gov/alerts?point={lat},{lon}').json()
alerts = response['features']
print(f"Alerts: {len(alerts)}")

# Timezones
utc = pytz.utc
eastern = pytz.timezone('US/Eastern')

# Severity rank helper
severity_rank = {
    "Extreme": 1,
    "Severe": 2,
    "Moderate": 3,
    "Minor": 4,
    "Unknown": 5,
}

# Sort by severity, then by sent time (descending)
alerts.sort(
    key=lambda x: (
        severity_rank.get(x['properties']['severity'], 99),
        -datetime.strptime(x['properties']['sent'], "%Y-%m-%dT%H:%M:%S%z").timestamp()
    )
)

# Filter alerts by severity
extreme_alerts = [a for a in alerts if a['properties']['severity'] == "Extreme"]
high_alerts = [a for a in alerts if a['properties']['severity'] == "Severe"]

# Write alerts to HTML
with open('alert.html', 'w', encoding='utf-8') as file:
    file.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="300">
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            line-height: 1.6;
            background-color: white;
            color: black;
            transition: background-color 0.5s, color 0.5s;
        }
        .dark-mode {
            background-color: #121212;
            color: #e0e0e0;
        }
        button {
            position: fixed;
            top: 10px;
            right: 10px;
            margin-left: 10px;
            padding: 10px;
            font-size: 14px;
            z-index: 1000;
        }
    </style>
</head>
<body>

<button onclick="toggleScroll()">Pause Scroll</button>
<button onclick="toggleDarkMode()">Night Mode</button>

<script>
let scrollSpeed = 1;
let delay = 50;
let scrollEnabled = true;

function scrollPage() {
    if (scrollEnabled) {
        window.scrollBy(0, scrollSpeed);
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
            window.scrollTo(0, 0);
        }
    }
}
setInterval(scrollPage, delay);

function toggleScroll() {
    scrollEnabled = !scrollEnabled;
    document.querySelector('button').innerText = scrollEnabled ? "Pause Scroll" : "Resume Scroll";
}

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}
</script>
""")

    # Audio alert logic for both levels
    if extreme_alerts or high_alerts:
        file.write("<script>\n")
        file.write("const playedAlerts = JSON.parse(localStorage.getItem('playedAlerts') || '{}');\n")

        if extreme_alerts:
            extreme_ids = [a['id'] for a in extreme_alerts]
            file.write(f"const extremeAlerts = {extreme_ids};\n")
            file.write("""
extremeAlerts.forEach(id => {
    if (!playedAlerts[id]) {
        const audio = new Audio('extreme.mp3');
        audio.play();
        playedAlerts[id] = true;
    }
});
""")

        if high_alerts:
            high_ids = [a['id'] for a in high_alerts]
            file.write(f"const highAlerts = {high_ids};\n")
            file.write("""
highAlerts.forEach(id => {
    if (!playedAlerts[id]) {
        const audio = new Audio('high.mp3');
        audio.play();
        playedAlerts[id] = true;
    }
});
""")

        file.write("localStorage.setItem('playedAlerts', JSON.stringify(playedAlerts));\n")
        file.write("</script>\n")

    # Write alert content
    for x in alerts:
        sent_time_utc = datetime.strptime(x['properties']['sent'], "%Y-%m-%dT%H:%M:%S%z")
        sent_time_est = sent_time_utc.astimezone(eastern)
        readable_time = sent_time_est.strftime("%Y-%m-%d %I:%M %p %Z")

        file.write(f"<h1>{x['properties']['headline']}</h1>")
        file.write(f"<h3>{x['properties']['areaDesc']}</h3>")
        file.write(f"<p><strong>Severity:</strong> {x['properties']['severity']}</p>")
        file.write(f"<p><strong>Sent Time:</strong> {readable_time}</p>")
        file.write(f"<p>{x['properties']['description']}</p>")
        file.write("<hr>")

    file.write("</body></html>")
