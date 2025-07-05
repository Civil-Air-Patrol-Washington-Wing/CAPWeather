import requests
import datetime
import pytz
import json

# USGS API Endpoint
USGS_API = "https://waterservices.usgs.gov/nwis/site/"

# Parameters for Maryland, stream sites
params = {
    "stateCd": "MD",             # Maryland
    "siteType": "ST",            # Streams
    "format": "json",
    "siteStatus": "active"
}

# Request data
response = requests.get(USGS_API, params=params)
data = response.json()

# Extract relevant site info
sites = data.get("value", {}).get("site", [])

# HTML structure
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Maryland Streams and Rivers - USGS Data</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f4f4;
            margin: 0;
            padding: 20px;
            height: 100vh;
            overflow: hidden;
        }
        .content {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
        }
        ul {
            list-style: none;
            padding-left: 0;
        }
        li {
            margin-bottom: 10px;
            background: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        #scroll-container {
            height: 90vh;
            overflow: hidden;
            position: relative;
        }
        #scroll-content {
            position: absolute;
            animation: scrollDown linear 60s infinite;
        }
        @keyframes scrollDown {
            0% { top: 0; }
            100% { top: -100%; }
        }
    </style>
</head>
<body>
    <div class="content">
        <h1>Maryland Streams and Rivers</h1>
        <div id="scroll-container">
            <div id="scroll-content">
                <ul>
"""

# Append each site to HTML
for site in sites:
    site_name = site.get("siteName", "Unnamed Site")
    site_code = site.get("siteCode", [{}])[0].get("value", "N/A")
    html_content += f"<li><strong>{site_name}</strong><br>Site Code: {site_code}</li>\n"

# Close HTML
html_content += """
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Write to HTML file
with open("maryland_streams.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML file 'maryland_streams.html' created successfully.")
