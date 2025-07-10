from flask import Flask, request
from user_agents import parse
import requests
from datetime import datetime

app = Flask(__name__)

def is_human(user_agent):
    bots = ["bot", "crawl", "spider", "preview", "facebookexternalhit", "WhatsApp", "Telegram"]
    return not any(bot in user_agent.lower() for bot in bots)

def get_geo(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return res.get("city", "Unbekannt"), res.get("country", "Unbekannt")
    except:
        return "Unbekannt", "Unbekannt"

@app.route("/")
def index():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua_string = request.headers.get('User-Agent', '')
    ua = parse(ua_string)
    mensch = is_human(ua_string)
    stadt, land = get_geo(ip)

    print("🧠 Neuer Zugriff erkannt:")
    print(f"   Zeitpunkt       : {now} UTC")
    print(f"   IP-Adresse      : {ip}")
    print(f"   Browser         : {ua.browser.family} {ua.browser.version_string}")
    print(f"   Betriebssystem  : {ua.os.family} {ua.os.version_string}")
    print(f"   Gerätetyp       : {ua.device.family}")
    print(f"   User-Agent      : {ua_string}")
    print(f"   Geostandort     : {stadt}, {land}")
    print(f"   ECHTER MENSCH   : {'✅ JA' if mensch else '❌ NEIN'}")
    print("-" * 50)

    return f"""
    <html>
    <head>
        <title>Vertrau mir, Bruder</title>
        <style>
            body {{
                background-color: #111;
                color: #eee;
                font-family: monospace;
                text-align: center;
                padding: 40px;
            }}
            .blink {{
                color: red;
                font-size: 28px;
                animation: blink 1s infinite;
            }}
            @keyframes blink {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0; }}
                100% {{ opacity: 1; }}
            }}
            button {{
                background-color: #333;
                border: none;
                color: white;
                padding: 12px 20px;
                margin: 20px;
                font-size: 16px;
                cursor: pointer;
            }}
        </style>
        <script>
            function showData() {{
                document.getElementById("datenbereich").style.display = "block";
            }}
        </script>
    </head>
    <body>
        <h1 class="blink">CHECKST DU?!</h1>
        <p>Du hast da echt draufgeklickt.</p>
        <button onclick="showData()">Meine Daten zurück</button>

        <div id="datenbereich" style="display:none; margin-top:30px;">
            <h3>Diese Infos haben wir bekommen:</h3>
            <ul style="text-align:left; display:inline-block;">
                <li><b>IP-Adresse:</b> {ip}</li>
                <li><b>Browser:</b> {ua.browser.family} {ua.browser.version_string}</li>
                <li><b>System:</b> {ua.os.family} {ua.os.version_string}</li>
                <li><b>Gerät:</b> {ua.device.family}</li>
                <li><b>Standort:</b> {stadt}, {land}</li>
                <li><b>Zeitpunkt:</b> {now} UTC</li>
                <li><b>Echter Mensch:</b> {'✅ JA' if mensch else '❌ NEIN'}</li>
            </ul>
            <p style='color:gray;'>All das wurde übermittelt, nur weil du den Link geöffnet hast.</p>
        </div>
    </body>
    </html>
    """
