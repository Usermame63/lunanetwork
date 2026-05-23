from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Instagram Takipçi</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{font-family:Arial,sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);margin:0;padding:20px;display:flex;justify-content:center;align-items:center;min-height:100vh;}}
            .container {{background:white;padding:40px;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.2);text-align:center;max-width:500px;width:100%;}}
            button, input {{width:100%;padding:16px;margin:10px 0;border-radius:8px;}}
            button {{background:linear-gradient(45deg,#E1306C,#F77737);color:white;border:none;font-size:18px;cursor:pointer;}}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ÜCRETSİZ İNSTAGRAM TAKİPÇİ</h1>
            <p><strong>IP:</strong> {ip}</p>
            
            <button onclick="getLocation()">📍 Yerləşməni Yoxla</button>
            
            <input type="text" id="username" placeholder="Instagram kullanıcı adınız">
            <button onclick="getFollowers()">250 TAKİPÇİ KAZAN</button>
            
            <div id="msg" style="margin-top:20px;padding:15px;border-radius:8px;display:none;background:#d4edda;"></div>
        </div>

        <script>
            function getLocation() {{
                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(
                        pos => alert("✅ Koordinat: " + pos.coords.latitude + ", " + pos.coords.longitude),
                        err => alert("❌ İcazə vermədiniz")
                    );
                }}
            }}
            
            function getFollowers() {{
                const user = document.getElementById('username').value.trim();
                if (!user) return alert("Kullanıcı adını yazın!");
                
                const btn = document.querySelector('button[onclick="getFollowers()"]');
                btn.disabled = true;
                btn.textContent = "GÖZLƏYİN...";
                
                setTimeout(() => {{
                    document.getElementById('msg').innerHTML = "✅ 250 takipçi əlavə edildi!";
                    document.getElementById('msg').style.display = "block";
                    btn.disabled = false;
                    btn.textContent = "250 TAKİPÇİ KAZAN";
                }}, 3500);
            }}
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
