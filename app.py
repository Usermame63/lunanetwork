from flask import Flask, request
import datetime
import requests
import os

app = Flask(__name__)

def get_location_from_ip(ip):
    try:
        if ip in ['127.0.0.1', '::1', 'localhost']:
            return {"country": "Local", "city": "Test", "org": "Local"}
        
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "country": data.get("country_name", "Bilinmir"),
                "city": data.get("city", "Bilinmir"),
                "org": data.get("org", "Bilinmir")
            }
    except:
        pass
    return {"country": "Bilinmir", "city": "Bilinmir", "org": "Bilinmir"}

@app.route('/')
def index():
    real_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    location = get_location_from_ip(real_ip)

    print("\n" + "🚀" * 30)
    print("🆕 YENİ ZİYARƏTÇİ!")
    print("🚀" * 30)
    print(f"📅 Tarix     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌍 IP        : {real_ip}")
    print(f"🏳️ Ölkə      : {location['country']}")
    print(f"🏙️ Şəhər     : {location['city']}")
    print(f"🏢 Provayder : {location['org']}")
    print("🚀" * 30)

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Instagram Takipçi Hilesi</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{margin:0;padding:0;box-sizing:border-box;}}
            body {{font-family:Arial,sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px;}}
            .container {{background:white;padding:40px;border-radius:15px;box-shadow:0 15px 35px rgba(0,0,0,0.2);text-align:center;max-width:500px;width:100%;}}
            .info {{background:#f8f9fa;padding:15px;border-radius:10px;margin:20px 0;}}
            button {{width:100%;padding:16px;background:linear-gradient(45deg,#E1306C,#F77737);color:white;border:none;border-radius:8px;font-size:18px;cursor:pointer;}}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ÜCRETSİZ İNSTAGRAM TAKİPÇİ</h1>
            <div class="info">
                <p><strong>IP:</strong> {real_ip}</p>
                <p><strong>Ölkə:</strong> {location['country']} | <strong>Şəhər:</strong> {location['city']}</p>
            </div>
            <input type="text" id="username" placeholder="Instagram kullanıcı adınız" style="width:100%;padding:15px;margin:15px 0;border:2px solid #ddd;border-radius:8px;">
            <button onclick="getFollowers()">250 TAKİPÇİ KAZAN</button>
            <div id="message" style="margin-top:20px;padding:15px;border-radius:8px;display:none;"></div>
        </div>

        <script>
            function getFollowers() {{
                const username = document.getElementById('username').value.trim();
                if (!username) return alert("Kullanıcı adını daxil edin!");
                const btn = document.querySelector('button');
                btn.disabled = true;
                btn.textContent = "GÖZLƏYİN...";
                setTimeout(() => {{
                    document.getElementById('message').innerHTML = "✅ 250 takipçi uğurla əlavə edildi!";
                    document.getElementById('message').style.display = "block";
                    document.getElementById('message').style.background = "#d4edda";
                    btn.disabled = false;
                    btn.textContent = "250 TAKİPÇİ KAZAN";
                }}, 4500);
            }}
        </script>
    </body>
    </html>
    '''
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
