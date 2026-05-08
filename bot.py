import requests
import datetime

# Hava durumu çekilecek şehirler ve koordinatları (İstediğin gibi ekleyip çıkarabilirsin)
sehirler = {
    "Doğubayazıt": {"lat": 39.5453, "lon": 44.0836},
    "Ağrı Merkez": {"lat": 39.7191, "lon": 43.0503},
    "İstanbul": {"lat": 41.0082, "lon": 28.9784},
    "Ankara": {"lat": 39.9199, "lon": 32.9247},
    "İzmir": {"lat": 38.4127, "lon": 27.1384},
    "Antalya": {"lat": 36.8969, "lon": 30.7133},
    "Bursa": {"lat": 40.1824, "lon": 29.0671},
    "Van": {"lat": 38.4924, "lon": 43.3831}
}

# API'den gelen kodları şık ikonlara ve renklere çeviren sistem
def durum_analizi(kod):
    if kod == 0: return "☀️", "Açık", "#fcd34d" # Sarı
    elif kod in [1, 2, 3]: return "⛅", "Parçalı Bulutlu", "#e2e8f0" # Beyazımsı
    elif kod in [45, 48]: return "🌫️", "Sisli", "#94a3b8" # Gri
    elif kod in [51, 53, 55, 56, 57]: return "🌦️", "Çiseleyen", "#7dd3fc" # Açık Mavi
    elif kod in [61, 63, 65, 66, 67, 80, 81, 82]: return "🌧️", "Yağmurlu", "#38bdf8" # Mavi
    elif kod in [71, 73, 75, 77, 85, 86]: return "❄️", "Kar Yağışlı", "#ffffff" # Beyaz
    elif kod in [95, 96, 99]: return "🌩️", "Fırtınalı", "#a78bfa" # Mor
    else: return "🌡️", "Belirsiz", "#cbd5e1"

# === HTML ÜST KISIM (İnadına TV Özel Tasarımı) ===
html_icerik = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Canlı Hava Durumu - İnadına TV</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 15px; }
        .header { text-align: center; margin-bottom: 25px; padding-top: 10px; }
        .baslik { font-size: 24px; font-weight: 800; color: #0ea5e9; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
        .alt-baslik { font-size: 13px; color: #94a3b8; font-weight: 500; }
        
        .grid-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 12px; }
        
        .kart { background: linear-gradient(145deg, #1e293b, #0f172a); border-radius: 16px; padding: 20px 10px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 1px solid #334155; position: relative; overflow: hidden; transition: transform 0.3s; }
        .kart:hover { transform: translateY(-5px); border-color: #0ea5e9; }
        .ust-cizgi { position: absolute; top: 0; left: 0; width: 100%; height: 4px; }
        
        .sehir { font-size: 15px; font-weight: 700; color: #f1f5f9; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .ikon { font-size: 42px; margin: 10px 0; display: block; line-height: 1; }
        .sicaklik { font-size: 28px; font-weight: 800; margin-bottom: 8px; }
        
        .durum { font-size: 11px; font-weight: 600; color: #cbd5e1; background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 12px; display: inline-block; }
        .ruzgar { margin-top: 15px; font-size: 11px; color: #64748b; font-weight: 500; border-top: 1px solid #334155; padding-top: 10px; }
        
        .footer { text-align: center; margin-top: 35px; font-size: 12px; color: #64748b; line-height: 1.6; }
        .marka { color: #0ea5e9; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <div class="baslik">☁️ HAVA DURUMU</div>
        <div class="alt-baslik">Canlı Meteoroloji Verileri</div>
    </div>
    <div class="grid-container">
"""

print("Hava durumu verileri çekiliyor...")
basarili_sayi = 0

for sehir_adi, koord in sehirler.items():
    # Ücretsiz Open-Meteo API'sine bağlanıyoruz
    url = f"https://api.open-meteo.com/v1/forecast?latitude={koord['lat']}&longitude={koord['lon']}&current_weather=true&timezone=Europe%2FMoscow"
    cevap = requests.get(url)
    
    if cevap.status_code == 200:
        veri = cevap.json()
        if "current_weather" in veri:
            anlik = veri["current_weather"]
            sicaklik = anlik["temperature"]
            ruzgar_hizi = anlik["windspeed"]
            hava_kodu = anlik["weathercode"]
            
            ikon, aciklama, renk = durum_analizi(hava_kodu)
            
            html_icerik += f"""
            <div class="kart">
                <div class="ust-cizgi" style="background-color: {renk};"></div>
                <div class="sehir">{sehir_adi}</div>
                <div class="ikon">{ikon}</div>
                <div class="sicaklik" style="color: {renk};">{sicaklik}°C</div>
                <div class="durum">{aciklama}</div>
                <div class="ruzgar">💨 Rüzgar: {ruzgar_hizi} km/s</div>
            </div>
            """
            basarili_sayi += 1
            print(f"{sehir_adi} başarıyla çekildi.")

# Güncel zamanı ekliyoruz
zaman = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

html_icerik += f"""
    </div>
    <div class="footer">
        © 2026 <span class="marka">İnadına TV</span> Özel Servisi<br>
        Son Güncelleme: {zaman}
    </div>
</body>
</html>
"""

# Dosyayı kaydetme
with open("index.html", "w", encoding="utf-8") as dosya:
    dosya.write(html_icerik)

print(f"İşlem tamam! {basarili_sayi} şehrin verisi index.html dosyasına yazıldı.")
