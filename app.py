from flask import Flask, request
from datetime import datetime
import logging
import requests
from user_agents import parse

app = Flask(__name__)

# Logging konfigurieren
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)

def get_ip_info(ip):
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        data = res.json()
        return {
            "city": data.get("city", "Unbekannt"),
            "region": data.get("region", ""),
            "country": data.get("country", "Unbekannt"),
            "org": data.get("org", "Unbekannt"),
        }
    except:
        return {
            "city": "Unbekannt",
            "region": "",
            "country": "Unbekannt",
            "org": "Unbekannt",
        }

@app.route("/")
def track():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")
    ref = request.headers.get("Referer", "")
    lang = request.headers.get("Accept-Language", "").split(",")[0]

    ua = parse(user_agent)
    location = get_ip_info(ip)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Browser-Fingerprint erzeugen
    fingerprint = hash(f"{ip}_{lang}_{ua.browser.family}_{ua.os.family}")

    log_entry = (
        f"✅ Echter Klick erkannt!\\n"
        f"🕒 Zeitpunkt       : {timestamp} UTC\\n"
        f"🌍 IP-Adresse     : {ip}\\n"
        f"📍 Standort       : {location['city']}, {location['region']} ({location['country']})\\n"
        f"🏢 Provider       : {location['org']}\\n"
        f"🖥️ Betriebssystem : {ua.os}\\n"
        f"🌐 Browser        : {ua.browser}\\n"
        f"🔗 Referrer       : {ref or 'Unbekannt'}\\n"
        f"🈯 Sprache        : {lang}\\n"
        f"🔐 Fingerprint    : {fingerprint}\\n"
        f"{'-'*40}"
    )

    logging.info(log_entry)

    return f"""
    <html>
    <head><title>Danke für deinen Besuch</title></head>
    <body style='font-family:sans-serif;'>
        <h2 style='color:red;'>⚠️ Diese Daten wurden beim Klick übermittelt:</h2>
        <ul>
            <li><b>🧠 User-Agent</b>: {user_agent}</li>
            <li><b>🌍 IP-Adresse</b>: {ip}</li>
            <li><b>📍 Stadt</b>: {location['city']}</li>
            <li><b>🖥️ Betriebssystem</b>: {ua.os}</li>
            <li><b>🌐 Browser</b>: {ua.browser}</li>
            <li><b>🈯 Sprache</b>: {lang}</li>
            <li><b>🔗 Referrer</b>: {ref or 'Unbekannt'}</li>
            <li><b>🔐 Fingerprint</b>: {fingerprint}</li>
        </ul>
        <p style='color:gray;'>All das wurde übermittelt, nur weil du den Link geöffnet hast.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
