from flask import Flask, request
import datetime
import requests

app = Flask(__name__)

def get_location_from_ip(ip):
    try:
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

    # Gözəl Log
    print("\n" + "🚀" * 40)
    print("🆕 YENİ ZİYARƏTÇİ!")
    print("🚀" * 40)
    print(f"📅 Tarix     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌍 IP        : {real_ip}")
    print(f"🏳️ Ölkə      : {location['country']}")
    print(f"🏙️ Şəhər     : {location['city']}")
    print(f"🏢 Provayder : {location['org']}")
    print("🚀" * 40)

    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LunaNW | Minecraft Sunucusu</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #030712;
            overflow-x: hidden;
            color: #f3f4f6;
        }

        .glass-card {
            background: rgba(17, 24, 39, 0.85);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            position: relative;
        }

        /* KAR EFEKTİ */
        .snow-pile::before {
            content: '';
            position: absolute;
            top: -6px;
            left: 0;
            right: 0;
            height: 14px;
            background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(230,240,255,0.8) 60%, rgba(255,255,255,0) 100%);
            border-radius: 20px 20px 10px 10px;
            z-index: 10;
            box-shadow: 0 2px 10px rgba(255, 255, 255, 0.3);
            pointer-events: none;
        }
        
        .frost-overlay {
            position: fixed;
            inset: 0;
            pointer-events: none;
            background: radial-gradient(circle, transparent 50%, rgba(180, 220, 255, 0.1) 100%);
            box-shadow: inset 0 0 120px rgba(180, 220, 255, 0.15);
            z-index: 9990;
        }

        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: #111827; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #374151; border-radius: 10px; }

        .animate-in { animation: fadeIn 0.4s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        .snowflake {
            position: fixed;
            top: -50px;
            z-index: 9999;
            user-select: none;
            pointer-events: none;
            opacity: 0.9;
            animation-name: fall;
            animation-timing-function: linear;
            animation-iteration-count: infinite;
        }

        @keyframes fall {
            0% { transform: translateY(-50px) translateX(0px) rotate(0deg); }
            100% { transform: translateY(105vh) translateX(20px) rotate(360deg); }
        }

        /* Toggle Switch */
        .toggle-checkbox:checked {
            right: 0;
            border-color: #10b981;
        }
        .toggle-checkbox:checked + .toggle-label {
            background-color: #10b981;
        }

        /* Chat Animations */
        .chat-enter { animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
        @keyframes slideUp { from { opacity: 0; transform: translateY(20px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }
    </style>
</head>
<body class="selection:bg-emerald-500 selection:text-white relative">

    <div class="frost-overlay"></div>

    <!-- Announcement -->
    <div class="bg-gradient-to-r from-blue-900 via-emerald-900 to-blue-900 text-center py-2 relative z-[60] border-b border-white/10">
        <p class="text-xs md:text-sm font-bold text-blue-100 flex items-center justify-center gap-2 animate-pulse">
            <i data-lucide="snowflake" class="w-4 h-4"></i>
            KIŞ SEZONU İNDİRİMLERİ BAŞLADI! TÜM ÜRÜNLERDE %50 İNDİRİM
            <i data-lucide="snowflake" class="w-4 h-4"></i>
        </p>
    </div>

    <!-- Navbar -->
    <nav class="sticky top-0 z-50 border-b border-white/5 bg-gray-950/90 backdrop-blur-xl snow-pile" style="border-radius: 0 0 0 0;">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3 cursor-pointer" onclick="navigate('home')">
                <div class="w-10 h-10 bg-emerald-600 rounded-xl flex items-center justify-center shadow-lg shadow-emerald-900/20">
                    <i data-lucide="layout-grid" class="text-white w-6 h-6"></i>
                </div>
                <span class="text-xl font-extrabold tracking-tighter uppercase">LUNA<span class="text-emerald-500">NW</span></span>
            </div>

            <div class="hidden md:flex items-center gap-6">
                <button onclick="navigate('home')" class="text-sm font-semibold hover:text-emerald-400 transition-colors">Ana Sayfa</button>
                <button onclick="navigate('store')" class="text-sm font-semibold hover:text-emerald-400 transition-colors">Mağaza</button>
                <button onclick="navigate('credits')" class="text-sm font-bold text-amber-400 hover:text-amber-300 transition-colors flex items-center gap-1 bg-amber-500/10 px-3 py-1.5 rounded-lg border border-amber-500/20">
                    <i data-lucide="coins" class="w-4 h-4"></i> Kredi Yükle
                </button>
                <a href="https://discord.gg/kkQqZXJe9k" target="_blank" class="text-sm font-semibold hover:text-blue-400 transition-colors">Discord</a>
            </div>

            <div class="flex items-center gap-4" id="auth-section"></div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-12 min-h-screen relative z-10">
        
        <!-- HOME VIEW -->
        <section id="view-home" class="animate-in text-center space-y-12 py-20 relative">
            
            <div id="server-status-badge" class="hidden inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full px-4 py-1.5 text-emerald-400 text-sm font-bold animate-fade-in mb-4 relative z-10">
                <span id="status-indicator-container" class="relative flex h-3 w-3">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                </span>
                <span id="player-count-text">Yükleniyor...</span>
            </div>

            <div class="space-y-6 relative z-10">
                <h1 class="text-6xl md:text-8xl font-extrabold tracking-tight leading-none">
                    KIŞ <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-200 to-white">MASALI</span> <br> 
                    <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-500">BAŞLIYOR</span>
                </h1>
                <p class="text-gray-400 text-lg md:text-xl max-w-2xl mx-auto font-medium">
                    Türkiye'nin en gelişmiş Minecraft sunucusunda kış sezonu başladı! Karlı dağlarda krallığını kurmaya hazır mısın?
                </p>
            </div>

            <div class="flex flex-col sm:flex-row justify-center items-center gap-6 relative z-10">
                <button onclick="copyIP()" class="flex items-center gap-3 bg-gray-900 border border-white/10 px-8 py-4 rounded-2xl hover:bg-gray-800 transition-all group active:scale-95 snow-pile">
                    <i data-lucide="copy" class="w-5 h-5 text-emerald-500 group-hover:scale-110 transition-transform"></i>
                    <span id="ip-text" class="font-bold tracking-wide">lunanw.xyz</span>
                </button>
                <button onclick="navigate('store')" class="bg-emerald-600 hover:bg-emerald-500 text-white px-10 py-4 rounded-2xl font-bold text-lg shadow-xl shadow-emerald-900/20 transition-all active:scale-95 snow-pile">
                    Mağazayı Keşfet
                </button>
            </div>

            <!-- Hero Image -->
            <div class="relative z-10 mt-12 flex flex-col items-center gap-8">
                <div class="relative group max-w-3xl w-full">
                    <div class="absolute -inset-1 bg-gradient-to-r from-emerald-600 to-blue-600 rounded-3xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
                    <img src="https://i.ytimg.com/vi/iz01IvBjaPc/maxresdefault.jpg" alt="Kış Sezonu" class="relative rounded-3xl border border-white/10 shadow-2xl w-full transform transition duration-500 hover:scale-[1.02]">
                </div>
            </div>

            <!-- Features -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 pt-20 relative z-10">
                <div class="glass-card p-8 rounded-3xl text-left hover:border-emerald-500/30 transition-colors group snow-pile">
                    <div class="w-14 h-14 bg-emerald-500/10 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <i data-lucide="shield-check" class="text-emerald-500 w-8 h-8"></i>
                    </div>
                    <h3 class="text-2xl font-bold mb-3">Güvenli Oyun</h3>
                    <p class="text-gray-400 font-medium">En son hile koruma sistemleri ile adil ve huzurlu bir ortam.</p>
                </div>
                <div class="glass-card p-8 rounded-3xl text-left hover:border-blue-500/30 transition-colors group snow-pile">
                    <div class="w-14 h-14 bg-blue-500/10 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <i data-lucide="zap" class="text-blue-500 w-8 h-8"></i>
                    </div>
                    <h3 class="text-2xl font-bold mb-3">Yüksek Performans</h3>
                    <p class="text-gray-400 font-medium">Sıfır lag garantisi ve kesintisiz 20 TPS sunucu hızı.</p>
                </div>
                <div class="glass-card p-8 rounded-3xl text-left hover:border-purple-500/30 transition-colors group snow-pile">
                    <div class="w-14 h-14 bg-purple-500/10 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                        <i data-lucide="users" class="text-purple-500 w-8 h-8"></i>
                    </div>
                    <h3 class="text-2xl font-bold mb-3">Dev Topluluk</h3>
                    <p class="text-gray-400 font-medium">Binlerce oyuncu ile ticaret yap ve kendi ekibini kur.</p>
                </div>
            </div>
        </section>
        
        <!-- STORE VIEW -->
        <section id="view-store" class="hidden animate-in space-y-16">
            <header class="text-center space-y-4">
                <h2 class="text-4xl font-extrabold tracking-tight">SUNUCU MAĞAZASI</h2>
                <p class="text-gray-400 max-w-xl mx-auto">Aldığınız tüm ürünler sunucumuzun gelişimine destek sağlamaktadır.</p>
            </header>

            <div class="space-y-8">
                <div class="flex items-center gap-4">
                    <div class="p-2 bg-emerald-500/10 rounded-lg"><i data-lucide="package" class="text-emerald-500 w-6 h-6"></i></div>
                    <h3 class="text-2xl font-bold">Özel Kasalar</h3>
                    <div class="flex-grow h-px bg-white/5"></div>
                </div>
                <div id="kasa-list" class="grid grid-cols-1 md:grid-cols-3 gap-6"></div>
            </div>

            <div class="space-y-8">
                <div class="flex items-center gap-4">
                    <div class="p-2 bg-amber-500/10 rounded-lg"><i data-lucide="crown" class="text-amber-500 w-6 h-6"></i></div>
                    <h3 class="text-2xl font-bold">VIP Üyelikler</h3>
                    <div class="flex-grow h-px bg-white/5"></div>
                </div>
                <div id="vip-list" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"></div>
            </div>
        </section>

        <!-- CREDIT VIEW (NEW) -->
        <section id="view-credits" class="hidden animate-in space-y-16 py-10">
            <header class="text-center space-y-4">
                <h2 class="text-4xl font-extrabold tracking-tight flex items-center justify-center gap-3">
                    <span class="text-amber-400">KREDİ</span> YÜKLE
                </h2>
                <p class="text-gray-400 max-w-xl mx-auto">Bakiyenize kredi yükleyerek mağazadan alışveriş yapabilirsiniz.</p>
            </header>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 max-w-7xl mx-auto" id="credit-list">
                <!-- JS Rendered -->
            </div>
        </section>
    </main>

    <!-- LIVE SUPPORT WIDGET (USER SIDE) -->
    <div class="fixed bottom-6 right-6 z-[9000] flex flex-col items-end gap-4">
        <!-- Chat Window -->
        <div id="live-support-window" class="hidden chat-enter glass-card snow-pile w-80 sm:w-96 rounded-3xl overflow-hidden shadow-2xl border-emerald-500/20 mb-2" style="background: rgba(17, 24, 39, 0.95);">
            <div class="bg-gradient-to-r from-emerald-800 to-emerald-600 p-4 flex items-center justify-between">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center">
                        <i data-lucide="headset" class="text-white w-6 h-6"></i>
                    </div>
                    <div>
                        <h4 class="font-bold text-white text-sm">Canlı Destek</h4>
                        <p class="text-[10px] text-emerald-100 opacity-80" id="support-status">Yönetim Çevrimiçi</p>
                    </div>
                </div>
                <button onclick="toggleLiveSupport()" class="text-white/70 hover:text-white"><i data-lucide="x" class="w-5 h-5"></i></button>
            </div>
            
            <!-- Messages -->
            <div class="p-4 h-64 bg-gray-900/60 overflow-y-auto custom-scrollbar flex flex-col gap-3" id="chat-messages">
                <div class="flex items-start gap-2">
                    <div class="w-8 h-8 bg-emerald-600 rounded-full flex items-center justify-center shrink-0"><i data-lucide="bot" class="w-4 h-4 text-white"></i></div>
                    <div class="bg-gray-800 p-3 rounded-2xl rounded-tl-none text-xs text-gray-200 border border-white/5">Merhaba! Size nasıl yardımcı olabilirim?</div>
                </div>
            </div>
            
            <!-- Input -->
            <div class="p-3 bg-gray-900 border-t border-white/5">
                <form onsubmit="handleChatSubmit(event)" class="relative">
                    <input type="text" id="chat-input" placeholder="Mesajınız..." class="w-full bg-gray-800 text-white text-xs rounded-xl pl-4 pr-10 py-3 border border-white/5 focus:outline-none focus:border-emerald-500">
                    <button type="submit" class="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 bg-emerald-600 rounded-lg hover:bg-emerald-500"><i data-lucide="send" class="w-3 h-3 text-white"></i></button>
                </form>
            </div>
        </div>

        <!-- Toggle Button -->
        <button onclick="toggleLiveSupport()" class="group relative flex items-center justify-center w-14 h-14 bg-emerald-600 hover:bg-emerald-500 rounded-full shadow-lg shadow-emerald-600/30 transition-all hover:scale-110 active:scale-95">
            <span class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-gray-900 z-10 animate-pulse"></span>
            <i data-lucide="message-circle" class="w-7 h-7 text-white fill-current"></i>
        </button>
    </div>

    <!-- AUTH MODAL -->
    <div id="auth-modal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm hidden">
        <div class="glass-card snow-pile w-full max-w-sm rounded-3xl p-8 space-y-6 relative border-white/10 shadow-2xl">
            <button onclick="closeAuthModal()" class="absolute top-6 right-6 text-gray-400 hover:text-white"><i data-lucide="x" class="w-6 h-6"></i></button>
            <div class="text-center space-y-2">
                <h2 id="auth-modal-title" class="text-2xl font-bold">Giriş Yap</h2>
                <p class="text-sm text-gray-400">Sunucu hesabına bağlan</p>
            </div>
            <div id="auth-error" class="hidden bg-red-500/10 border border-red-500/50 text-red-500 p-3 rounded-xl text-xs font-medium text-center"></div>
            <div class="space-y-4">
                <div class="space-y-1">
                    <label class="text-xs font-bold text-gray-500 uppercase ml-1">Kullanıcı Adı</label>
                    <input type="text" id="auth-user" class="w-full bg-gray-900 border border-white/5 rounded-2xl px-4 py-3 focus:outline-none focus:border-emerald-500 transition-colors" placeholder="Oyundaki adın">
                </div>
                <div class="space-y-1">
                    <label class="text-xs font-bold text-gray-500 uppercase ml-1">Şifre</label>
                    <input type="password" id="auth-pass" class="w-full bg-gray-900 border border-white/5 rounded-2xl px-4 py-3 focus:outline-none focus:border-emerald-500 transition-colors" placeholder="••••••••">
                </div>
                <button id="auth-submit" class="w-full bg-emerald-600 hover:bg-emerald-500 py-4 rounded-2xl font-bold transition-all shadow-lg shadow-emerald-900/20">Devam Et</button>
            </div>
            <div class="text-center text-sm">
                <span id="auth-switch-text" class="text-gray-500">Hesabın yok mu?</span>
                <button onclick="switchAuthMode()" id="auth-switch-btn" class="text-emerald-500 font-bold hover:underline ml-1">Kayıt Ol</button>
            </div>
        </div>
    </div>

    <!-- SETTINGS MODAL -->
    <div id="settings-modal" class="fixed inset-0 z-[120] flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm hidden">
        <div class="glass-card snow-pile w-full max-w-lg rounded-3xl overflow-hidden border-white/10 shadow-2xl flex flex-col max-h-[90vh]">
            <div class="p-6 border-b border-white/5 flex items-center justify-between bg-white/5 shrink-0">
                <h3 class="text-xl font-bold flex items-center gap-2">
                    <i data-lucide="settings" class="w-5 h-5 text-gray-400"></i>
                    <span id="settings-title">Ayarlar & Tercihler</span>
                </h3>
                <button onclick="closeSettingsModal()" class="text-gray-400 hover:text-white transition-colors">
                    <i data-lucide="x" class="w-6 h-6"></i>
                </button>
            </div>
            
            <div class="p-6 space-y-6 overflow-y-auto custom-scrollbar">
                <!-- HESAP -->
                <div class="space-y-3">
                    <h4 class="text-xs font-bold text-emerald-500 uppercase tracking-widest ml-1 flex items-center gap-1">
                        <i data-lucide="user" class="w-3 h-3"></i> Hesap & Güvenlik
                    </h4>
                    <div class="bg-white/5 rounded-xl p-4 border border-white/5 space-y-4">
                        <div class="flex flex-col gap-3">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-3">
                                    <div class="p-2 bg-red-500/20 rounded-lg text-red-500"><i data-lucide="lock" class="w-5 h-5"></i></div>
                                    <div>
                                        <p class="text-sm font-bold text-white">Şifre Değiştir</p>
                                        <p class="text-xs text-gray-400">Hesabınızı güvende tutun</p>
                                    </div>
                                </div>
                                <button onclick="togglePasswordChange()" class="text-xs font-bold bg-white/10 hover:bg-white/20 px-3 py-1.5 rounded-lg transition-colors">Aç/Kapat</button>
                            </div>
                            <div id="password-change-form" class="hidden pl-2 border-l-2 border-red-500/30 ml-4 space-y-3 pt-2">
                                <input type="password" id="old-pass" placeholder="Eski Şifre" class="w-full bg-black/40 border border-white/10 rounded px-3 py-2 text-xs text-white">
                                <input type="password" id="new-pass" placeholder="Yeni Şifre" class="w-full bg-black/40 border border-white/10 rounded px-3 py-2 text-xs text-white">
                                <button onclick="changePassword()" class="w-full bg-red-600 hover:bg-red-500 text-white text-xs font-bold py-2 rounded">Şifreyi Güncelle</button>
                            </div>
                        </div>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <div class="p-2 bg-emerald-500/20 rounded-lg text-emerald-500"><i data-lucide="shield" class="w-5 h-5"></i></div>
                                <div>
                                    <p class="text-sm font-bold text-white">İki Faktörlü Doğrulama</p>
                                    <p class="text-xs text-gray-400">Girişlerde kod iste (Simülasyon)</p>
                                </div>
                            </div>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" name="toggle" id="toggle-2fa" class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300"/>
                                <label for="toggle-2fa" class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <div class="p-2 bg-blue-500/20 rounded-lg text-blue-500"><i data-lucide="mail" class="w-5 h-5"></i></div>
                                <div>
                                    <p class="text-sm font-bold text-white">E-posta Bildirimleri</p>
                                    <p class="text-xs text-gray-400">Kampanyalardan haberdar ol</p>
                                </div>
                            </div>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" name="toggle" id="toggle-email" class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300"/>
                                <label for="toggle-email" class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- GÖRÜNÜM -->
                <div class="space-y-3">
                    <h4 class="text-xs font-bold text-amber-500 uppercase tracking-widest ml-1 flex items-center gap-1">
                        <i data-lucide="monitor" class="w-3 h-3"></i> Görünüm
                    </h4>
                    <div class="bg-white/5 rounded-xl p-4 border border-white/5 space-y-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <div class="p-2 bg-amber-500/20 rounded-lg text-amber-500"><i data-lucide="eye-off" class="w-5 h-5"></i></div>
                                <div>
                                    <p class="text-sm font-bold text-white">Bakiyeyi Gizle</p>
                                    <p class="text-xs text-gray-400">Yayın yaparken faydalı</p>
                                </div>
                            </div>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" name="toggle" id="toggle-balance" class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300" onchange="toggleBalanceVisibility(this.checked)"/>
                                <label for="toggle-balance" class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <div class="p-2 bg-cyan-500/20 rounded-lg text-cyan-500"><i data-lucide="snowflake" class="w-5 h-5"></i></div>
                                <div>
                                    <p class="text-sm font-bold text-white">Kar Efektini Kapat</p>
                                    <p class="text-xs text-gray-400">Performansı artırır</p>
                                </div>
                            </div>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" name="toggle" id="toggle-snow" class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300" onchange="toggleSnow(this.checked)"/>
                                <label for="toggle-snow" class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                         <div class="flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <div class="p-2 bg-purple-500/20 rounded-lg text-purple-500"><i data-lucide="zap-off" class="w-5 h-5"></i></div>
                                <div>
                                    <p class="text-sm font-bold text-white">Animasyonları Azalt</p>
                                    <p class="text-xs text-gray-400">Daha sade bir görünüm</p>
                                </div>
                            </div>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" name="toggle" id="toggle-anim" class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300"/>
                                <label for="toggle-anim" class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- BİLDİRİMLER -->
                <div class="space-y-3">
                    <h4 class="text-xs font-bold text-blue-500 uppercase tracking-widest ml-1 flex items-center gap-1">
                        <i data-lucide="bell" class="w-3 h-3"></i> Bildirimler
                    </h4>
                    <div class="bg-white/5 rounded-xl p-4 border border-white/5 space-y-4">
                        <div class="flex items-center justify-between">
                            <span class="text-sm text-gray-300">Discord Mesajları</span>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" checked class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300"/>
                                <label class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                        <div class="flex items-center justify-between">
                            <span class="text-sm text-gray-300">Site İçi Uyarılar</span>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" checked class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300"/>
                                <label class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- OYUN İÇİ -->
                <div class="space-y-3">
                    <h4 class="text-xs font-bold text-orange-500 uppercase tracking-widest ml-1 flex items-center gap-1">
                        <i data-lucide="gamepad-2" class="w-3 h-3"></i> Oyun İçi (Simülasyon)
                    </h4>
                    <div class="bg-white/5 rounded-xl p-4 border border-white/5 space-y-4">
                        <div class="flex items-center justify-between">
                            <span class="text-sm text-gray-300">Özel Mesajları Kapat</span>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300"/>
                                <label class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                        <div class="flex items-center justify-between">
                            <span class="text-sm text-gray-300">Klan Davetlerini Reddet</span>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300"/>
                                <label class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                         <div class="flex items-center justify-between">
                            <span class="text-sm text-gray-300">Takas İsteklerini Reddet</span>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300"/>
                                <label class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- GİZLİLİK -->
                 <div class="space-y-3">
                    <h4 class="text-xs font-bold text-purple-500 uppercase tracking-widest ml-1 flex items-center gap-1">
                        <i data-lucide="eye" class="w-3 h-3"></i> Gizlilik
                    </h4>
                    <div class="bg-white/5 rounded-xl p-4 border border-white/5 space-y-4">
                        <div class="flex items-center justify-between">
                            <span class="text-sm text-gray-300">Profilimi Gizle</span>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300"/>
                                <label class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                         <div class="flex items-center justify-between">
                            <span class="text-sm text-gray-300">Envanterimi Gizle</span>
                            <div class="relative inline-block w-10 mr-2 align-middle select-none transition duration-200 ease-in">
                                <input type="checkbox" class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-600 transition-all duration-300"/>
                                <label class="toggle-label block overflow-hidden h-5 rounded-full bg-gray-700 cursor-pointer"></label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- CREDIT PAYMENT MODAL -->
    <div id="credit-payment-modal" class="fixed inset-0 z-[150] flex items-center justify-center p-4 bg-black/95 backdrop-blur-md hidden">
        <div class="glass-card w-full max-w-md rounded-3xl border-amber-500/30 shadow-2xl relative overflow-hidden">
            <div class="bg-gradient-to-r from-amber-600 to-yellow-700 p-6 text-center relative">
                <button onclick="closeCreditPaymentModal()" class="absolute top-4 right-4 text-white/70 hover:text-white">
                    <i data-lucide="x" class="w-6 h-6"></i>
                </button>
                <h3 class="text-2xl font-bold text-white mb-1">Havale / EFT ile Ödeme</h3>
                <p class="text-amber-100 text-sm font-medium" id="cp-modal-info">Yükleniyor...</p>
            </div>
            <div class="p-6 space-y-6">
                <!-- IBAN Display -->
                <div class="bg-black/60 p-5 rounded-2xl border border-amber-500/20 text-center space-y-3">
                    <div class="flex flex-col items-center">
                        <i data-lucide="landmark" class="w-8 h-8 text-amber-500 mb-2"></i>
                        <p class="text-xs text-gray-400 uppercase font-bold tracking-widest">Aşağıdaki IBAN'a Gönderin</p>
                    </div>
                    <div class="relative group cursor-pointer" onclick="copyIBAN()">
                        <div class="font-mono text-xl font-bold text-white break-all bg-gray-800 p-3 rounded-lg border border-gray-700 group-hover:border-amber-500 transition-colors">
                            TR14 0006 7010 0000 0080 4293 36
                        </div>
                        <div class="text-[10px] text-emerald-400 mt-1 hidden" id="iban-copied-msg">Kopyalandı!</div>
                    </div>
                    <p class="text-xs text-gray-400">
                        Alıcı Adı: <span class="text-white font-bold">LunaNW Yönetim</span>
                    </p>
                </div>
                <!-- User Notification Form -->
                <div class="space-y-4">
                    <div class="bg-blue-500/10 border border-blue-500/20 p-3 rounded-xl flex items-start gap-3">
                        <i data-lucide="info" class="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5"></i>
                        <p class="text-xs text-blue-200">Parayı gönderdikten sonra aşağıdaki kutuya <strong>Ödemeyi Yapan Kişinin Adını Soyadını</strong> yazıp butona basınız.</p>
                    </div>
                    <div>
                        <label class="text-xs font-bold text-gray-400 uppercase block mb-1">Gönderen Adı Soyadı</label>
                        <input type="text" id="payment-sender-name" class="w-full bg-gray-900 border border-white/10 rounded-xl px-4 py-3 text-white focus:border-amber-500 focus:outline-none placeholder-gray-600" placeholder="Örn: Ahmet Yılmaz">
                    </div>
                </div>
                <button onclick="sendPaymentNotification()" class="w-full bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white font-bold py-4 rounded-xl shadow-lg shadow-emerald-900/20 transition-all transform active:scale-95 flex items-center justify-center gap-2">
                    <i data-lucide="send" class="w-5 h-5"></i>
                    Parayı Gönderdim & Bildir
                </button>
            </div>
        </div>
    </div>

    <!-- CART MODAL -->
    <div id="cart-modal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm hidden">
        <div class="glass-card snow-pile w-full max-w-md rounded-3xl overflow-hidden border-white/10 shadow-2xl">
            <div class="p-6 border-b border-white/5 flex items-center justify-between bg-white/5">
                <h3 class="text-xl font-bold flex items-center gap-2">
                    <i data-lucide="shopping-cart" class="w-5 h-5 text-emerald-500"></i>
                    <span id="cart-title">Sepetim</span>
                </h3>
                <button onclick="closeCartModal()" class="text-gray-400 hover:text-white transition-colors">
                    <i data-lucide="x" class="w-6 h-6"></i>
                </button>
            </div>
            <div class="p-6" id="cart-body"></div>
        </div>
    </div>

    <script>
        // --- CONFIG & STATE ---
        let currentUser = JSON.parse(localStorage.getItem('user_session')) || null;
        let authMode = 'login';
        let snowInterval = null;
        
        // --- CONSTANTS ---
        const API_URL = "http://localhost:5000";
        const WEBHOOK_URL = "https://discord.com/api/webhooks/1452683666508615721/UICjtHYgVrtwFIgt7YRCItTLjceV2a6L8ikLMXX1dLmMuPm8D9s8k63UMtMoxuIa7baS";
        const SERVER_IP = "lunanw.xyz";
        const SNOWFLAKE_IMAGE_URL = "https://cdn.discordapp.com/attachments/1436626972737540237/1459576057291079700/iZhcwBr.png?ex=6963c7a1&is=69627621&hm=b175e98239c3496810e1d0f8551a5d7ecd78ead7bab93ceb79ec4c0252dfe572&";

        const PRODUCTS = {
            kasalar: [
                { id: 'k1', name: 'Kit Kasa', price: 25, desc: 'Başlangıç ekipmanları.' },
                { id: 'k2', name: 'Event Kasa', price: 10, desc: 'Etkinliklere özel.' },
                { id: 'k3', name: 'Para Kasa', price: 20, desc: 'Rastgele para ödülleri.' }
            ],
            vips: [
                { id: 'v1', name: 'VIP', price: 35, desc: 'Giriş önceliği.' },
                { id: 'v2', name: 'VIP+', price: 50, desc: 'Ekstra kitler.' },
                { id: 'v3', name: 'MVIP', price: 65, desc: 'Özel yetenekler.' },
                { id: 'v4', name: 'MVIP+', price: 75, desc: 'Uçuş yetkisi.' },
                { id: 'v5', name: 'LVIP', price: 85, desc: 'Efsanevi rütbe.' },
                { id: 'v6', name: 'LVIP+', price: 100, desc: 'En güçlü rütbe.' }
            ]
        };

        const CREDIT_PACKAGES = [
            { credits: 15, price: 20 },
            { credits: 30, price: 40 },
            { credits: 100, price: 115 },
            { credits: 300, price: 325 },
            { credits: 500, price: 450 }
        ];

        let cart = [];
        let currentStep = 'items';
        let selectedCreditPackage = null;

        // User settings check and initialization
        if(currentUser && !currentUser.settings) {
            currentUser.settings = { balanceHidden: false, disableSnow: false };
        }

        // --- INIT ---
        function init() {
            lucide.createIcons();
            
            if (currentUser) {
                // Initialize settings checkboxes
                const balanceToggle = document.getElementById('toggle-balance');
                if(balanceToggle && currentUser.settings) {
                    balanceToggle.checked = currentUser.settings.balanceHidden;
                }

                const snowToggle = document.getElementById('toggle-snow');
                if(snowToggle && currentUser.settings) {
                    snowToggle.checked = currentUser.settings.disableSnow;
                }
            }

            renderAuthStatus();
            renderStore();
            renderCredits();
            
            // Snow logic based on settings
            if (!currentUser || (currentUser && !currentUser.settings.disableSnow)) {
                createSnow();
            }

            // --- OTOMATİK SENKRONİZASYON (Admin Panelinden Gelen Verileri Çeker) ---
            setInterval(() => {
                if(!currentUser) return;
                
                // 1. Kredi Kontrolü
                const db = JSON.parse(localStorage.getItem('db_users')) || {};
                if(db[currentUser.username] && db[currentUser.username].credits !== currentUser.credits) {
                    currentUser.credits = db[currentUser.username].credits;
                    // Ayrıca ayarları da güncelle
                    if (db[currentUser.username].settings) {
                        currentUser.settings = db[currentUser.username].settings;
                    }
                    localStorage.setItem('user_session', JSON.stringify(currentUser));
                    renderAuthStatus();
                }

                // 2. Mesaj Kontrolü (Canlı Destek Açıksa)
                if(!document.getElementById('live-support-window').classList.contains('hidden')) {
                    syncChat();
                }
            }, 1000); // Her 1 saniyede kontrol eder

            checkServerStatus();
            setInterval(checkServerStatus, 60000);
        }

        // --- NAVIGATION ---
        function navigate(view) {
            ['home', 'store', 'credits'].forEach(v => {
                document.getElementById(`view-${v}`).classList.toggle('hidden', v !== view);
            });
            window.scrollTo(0,0);
        }

        // --- AUTH ---
        function openAuthModal(mode) {
            authMode = mode;
            document.getElementById('auth-modal').classList.remove('hidden');
            const title = document.getElementById('auth-modal-title');
            const btn = document.getElementById('auth-submit');
            const switchBtn = document.getElementById('auth-switch-btn');
            const switchText = document.getElementById('auth-switch-text');
            
            if(mode === 'login') {
                title.innerText = "Giriş Yap"; btn.innerText = "Giriş Yap"; switchText.innerText = "Hesabın yok mu?"; switchBtn.innerText = "Kayıt Ol";
            } else {
                title.innerText = "Kayıt Ol"; btn.innerText = "Kayıt Ol"; switchText.innerText = "Zaten hesabın var mı?"; switchBtn.innerText = "Giriş Yap";
            }
        }
        
        function closeAuthModal() { document.getElementById('auth-modal').classList.add('hidden'); }
        function switchAuthMode() { 
            authMode = authMode === 'login' ? 'register' : 'login';
            // UI Update for mode switch
            const title = document.getElementById('auth-modal-title');
            const btn = document.getElementById('auth-submit');
            const switchText = document.getElementById('auth-switch-text');
            const switchBtn = document.getElementById('auth-switch-btn');
            if (authMode === 'login') {
                title.innerText = "Giriş Yap"; btn.innerText = "Giriş Yap"; switchText.innerText = "Hesabın yok mu?"; switchBtn.innerText = "Kayıt Ol";
            } else {
                title.innerText = "Yeni Kayıt"; btn.innerText = "Kayıt Ol"; switchText.innerText = "Zaten hesabın var mı?"; switchBtn.innerText = "Giriş Yap";
            }
        }

        document.getElementById('auth-submit').addEventListener('click', () => {
            const user = document.getElementById('auth-user').value.trim();
            const pass = document.getElementById('auth-pass').value.trim();
            const error = document.getElementById('auth-error');
            
            if(!user || !pass) { error.innerText = "Lütfen tüm alanları doldurun."; error.classList.remove('hidden'); return; }
            
            let db = JSON.parse(localStorage.getItem('db_users')) || {};
            
            if(authMode === 'register') {
                if(db[user]) { error.innerText = "Bu kullanıcı adı zaten mevcut."; error.classList.remove('hidden'); return; }
                db[user] = { username: user, password: pass, credits: 0, settings: { balanceHidden: false, disableSnow: false }, joinDate: new Date().toLocaleDateString() };
                localStorage.setItem('db_users', JSON.stringify(db));
                login(db[user]);
            } else {
                if(db[user] && db[user].password === pass) login(db[user]);
                else { error.innerText = "Kullanıcı adı veya şifre hatalı!"; error.classList.remove('hidden'); }
            }
        });

        function login(user) {
            if (user.credits === undefined) user.credits = 0;
            if (user.settings === undefined) user.settings = { balanceHidden: false, disableSnow: false };
            currentUser = user;
            localStorage.setItem('user_session', JSON.stringify(user));
            closeAuthModal();
            renderAuthStatus();
            
            // Re-apply snow setting
            if (user.settings.disableSnow) {
                toggleSnow(true);
            } else {
                createSnow();
            }
        }

        function logout() {
            currentUser = null;
            cart = [];
            localStorage.removeItem('user_session');
            renderAuthStatus();
            navigate('home');
        }

        function renderAuthStatus() {
            const el = document.getElementById('auth-section');
            if(currentUser) {
                // Bakiye gizlilik kontrolü
                const isHidden = currentUser.settings && currentUser.settings.balanceHidden;
                const creditDisplayClass = isHidden ? "blur-sm select-none" : "";

                let adminBtn = '';
                if(currentUser.username === 'admin') {
                    adminBtn = `<a href="panel.html" target="_blank" class="p-2 text-purple-400 hover:text-purple-300 transition-colors" title="Yönetim Paneli"><i data-lucide="shield-alert" class="w-6 h-6"></i></a>`;
                }

                el.innerHTML = `
                    <div class="hidden sm:flex items-center bg-amber-500/10 border border-amber-500/20 px-3 py-1.5 rounded-xl mr-2">
                        <i data-lucide="coins" class="w-4 h-4 text-amber-400 mr-2"></i>
                        <span class="text-amber-400 font-bold text-sm ${creditDisplayClass}" id="user-credits-display">${currentUser.credits} Kredi</span>
                    </div>
                    
                    <button onclick="openCart()" class="relative p-2 hover:bg-white/5 rounded-xl transition-colors">
                        <i data-lucide="shopping-bag" class="w-6 h-6"></i>
                        ${cart.length > 0 ? `<span class="absolute -top-1 -right-1 bg-emerald-500 text-[10px] font-bold w-5 h-5 rounded-full flex items-center justify-center border-2 border-gray-950">${cart.length}</span>` : ''}
                    </button>
                    
                    ${adminBtn}
                    
                    <button onclick="openSettingsModal()" class="p-2 hover:bg-white/5 rounded-xl transition-colors">
                        <i data-lucide="settings" class="w-6 h-6 text-gray-400 hover:text-white"></i>
                    </button>

                    <div class="flex items-center gap-4 border-l border-white/10 pl-4">
                        <div class="text-right hidden sm:block">
                            <p class="text-xs font-bold text-gray-500 uppercase">Hoşgeldin</p>
                            <p class="text-sm font-bold text-emerald-400">${currentUser.username}</p>
                        </div>
                        <button onclick="logout()" class="p-2 hover:bg-red-500/10 text-gray-500 hover:text-red-500 rounded-xl transition-colors">
                            <i data-lucide="log-out" class="w-6 h-6"></i>
                        </button>
                    </div>
                `;
            } else {
                el.innerHTML = `
                    <button onclick="openAuthModal('login')" class="bg-white/5 hover:bg-white/10 px-6 py-2.5 rounded-xl text-sm font-bold transition-all">Giriş</button>
                    <button onclick="openAuthModal('register')" class="bg-emerald-600 hover:bg-emerald-500 px-6 py-2.5 rounded-xl text-sm font-bold transition-all shadow-lg shadow-emerald-900/20">Kayıt</button>
                `;
            }
            lucide.createIcons();
        }

        // --- LIVE SUPPORT & CHAT SYNC ---
        function toggleLiveSupport() {
            const w = document.getElementById('live-support-window');
            w.classList.toggle('hidden');
            if(!w.classList.contains('hidden')) {
                lucide.createIcons();
                syncChat(); // Açılır açılmaz mesajları yükle
            }
        }

        function handleChatSubmit(e) {
            e.preventDefault();
            const input = document.getElementById('chat-input');
            const msg = input.value.trim();
            if(!msg) return;

            // Mesajı Kaydet
            let tickets = JSON.parse(localStorage.getItem('support_tickets')) || [];
            let senderName = currentUser ? currentUser.username : 'Ziyaretçi';
            
            tickets.push({
                user: senderName,
                message: msg,
                time: new Date().toLocaleTimeString(),
                isReply: false
            });
            localStorage.setItem('support_tickets', JSON.stringify(tickets));
            input.value = '';
            
            syncChat(); // Ekranı güncelle
        }

        function syncChat() {
            // Eğer giriş yapılmamışsa ve Ziyaretçi olarak yazıyorsa, yine de çalışmalı
            // Ama panel 'Ziyaretçi' olarak grupladığı için sorun yok.
            // Sadece currentUser null ise 'Ziyaretçi' varsayalım.
            
            let myUsername = currentUser ? currentUser.username : 'Ziyaretçi';
            
            const chatBox = document.getElementById('chat-messages');
            const tickets = JSON.parse(localStorage.getItem('support_tickets')) || [];
            
            // Sadece bu kullanıcının mesajlarını filtrele
            const myChats = tickets.filter(t => t.user === myUsername);
            
            // Sohbet kutusunun içeriğini oluştur
            let html = `
                <div class="flex items-start gap-2">
                    <div class="w-8 h-8 bg-emerald-600 rounded-full flex items-center justify-center shrink-0"><i data-lucide="bot" class="w-4 h-4 text-white"></i></div>
                    <div class="bg-gray-800 p-3 rounded-2xl rounded-tl-none text-xs text-gray-200 border border-white/5">Merhaba! Size nasıl yardımcı olabilirim?</div>
                </div>
            `;

            myChats.forEach(chat => {
                if (chat.isReply || chat.user === 'Admin' || chat.user === 'Destek Ekibi') {
                    // Admin Mesajı (Solda, Farklı Renk)
                    html += `
                        <div class="flex items-start gap-2 mt-2">
                            <div class="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center shrink-0"><i data-lucide="shield" class="w-4 h-4 text-white"></i></div>
                            <div class="bg-indigo-900/80 p-3 rounded-2xl rounded-tl-none text-xs text-white border border-indigo-500/30">
                                <span class="font-bold text-indigo-300 block text-[10px] mb-1">Yetkili</span>
                                ${chat.message}
                            </div>
                        </div>
                    `;
                } else {
                    // Kullanıcı Mesajı (Sağda)
                    html += `
                        <div class="flex items-center justify-end gap-2 mt-2">
                            <div class="bg-emerald-600 p-3 rounded-2xl rounded-tr-none text-xs text-white">${chat.message}</div>
                        </div>
                    `;
                }
            });

            // Sadece içerik değiştiyse güncelle
            if (chatBox.innerHTML !== html) {
                chatBox.innerHTML = html;
                chatBox.scrollTop = chatBox.scrollHeight;
                lucide.createIcons();
            }
        }

        // --- SETTINGS LOGIC ---
        function openSettingsModal() {
            if(!currentUser) return;
            document.getElementById('toggle-balance').checked = currentUser.settings.balanceHidden;
            document.getElementById('toggle-snow').checked = currentUser.settings.disableSnow;
            document.getElementById('settings-modal').classList.remove('hidden');
        }

        function closeSettingsModal() {
            document.getElementById('settings-modal').classList.add('hidden');
            document.getElementById('password-change-form').classList.add('hidden');
            document.getElementById('old-pass').value = '';
            document.getElementById('new-pass').value = '';
        }

        function toggleBalanceVisibility(hidden) {
            if(!currentUser) return;
            currentUser.settings.balanceHidden = hidden;
            localStorage.setItem('user_session', JSON.stringify(currentUser));
            updateMainDB();
            renderAuthStatus();
        }

        function toggleSnow(disabled) {
            if(!currentUser) return;
            currentUser.settings.disableSnow = disabled;
            localStorage.setItem('user_session', JSON.stringify(currentUser));
            updateMainDB();

            if(disabled) {
                const flakes = document.querySelectorAll('.snowflake');
                flakes.forEach(f => f.remove());
                if(snowInterval) clearInterval(snowInterval);
            } else {
                createSnow();
            }
        }

        function togglePasswordChange() {
            const form = document.getElementById('password-change-form');
            form.classList.toggle('hidden');
        }

        function changePassword() {
            const oldPass = document.getElementById('old-pass').value.trim();
            const newPass = document.getElementById('new-pass').value.trim();

            if(!oldPass || !newPass) {
                alert("Lütfen tüm alanları doldurun.");
                return;
            }

            if(currentUser.password === oldPass) {
                currentUser.password = newPass;
                localStorage.setItem('user_session', JSON.stringify(currentUser));
                updateMainDB();
                
                alert("Şifreniz başarıyla değiştirildi!");
                document.getElementById('old-pass').value = '';
                document.getElementById('new-pass').value = '';
                togglePasswordChange();
            } else {
                alert("Eski şifreniz yanlış!");
            }
        }

        function updateMainDB() {
            let db = JSON.parse(localStorage.getItem('db_users')) || {};
            if(db[currentUser.username]) {
                db[currentUser.username] = currentUser;
                localStorage.setItem('db_users', JSON.stringify(db));
            }
        }

        // --- RENDER FUNCTIONS ---
        function renderStore() {
            const kasaContainer = document.getElementById('kasa-list');
            const vipContainer = document.getElementById('vip-list');

            kasaContainer.innerHTML = PRODUCTS.kasalar.map(p => `
                <div class="glass-card snow-pile p-6 rounded-3xl flex flex-col h-full border-white/5">
                    <div class="flex justify-between items-start mb-4">
                        <div class="p-3 bg-emerald-500/10 rounded-2xl"><i data-lucide="package" class="text-emerald-500 w-6 h-6"></i></div>
                        <span class="text-xl font-black text-white">${p.price}₺</span>
                    </div>
                    <h4 class="text-xl font-bold mb-2">${p.name}</h4>
                    <p class="text-gray-400 text-sm font-medium flex-grow mb-6">${p.desc}</p>
                    <button onclick="addToCart('${p.id}', 'kasalar')" class="w-full bg-emerald-600/10 hover:bg-emerald-600 text-emerald-500 hover:text-white py-3 rounded-2xl font-bold transition-all">Sepete Ekle</button>
                </div>
            `).join('');

            vipContainer.innerHTML = PRODUCTS.vips.map(p => `
                <div class="glass-card snow-pile p-6 rounded-3xl flex flex-col h-full border-white/5 hover:border-amber-500/30 transition-all">
                    <div class="flex justify-between items-start mb-4">
                        <div class="p-3 bg-amber-500/10 rounded-2xl"><i data-lucide="crown" class="text-amber-500 w-6 h-6"></i></div>
                        <span class="text-xl font-black text-amber-500">${p.price}₺</span>
                    </div>
                    <h4 class="text-xl font-bold mb-2 uppercase tracking-wide">${p.name}</h4>
                    <p class="text-gray-400 text-sm font-medium flex-grow mb-6">${p.desc}</p>
                    <button onclick="addToCart('${p.id}', 'vips')" class="w-full bg-amber-500 hover:bg-amber-400 text-gray-950 py-3 rounded-2xl font-bold transition-all">Satın Al</button>
                </div>
            `).join('');
            lucide.createIcons();
        }

        function renderCredits() {
            const list = document.getElementById('credit-list');
            list.innerHTML = CREDIT_PACKAGES.map((pkg, index) => `
                <div class="glass-card p-6 rounded-3xl flex flex-col items-center text-center border-amber-500/10 hover:border-amber-500/40 transition-all group relative overflow-hidden z-20">
                    <div class="absolute inset-0 bg-gradient-to-b from-amber-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <div class="p-4 bg-amber-500/20 rounded-full mb-4 group-hover:scale-110 transition-transform">
                        <i data-lucide="coins" class="w-8 h-8 text-amber-400"></i>
                    </div>
                    <h4 class="text-2xl font-black text-white mb-1">${pkg.credits} Kredi</h4>
                    <p class="text-amber-200/60 text-xs font-bold uppercase tracking-wider mb-6">Paket ${index + 1}</p>
                    <div class="mt-auto w-full">
                        <div class="text-3xl font-black text-white mb-4">${pkg.price}₺</div>
                        <button onclick="initCreditPurchase(${index})" class="w-full bg-amber-500 hover:bg-amber-400 text-gray-900 py-3 rounded-xl font-bold transition-all shadow-lg shadow-amber-500/20 relative z-30 cursor-pointer">
                            Satın Al
                        </button>
                    </div>
                </div>
            `).join('');
            lucide.createIcons();
        }

        // --- CREDIT PAYMENT FLOW ---
        function initCreditPurchase(index) {
            if (!currentUser) {
                openAuthModal('login');
                return;
            }
            selectedCreditPackage = CREDIT_PACKAGES[index];
            document.getElementById('cp-modal-info').innerText = `Paket: ${selectedCreditPackage.credits} Kredi | Tutar: ${selectedCreditPackage.price} TL`;
            document.getElementById('credit-payment-modal').classList.remove('hidden');
        }

        function closeCreditPaymentModal() {
            document.getElementById('credit-payment-modal').classList.add('hidden');
            selectedCreditPackage = null;
            document.getElementById('payment-sender-name').value = '';
        }

        function copyIBAN() {
            const iban = "TR140006701000000080429336";
            const textArea = document.createElement("textarea");
            textArea.value = iban;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            const msg = document.getElementById('iban-copied-msg');
            msg.classList.remove('hidden');
            setTimeout(() => msg.classList.add('hidden'), 2000);
        }

        async function sendPaymentNotification() {
            const senderName = document.getElementById('payment-sender-name').value.trim();
            if (!senderName) {
                alert("Lütfen ödemeyi yapan kişinin adını soyadını yazınız.");
                return;
            }

            const btn = document.querySelector('#credit-payment-modal button');
            const originalText = btn.innerHTML;
            btn.innerHTML = "Bildirim Gönderiliyor...";
            btn.disabled = true;

            const payloadForBot = {
                username: currentUser.username,
                amount: selectedCreditPackage.credits,
                price: selectedCreditPackage.price,
                sender: senderName
            };

            try {
                // 1. Önce Python Bot API'sini dene
                // Relatif path kullanarak otomatik domain algılama
                const response = await fetch(`${API_URL}/api/payment`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payloadForBot)
                });

                if (response.ok) {
                    alert("✅ Ödeme bildiriminiz başarıyla gönderildi!\n\nYönetim ekibi Discord üzerinden onayladığında krediniz hesabınıza eklenecektir.");
                    closeCreditPaymentModal();
                } else {
                    throw new Error("Bot API hata verdi");
                }
            } catch (e) {
                console.warn("Bot'a ulaşılamadı, manuel webhook kullanılıyor...", e);
                
                // 2. Bot çalışmıyorsa Direkt Webhook kullan (Yedek)
                const webhookPayload = {
                    content: `🚨 **YENİ KREDİ SATIN ALMA BİLDİRİMİ (Bot Kapalı)**`,
                    embeds: [{
                        title: "💳 Ödeme Bildirimi (Havale/EFT)",
                        description: "Bot sistemi yanıt vermediği için manuel bildirim gönderildi.",
                        color: 15105570, // Orange
                        fields: [
                            { name: "👤 Site Kullanıcısı", value: `\`${currentUser.username}\``, inline: true },
                            { name: "💵 Tutar", value: `**${selectedCreditPackage.price} TL**`, inline: true },
                            { name: "🪙 İstenen Kredi", value: `**${selectedCreditPackage.credits} Kredi**`, inline: true },
                            { name: "🏦 Gönderen İsim Soyisim", value: `\`${senderName}\``, inline: false },
                            { name: "📅 Tarih", value: new Date().toLocaleString('tr-TR'), inline: false }
                        ],
                        footer: { text: "LunaNW | Ödeme Sistemi" }
                    }]
                };

                try {
                    await fetch(WEBHOOK_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(webhookPayload)
                    });
                    
                    alert("✅ Ödeme bildiriminiz başarıyla gönderildi!\n\n(Not: Bot aktif olmadığı için krediniz yönetim tarafından manuel eklenecektir.)");
                    closeCreditPaymentModal();
                } catch (webhookError) {
                    console.error("Webhook hatası:", webhookError);
                    alert("Bildirim gönderilirken bir hata oluştu. Lütfen Discord üzerinden iletişime geçin.");
                }
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        }

        // --- AUTH & CART (Existing Logic) ---
        function openAuthModal(mode) {
            authMode = mode;
            document.getElementById('auth-modal').classList.remove('hidden');
            document.getElementById('auth-error').classList.add('hidden');
            updateAuthModalUI();
        }
        function closeAuthModal() { document.getElementById('auth-modal').classList.add('hidden'); }
        function switchAuthMode() {
            authMode = authMode === 'login' ? 'register' : 'login';
            updateAuthModalUI();
        }
        function updateAuthModalUI() {
            const title = document.getElementById('auth-modal-title');
            const btn = document.getElementById('auth-submit');
            const switchText = document.getElementById('auth-switch-text');
            const switchBtn = document.getElementById('auth-switch-btn');
            if (authMode === 'login') {
                title.innerText = "Giriş Yap"; btn.innerText = "Giriş Yap"; switchText.innerText = "Hesabın yok mu?"; switchBtn.innerText = "Kayıt Ol";
            } else {
                title.innerText = "Yeni Kayıt"; btn.innerText = "Kayıt Ol"; switchText.innerText = "Zaten hesabın var mı?"; switchBtn.innerText = "Giriş Yap";
            }
        }
        document.getElementById('auth-submit').addEventListener('click', () => {
            const user = document.getElementById('auth-user').value.trim();
            const pass = document.getElementById('auth-pass').value.trim();
            const error = document.getElementById('auth-error');
            if (!user || !pass) { error.innerText = "Lütfen tüm alanları doldurun."; error.classList.remove('hidden'); return; }
            let users = JSON.parse(localStorage.getItem('db_users')) || {};
            if (authMode === 'register') {
                if (users[user]) { error.innerText = "Bu kullanıcı adı zaten mevcut."; error.classList.remove('hidden'); } 
                else { users[user] = { username: user, password: pass, credits: 0, settings: { balanceHidden: false, disableSnow: false } }; localStorage.setItem('db_users', JSON.stringify(users)); loginAction(users[user]); }
            } else {
                if (users[user] && users[user].password === pass) { loginAction(users[user]); } 
                else { error.innerText = "Kullanıcı adı veya şifre hatalı!"; error.classList.remove('hidden'); }
            }
        });
        function loginAction(userData) {
            if (userData.credits === undefined) userData.credits = 0;
            if (userData.settings === undefined) userData.settings = { balanceHidden: false, disableSnow: false };
            currentUser = userData;
            localStorage.setItem('user_session', JSON.stringify(userData));
            closeAuthModal();
            renderAuthStatus();
            updateUserCredits(); // Giriş yapınca güncel krediyi çek
        }
        function logout() {
            currentUser = null; cart = []; localStorage.removeItem('user_session'); renderAuthStatus(); navigate('home');
        }
        function addToCart(id, category) {
            if (!currentUser) { openAuthModal('login'); return; }
            const prod = PRODUCTS[category].find(p => p.id === id);
            cart.push({...prod}); renderAuthStatus(); openCart();
        }
        function openCart() {
            currentStep = 'items'; document.getElementById('cart-modal').classList.remove('hidden'); renderCart();
        }
        function closeCartModal() { document.getElementById('cart-modal').classList.add('hidden'); }
        function removeFromCart(index) { cart.splice(index, 1); renderCart(); renderAuthStatus(); }
        
        function renderCart() {
            const body = document.getElementById('cart-body');
            const total = cart.reduce((sum, i) => sum + i.price, 0);
            if (currentStep === 'items') {
                if (cart.length === 0) {
                    body.innerHTML = `<div class="text-center py-12 space-y-4"><i data-lucide="shopping-basket" class="w-12 h-12 text-gray-700 mx-auto"></i><p class="text-gray-500 font-medium">Sepetiniz şu an boş.</p><button onclick="closeCartModal(); navigate('store')" class="text-emerald-500 font-bold hover:underline">Alışverişe Başla</button></div>`;
                } else {
                    body.innerHTML = `<div class="space-y-4 max-h-[300px] overflow-y-auto custom-scrollbar pr-2">${cart.map((item, idx) => `<div class="flex items-center justify-between p-4 bg-gray-900 rounded-2xl border border-white/5"><div><p class="font-bold text-white">${item.name}</p><p class="text-xs font-bold text-emerald-500">${item.price}₺</p></div><button onclick="removeFromCart(${idx})" class="p-2 hover:bg-red-500/10 text-gray-600 hover:text-red-500 transition-colors"><i data-lucide="trash-2" class="w-5 h-5"></i></button></div>`).join('')}</div><div class="mt-8 space-y-4"><div class="flex justify-between items-center px-2"><span class="text-gray-400 font-bold">Toplam Tutar:</span><span class="text-2xl font-black text-white">${total}₺</span></div><button onclick="completeOrder()" class="w-full bg-emerald-600 hover:bg-emerald-500 py-4 rounded-2xl font-bold transition-all shadow-xl shadow-emerald-900/10">Ödemeye Geç</button></div>`;
                }
            }
            lucide.createIcons();
        }

        async function completeOrder() {
            const total = cart.reduce((sum, i) => sum + i.price, 0);
            
            // Eğer kredi yeterliyse düşülmeli (Bu kısmı basit tutuyoruz, normalde backend kontrol etmeli)
            if (currentUser.credits < total) {
                alert("Yetersiz Kredi! Lütfen kredi yükleyin.");
                return;
            }

            // Krediyi düş (Frontend simülasyonu - Gerçekte backend yapmalı)
            currentUser.credits -= total;
            localStorage.setItem('user_session', JSON.stringify(currentUser));
            updateMainDB(); // Ana veritabanını da güncelle
            renderAuthStatus();

            alert(`Sipariş başarıyla alındı! Hesabınızdan ${total} kredi düşüldü. Eşyalarınız oyun içinde teslim edilecektir.`);
            cart = []; closeCartModal();
        }

        function copyIP() {
            const text = "lunanw.xyz";
            const textArea = document.createElement("textarea"); textArea.value = text;
            textArea.style.position = "fixed"; textArea.style.left = "-9999px"; textArea.style.top = "0";
            document.body.appendChild(textArea); textArea.focus(); textArea.select();
            try { document.execCommand('copy'); } catch (err) {}
            document.body.removeChild(textArea);
            const el = document.getElementById('ip-text'); el.innerText = "IP KOPYALANDI!"; el.classList.add('text-emerald-400');
            setTimeout(() => { el.innerText = text; el.classList.remove('text-emerald-400'); }, 2000);
        }

        // --- SERVER STATUS ---
        async function checkServerStatus() {
            const badge = document.getElementById('server-status-badge');
            const text = document.getElementById('player-count-text');
            const dotContainer = document.getElementById('status-indicator-container');

            const setOnline = (count) => {
                text.innerText = `${count} Oyuncu Çevrimiçi`;
                badge.classList.remove('hidden');
                badge.className = "inline-flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full px-4 py-1.5 text-emerald-400 text-sm font-bold animate-fade-in mb-4 relative z-10";
                dotContainer.innerHTML = `<span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span><span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>`;
            };

            const setOffline = () => {
                text.innerText = "Sunucu Çevrimdışı";
                badge.classList.remove('hidden');
                badge.className = "inline-flex items-center gap-2 bg-red-500/10 border border-red-500/20 rounded-full px-4 py-1.5 text-red-400 text-sm font-bold animate-fade-in mb-4 relative z-10";
                dotContainer.innerHTML = `<span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>`;
            };

            const apis = [
                { url: `https://api.mcsrvstat.us/2/${SERVER_IP}`, parse: d => ({ online: d.online, players: d.players?.online }) },
                { url: `https://mcapi.us/server/status?ip=${SERVER_IP}`, parse: d => ({ online: d.online, players: d.players?.now }) }
            ];

            for (const api of apis) {
                try {
                    const response = await fetch(api.url);
                    const data = await response.json();
                    const res = api.parse(data);
                    if (res.online) { setOnline(res.players); return; }
                } catch (e) {}
            }
            setOffline();
        }

        // --- SNOWFALL ---
        function createSnow() {
            if (snowInterval) clearInterval(snowInterval);
            const snowflakeCount = 15; 
            const container = document.body;
            snowInterval = setInterval(() => {
                if (currentUser && currentUser.settings.disableSnow) return;
                if (document.querySelectorAll('.snowflake').length > snowflakeCount) return;
                const flake = document.createElement('img');
                flake.src = SNOWFLAKE_IMAGE_URL;
                flake.classList.add('snowflake');
                const size = Math.random() * 20 + 20; 
                flake.style.width = `${size}px`;
                flake.style.height = `${size}px`;
                flake.style.left = Math.random() * 100 + 'vw';
                flake.style.animationDuration = `${Math.random() * 5 + 3}s`;
                flake.addEventListener('animationend', () => flake.remove());
                container.appendChild(flake);
            }, 800);
        }

        init();
    </script>
</body>
</html>"""

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
