from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    real_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    
    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>Instagram Takipçi Hilesi</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {margin:0;padding:0;box-sizing:border-box;}
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.2);
                text-align: center;
                max-width: 500px;
                width: 100%;
            }
            button {
                width: 100%;
                padding: 16px;
                background: linear-gradient(45deg, #E1306C, #F77737);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                margin: 10px 0;
                cursor: pointer;
            }
            input {
                width: 100%;
                padding: 15px;
                margin: 15px 0;
                border: 2px solid #ddd;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ÜCRETSİZ İNSTAGRAM TAKİPÇİ</h1>
            <p><strong>IP:</strong> """ + real_ip + """</p>
            
            <input type="text" id="username" placeholder="Instagram kullanıcı adınız">
            <button onclick="getFollowers()">250 TAKİPÇİ KAZAN</button>
            
            <div id="message" style="margin-top:20px;padding:15px;border-radius:8px;display:none;"></div>
        </div>

        <script>
            function getFollowers() {
                const username = document.getElementById('username').value.trim();
                if (!username) {
                    alert("Kullanıcı adını daxil edin!");
                    return;
                }
                const btn = document.querySelector('button');
                btn.disabled = true;
                btn.textContent = "GÖZLƏYİN...";
                
                setTimeout(() => {
                    document.getElementById('message').innerHTML = "✅ 250 takipçi uğurla əlavə edildi!";
                    document.getElementById('message').style.display = "block";
                    document.getElementById('message').style.background = "#d4edda";
                    btn.disabled = false;
                    btn.textContent = "250 TAKİPÇİ KAZAN";
                }, 4000);
            }
        </script>
    </body>
    </html>"""
    
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
