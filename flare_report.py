import requests
import json
from datetime import datetime

# Set your start and end dates (format: YYYY-MM-DD)
start_date = "2025-06-01"
end_date = "2025-06-30"
api_key = "yBESXp2E0mkxktSh6tXJAo2GmAgGnt2pYk08EWxu"

# Construct the API URL
url = f"https://api.nasa.gov/DONKI/FLR?startDate={start_date}&endDate={end_date}&api_key={api_key}"

# Perform the GET request
response = requests.get(url)
data = response.json()

# Prepare HTML structure
html_content = f"""
<html>
<head>
    <meta charset="UTF-8">
    <title>NASA Solar Flares ({start_date} to {end_date})</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; background-color: #f4f4f4; padding: 20px; }}
        h1 {{ color: #333; }}
        .flare {{ background-color: #fff; border-left: 6px solid #2196F3; margin-bottom: 20px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .flare a {{ text-decoration: none; color: #2196F3; }}
        .flare h2 {{ margin: 0 0 10px 0; }}
        .label {{ font-weight: bold; }}
    </style>
</head>
<body>
    <h1>NASA Solar Flare Events ({start_date} to {end_date})</h1>
"""

# Convert JSON data to readable HTML blocks
for flare in data:
    instruments = ", ".join([inst["displayName"] for inst in flare.get("instruments", [])])
    linked_events = flare.get("linkedEvents") or []
    linked_html = ""
    if linked_events:
        linked_html = "<ul>" + "".join(
            f"<li>{event['activityID']}</li>" for event in linked_events
        ) + "</ul>"

    notifications = flare.get("sentNotifications") or []
    notification_html = ""
    if notifications:
        notification_html = "<ul>" + "".join(
            f"<li><a href='{note['messageURL']}'>{note['messageID']} ({note['messageIssueTime']})</a></li>"
            for note in notifications
        ) + "</ul>"

    html_content += f"""
    <div class="flare">
        <h2>{flare['flrID']} ({flare['classType']})</h2>
        <p><span class="label">Begin:</span> {flare['beginTime']} | <span class="label">Peak:</span> {flare['peakTime']} | <span class="label">End:</span> {flare['endTime']}</p>
        <p><span class="label">Location:</span> {flare.get('sourceLocation', 'N/A')} | <span class="label">Region:</span> {flare.get('activeRegionNum', 'N/A')}</p>
        <p><span class="label">Instruments:</span> {instruments}</p>
        <p><span class="label">Link:</span> <a href="{flare['link']}">{flare['link']}</a></p>
        {'<p><span class="label">Linked Events:</span>' + linked_html + '</p>' if linked_html else ''}
        {'<p><span class="label">Notifications:</span>' + notification_html + '</p>' if notification_html else ''}
    </div>
    """

# Finalize and write the HTML
html_content += "</body></html>"

with open("solar_flares_report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML file saved as solar_flares_report.html")
