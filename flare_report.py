import requests
from datetime import datetime, timedelta, timezone

# Automatically calculate date range
end_date = datetime.now(timezone.utc).date()
start_date = end_date - timedelta(days=7)

# Format dates as YYYY-MM-DD strings
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# NASA API key and URL
api_key = "yBESXp2E0mkxktSh6tXJAo2GmAgGnt2pYk08EWxu"
url = f"https://api.nasa.gov/DONKI/FLR?startDate={start_date_str}&endDate={end_date_str}&api_key={api_key}"


# Fetch data
response = requests.get(url)
data = response.json()

# HTML template with auto-scroll
html_content = f"""
<html>
<head>
    <meta charset="UTF-8">
    <title>NASA Solar Flares ({start_date_str} to {end_date_str})</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #333; }}
        .flare {{
            background: white;
            border-left: 6px solid #2196F3;
            margin-bottom: 20px;
            padding: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .flare a {{ color: #2196F3; text-decoration: none; }}
        .flare h2 {{ margin-top: 0; }}
        .label {{ font-weight: bold; }}
    </style>
    <script>
        let scrollSpeed = 0.5;
        let scrollInterval = 20;
        window.onload = function() {{
            function autoScroll() {{
                window.scrollBy(0, scrollSpeed);
                if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {{
                    window.scrollTo(0, 0);
                }}
            }}
            setInterval(autoScroll, scrollInterval);
        }};
    </script>
</head>
<body>
    <h1>NASA Solar Flare Events ({start_date_str} to {end_date_str})</h1>
"""

# Add each flare
for flare in data:
    instruments = ", ".join([inst["displayName"] for inst in flare.get("instruments", [])])
    linked_events = flare.get("linkedEvents") or []
    linked_html = "<ul>" + "".join(
        f"<li>{e['activityID']}</li>" for e in linked_events
    ) + "</ul>" if linked_events else ""

    notifications = flare.get("sentNotifications") or []
    notification_html = "<ul>" + "".join(
        f"<li><a href='{note['messageURL']}'>{note['messageID']} ({note['messageIssueTime']})</a></li>"
        for note in notifications
    ) + "</ul>" if notifications else ""

    html_content += f"""
    <div class="flare">
        <h2>{flare['flrID']} ({flare['classType']})</h2>
        <p><span class="label">Begin:</span> {flare['beginTime']} |
           <span class="label">Peak:</span> {flare['peakTime']} |
           <span class="label">End:</span> {flare['endTime']}</p>
        <p><span class="label">Location:</span> {flare.get('sourceLocation', 'N/A')} |
           <span class="label">Region:</span> {flare.get('activeRegionNum', 'N/A')}</p>
        <p><span class="label">Instruments:</span> {instruments}</p>
        <p><span class="label">Link:</span> <a href="{flare['link']}">{flare['link']}</a></p>
        {'<p><span class="label">Linked Events:</span>' + linked_html + '</p>' if linked_html else ''}
        {'<p><span class="label">Notifications:</span>' + notification_html + '</p>' if notification_html else ''}
    </div>
    """

html_content += "</body></html>"

# Save to file
with open("solar_flares_report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML report saved for {start_date_str} to {end_date_str}.")
