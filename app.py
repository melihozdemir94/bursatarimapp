from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

VISITOR_COUNT = 1248

BURSA_ILCELER = {
    "Osmangazi": {"lat": 40.1828, "lon": 29.0669, "crop": "Şeftali, Meyvecilik", "pest": "Doğu Meyve Güvesi", "spray": "Rüzgarsız sabah saatlerinde (06:00 - 09:00)", "fertilizer": "Meyve büyütme dönemi potasyum takviyesi"},
    "Nilüfer": {"lat": 40.2125, "lon": 28.9833, "crop": "Sebze, Bağcılık", "pest": "Bağ Küllemesi", "spray": "Sıcaklığın 25°C altında olduğu saatler", "fertilizer": "Damla sulama ile dengeli NPK gübresi"},
    "Yıldırım": {"lat": 40.1917, "lon": 29.1167, "crop": "Şeftali, Kiraz", "pest": "Meyve Sinekleri", "spray": "Akşamüstü nem oranı yükselmeden", "fertilizer": "Organik madde ve kompost uygulaması"},
    "Gemlik": {"lat": 40.4314, "lon": 29.1556, "crop": "Zeytin", "pest": "Zeytin Halkalı Leke, Zeytin Sineği", "spray": "Nem düşüşe geçtiğinde bakırlı bileşikler", "fertilizer": "Yapraktan Bor ve Çinko takviyesi"},
    "Mudanya": {"lat": 40.3753, "lon": 28.8822, "crop": "Zeytin, Siyah İncir", "pest": "Zeytin Güvesi, İncir Basrası", "spray": "Erken sabah çiğ kalktıktan sonra", "fertilizer": "Azotlu ve Potasyumlu besleme"},
    "İnegöl": {"lat": 40.0781, "lon": 29.5133, "crop": "Elma, Ayva, Ayçiçeği", "pest": "Elma İç Kurdu, Kara Leke", "spray": "Sistemik fungusit uygulaması", "fertilizer": "Taban gübrelemesi ve Fosfor takviyesi"},
    "Orhangazi": {"lat": 40.4908, "lon": 29.3092, "crop": "Zeytin, Turşuluk Sebze", "pest": "Zeytin Pamuklu Biti", "spray": "Rüzgar hızının 10 km/s altında olduğu zamanlar", "fertilizer": "Toprak analizine dayalı yaprak gübresi"},
    "İznik": {"lat": 40.4286, "lon": 29.7214, "crop": "Zeytin, Üzüm, Meyve", "pest": "Bağ Mildiyösü, Halkalı Leke", "spray": "Yağışsız 24 saatlik periyotlarda", "fertilizer": "Kalsiyum Nitrat ve Magnezyum"},
    "Karacabey": {"lat": 40.2150, "lon": 28.3569, "crop": "Domates, Mısır, Çeltik", "pest": "Kırmızı Örümcek, Yeşil Kurt", "spray": "Rüzgar yüksekse erteleyin!", "fertilizer": "Damlama sulama ile Azot beslemesi"},
    "Mustafakemalpaşa": {"lat": 40.0350, "lon": 28.4117, "crop": "Domates, Biber, Tatlı Mısır", "pest": "Yaprak Biti, Mildiyö", "spray": "Serin ve rüzgarsız hava koşullarında", "fertilizer": "Tabandan ve yapraktan kombine gübreleme"},
    "Yenişehir": {"lat": 40.2644, "lon": 29.6528, "crop": "Biber, Biberiye, Tahıl", "pest": "Thrips, Hububat Hortumlu Böceği", "spray": "Erken sabah periyodu", "fertilizer": "Üre ve Amonyum Sülfat takviyesi"},
    "Kestel": {"lat": 40.1978, "lon": 29.2136, "crop": "Şeftali, Böğürtlen", "pest": "Külleme, Monilya", "spray": "Çiçeklenme sonrası koruyucu koruma", "fertilizer": "Organik gübre ve iz elementler"},
    "Gürsu": {"lat": 40.2147, "lon": 29.1936, "crop": "Deveci Armudu, Şeftali", "pest": "Armut Psillidi, Ateş Yanıklığı", "spray": "Hassas periyotta hedeflenmiş ilaçlama", "fertilizer": "Kalsiyum ve Potasyum ağırlıklı"},
    "Orhaneli": {"lat": 39.9042, "lon": 28.9878, "crop": "Ceviz, Gölet Sulamalı Tarım", "pest": "Ceviz İç Kurdu", "spray": "Rüzgarsız gün ortası öncesi", "fertilizer": "Çinko ve Hümik Asit desteği"},
    "Keles": {"lat": 39.9136, "lon": 29.1417, "crop": "Çilek, Kiraz", "pest": "Çilek Kök Boğazı Çürüklüğü", "spray": "Hasat sonrası koruyucu uygulama", "fertilizer": "Damla sulama ile dengeli NPK"},
    "Büyükorhan": {"lat": 39.7744, "lon": 28.8814, "crop": "Hububat, Gölet Tarımı", "pest": "Süve, Kımıl", "spray": "Sabah erken saatler", "fertilizer": "Toprak hazırlığı organik gübreleme"},
    "Harmancık": {"lat": 39.6975, "lon": 29.1558, "crop": "Ceviz, Tahıl", "pest": "Ceviz Yaprak Biti", "spray": "Sıcaklığın uygun olduğu saatler", "fertilizer": "Azotlu üst gübreleme"}
}

def fetch_weather_data(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relativehumidity_2m"
        response = requests.get(url, timeout=4)
        data = response.json()
        temp = data['current_weather']['temperature']
        wind = data['current_weather']['windspeed']
        humidity = data['hourly']['relativehumidity_2m'][0]
        return temp, wind, humidity
    except Exception:
        return 22.0, 12.0, 65

@app.route('/')
def index():
    global VISITOR_COUNT
    VISITOR_COUNT += 1
    return render_template('index.html', visitor_count=VISITOR_COUNT)

@app.route('/api/ilce/<name>')
def get_ilce_data(name):
    if name in BURSA_ILCELER:
        info = BURSA_ILCELER[name]
        temp, wind, humidity = fetch_weather_data(info['lat'], info['lon'])
        return jsonify({
            "success": True,
            "district": name,
            "temp": temp,
            "wind": wind,
            "humidity": humidity,
            "crop": info['crop'],
            "pest": info['pest'],
            "spray": info['spray'],
            "fertilizer": info['fertilizer']
        })
    return jsonify({"success": False, "error": "İlçe bulunamadı"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)