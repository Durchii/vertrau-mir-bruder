from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def track():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr).split(',')[0].strip()
    ua = request.headers.get('User-Agent', 'unbekannt')
    lang = request.headers.get('Accept-Language', 'unbekannt')
    ref = request.headers.get('Referer', 'direkter Zugriff')

    print("==== NEUER KLICK ====")
    print(f"🕒 Zeitpunkt     : {timestamp}")
    print(f"🌍 IP-Adresse    : {ip_address}")
    print(f"🖥️  User-Agent   : {ua}")
    print(f"🌐 Sprache      : {lang}")
    print(f"🔗 Referrer     : {ref}")
    print("=====================
")

    return f"""    <html>
      <head>
        <title>Danke für deinen Besuch</title>
        <meta charset="utf-8">
        <style>
          body {{ font-family: sans-serif; background:#fffbe6; color:#333; padding:2rem; text-align:center; }}
          .small {{ margin-top:2rem; font-size:0.9rem; color:#999; }}
          .checkstdu {{ margin-top:3rem; font-size:3rem; font-weight:bold; color:red; animation:blinker 0.7s linear infinite; }}
          @keyframes blinker {{ 50% {{ opacity:0; }} }}
          .fake-btn {{ margin-top:2rem; padding:1rem 2rem; font-size:1.2rem; background:#e63946; color:#fff; border:none; border-radius:8px; cursor:pointer; transition:0.3s ease; }}
          .fake-btn:hover {{ background:#a4161a; }}
          .hidden {{ display:none; margin-top:2rem; }}
          .surprise-text {{ font-size:1.3rem; color:#222; margin-bottom:1rem; font-weight:bold; }}
          img {{ max-width:100%; height:auto; border:3px dashed red; border-radius:10px; }}
          .info-box {{ margin-top:2rem; background:#ffe6e6; padding:1rem; border:1px solid #e63946; border-radius:8px; display:inline-block; text-align:left; }}
        </style>
        <script>
          function showSurprise(){{ document.getElementById("surprise").style.display = "block"; }}
        </script>
      </head>
      <body>
        <h2>Danke für deinen Besuch.</h2>
        <p>Wow. Einfach draufgeklickt.<br><br><strong>Wie leichtgläubig kann man sein?</strong><br><br>Vielen lieben Dank für deine ganzen privaten Daten. 😊<br>Unter anderem deine Bankdaten, Login‑Daten und deine Lieblingskekssorte.<br><br>Keine Sorge – nur Spaß. Oder...?</p>
        <p class="small">(Kleiner Denkanstoß: Vielleicht nicht jeden Link einfach anklicken, Bruder.)</p>
        <div class="checkstdu">CHECKST DU?!</div>

        <button class="fake-btn" onclick="showSurprise()">Ich will meine Daten zurück</button>

        <div id="surprise" class="hidden">
          <p class="surprise-text">
            Oh mein Gott, wirklich? Dein Ernst?<br>
            Wie kann man nur so beschränkt sein?<br>
            Dass du ehrlich jetzt noch hier auf diesen <u>Button</u> klickst?<br><br>
            <strong>Wie man sieht, hast du nichts gecheckt.</strong><br>
            Überweis mir 50 Mark per PayPal an <u>info@BruderIchBinWirklichDoof.de</u>
          </p>
          <img src="https://i.imgur.com/9x6zM0F.png" alt="Facepalm">
        </div>

        <div class="info-box">
          <strong>Daten, die ich sehe:</strong><br>
          • Uhrzeit: {timestamp}<br>
          • Deine IP: {ip_address}<br>
          • Browser/OS: {ua}<br>
          • Sprache: {lang}<br>
          • Referrer (Herkunft): {ref}
        </div>
      </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
