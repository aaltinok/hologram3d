"""Altı robot için adım adım yapım rehberi içeriği.

Not: Rehberler genel / tipik kit ve parçalara göredir. Kendi kitinizin kılavuzu ve parça veri sayfaları önceliklidir.
`yeni` listesindeki anahtarlar, hologramdaki parça gruplarıdır (adım ilerledikçe hologramda belirir).
"""
from __future__ import annotations


def S(baslik, yeni, yap, kontrol, sure, ipucu=None, uyari=None, vurgu=None):
    return {"baslik": baslik, "yeni": yeni, "vurgu": vurgu or [], "yap": yap, "kontrol": kontrol,
            "sure": sure, "ipucu": ipucu, "uyari": uyari}


def N(lines, x, y, w, h):
    return {"lines": lines, "x": x, "y": y, "w": w, "h": h}


def E(a, b, stil="sinyal", etiket=None, off=0.0, mid=0.0):
    return {"a": a, "b": b, "stil": stil, "etiket": etiket, "off": off, "mid": mid}


GUIDES: dict = {}

# =====================================================================================================
# QUADCOPTER
# =====================================================================================================
GUIDES["quad"] = {
    "zorluk": "Orta–Zor", "sure": "12–20 saat", "butce": "Orta–Yüksek",
    "hedef": ("5 inç sınıfında, X şasili, 4S LiPo ile uçan; fotoğraf / FPV için temel bir quadcopter. "
              "Aynı yöntem 7 inç veya daha büyük şasilere de uygulanır."),
    "beceri": ["Lehim", "Temel elektronik", "Betaflight / ArduPilot ayarı", "Uçuş güvenliği"],
    "ogrenme": ["İtki/ağırlık (TWR) hesabı ve parça seçimi", "ESC, motor ve uçuş kartı ilişkisi",
                "Motor yönleri ve karıştırıcı (mixer) mantığı", "PID ile yatış dengesi"],
    "araclar": ["Havya (ayarlanabilir) + lehim teli", "İnce uçlu cımbız ve yan keski", "Allen anahtar seti (1,5–3 mm)",
                "Vida sabitleyici (mavi)", "Multimetre", "Isı büzüşmeli makaron + ısı tabancası",
                "LiPo şarj aleti + LiPo güvenlik çantası", "USB kablo + bilgisayar", "Zip-tie, çift taraflı bant", "Hassas terazi"],
    "malzeme": [
        ("Şasi (5 inç, karbon fiber X)", 1, "Kol kalınlığı ≥ 4 mm; ara parça ve vidalar dahil"),
        ("Fırçasız motor (örn. 2207 sınıfı)", 4, "KV, batarya hücre sayısına göre seçilir"),
        ("Pervane 5 inç", "2 CW + 2 CCW", "Yedek en az 2 takım alın"),
        ("4'ü 1 arada ESC (30–45 A)", 1, "BLHeli_S / BLHeli_32 / Bluejay; 4S–6S uyumlu"),
        ("Uçuş kontrol kartı (F4 / F7)", 1, "30,5 × 30,5 mm; Betaflight uyumlu"),
        ("LiPo batarya 4S 1300–3000 mAh", "1–2", "XT60 konnektörlü; ≥ 75C"),
        ("Alıcı + verici (ELRS / Crossfire)", 1, "UART ile uçuş kartına bağlanır"),
        ("Kamera + video vericisi", "1 (ops.)", "FPV uçuş için"),
        ("GPS + pusula", "1 (ops.)", "Konum tutma ve eve dönüş için"),
        ("XT60 konnektör + 1000 µF kapasitör", "1 + 1", "Batarya girişindeki gerilim sıçramalarını azaltır"),
        ("M3 vida seti + titreşim sönümleyici lastik halka", 1, "Uçuş kartı yumuşak monte edilir"),
        ("Buzzer", 1, "Kayıp quad'ı bulmak ve uyarılar için"),
        ("Isı büzüşmeli makaron, bağ, batarya kayışı", 1, "Kablo düzeni ve batarya sabitleme"),
    ],
    "adimlar": [
        S("Tasarım hesabı ve parça seçimi", [],
          ["Hedef toplam kütleyi belirleyin ve TWR hesaplayın (hedef ≥ 2, serbest uçuş için 3–4).",
           "Boşta devir ≈ KV × batarya gerilimi: motor KV'sini hücre sayısına göre seçin.",
           "ESC sürekli akımı, motorun tepe akımından en az %20 yüksek olsun.",
           "Sayfanın altındaki 'İtki ve uçuş süresi' hesaplayıcısıyla pervane, batarya ve kütleyi deneyin."],
          "TWR ≥ 2 ve tahmini uçuş süresi hedefinizi karşılıyor.", "1 saat",
          ipucu="Önce batarya ve motoru, sonra ESC ve pervaneyi seçin; her şey ağırlığı artırır."),
        S("Şasiyi monte et", ["frame"],
          ["Alt plakaya ara parçaları (standoff) takın, üst plakayı yerleştirin.",
           "Vidaları çapraz sırayla, vida sabitleyiciyle ve yalnızca hafifçe sıkın.",
           "Alt plakaya batarya kayışı yuvasını ve iniş takımı yuvalarını hazırlayın."],
          "Gövde burulmaya karşı sert; plakalar paralel ve vidalar tam oturmuş.", "30 dk",
          uyari="Karbon fiber tozu zararlıdır: kesme veya zımparalama yaparsanız maske ve gözlük kullanın."),
        S("Kolları ve motorları tak", ["arms", "motors"],
          ["Kolları gövdeye sabitleyin; X biçiminde simetrik olduklarını kontrol edin.",
           "Motorları kollara, motor boyuna uygun KISA vidalarla bağlayın.",
           "Motor kablolarını kol boyunca yönlendirip bağlayın; pervane diskine kablo girmemeli."],
          "Dört motor da aynı hizada; motor milleri elle düzgün dönüyor, sürtünme yok.", "45 dk",
          uyari="Vida boyu fazla uzunsa motor sargısına değer ve motoru bozar. Vida boyu = kol kalınlığı + dişli derinlik − 0,5 mm."),
        S("ESC lehimi ve güç kablosu", ["esc"],
          ["Pedleri kalaylayın; motor kablolarını ESC pedlerine lehimleyin (sıra, yönü belirler; yazılımda ters çevrilebilir).",
           "XT60 kablosunu ESC güç pedlerine lehimleyin (kırmızı +, siyah −) ve kapasitörü pedlere paralel bağlayın.",
           "Tüm lehimleri ısı büzüşmeli makaronla kapatın."],
          "Multimetre süreklilik modunda + ile − arasında bip yok (kısa devre yok). Lehimler parlak ve pürüzsüz.", "1–1,5 saat",
          uyari="Kısa devre LiPo yangınına yol açabilir. Bu aşamada batarya kesinlikle bağlı olmamalı.",
          ipucu="Kapasitörün + bacağı ESC +, − bacağı ESC − tarafına gelir; bacakları kısa tutun."),
        S("Uçuş kontrol kartını yerleştir", ["fc"],
          ["Kartı titreşim sönümleyici lastik halkalarla 4 vidaya yerleştirin; okun yönü ÖNE baksın.",
           "ESC'den gelen sinyal kablosunu (DShot + 5 V/GND) karta bağlayın.",
           "Alıcıyı boş bir UART'a bağlayın (CRSF'de TX ↔ RX çapraz)."],
          "Kart USB ile bilgisayara bağlanınca LED yanıyor ve Betaflight'e bağlanıyor.", "45 dk",
          ipucu="Vidaları lastik halkaları ezecek kadar sıkmayın; kart 'yüzmeli'."),
        S("Kamera, GPS ve yardımcı parçalar", ["camera", "gps"],
          ["Kamerayı ön tarafa sabitleyin, video vericisini kartın OSD / VTX girişine bağlayın.",
           "GPS'i okun yönü ileri bakacak şekilde, motor kablolarından ve ESC'den uzağa yerleştirin.",
           "Buzzer'ı bağlayın; kabloları bağlarla toplayın."],
          "Kablolar pervane yoluna girmiyor; GPS pusulası yön olarak doğru yerleştirilmiş.", "45 dk"),
        S("Batarya ve iniş takımı", ["battery", "legs"],
          ["İniş takımı ayaklarını takın.", "Bataryayı kayışla sıkıca sabitleyin.",
           "Quad'ı iki parmağınızla (kollar arasından) tutarak denge noktasını bulun: ağırlık merkezi (CG) tam ortada olmalı."],
          "Batarya sallanmıyor; CG gövdenin ortasında, tek bir tarafa yatmıyor.", "30 dk",
          ipucu="CG ortada değilse bataryayı ileri geri kaydırın."),
        S("Yazılım yapılandırması", [],
          ["Betaflight Configurator ile kartın yazılımını güncelleyin.",
           "Ports: alıcının bağlı olduğu UART'ta 'Serial RX'i açın. Configuration: ESC/motor protokolünü (örn. DShot300/600) seçin.",
           "Receiver sekmesinde kanal haritasını ve çubuk hareketlerini doğrulayın; Modes sekmesinde ARM anahtarını tanımlayın.",
           "Failsafe ayarlarını yapın (sinyal kaybında motorları durdur / güvenli iniş)."],
          "Receiver sekmesinde çubuklar doğru ve aynı yönde hareket ediyor; kart eğilince 3B model doğru eğiliyor.", "1 saat",
          vurgu=["fc"],
          uyari="Betaflight'in motor sırası ve yön diyagramı (Motors sekmesi) esastır. Bu uygulamadaki mixer örneği yalnızca eğitim amaçlıdır."),
        S("Pervanesiz motor testi", [],
          ["PERVANELERİ TAKMADAN, bataryayla Motors sekmesinde çok düşük gazla her motoru tek tek döndürün.",
           "Dönüş yönlerini diyagramla karşılaştırın; ters olan motoru ESC yapılandırmasından çevirin.",
           "Verici ile ARM yapıp düşük gazda dört motoru birlikte deneyin, ardından failsafe'i (vericiyi kapatma) test edin."],
          "Dört motor doğru yönde dönüyor; vericiyi kapatınca motorlar duruyor.", "30 dk", vurgu=["motors", "esc"],
          uyari="Bu testte pervane takılı olmamalı. Çevrede kimse bulunmamalı."),
        S("Pervaneleri tak ve ilk uçuş", ["props"],
          ["CW ve CCW pervaneleri diyagrama uygun motorlara takın; somunları sıkın.",
           "Geniş, açık bir alan seçin; quad'ı düz zemine koyun ve uzaktan ARM edin.",
           "İlk uçuşta 30–50 cm yükselip asılı kalın (hover); yalpalama, titreşim ve yön eğilimlerini gözleyin."],
          "Quad kararlı asılı kalıyor; kısa süreli uçuşta motorlar ve ESC aşırı ısınmıyor.", "1 saat",
          uyari="İnsanlardan, hayvanlardan ve binalardan uzak olun; güvenlik gözlüğü kullanın. Uçuş öncesi yerel mevzuatı (SHGM) kontrol edin."),
    ],
    "kablolama": {
        "boyut": (980, 380),
        "nodes": {
            "rx": N(["Alıcı (ELRS/CRSF)", "UART"], 30, 40, 190, 60),
            "gps": N(["GPS + pusula", "UART + I²C"], 30, 130, 190, 60),
            "batt": N(["LiPo 4S", "14,8 V · XT60"], 30, 250, 190, 64),
            "fc": N(["Uçuş kontrol kartı", "F4/F7 · Betaflight"], 290, 40, 200, 74),
            "esc": N(["4'ü 1 arada ESC", "DShot · 30–45 A"], 290, 230, 200, 74),
            "cam": N(["Kamera + VTX", "FPV (opsiyonel)"], 570, 40, 180, 60),
            "bz": N(["Buzzer + LED", "BZ+ / BZ−"], 570, 130, 180, 60),
            "m1": N(["Motor M1", "arka sağ"], 790, 40, 170, 48),
            "m2": N(["Motor M2", "ön sağ"], 790, 100, 170, 48),
            "m3": N(["Motor M3", "arka sol"], 790, 160, 170, 48),
            "m4": N(["Motor M4", "ön sol"], 790, 220, 170, 48),
        },
        "edges": [
            E("rx", "fc", "i2c", "UART"), E("gps", "fc", "i2c", "UART + SDA/SCL", off=14),
            E("batt", "esc", "guc", "XT60 + 1000 µF"), E("esc", "fc", "sinyal", "DShot + 5 V/GND"),
            E("fc", "cam", "sinyal"), E("fc", "bz", "sinyal", off=0),
            E("esc", "m1", "faz", "3 faz", mid=130), E("esc", "m2", "faz", mid=130),
            E("esc", "m3", "faz", mid=130), E("esc", "m4", "faz", mid=130),
        ],
        "pinler": [
            ("LiPo 4S", "ESC güç pedleri", "XT60 (+ kırmızı, − siyah)", "Kapasitör pedlere paralel; batarya en son bağlanır"),
            ("ESC", "Motor M1–M4", "3 faz kablosu", "Sıra, dönüş yönünü belirler"),
            ("ESC", "Uçuş kartı", "Sinyal + 5 V + GND (konnektör)", "DShot protokolü"),
            ("Alıcı", "Uçuş kartı (UART)", "TX ↔ RX çapraz, 5 V, GND", "CRSF / ELRS için"),
            ("GPS", "Uçuş kartı", "UART TX/RX + I²C SCL/SDA, 5 V", "Pusula motorlardan uzakta olmalı"),
            ("Kamera / VTX", "Uçuş kartı", "Video, OSD UART", "Opsiyonel"),
            ("Buzzer", "Uçuş kartı", "BZ+ / BZ−", "Uyarı sesleri"),
        ],
    },
    "kod": [
        {"baslik": "Betaflight kurulum kontrol listesi", "dil": "text", "dosya": "betaflight_kontrol_listesi.txt",
         "aciklama": "Yazılım tarafında sırayla yapılacaklar (menü adları Betaflight Configurator'dadır).",
         "kod": ("1. Firmware Flasher  -> kartın hedefini (target) seç, güncel kararlı sürümü yükle\n"
                 "2. Ports            -> alıcının bağlı olduğu UART'ta Serial RX = AÇIK\n"
                 "3. Configuration    -> ESC/Motor protokolü: DShot300 veya DShot600\n"
                 "                       Receiver Mode: Serial (CRSF/ELRS)\n"
                 "4. Receiver         -> Kanal haritası AETR; çubukları oynatıp doğrula\n"
                 "5. Modes            -> ARM anahtarı + ANGLE (başlangıç için) + BEEPER\n"
                 "6. Failsafe         -> Sinyal kaybında motorları durdur / yumuşak iniş\n"
                 "7. Motors           -> PERVANESİZ: yönleri test et, ters olanı çevir\n"
                 "8. PID Tuning       -> Başlangıçta varsayılan; titreşim varsa önce mekaniği kontrol et")},
        {"baslik": "Motor karıştırıcı (mixer) mantığı", "dil": "python", "dosya": "quad_mixer.py", "fn": "physics.quad_mix",
         "aciklama": "Gaz + roll/pitch/yaw girişlerinin dört motora dağıtımı. Bu, eğitim amaçlı örnektir; gerçek kart kendi diyagramını kullanır."},
        {"baslik": "Roll ekseni PD denge simülasyonu", "dil": "python", "dosya": "roll_pd.py", "fn": "physics.quad_roll_step",
         "aciklama": "Tek eksenli PD denetleyicinin basamak yanıtı; Kp / Kd değerlerinin etkisini bununla inceleyin."},
    ],
    "test": [
        "Gövde sağlam: vidalar sabit, kollar simetrik, pervane diskinde kablo yok.",
        "Kısa devre yok: bataryasız halde + / − arasında multimetre bip sesi vermiyor.",
        "Uçuş kartı eksenleri doğru: quad'ı öne eğince Betaflight 3B modeli de öne eğiliyor.",
        "Alıcı çubukları doğru kanalda ve doğru yönde.",
        "Motor yönleri diyagramla uyumlu (pervanesiz test).",
        "Failsafe testi: vericiyi kapatınca motorlar duruyor (pervanesiz).",
        "Ağırlık merkezi ortada; batarya sabit.",
        "İlk hover: 30–50 cm'de kararlı, ısınma yok.",
    ],
    "sorun": [
        ("Motor dönmüyor", "ARM yapılmamış, ESC protokolü uyumsuz veya sinyal kablosu gevşek", "Modes'ta ARM'ı, protokolü ve konnektörü kontrol edin"),
        ("Havalanır havalanmaz bir yana devriliyor", "Motor / pervane yönü ya da kart yönü yanlış", "Motor diyagramını, pervane CW/CCW'yi ve kartın ön okunu kontrol edin"),
        ("Görüntüde titreşim (jello) / yalpalama", "Pervane dengesiz veya hasarlı, kart sert monte edilmiş", "Pervaneyi değiştirin, lastik halkaları ve vidaları kontrol edin"),
        ("Uçuş süresi kısa", "Batarya zayıf veya quad ağır", "Kapasiteyi artırın, kütleyi azaltın; hesaplayıcıyla karşılaştırın"),
        ("Alıcı bağlanmıyor", "UART / protokol ayarı hatalı, TX–RX çapraz değil", "Ports ve Receiver ayarlarını, bağlantıyı kontrol edin"),
        ("ESC veya motor aşırı ısınıyor", "Akım yetersiz veya pervane çok büyük", "Daha yüksek akımlı ESC, daha küçük pervane deneyin"),
    ],
    "guvenlik": [
        "LiPo bataryaları şarj ederken başında olun, güvenlik çantası kullanın; şişmiş veya hasarlı bataryayı kullanmayın.",
        "Bench testlerinde pervaneleri TAKMAYIN; pervaneli testte güvenlik gözlüğü kullanın.",
        "Bataryayı en son bağlayın, en önce çıkarın; lehim sonrası mutlaka kısa devre kontrolü yapın.",
        "Açık alanda, insan ve hayvanlardan uzak uçun; İHA kullanımı için yerel mevzuat ve izin gereklilikleri (SHGM) geçerlidir.",
    ],
    "gelistir": ["GPS ile konum tutma ve otomatik eve dönüş (GPS Rescue / ArduPilot)", "Gimbal'lı kamera ve gelişmiş görüntü aktarımı",
                 "7 inç şasi ile uzun menzil / uzun uçuş süresi", "Telemetri ve veri kaydı (blackbox) ile PID ince ayarı"],
}

# =====================================================================================================
# ÇİZGİ İZLEYEN ARABA
# =====================================================================================================
GUIDES["araba"] = {
    "zorluk": "Kolay–Orta", "sure": "4–8 saat", "butce": "Düşük",
    "hedef": "5 kanallı IR sensörlü, Arduino Nano kontrollü, PD denetimli çizgi izleyen robot araba.",
    "beceri": ["Temel elektronik", "Arduino C++", "PD kontrol ayarı"],
    "ogrenme": ["Diferansiyel sürüş", "Analog sensör kalibrasyonu", "PD denetleyici ayarı", "Pist üzerinde test ve ayar"],
    "araclar": ["Tornavida seti", "Yan keski", "Multimetre", "USB kablo + bilgisayar (Arduino IDE)", "Jumper kablo", "Çift taraflı bant / zip-tie",
                "Siyah bant (≈ 19 mm) + beyaz zemin (pist için)"],
    "malzeme": [
        ("Arduino Nano (ATmega328P)", 1, "USB kablo ile programlanır"),
        ("Nano genişletme / terminal kartı", "1 (ops.)", "Lehimsiz bağlantı için"),
        ("TT redüktörlü DC motor + tekerlek (Ø ≈ 65 mm)", 2, "Tipik 3–6 V; 7,4 V pilde PWM sınırlanır"),
        ("Destek makarası / küre tekerlek", "1–2", "Ön desteği sağlar"),
        ("Akrilik şasi + ayaklar", 1, "Sensör yuvaları ayarlanabilir"),
        ("Motor sürücü (TB6612FNG)", 1, "L298N de kullanılabilir (daha çok gerilim kaybeder)"),
        ("IR çizgi sensörü, 5 kanallı analog", 1, "TCRT5000 tabanlı modül tipik"),
        ("Batarya: 2S LiPo (7,4 V) + şarj aleti", 1, "Anahtar ile hat üzerinden bağlanır"),
        ("Açma / kapama anahtarı", 1, ""),
        ("Jumper / şerit kablo, M3 vida ve somun", 1, ""),
    ],
    "adimlar": [
        S("Şasiyi hazırla", ["chassis"],
          ["Akrilik şasinin koruyucu filmini soyun.", "Ayakları (bumper) ve montaj vidalarını yerleştirin.",
           "Sensör yuvasının konumunu ön tarafta, zemine yakın kalacak şekilde belirleyin."],
          "Şasi düz duruyor, vidalar tam oturmuş.", "20 dk"),
        S("Motorları ve aksı monte et", ["motor"],
          ["TT motorlarını braketleriyle şasinin iki yanına simetrik sabitleyin.", "Motor kablolarını motorun terminallerine lehimleyin veya konnektörle bağlayın.",
           "Aks çizgisinin iki motorda da aynı hizada olduğunu kontrol edin."],
          "İki motor birbirine paralel ve aynı hizada.", "30 dk",
          ipucu="Motor terminallerine küçük bir seramik kondansatör (100 nF) lehimlemek sensör gürültüsünü azaltır."),
        S("Tekerlekleri ve destek makaralarını tak", ["wheel", "caster"],
          ["Tekerlekleri motor millerine geçirin.", "Ön destek makarasını/küreyi şasiye vidalayın; yüksekliği tekerlek çapıyla uyumlu olsun."],
          "Robot düz zeminde dört (üç) noktada sallanmadan duruyor.", "20 dk"),
        S("Sürücü kartı ve Arduino Nano", ["board", "terminal", "nano"],
          ["Motor sürücüyü şasiye bantlayın / vidalayın.", "Arduino Nano'yu terminal kartına (veya breadboard'a) takın.",
           "Pin eşleşmesini rehberdeki Kablolama sekmesine göre yapın."],
          "Nano USB ile bilgisayara bağlanınca tanınıyor, LED yanıyor.", "40 dk",
          uyari="Nano'yu takarken yön işaretlerine ve USB ucunun konumuna dikkat edin."),
        S("Sensör dizisi ve kablolar", ["sensor", "cable"],
          ["IR dizisini şasinin önüne, zemine 3–8 mm mesafede sabitleyin.", "Sensör kablosunu (VCC, GND, OUT1–OUT5) Nano'ya bağlayın: OUT1…OUT5 → A0…A4.",
           "Kabloları şasi üzerine bantla toplayın; tekerleğe değmesin."],
          "Sensör zemine paralel; dizi çizgiye dik ve ortada.", "30 dk",
          ipucu="Sensör yüksekliği çok fazla olursa çizgi ile zemin arasındaki fark küçülür."),
        S("Güç ve kablolama kontrolü", [],
          ["Bataryayı anahtar üzerinden sürücünün VM/GND ve Nano'nun VIN/GND girişine bağlayın.", "Tüm GND hatlarının ortak olduğunu doğrulayın.",
           "Bataryayı bağlamadan önce multimetreyle + / − arasında kısa devre olmadığını kontrol edin."],
          "Kısa devre yok; kart LED'leri açılışta düzgün yanıyor.", "20 dk", vurgu=["board", "cable"],
          uyari="Pil kutuplarını ters bağlamayın; sürücü ve Nano zarar görür."),
        S("Motor testi (tekerlekler havada)", [],
          ["Rehberdeki 'motor_testi.ino' kodunu yükleyin.", "Robotu havaya kaldırıp her motorun ileri ve geri dönüşünü gözleyin.",
           "Yön ters ise kod içinde IN1/IN2 (veya IN3/IN4) pinlerini değiştirin."],
          "İki motor da 'ileri' komutunda robotu ileri götürecek yönde dönüyor.", "15 dk", vurgu=["motor", "wheel"]),
        S("Sensör kalibrasyonu", [],
          ["'cizgi_izleyen.ino' kodunu yükleyin; robotu çizginin üzerine koyup açın.", "Robot 3 sn boyunca yerinde dönerek her sensörün en açık/koyu değerini öğrenir.",
           "Seri monitörden okumaları kontrol edin; siyah çizgide okuma yükseliyorsa BLACK_IS_HIGH = true olmalı."],
          "Siyah çizgide ve beyaz zeminde normalize değerler belirgin biçimde farklı.", "20 dk", vurgu=["sensor"]),
        S("PD ayarı ve pist testi", [],
          ["Önce Kd = 0 ile Kp'yi, robot hafif salınım yapana kadar artırın.", "Salınım azalana kadar Kd'yi artırın.",
           "Hızı (baseSpeed) kademeli artırın; virajlarda çizgiyi kaçırırsa Kp/Kd'yi ve hızı birlikte ayarlayın.",
           "Sayfadaki 'Çizgi izleme (PD kontrol) simülasyonu'yla başlangıç değerlerini deneyin."],
          "Robot test pistini çizgiyi kaçırmadan, düzgün biçimde tamamlıyor.", "1–3 saat",
          vurgu=["sensor", "nano"], ipucu="Aynı pistte aynı pille test edin; pil gerilimi düştükçe davranış değişir."),
    ],
    "kablolama": {
        "boyut": (980, 380),
        "nodes": {
            "ir": N(["IR çizgi sensörü", "5 kanal · A0–A4"], 30, 40, 190, 60),
            "nano": N(["Arduino Nano", "ATmega328P"], 310, 40, 200, 74),
            "batt": N(["Batarya 2S LiPo", "7,4 V + anahtar"], 30, 230, 190, 64),
            "drv": N(["Motor sürücü", "TB6612FNG"], 310, 220, 200, 80),
            "ml": N(["Sol motor", "TT redüktörlü"], 600, 170, 180, 52),
            "mr": N(["Sağ motor", "TT redüktörlü"], 600, 255, 180, 52),
        },
        "edges": [
            E("ir", "nano", "sinyal", "5 analog + 5 V/GND"), E("batt", "nano", "guc", "VIN", off=-12),
            E("batt", "drv", "guc", "VM / GND", off=8), E("nano", "drv", "sinyal", "7 sinyal (PWM/IN/STBY)"),
            E("drv", "ml", "faz"), E("drv", "mr", "faz"),
        ],
        "pinler": [
            ("Arduino D5", "TB6612 PWMA", "PWM", "Sol motor hızı"), ("Arduino D7 / D8", "TB6612 AIN1 / AIN2", "Dijital", "Sol motor yönü"),
            ("Arduino D6", "TB6612 PWMB", "PWM", "Sağ motor hızı"), ("Arduino D9 / D10", "TB6612 BIN1 / BIN2", "Dijital", "Sağ motor yönü"),
            ("Arduino D4", "TB6612 STBY", "Dijital", "HIGH olmalı"), ("Arduino 5V", "TB6612 VCC", "5 V", "Mantık besleme"),
            ("IR OUT1…OUT5", "Arduino A0…A4", "Analog", "Soldan sağa"), ("IR VCC / GND", "Arduino 5V / GND", "Güç", ""),
            ("Batarya +", "TB6612 VM ve Nano VIN", "7,4 V", "Anahtar üzerinden"), ("Tüm GND", "Ortak", "Toprak", "Mutlaka ortak"),
            ("TB6612 AO1/AO2", "Sol motor", "Motor", ""), ("TB6612 BO1/BO2", "Sağ motor", "Motor", ""),
        ],
    },
    "kod": [
        {"baslik": "Motor testi", "dil": "cpp", "dosya": "motor_testi.ino",
         "aciklama": "Tekerlekler havadayken her motoru ileri / geri döndürür.",
         "kod": """// Motor testi: TB6612FNG + Arduino Nano
const uint8_t STBY = 4, AIN1 = 7, AIN2 = 8, PWMA = 5, BIN1 = 9, BIN2 = 10, PWMB = 6;

void motor(uint8_t in1, uint8_t in2, uint8_t pwm, int v) {
  v = constrain(v, -200, 200);          // TT motorları 7,4 V pilde korumak için sınır
  digitalWrite(in1, v > 0);
  digitalWrite(in2, v < 0);
  analogWrite(pwm, abs(v));
}

void setup() {
  const uint8_t pins[] = {STBY, AIN1, AIN2, PWMA, BIN1, BIN2, PWMB};
  for (uint8_t i = 0; i < 7; i++) pinMode(pins[i], OUTPUT);
  digitalWrite(STBY, HIGH);             // sürücüyü uyandır
}

void loop() {
  motor(AIN1, AIN2, PWMA, 120);  delay(1500); motor(AIN1, AIN2, PWMA, 0);    delay(500);   // sol ileri
  motor(AIN1, AIN2, PWMA, -120); delay(1500); motor(AIN1, AIN2, PWMA, 0);    delay(500);   // sol geri
  motor(BIN1, BIN2, PWMB, 120);  delay(1500); motor(BIN1, BIN2, PWMB, 0);    delay(500);   // sağ ileri
  motor(BIN1, BIN2, PWMB, -120); delay(1500); motor(BIN1, BIN2, PWMB, 0);    delay(1500);  // sağ geri
}
"""},
        {"baslik": "Çizgi izleyen robot (PD kontrol)", "dil": "cpp", "dosya": "cizgi_izleyen.ino",
         "aciklama": "3 sn kalibrasyon + 5 kanallı çizgi konumu + PD kontrol. Kp, Kd ve baseSpeed pistte ayarlanır.",
         "kod": """// Çizgi izleyen robot: 5 kanallı analog IR dizisi + PD kontrol
// Kart: Arduino Nano   Sürücü: TB6612FNG
const uint8_t SENS[5] = {A0, A1, A2, A3, A4};
const uint8_t STBY = 4, AIN1 = 7, AIN2 = 8, PWMA = 5, BIN1 = 9, BIN2 = 10, PWMB = 6;
const bool BLACK_IS_HIGH = true;    // siyah çizgide okuma yükseliyorsa true
const int  MAXPWM = 200;            // TT motorları 7,4 V pilde korumak için sınır
int   baseSpeed = 130;              // 0..MAXPWM
float Kp = 0.06, Kd = 0.40;         // başlangıç değerleri: pistte ayarlayın
int   minV[5], maxV[5];
int   lastError = 0;

void motor(uint8_t in1, uint8_t in2, uint8_t pwm, int v) {
  v = constrain(v, -MAXPWM, MAXPWM);
  digitalWrite(in1, v > 0);
  digitalWrite(in2, v < 0);
  analogWrite(pwm, abs(v));
}
void drive(int left, int right) {
  motor(AIN1, AIN2, PWMA, left);
  motor(BIN1, BIN2, PWMB, right);
}

void calibrate() {                  // 3 sn yerinde dön, her sensörün min/max değerini kaydet
  for (uint8_t i = 0; i < 5; i++) { minV[i] = 1023; maxV[i] = 0; }
  drive(90, -90);
  unsigned long t0 = millis();
  while (millis() - t0 < 3000) {
    for (uint8_t i = 0; i < 5; i++) {
      int v = analogRead(SENS[i]);
      if (v < minV[i]) minV[i] = v;
      if (v > maxV[i]) maxV[i] = v;
    }
  }
  drive(0, 0);
}

// Çizgi konumu: 0..4000 (2000 = ortada). Çizgi görünmüyorsa -1
int readLine() {
  long sum = 0, wsum = 0;
  for (uint8_t i = 0; i < 5; i++) {
    int range = maxV[i] - minV[i];
    int v = (range < 20) ? 0 : constrain(map(analogRead(SENS[i]), minV[i], maxV[i], 0, 1000), 0, 1000);
    if (!BLACK_IS_HIGH) v = 1000 - v;
    sum  += v;
    wsum += (long)v * i * 1000;
  }
  if (sum < 200) return -1;
  return wsum / sum;
}

void setup() {
  const uint8_t pins[] = {STBY, AIN1, AIN2, PWMA, BIN1, BIN2, PWMB};
  for (uint8_t i = 0; i < 7; i++) pinMode(pins[i], OUTPUT);
  digitalWrite(STBY, HIGH);
  delay(1000);
  calibrate();
  delay(500);
}

void loop() {
  int pos = readLine();
  int error = (pos < 0) ? (lastError > 0 ? 2000 : -2000)   // çizgi kayıp: son yöne doğru dön
                        : pos - 2000;
  float corr = Kp * error + Kd * (error - lastError);
  lastError = error;
  drive(baseSpeed + corr, baseSpeed - corr);               // çizgi sağdaysa sağa dön
}
"""},
    ],
    "test": [
        "Pil kutupları doğru; bağlamadan önce kısa devre yok.",
        "Motorlar komutla ileri/geri doğru yönde dönüyor.",
        "Sensör dizisi zemine paralel, 3–8 mm yükseklikte.",
        "Kalibrasyon sonrası siyah çizgi ve beyaz zemin değerleri belirgin biçimde ayrılıyor.",
        "Düz çizgide robot sürüklenmeden ilerliyor (gerekirse iki motor hızını eşitleyin).",
        "Test pistini (viraj + düz) çizgiyi kaçırmadan tamamlıyor.",
    ],
    "sorun": [
        ("Robot zikzak yapıyor", "Kp çok yüksek veya Kd çok düşük", "Kp'yi düşürün, Kd'yi artırın"),
        ("Virajlarda çizgiyi kaçırıyor", "Hız yüksek, sensör çok geride", "baseSpeed'i düşürün, sensörü öne alın"),
        ("Robot hiç dönmüyor veya hep aynı yöne dönüyor", "Motor yönü ters veya BLACK_IS_HIGH hatalı", "Motor pinlerini ve BLACK_IS_HIGH değerini kontrol edin"),
        ("Motorlar çalışmıyor", "STBY LOW, pil boş veya VM bağlı değil", "STBY = HIGH, pil gerilimi ve VM hattını kontrol edin"),
        ("Okumalar kararsız", "Dış ışık, sensör yüksekliği veya gevşek kablo", "Yüksekliği ayarlayın, kabloları sabitleyin, kalibrasyonu tekrarlayın"),
        ("Robot bir yana çekiyor", "İki motorun hızı eşit değil", "Hızlardan birine küçük bir ofset (trim) ekleyin"),
    ],
    "guvenlik": [
        "Pil kutuplarını ters bağlamayın; LiPo kullanıyorsanız kısa devre ve aşırı deşarja karşı dikkatli olun.",
        "Test sırasında robotu masa kenarından uzak tutun; ilk motor testlerini tekerlekler havadayken yapın.",
        "Lehim yaparken havalandırma ve havya standı kullanın.",
    ],
    "gelistir": ["Enkoder ekleyip hız kontrolü (PID)", "Bluetooth ile uzaktan ayar", "Engel algılama (ultrasonik)", "7–8 kanallı sensörle daha keskin virajlar"],
}

# =====================================================================================================
# 6 EKSENLİ ROBOT KOL
# =====================================================================================================
GUIDES["kol"] = {
    "zorluk": "Orta", "sure": "8–14 saat", "butce": "Orta",
    "hedef": "Altı servolu (6 serbestlik dereceli) masaüstü robot kol: dönen taban, omuz, dirsek, iki eksenli bilek ve tutucu.",
    "beceri": ["Mekanik montaj", "Servo kontrolü (PWM / I²C)", "Güç dağıtımı", "Kinematik"],
    "ogrenme": ["Servo ortalama ve horn takma", "Eklem sınırları ve yumuşak hareket", "PCA9685 ile çok servo kontrolü", "İleri / ters kinematik"],
    "araclar": ["Tornavida ve Allen anahtar seti", "Servo test cihazı (veya Arduino)", "Multimetre", "Ayarlanabilir güç kaynağı (5–6 V, ≥ 5 A)",
                "Vida sabitleyici (mavi)", "Zip-tie, spiral kablo kılıfı", "USB kablo + bilgisayar"],
    "malzeme": [
        ("Metal dişli servo (taban, omuz, dirsek: yüksek tork)", 3, "MG996R sınıfı tipik; tork ihtiyacını kol uzunluğuyla hesaplayın"),
        ("Servo (bilek eğilme, bilek dönme, tutucu)", 3, "MG90S / MG995 sınıfı tipik"),
        ("Alüminyum kol kiti (braketler, taban plakaları, tutucu)", 1, "Vida ve ara parçalar dahil"),
        ("PCA9685 16 kanallı servo sürücü", 1, "I²C adresi 0x40"),
        ("Arduino Uno / Nano veya ESP32", 1, "I²C: Uno/Nano A4–A5"),
        ("Güç kaynağı 5–6 V, ≥ 5 A", 1, "Servo gücü Arduino'dan ALINMAZ"),
        ("Kapasitör 1000 µF (≥ 10 V)", 1, "PCA9685 V+ girişine paralel"),
        ("Acil durdurma / ana şalter", 1, "Servo güç hattına seri"),
        ("Vantuz ayaklar, vida seti, jumper kablo", 1, ""),
    ],
    "adimlar": [
        S("Servoları 90°'ye ortala (monte etmeden)", [],
          ["Her servoyu servo test cihazıyla (veya PCA9685 + Arduino ile) orta konuma, yani 90° (≈ 1500 µs) getirin.",
           "Servo ortada iken horn'u (kolu) takın; horn'u bu konumda sabitleyin.", "Servoları etiketleyin (1: taban … 6: tutucu)."],
          "Altı servonun hepsi ortada ve horn'ları aynı referansla takılmış.", "45 dk",
          uyari="Servoyu monte ettikten sonra horn'u zorla çevirmeyin; dişliler hasar görebilir."),
        S("Taban plakası ve vantuzlar", ["base"],
          ["Alt ve üst taban plakasını ara ayaklarla birleştirin.", "Vantuzları ve (isterseniz) ağırlık plakasını takın."],
          "Taban masada sallanmıyor, plakalar paralel.", "20 dk"),
        S("Dönel tabla ve taban servosu", ["turn"],
          ["Taban servosunu (servo 1) iki plaka arasına sabitleyin.", "Tablayı servo miline bağlayın; tabla yatağında sürtünmesiz dönmeli."],
          "Tabla elle çevrildiğinde düzgün ve gıcırtısız dönüyor.", "40 dk"),
        S("Kontrol kartı ve güç", ["ctrl"],
          ["PCA9685'i ve Arduino'yu tabanın içine sabitleyin.", "1000 µF kapasitörü PCA9685 V+/GND girişine takın.",
           "Güç kaynağını ana şalter üzerinden PCA9685 V+ girişine bağlayın; GND'leri ortak yapın."],
          "Şalter kapalıyken kısa devre yok; Arduino USB ile tanınıyor.", "45 dk",
          uyari="Servo gücünü Arduino'nun 5V pininden almayın; Arduino zarar görür."),
        S("Omuz eklemi", ["shoulder"],
          ["U braketi dönen tablaya vidalayın.", "Omuz servosunu (servo 2) braketin içine yerleştirin.", "Eklemin iki yanındaki göbek (hub) vidalarını sıkın."],
          "Omuz ekseni yatay ve braketler paralel.", "40 dk"),
        S("Üst kol ve dirsek", ["upper", "elbow"],
          ["Üst kol braketini omuz servosuna bağlayın.", "Dirsek servosunu (servo 3) üst kolun ucuna yerleştirin.", "Kabloları kol boyunca spiral kılıfla yönlendirin."],
          "Üst kol serbest hareket ediyor; kablolar eklemde sıkışmıyor.", "45 dk"),
        S("Ön kol ve bilek", ["forearm", "wrist"],
          ["Ön kol braketini dirseğe bağlayın.", "Bilek eğilme servosunu (servo 4), ardından bilek dönme servosunu (servo 5) takın."],
          "Bilek her iki eksende de sürtünmesiz hareket ediyor.", "45 dk"),
        S("Tutucu", ["gripper"],
          ["Tutucu servosunu (servo 6) tutucu gövdesine bağlayın.", "Parmak mekanizmasını takın; parmaklar tam kapalı ve tam açıkken çarpmamalı."],
          "Tutucu elle açılıp kapanırken engel yok; parmak uçları hizalı.", "40 dk"),
        S("Kablo düzeni ve güç testi", [],
          ["Servoları PCA9685 kanallarına sırayla takın (servo 1 → kanal 0 … servo 6 → kanal 5); sinyal kablosu (sarı) yukarı bakmalı.",
           "Güç kaynağını önce 5 V, düşük akım limitiyle açın; servoların ani sıçramasını gözleyin.", "Kablo demetlerini eklemlerde gevşek bırakıp bağlarla toplayın."],
          "Güç açıldığında kol aniden savrulmuyor; akım beklenen aralıkta.", "40 dk", vurgu=["ctrl"],
          uyari="Kol hareket ederken parmaklarınızı eklemlerden uzak tutun (sıkışma tehlikesi)."),
        S("Kalibrasyon ve ilk hareket", [],
          ["'robot_kol.ino' kodunu yükleyin; her eklem için LO/HI sınırlarını kolun çarpmayacağı değerlere ayarlayın.",
           "SERVOMIN / SERVOMAX değerlerini servonuza göre kalibre edin.", "Önce yavaş (≥ 1500 ms) hareketlerle deneyin; ardından ters kinematik ile hedef noktalara gidin."],
          "Kol tüm eklem sınırlarında çarpışma ve zorlanma sesi olmadan hareket ediyor; ev (home) konumuna dönüyor.", "1–2 saat",
          ipucu="Ters kinematik için sayfadaki 'Ters kinematik' sekmesi kol uzunluklarını girerek açıları verir."),
    ],
    "kablolama": {
        "boyut": (980, 440),
        "nodes": {
            "ard": N(["Arduino Uno/Nano", "I²C: A4 / A5"], 30, 40, 200, 74),
            "psu": N(["Güç kaynağı", "5–6 V · ≥ 5 A"], 30, 250, 200, 74),
            "pca": N(["PCA9685", "16 kanal servo sürücü", "I²C 0x40"], 330, 150, 220, 86),
            "s1": N(["Servo 1 · Taban", "Kanal 0"], 740, 20, 200, 48), "s2": N(["Servo 2 · Omuz", "Kanal 1"], 740, 78, 200, 48),
            "s3": N(["Servo 3 · Dirsek", "Kanal 2"], 740, 136, 200, 48), "s4": N(["Servo 4 · Bilek eğ.", "Kanal 3"], 740, 194, 200, 48),
            "s5": N(["Servo 5 · Bilek dön.", "Kanal 4"], 740, 252, 200, 48), "s6": N(["Servo 6 · Tutucu", "Kanal 5"], 740, 310, 200, 48),
        },
        "edges": [
            E("ard", "pca", "i2c", "SDA/SCL + 5 V/GND"), E("psu", "pca", "guc", "V+ (servo gücü)", off=14, mid=20),
            E("psu", "ard", "guc", "ortak GND"),
            E("pca", "s1", "faz", "PWM kanalları", mid=40), E("pca", "s2", "faz", mid=40), E("pca", "s3", "faz", mid=40),
            E("pca", "s4", "faz", mid=40), E("pca", "s5", "faz", mid=40), E("pca", "s6", "faz", mid=40),
        ],
        "pinler": [
            ("Arduino A4 (SDA)", "PCA9685 SDA", "I²C", "ESP32'de GPIO21"), ("Arduino A5 (SCL)", "PCA9685 SCL", "I²C", "ESP32'de GPIO22"),
            ("Arduino 5V", "PCA9685 VCC", "Mantık besleme", "Yalnızca mantık; servo gücü değil"),
            ("Güç kaynağı +", "PCA9685 V+", "5–6 V", "Şalter + 1000 µF kapasitör üzerinden"),
            ("Güç kaynağı −", "Arduino GND + PCA9685 GND", "Toprak", "GND'ler ortak olmalı"),
            ("Servo 1…6", "PCA9685 kanal 0…5", "3 pin", "Sarı sinyal, kırmızı +, kahverengi −"),
        ],
    },
    "kod": [
        {"baslik": "Robot kol: PCA9685 ile yumuşak hareket", "dil": "cpp", "dosya": "robot_kol.ino",
         "aciklama": "Eklem sınırları, açı → darbe dönüşümü ve S-eğrisi ile yumuşak hareket. LO/HI ve SERVOMIN/MAX değerlerini kalibre edin.",
         "kod": """// 6 eksenli robot kol: Arduino + PCA9685 (Adafruit_PWMServoDriver kütüphanesi)
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm(0x40);
const uint16_t SERVOMIN = 150, SERVOMAX = 600;   // 50 Hz'de darbe sınırları: servonuza göre kalibre edin
const uint8_t  N = 6;
// Eklem sınırları (derece): taban, omuz, dirsek, bilek eğilme, bilek dönme, tutucu
const int LO[N] = {  0,  20,  10,  10,   0,  20};
const int HI[N] = {180, 160, 170, 170, 180, 110};
float cur[N] = {90, 90, 90, 90, 90, 90};

uint16_t pulse(int angle) { return map(angle, 0, 180, SERVOMIN, SERVOMAX); }

void setAngle(uint8_t ch, float a) {
  a = constrain(a, LO[ch], HI[ch]);
  pwm.setPWM(ch, 0, pulse((int)a));
  cur[ch] = a;
}

// Hedef açılara 'ms' süresinde S-eğrisiyle (yumuşak başla / yumuşak bitir) git
void moveTo(const float target[N], uint16_t ms) {
  float start[N];
  for (uint8_t i = 0; i < N; i++) start[i] = cur[i];
  const uint16_t steps = ms / 20;
  for (uint16_t s = 1; s <= steps; s++) {
    float k = (float)s / steps;
    k = k * k * (3 - 2 * k);
    for (uint8_t i = 0; i < N; i++) setAngle(i, start[i] + (target[i] - start[i]) * k);
    delay(20);
  }
}

void setup() {
  pwm.begin();
  pwm.setPWMFreq(50);
  delay(10);
  for (uint8_t i = 0; i < N; i++) setAngle(i, 90);   // ev konumu
  delay(800);
}

void loop() {
  const float a[N] = { 90,  60, 120,  90, 90,  40};  // uzan, tutucuyu kapat
  const float b[N] = {135, 100,  80, 110, 90, 100};  // yana dön, tutucuyu aç
  moveTo(a, 1500);
  delay(300);
  moveTo(b, 1500);
  delay(300);
}
"""},
        {"baslik": "Ters kinematik (3R düzlemsel)", "dil": "python", "dosya": "ters_kinematik.py", "fn": "kinematics.ik_planar_3r",
         "aciklama": "Uç nokta (x, z) ve uç yönelimi φ verildiğinde omuz, dirsek ve bilek açılarını hesaplar. Sonucu LO/HI sınırlarına göre kontrol edin."},
    ],
    "test": [
        "Servolar monte edilmeden ortalandı; horn'lar ortada takılı.",
        "Güç ve GND bağlantıları doğru; servo gücü Arduino'dan alınmıyor.",
        "Her eklemde LO/HI sınırları çarpışmayı önleyecek şekilde ayarlı.",
        "Ev (home) konumuna dönüşte kol zorlanmıyor.",
        "Tutucu parmakları tam açık/kapalı konumda çarpmıyor.",
        "Kol yavaş hareketlerde titremiyor; kablolar eklemlerde sıkışmıyor.",
    ],
    "sorun": [
        ("Servo titriyor / zonklıyor", "Güç yetersiz veya GND ortak değil", "Güç kaynağını ve kapasitörü, ortak GND'yi kontrol edin"),
        ("Arduino sürekli resetleniyor", "Servo gücü Arduino hattından alınıyor", "Servo gücünü ayrı besleyin"),
        ("Eklem sınıra çarpıp ses çıkarıyor", "LO/HI sınırları geniş", "Sınırları daraltın, SERVOMIN/MAX'i kalibre edin"),
        ("Servo yön tersine gidiyor", "Servo montaj yönü / horn ofseti", "Açıyı 180−a ile çevirin veya horn'u yeniden takın"),
        ("PCA9685 bulunamıyor", "I²C bağlantısı veya adres hatalı", "SDA/SCL'yi ve adresi (0x40) kontrol edin; I²C tarayıcıyla deneyin"),
        ("Kol omuzda yavaş / zayıf", "Tork yetersiz veya kol çok uzun", "Daha güçlü servo, karşı ağırlık veya daha kısa kol"),
    ],
    "guvenlik": [
        "Eklemler arasında parmak sıkışabilir; kol hareket ederken elinizi yaklaştırmayın.",
        "Servoların tepe akımı yüksektir (tipik 2–3 A / servo); uygun kablo ve güç kaynağı kullanın.",
        "Kablolamayı değiştirirken güç kaynağını kapatın; acil durdurma anahtarını erişilebilir tutun.",
    ],
    "gelistir": ["Ters kinematikle nokta-nokta hareket", "Kamera ve renk / nesne tanıma ile otomatik al-bırak", "Akım ölçümüyle tutma kuvveti geri bildirimi", "Joystick veya telefon ile uzaktan kontrol"],
}

# =====================================================================================================
# ALTI BACAKLI ROBOT
# =====================================================================================================
GUIDES["hexapod"] = {
    "zorluk": "Zor", "sure": "20–35 saat (baskı dahil)", "butce": "Orta–Yüksek",
    "hedef": "12 servolu (bacak başına kalça + diz) tripod yürüyüşlü, ESP32 kontrollü altı bacaklı robot.",
    "beceri": ["3B baskı", "Servo montajı", "I²C / PCA9685", "Yürüyüş algoritması"],
    "ogrenme": ["Tripod / ripple / wave yürüyüşleri", "Servo ofset kalibrasyonu", "Güç dağıtımı (UBEC)", "Tork ve ağırlık hesabı"],
    "araclar": ["3B yazıcı (PLA+ / PETG)", "Tornavida ve Allen anahtar seti", "Servo test cihazı", "Multimetre", "Havya", "Zip-tie, spiral kablo kılıfı", "USB kablo + bilgisayar"],
    "malzeme": [
        ("Servo (bacak başına 2)", 12, "Kütleye göre seçin: dizde tork ≥ 2 × (m/3) × L"),
        ("3B baskılı gövde kabuğu, braketler ve pençeler", "1 set", "PETG / PLA+, ≥ %30 dolgu; pençe için daha yüksek dolgu"),
        ("PCA9685 16 kanallı servo sürücü", 1, "12 servo için yeterli"),
        ("ESP32 geliştirme kartı", 1, "Wi-Fi / Bluetooth ile kontrol; anten"),
        ("LiPo 2S 7,4 V (1500–2200 mAh)", 1, "Konnektör + şarj aleti"),
        ("UBEC / buck dönüştürücü 6 V, ≥ 10 A", 1, "Servo gücü için; tepe akımı hesaplayın"),
        ("Ana şalter + sigorta", 1, ""),
        ("M2 / M3 vida, somun, rulman (ops.)", "1 set", "Bacak eklemleri için"),
        ("Kablo kılıfı, zip-tie, jumper", 1, ""),
    ],
    "adimlar": [
        S("3B baskı ve servo ortalama", [],
          ["Parçaları basın; destekleri temizleyin, delikleri matkap/raybayla ölçüye getirin.",
           "Tüm servoları servo testiyle 90°'ye ortalayın ve etiketleyin (R1…R3, L1…L3: hip ve knee).",
           "Servo tork kontrolü: dizde gereken tork ≥ 2 × (kütle/3) × bacak uzunluğu."],
          "Parçalar ölçüye uygun; servolar ortalanmış ve etiketli.", "6–12 saat (baskı)",
          ipucu="Örnek: 1,5 kg robot, 10 cm bacak → 2 × 0,5 kg × 10 cm = 10 kg·cm tork gerekir."),
        S("Gövde kabuğu ve taban", ["shell"],
          ["Kabuk ile taban plakasını birleştirin; kalça servolarının oturacağı yuvaları kontrol edin.", "Ön yüzdeki havalandırma ve port deliklerini temizleyin."],
          "Kabuk eğilmeden, kapaklar tam oturuyor.", "40 dk"),
        S("Elektronik yerleşimi", ["elec"],
          ["ESP32, PCA9685, UBEC ve bataryayı gövde içine yerleştirip sabitleyin.", "Bataryayı alçakta ve ortada tutun (ağırlık merkezi)."],
          "Hiçbir parça gevşek değil; batarya bağlantıları erişilebilir.", "40 dk"),
        S("Anten", ["antenna"],
          ["Kablosuz modülün (ESP32) anteni kabuktan dışarı çıkacak şekilde yönlendirin.", "Anten kablosunu sıkıştırmadan sabitleyin."],
          "Anten kablosu sıkışmıyor; metal parçalara yaslanmıyor.", "15 dk"),
        S("Kalça servoları", ["hip"],
          ["Altı kalça servosunu (R1…L3) gövdenin iki yanındaki yuvalara 90° ortalı olarak vidalayın.", "Servo horn'unu bacağın DIŞARI baktığı konumda takın."],
          "Altı bacak da gövdeye dik (90° konumda) ve simetrik.", "1 saat",
          uyari="Horn'u takarken servo mili 90°'de kalmalı; aksi halde ofset kalibrasyonu zorlaşır."),
        S("Bacak braketleri", ["bracket"],
          ["Her bacak için kalça horn'una dikey braketi vidalayın.", "Braket içine diz servosunu yerleştirin (kablo yönü gövdeye doğru)."],
          "Altı braket da aynı yükseklikte ve dikey.", "1 saat"),
        S("Diz servoları", ["knee"],
          ["Diz servolarını braketlere sabitleyin; diz horn'unu 90° konumunda, pençe aşağı doğru bakacak şekilde takın.", "Hareket aralığında (± 40°) braket veya gövdeyle çarpışma olmadığını elle deneyin."],
          "Diz eklemleri sürtünmesiz; çarpışma yok.", "1 saat"),
        S("Pençe bacaklar", ["claw"],
          ["Pençeleri diz horn'larına sabitleyin.", "Pençe uçlarının yere aynı yükseklikte bastığını kontrol edin (düz zemin)."],
          "Robot ayaktayken altı pençe de zemine eşit basıyor.", "40 dk"),
        S("Kablolama", ["wire"],
          ["Servoları PCA9685'e sırayla takın: kalça kanalları 0,2,4,6,8,10; diz kanalları 1,3,5,7,9,11.", "UBEC çıkışını PCA9685 V+ girişine, ESP32'yi UBEC 5 V çıkışına (veya USB) bağlayın.",
           "Kabloları bacak eklemlerinde gevşek bırakıp spiral kılıf ve bağlarla toplayın."],
          "Güç açıldığında 12 servo da kısa süre ortaya gidiyor; ısınan kablo veya parça yok.", "1–1,5 saat",
          uyari="12 servonun tepe akımı yüksektir; yetersiz UBEC, gerilim düşmesine ve resetlere yol açar."),
        S("Servo ofset kalibrasyonu (ayakta duruş)", [],
          ["'hexapod.ino' kodunu yükleyin; legPose(i,0,0) ile tüm bacakları nötr konuma getirin.", "hipOff[] ve kneeOff[] değerleriyle her bacağı aynı yükseklik ve açıya ayarlayın.",
           "SIDE[] işaretleri ile sol/sağ bacakların yönünü, gerekirse diz için ters çevirmeyi doğrulayın."],
          "Robot ayakta düz duruyor; altı bacak simetrik ve gövde yere paralel.", "1–2 saat", vurgu=["hip", "knee"]),
        S("Tripod yürüyüş", [],
          ["Kodda PHASE[] değerleri tripodu (0, 0,5, 0, 0,5, 0, 0,5) verir; BETA = 0,5.", "STRIDE_DEG ve LIFT_DEG'i küçük değerlerle başlatıp artırın; FREQ'i kademeli yükseltin.",
           "Yürüyüş yönü ters ise hip işaretini (SIDE) tersine çevirin; sayfadaki 'Yürüyüş analizi' ile tipik değerleri karşılaştırın."],
          "Robot üç bacak havadayken devrilmeden, düz bir çizgide yürüyor.", "2–4 saat", vurgu=["claw", "hip", "knee"],
          ipucu="Önce robotu havaya kaldırıp bacak hareketini gözleyin, sonra yere indirin."),
    ],
    "kablolama": {
        "boyut": (980, 380),
        "nodes": {
            "phone": N(["Telefon / kumanda", "Wi-Fi · Bluetooth"], 30, 40, 190, 60),
            "esp": N(["ESP32", "I²C: GPIO21/22"], 290, 40, 200, 74),
            "lipo": N(["LiPo 2S", "7,4 V · 1500–2200 mAh"], 30, 250, 190, 64),
            "ubec": N(["UBEC / buck", "6 V · ≥ 10 A"], 290, 250, 200, 64),
            "pca": N(["PCA9685", "16 kanal · I²C 0x40", "V+ = 6 V"], 570, 150, 200, 86),
            "hips": N(["6 × kalça", "servo", "Kanal 0,2,4…10"], 810, 40, 150, 74),
            "knees": N(["6 × diz", "servo", "Kanal 1,3,5…11"], 810, 230, 150, 74),
        },
        "edges": [
            E("phone", "esp", "kablosuz", "Wi-Fi / BT"), E("esp", "pca", "i2c", "SDA / SCL"),
            E("lipo", "ubec", "guc", "7,4 V"), E("ubec", "pca", "guc", "V+ 6 V", off=14),
            E("ubec", "esp", "guc", "5 V"), E("pca", "hips", "faz"), E("pca", "knees", "faz"),
        ],
        "pinler": [
            ("ESP32 GPIO21 (SDA)", "PCA9685 SDA", "I²C", "Varsayılan I²C pinleri"), ("ESP32 GPIO22 (SCL)", "PCA9685 SCL", "I²C", ""),
            ("ESP32 3V3", "PCA9685 VCC", "Mantık besleme", "Servo gücü değil"), ("UBEC 6 V", "PCA9685 V+", "Servo gücü", "Sigorta + şalter üzerinden"),
            ("UBEC 5 V / USB", "ESP32 5V", "Besleme", "Ortak GND"), ("Kalça servoları", "PCA9685 kanal 0,2,4,6,8,10", "3 pin", "R1,R2,R3,L1,L2,L3"),
            ("Diz servoları", "PCA9685 kanal 1,3,5,7,9,11", "3 pin", "R1,R2,R3,L1,L2,L3"),
        ],
    },
    "kod": [
        {"baslik": "Hexapod: PCA9685 ile tripod yürüyüş", "dil": "cpp", "dosya": "hexapod.ino",
         "aciklama": "Bacak sırası: R1, R2, R3, L1, L2, L3. Faz ve ayak yörüngesi, sayfadaki yürüyüş analiziyle aynı modeldir. Ofset ve yön işaretlerini kalibre edin.",
         "kod": """// Altı bacaklı robot: ESP32 / Arduino + PCA9685, tripod yürüyüş
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm(0x40);
const uint16_t SMIN = 150, SMAX = 600;            // servonuza göre kalibre edin

// Bacak sırası: R1, R2, R3, L1, L2, L3 (sağ ön/orta/arka, sol ön/orta/arka)
const uint8_t HIP[6]  = {0, 2, 4, 6, 8, 10};
const uint8_t KNEE[6] = {1, 3, 5, 7, 9, 11};
const int8_t  SIDE[6] = {+1, +1, +1, -1, -1, -1};     // sol bacaklarda hip yönü ters
int hipOff[6]  = {0, 0, 0, 0, 0, 0};                   // kalibrasyon ofsetleri (derece)
int kneeOff[6] = {0, 0, 0, 0, 0, 0};

const float PHASE[6] = {0, 0.5, 0, 0.5, 0, 0.5};       // tripod fazları
const float BETA = 0.5;                                // destek fazı oranı
const float STRIDE_DEG = 20, LIFT_DEG = 25;            // adım ve kaldırma genliği (derece)
const float FREQ = 1.0;                                // döngü frekansı (Hz)

void setServo(uint8_t ch, float deg) {
  deg = constrain(deg, 0, 180);
  pwm.setPWM(ch, 0, map((long)deg, 0, 180, SMIN, SMAX));
}

// swingDeg: kalça ileri(+)/geri(-), liftDeg: diz kaldırma (yön ters ise işareti değiştirin)
void legPose(uint8_t i, float swingDeg, float liftDeg) {
  setServo(HIP[i],  90 + hipOff[i]  + SIDE[i] * swingDeg);
  setServo(KNEE[i], 90 + kneeOff[i] + liftDeg);
}

void gait(float tau) {                                 // tau: 0..1 döngü fazı
  for (uint8_t i = 0; i < 6; i++) {
    float c = fmod(tau - PHASE[i] + 1.0, 1.0);
    float x, z;
    if (c < BETA) {                                    // destek: ayak yerde, gövdeye göre geri
      x = 0.5 - c / BETA;
      z = 0;
    } else {                                           // salınım: ayak havada, öne taşınır
      float s = (c - BETA) / (1.0 - BETA);
      x = -0.5 + (0.5 - 0.5 * cos(PI * s));
      z = sin(PI * s);
    }
    legPose(i, x * STRIDE_DEG, z * LIFT_DEG);
  }
}

void setup() {
  Wire.begin();
  pwm.begin();
  pwm.setPWMFreq(50);
  for (uint8_t i = 0; i < 6; i++) legPose(i, 0, 0);   // nötr duruş
  delay(1500);
}

void loop() {
  static uint32_t t0 = millis();
  float tau = fmod((millis() - t0) / 1000.0 * FREQ, 1.0);
  gait(tau);
  delay(10);
}
"""},
        {"baslik": "Yürüyüş çizelgesi ve ayak yörüngesi (Python)", "dil": "python", "dosya": "gait.py", "fn": "kinematics.foot_trajectory",
         "aciklama": "Kodda kullanılan ayak yörüngesinin Python karşılığı; stride/lift/β değerlerini sayfadaki analizle deneyebilirsiniz."},
    ],
    "test": [
        "Altı kalça ve altı diz servosu ortalanmış, etiketli.",
        "Güç açıldığında 12 servo da kısa süre ortaya gidiyor, gerilim düşmesi yok.",
        "Nötr duruşta altı pençe de zemine eşit basıyor.",
        "Sol / sağ bacakların hareket yönü simetrik.",
        "Robot havada iken tripod hareketi düzgün; bacaklar birbirine çarpmıyor.",
        "Yerde düz çizgide yürüyor, devrilmiyor; servolar aşırı ısınmıyor.",
    ],
    "sorun": [
        ("Robot bir yana çarpık duruyor", "Servo ofsetleri kalibre edilmemiş", "hipOff/kneeOff değerlerini ayarlayın"),
        ("Bacak ters yönde hareket ediyor", "SIDE veya diz işareti hatalı", "SIDE[i] ve diz liftDeg işaretini çevirin"),
        ("Servolar resetliyor / titriyor", "UBEC akımı yetersiz", "Daha yüksek akımlı UBEC, kısa ve kalın kablo, kapasitör"),
        ("Robot yürümeden yerinde sallanıyor", "Adım / frekans çok küçük, zemin kaygan", "STRIDE_DEG artırın, pençelere lastik / zımpara ekleyin"),
        ("Diz servosu yük altında yetersiz", "Tork düşük veya bacak çok uzun", "Daha güçlü servo, kütleyi azaltın"),
        ("Bacaklar birbirine çarpıyor", "Adım genliği büyük, kalça konumları yakın", "STRIDE_DEG azaltın, faz düzenini kontrol edin"),
    ],
    "guvenlik": [
        "Servoların toplam tepe akımı yüksektir; sigorta ve kalın kablo kullanın, LiPo kurallarına uyun.",
        "Bacaklar hareket ederken parmaklarınızı eklemlerden uzak tutun.",
        "İlk denemeleri robot havada (bacaklar serbest) yapın; sonra yere indirin.",
    ],
    "gelistir": ["Ripple ve wave yürüyüşlerini deneyin (sayfadaki gait analizi)", "Bacak başına 3. servo (3 eksenli bacak) ve ters kinematik",
                 "IMU ile gövde dengeleme", "Mesafe sensörüyle engelden kaçınma"],
}

# =====================================================================================================
# PALETLİ TANK ROBOT
# =====================================================================================================
GUIDES["tank"] = {
    "zorluk": "Kolay–Orta", "sure": "6–10 saat", "butce": "Düşük–Orta",
    "hedef": "İki DC motorlu, kayma yönlendirmeli (skid steer) paletli robot; Bluetooth ile sürülür, isteğe bağlı kamera kulesi taşır.",
    "beceri": ["Mekanik montaj", "Motor sürücü kullanımı", "Arduino C++", "Güç dağıtımı"],
    "ogrenme": ["Palet gerginliği ve tahrik sistemi", "Skid steer karıştırma (gaz + dönüş)", "Tork ve eğim hesabı", "Bluetooth ile kontrol"],
    "araclar": ["Tornavida / Allen anahtar seti", "Yan keski", "Multimetre", "Havya (motor kablosu için)", "USB kablo + bilgisayar", "Zip-tie, çift taraflı bant"],
    "malzeme": [
        ("Paletli şasi kiti (palet bandı, tahrik dişlisi, avara, yol tekerlekleri)", 1, "Kiti seçerken motor ve dişli kutusunun dahil olduğunu kontrol edin"),
        ("DC redüktörlü motor", 2, "Kitle birlikte gelir; 6–12 V tipik"),
        ("Arduino Uno / Nano veya ESP32", 1, "PWM çıkışlı pinler gerekir"),
        ("Motor sürücü (L298N veya TB6612FNG)", 1, "L298N ≈ 2 V gerilim düşürür"),
        ("Batarya: 2S LiPo (7,4 V) veya 6 × AA", 1, "Anahtar ile hatta bağlanır"),
        ("HC-05 / HC-06 Bluetooth", "1 (ops.)", "Telefondan komut için"),
        ("HC-SR04 ultrasonik sensör", "1 (ops.)", "Engel algılama"),
        ("Mini servo + kamera (kule)", "1 (ops.)", "Kamera kulesi için"),
        ("Jumper kablo, vida, anahtar", 1, ""),
    ],
    "adimlar": [
        S("Gövdeyi hazırla", ["hull"],
          ["Şasi plakalarını ve yan duvarları birleştirin.", "Elektronik için üst plaka ve montaj deliklerini hazırlayın.", "Ön tarafa gerekirse far / sensör yuvaları açın."],
          "Gövde düz ve burulmuyor; yan duvarlar paralel.", "30 dk"),
        S("Motorlar ve dişli kutuları", ["motors"],
          ["İki motoru gövdenin arka bölümüne, aynı hizada sabitleyin.", "Motor milini tahrik dişlisine bağlamak için mil yuvasını ve dişli kutusunu kontrol edin.",
           "Motor kablolarını uzunca bırakıp ucuna konnektör takın."],
          "İki motor simetrik ve milleri aynı eksende.", "40 dk"),
        S("Tahrik dişlisi, avara ve yol tekerlekleri", ["sprocket", "wheels"],
          ["Tahrik dişlisini motor miline sabitleyin (vida / pim).", "Önde avara tekerleği, altta yol tekerleklerini takın; hepsinin serbest döndüğünü kontrol edin."],
          "Tüm tekerlekler sürtünmesiz dönüyor; dişli milde kaymıyor.", "40 dk"),
        S("Palet bantlarını tak", ["track"],
          ["Palet bandını tahrik dişlisi ve avara üzerinden geçirin.", "Avarayı kaydırarak paleti gerin: banda parmakla bastırınca ≈ 5 mm esnemeli.",
           "Dişlinin palet dişlerine tam kavradığını kontrol edin."],
          "Palet gergin ama aşırı sıkı değil; elle çevirince atlamıyor.", "30 dk",
          uyari="Aşırı gergin palet motor ve dişli kutusunu zorlar; gevşek palet dişliden atlar."),
        S("Kontrol kartı ve batarya", ["ctrl"],
          ["Motor sürücüyü, Arduino'yu ve bataryayı gövde içine alçak ve ortada sabitleyin.", "Batarya, sürücü ve Arduino GND'lerini ortak yapın.",
           "L298N kullanıyorsanız ENA/ENB jumper'larını çıkarıp PWM pinlerine bağlayın."],
          "Hiçbir parça gevşek değil; kablolar paletlere veya tekerleklere değmiyor.", "45 dk",
          uyari="Pil kutuplarını ters bağlamayın; bağlantıdan önce kısa devre kontrolü yapın."),
        S("Kamera kulesi (opsiyonel)", ["turret"],
          ["Mini servoyu üst plakaya, kule yatağına bağlayın.", "Kamerayı veya sensörü kuleye sabitleyin; kabloları dönüşte sıkışmayacak şekilde bırakın."],
          "Kule serbest dönüyor; kablolar gerilmiyor.", "30 dk"),
        S("Kablolama kontrolü", [],
          ["Pin eşleşmesini Kablolama sekmesine göre yapın.", "Multimetreyle bataryanın + / − arasında kısa devre olmadığını doğrulayın.", "Anahtarı açıp sürücü ve Arduino LED'lerini gözleyin."],
          "Kısa devre yok; LED'ler normal yanıyor.", "20 dk", vurgu=["ctrl", "motors"]),
        S("Motor yön testi", [],
          ["Robotu paletler havada olacak şekilde destekleyin.", "'tank.ino' kodunu yükleyin; seri monitörden veya Bluetooth'tan F, B, L, R, S komutlarını gönderin.",
           "Palet 'ileri'de ters dönüyorsa motorun IN pinlerini değiştirin."],
          "F komutunda iki palet de robotu ileri götürüyor; L/R komutlarında doğru yöne dönüyor.", "20 dk", vurgu=["track", "sprocket"]),
        S("Sürüş ayarı ve saha testi", [],
          ["speedVal değerini zemine ve kütleye göre ayarlayın.", "Gerekirse bir paletin hızını küçük ofsetle dengeleyin (düz giderken yana çekiyorsa).",
           "Sayfadaki 'Kuvvet ve tork analizi' ile eğim ve yerinde dönüş için motor yeterliliğini kontrol edin."],
          "Robot düz giderken yana kaymıyor, yerinde dönebiliyor; eğimde paletler atlamıyor.", "1 saat", vurgu=["hull"]),
    ],
    "kablolama": {
        "boyut": (980, 420),
        "nodes": {
            "bt": N(["HC-05 Bluetooth", "RX / TX"], 30, 40, 190, 60),
            "uno": N(["Arduino Uno/Nano", "PWM: D5, D6"], 310, 40, 200, 74),
            "batt": N(["Batarya 2S LiPo", "7,4 V + anahtar"], 30, 230, 190, 64),
            "drv": N(["Motor sürücü", "L298N"], 310, 230, 200, 80),
            "us": N(["HC-SR04 (ops.)", "Trig / Echo"], 600, 30, 200, 48),
            "sv": N(["Kule servosu", "(opsiyonel)"], 600, 92, 200, 48),
            "ml": N(["Sol palet motoru", "DC redüktörlü"], 600, 230, 200, 48),
            "mr": N(["Sağ palet motoru", "DC redüktörlü"], 600, 292, 200, 48),
        },
        "edges": [
            E("bt", "uno", "i2c", "RX / TX"), E("uno", "drv", "sinyal", "ENA,ENB,IN1–IN4", off=-14),
            E("drv", "uno", "guc", "5 V", off=14), E("batt", "drv", "guc", "12V / GND"),
            E("uno", "us", "sinyal"), E("uno", "sv", "sinyal"),
            E("drv", "ml", "faz"), E("drv", "mr", "faz"),
        ],
        "pinler": [
            ("Arduino D5", "L298N ENA", "PWM", "Sol palet hızı (jumper çıkarılmış)"), ("Arduino D7 / D8", "L298N IN1 / IN2", "Dijital", "Sol yön"),
            ("Arduino D6", "L298N ENB", "PWM", "Sağ palet hızı"), ("Arduino D9 / D10", "L298N IN3 / IN4", "Dijital", "Sağ yön"),
            ("L298N 5V çıkış", "Arduino 5V / VIN", "Besleme", "Batarya ≤ 12 V iken yerleşik regülatör"), ("Batarya +", "L298N 12V girişi", "7,4 V", "Anahtar üzerinden"),
            ("Tüm GND", "Ortak", "Toprak", "Mutlaka ortak"), ("HC-05 TX / RX", "Arduino RX / TX", "UART", "Çapraz; yükleme sırasında çıkarın"),
            ("L298N OUT1/OUT2", "Sol palet motoru", "Motor", ""), ("L298N OUT3/OUT4", "Sağ palet motoru", "Motor", ""),
        ],
    },
    "kod": [
        {"baslik": "Paletli robot: skid steer sürüş", "dil": "cpp", "dosya": "tank.ino",
         "aciklama": "Seri / Bluetooth komutlarıyla sürüş: F ileri, B geri, L sola dön, R sağa dön, S dur, + / − hız. ENA/ENB PWM pinleri olmalı.",
         "kod": """// Paletli robot: L298N ile kayma yönlendirmeli (skid steer) sürüş
const uint8_t ENA = 5, IN1 = 7, IN2 = 8;     // sol palet
const uint8_t ENB = 6, IN3 = 9, IN4 = 10;    // sağ palet
int speedVal = 180;                          // 0..255

void motor(uint8_t en, uint8_t a, uint8_t b, int v) {
  v = constrain(v, -255, 255);
  digitalWrite(a, v > 0);
  digitalWrite(b, v < 0);
  analogWrite(en, abs(v));
}

// throttle: ileri(+) / geri(-), turn: sağa(+) / sola(-)
void drive(int throttle, int turn) {
  motor(ENA, IN1, IN2, throttle + turn);     // sol palet
  motor(ENB, IN3, IN4, throttle - turn);     // sağ palet
}

void setup() {
  const uint8_t pins[] = {ENA, IN1, IN2, ENB, IN3, IN4};
  for (uint8_t i = 0; i < 6; i++) pinMode(pins[i], OUTPUT);
  Serial.begin(9600);                        // HC-05 / USB seri
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    switch (c) {
      case 'F': drive( speedVal, 0); break;
      case 'B': drive(-speedVal, 0); break;
      case 'L': drive(0, -speedVal); break;   // yerinde sola dön
      case 'R': drive(0,  speedVal); break;   // yerinde sağa dön
      case 'S': drive(0, 0); break;
      case '+': speedVal = min(255, speedVal + 20); break;
      case '-': speedVal = max(60,  speedVal - 20); break;
    }
  }
}
"""},
        {"baslik": "Eğim ve yerinde dönüş için tork hesabı", "dil": "python", "dosya": "tork_hesabi.py", "fn": "physics.pivot_turn_track_force",
         "aciklama": "Yerinde dönüşte her paletin üretmesi gereken kuvvet (N). Dişli yarıçapıyla çarparak tork bulunur; sayfadaki analizle birlikte kullanın."},
    ],
    "test": [
        "Palet gerginliği doğru; dişliden atlamıyor.",
        "F/B komutlarında iki palet de aynı yönde, L/R'de zıt yönde dönüyor.",
        "Kısa devre yok; pil gerilimi yeterli.",
        "Düz giderken yana çekmiyor (gerekirse ofset eklendi).",
        "Yerinde dönüşte paletler atlamıyor.",
        "Beklenen eğimde (analiz sayfasındaki değer) tırmanabiliyor.",
    ],
    "sorun": [
        ("Palet dişliden atlıyor", "Gevşek palet veya hizasız tekerlek", "Avarayı kaydırıp paleti gerin, hizayı kontrol edin"),
        ("Robot düz gitmiyor", "İki motor hızı eşit değil", "Bir tarafa küçük hız ofseti ekleyin"),
        ("Motorlar yavaş / zayıf", "L298N gerilim düşümü, pil zayıf", "Pili şarj edin, TB6612FNG deneyin"),
        ("Arduino sürekli resetleniyor", "Motor gürültüsü / besleme düşümü", "Kapasitör ekleyin, Arduino'yu ayrı beslemeyi deneyin"),
        ("Yerinde dönemiyor", "Palet temas alanı büyük, tork yetersiz", "Daha güçlü motor / daha yüksek redüksiyon (analiz sayfası)"),
        ("Bluetooth komutu almıyor", "TX / RX ters veya baud hızı farklı", "Bağlantıyı çapraz yapın, 9600 baud kontrol edin"),
    ],
    "guvenlik": [
        "Pil kutuplarını ters bağlamayın; LiPo kullanıyorsanız kısa devre ve aşırı deşarja karşı dikkatli olun.",
        "Paletler dönerken parmaklarınızı palet ve dişli arasına sokmayın (ezilme tehlikesi).",
        "İlk testi paletler havadayken yapın; masa kenarında çalıştırmayın.",
    ],
    "gelistir": ["Ultrasonik ile engelden kaçınma", "ESP32-CAM ile canlı görüntü", "Enkoderle hız ve mesafe kontrolü", "Joystick / web arayüzü ile sürüş"],
}

# =====================================================================================================
# MARS ROVER TİPİ ROBOT
# =====================================================================================================
GUIDES["rover"] = {
    "zorluk": "Zor", "sure": "30–50 saat", "butce": "Yüksek",
    "hedef": "Rocker-bogie süspansiyonlu, 6 tekerlekli, 4 köşe tekerleği dönebilen arazi robotu (ESP32 kontrollü).",
    "beceri": ["Mekanik tasarım", "Motor sürücü ve güç dağıtımı", "Servo direksiyon", "Kinematik"],
    "ogrenme": ["Rocker-bogie geometrisi ve diferansiyel kol", "Engel aşma (h / D oranı)", "Ackermann benzeri direksiyon geometrisi", "Güç dağıtımı ve sigorta"],
    "araclar": ["Tornavida / Allen / lokma anahtar seti", "Matkap ve delik uçları", "Testere / eğe (alüminyum profil için)", "Multimetre", "Havya", "3B yazıcı (ops.)", "Vida sabitleyici", "USB kablo + bilgisayar"],
    "malzeme": [
        ("DC redüktörlü motor (12 V, 30–100 rpm)", 6, "Yük altında akım ≈ stall akımının yarısını geçmemeli"),
        ("Tekerlek (Ø 8–12 cm, tırtıklı)", 6, "Tırtık (cleat) gevşek zeminde tutunmayı artırır"),
        ("Yüksek torklu servo (direksiyon)", 4, "Ön ve arka köşe tekerlekleri için"),
        ("Servo (direk panı)", "1 (ops.)", "Kamera direği için"),
        ("Rocker-bogie yapısı: alüminyum profil / boru veya 3B baskı + rulman, cıvata", "1 set", "4 pivot noktası (rocker×2, bogie×2) + diferansiyel"),
        ("Diferansiyel çubuğu + bağlantı elemanları", 1, "İki rocker'ı bağlar"),
        ("Gövde kutusu + güneş paneli (ops.)", 1, "Panel dekoratif veya gerçek olabilir"),
        ("ESP32 geliştirme kartı", 1, "Wi-Fi ile kontrol"),
        ("Çift kanallı motor sürücü (motor akımına uygun)", 3, "Her biri iki motor sürer"),
        ("PCA9685 servo sürücü", 1, "5 servo için"),
        ("LiPo 3S 11,1 V", 1, "Sigorta + şalter şart"),
        ("Buck dönüştürücü 6 V, ≥ 10 A", 1, "Servolar için"),
        ("ESP32-CAM / kamera (ops.), anten", "1 (ops.)", ""),
    ],
    "adimlar": [
        S("Ölçüler ve geometri", [],
          ["Tekerlek çapını (D) seçin; konumları D'nin katları olarak planlayın (bu uygulamadaki model oranları: ön +2,24 D, orta −0,26 D, arka −2,10 D).",
           "İz genişliğini, dingil mesafesini ve ağırlık merkezi yüksekliğini seçin; devrilme ve engel aşma kontrolünü sayfadaki analizle yapın.",
           "Motor torkunu hesaplayın: kütle × g × (tekerlek yarıçapı) × güvenlik katsayısı ÷ 6 tekerlek."],
          "h / D hedefiniz ≤ 1,0 ve devrilme eşikleri hedef yamaç eğiminin en az 1,3 katı.", "2–4 saat",
          ipucu="Önce karton / MDF maketle geometriyi deneyin."),
        S("Rocker ve bogie yapısı", ["rocker", "bogie"],
          ["Her yan için rocker (uzun) ve bogie (kısa) kollarını kesin / basın.", "Rocker'ın ucuna bogie pivotunu rulman ve cıvata ile bağlayın.",
           "Pivotların sürtünmesiz ama boşluksuz dönmesini sağlayın."],
          "Rocker ve bogie elle oynatıldığında yumuşak ve boşluksuz hareket ediyor.", "4–6 saat"),
        S("Diferansiyel kol", ["diff"],
          ["Diferansiyel çubuğunu gövde üzerindeki merkez pivotuna bağlayın.", "Çubuğun uçlarını rocker pivotlarına bağlantı elemanlarıyla bağlayın."],
          "Bir rocker yukarı gidince diğeri aşağı gidiyor; gövde iki yanın ortalamasında kalıyor.", "2–3 saat",
          ipucu="Gövde eğimi iki yanın ortalamasıdır; sayfadaki 'Engel aşma' grafiğiyle karşılaştırın."),
        S("Tekerlekler ve motorlar", ["wheels"],
          ["Motorları tekerlek göbeklerine / braketlerine sabitleyin.", "Altı tekerleği rocker ve bogie uçlarına takın; hepsinin aynı hizada olduğunu doğrulayın."],
          "Altı tekerlek de düz zeminde aynı anda temas ediyor.", "3–5 saat"),
        S("Direksiyon servoları", ["motors"],
          ["Ön ve arka köşe tekerleklerinin üstüne servoları yerleştirin; servo ekseni tekerleğin dikey ekseniyle çakışsın.", "Servoları 90°'de ortalayıp horn'ları tekerlekler düz bakacak şekilde takın."],
          "Dört köşe tekerlek ± 45° dönüyor ve tekrar düze dönüyor.", "2–3 saat",
          uyari="Servo ortalama monte etmeden önce yapılmalı; aksi halde tekerlekler hizasız olur."),
        S("Gövde", ["body"],
          ["Elektronik kutusunu diferansiyel pivotunun üstüne sabitleyin.", "Sürücüleri, ESP32'yi, PCA9685'i ve bataryayı kutuya yerleştirin; ağırlığı alçakta ve ortada tutun."],
          "Gövde yatay ve rocker'lara çarpmıyor; ağırlık merkezi ortada.", "2 saat"),
        S("Güç ve güneş paneli", ["solar"],
          ["Güneş panelini (veya maketini) gövde üstüne direklerle monte edin.", "Gerçek panel kullanıyorsanız şarj kontrol devresi ekleyin; sigorta ve şalteri ana hatta yerleştirin."],
          "Panel gövdeye sağlam bağlı; kablo yok / düzenli.", "1 saat"),
        S("Direk ve kamera", ["mast"],
          ["Direği gövdenin ön köşesine yerleştirin, pan servosunu ve kamerayı takın.", "Kamera kablosunu direk içinden geçirin."],
          "Direk panı sürtünmesiz dönüyor; kamera görüntüsü kararlı.", "1–2 saat"),
        S("Anten ve iletişim", ["antenna"],
          ["ESP32 anteni veya çanak anten maketini gövdeye bağlayın.", "Kablosuz modülün metal parçalardan uzakta olmasına dikkat edin."],
          "Telefon / bilgisayar ESP32'ye bağlanabiliyor; sinyal kararlı.", "1 saat"),
        S("Kablolama", [],
          ["Üç motor sürücüyü ön / orta / arka tekerlek çiftlerine bağlayın; servoları PCA9685 kanallarına takın.", "Sigorta + şalteri LiPo çıkışına, buck'ı servo gücü için kurun; GND'leri ortak yapın.",
           "Kabloları rocker-bogie eklemlerinde gevşek bırakın ve spiral kılıfla toplayın."],
          "Güç açıldığında hiçbir parça ısınmıyor; kablolar eklem hareketinde gerilmiyor.", "3–4 saat", vurgu=["body", "motors"],
          uyari="Kablolama sırasında bataryayı çıkarın; sigortasız çalıştırmayın."),
        S("Test ve yazılım", [],
          ["Önce robotu askıda (tekerlekler havada) çalıştırın; sürüş yönlerini ve direksiyon açılarını kontrol edin.", "Rehberdeki direksiyon geometrisini kullanarak köşe tekerlek açılarını ve tekerlek hızlarını ayarlayın.",
           "Düşük hızda küçük bir engelle (h ≤ D) deneyin; ardından rampada test edin."],
          "Robot düz gidiyor, yay çiziyor ve yerinde dönebiliyor; D yüksekliğinde engeli aşabiliyor.", "3–5 saat", vurgu=["wheels", "rocker", "bogie"]),
    ],
    "kablolama": {
        "boyut": (980, 420),
        "nodes": {
            "esp": N(["ESP32", "PWM + DIR"], 260, 30, 190, 70),
            "lipo": N(["LiPo 3S", "11,1 V"], 30, 150, 180, 70),
            "dist": N(["Güç dağıtımı", "sigorta + şalter"], 260, 150, 190, 70),
            "buck": N(["Buck dönüştürücü", "6 V · ≥ 10 A"], 260, 280, 190, 70),
            "da": N(["Sürücü A", "ön sol + ön sağ"], 520, 20, 180, 56),
            "db": N(["Sürücü B", "orta sol + sağ"], 520, 90, 180, 56),
            "dc": N(["Sürücü C", "arka sol + sağ"], 520, 160, 180, 56),
            "pca": N(["PCA9685", "I²C · V+ = 6 V"], 520, 280, 180, 70),
            "ma": N(["Ön tekerlek motorları", "2 × DC"], 750, 20, 200, 56),
            "mb": N(["Orta tekerlek motorları", "2 × DC"], 750, 90, 200, 56),
            "mc": N(["Arka tekerlek motorları", "2 × DC"], 750, 160, 200, 56),
            "srv": N(["5 servo", "4 direksiyon + 1 direk"], 750, 280, 200, 70),
        },
        "edges": [
            E("lipo", "dist", "guc", "11,1 V"), E("dist", "buck", "guc", "11,1 V"),
            E("dist", "da", "guc", "VM", off=8, mid=10), E("dist", "db", "guc", off=8, mid=10), E("dist", "dc", "guc", off=8, mid=10),
            E("esp", "da", "sinyal", "PWM+DIR", off=-8, mid=-10), E("esp", "db", "sinyal", off=-8, mid=-10), E("esp", "dc", "sinyal", off=-8, mid=-10),
            E("buck", "pca", "guc", "6 V"), E("esp", "pca", "i2c", "SDA / SCL", off=-20, mid=25),
            E("da", "ma", "faz"), E("db", "mb", "faz"), E("dc", "mc", "faz"), E("pca", "srv", "faz"),
        ],
        "pinler": [
            ("LiPo 3S", "Sigorta + şalter → dağıtım", "11,1 V", "Sigorta motor toplam akımına göre"),
            ("Dağıtım", "Sürücü A/B/C VM", "11,1 V", "Kalın kablo"), ("Dağıtım", "Buck girişi", "11,1 V", ""),
            ("Buck 6 V", "PCA9685 V+", "Servo gücü", "Servolar için ayrı hat"), ("ESP32 PWM/DIR pinleri", "Sürücü PWM / IN girişleri", "Sinyal", "Her sürücü için 2 PWM + 4 yön pini"),
            ("ESP32 SDA / SCL", "PCA9685 SDA / SCL", "I²C", "GPIO21 / GPIO22"), ("Servo 1…4", "PCA9685 kanal 0…3", "3 pin", "FL, FR, RL, RR köşe tekerlekleri"),
            ("Servo 5", "PCA9685 kanal 4", "3 pin", "Direk panı (opsiyonel)"), ("Tüm GND", "Ortak", "Toprak", "Mutlaka ortak"),
        ],
    },
    "kod": [
        {"baslik": "Direksiyon geometrisi: köşe tekerlek açıları ve tekerlek hızları", "dil": "python", "dosya": "rover_direksiyon.py", "fn": "physics.rover_steering",
         "aciklama": "R dönüş yarıçapı (+ sol, − sağ, 0 yerinde dönüş) için köşe tekerlek açıları ve altı tekerleğin göreli hızları. Aşağıdaki hesaplayıcıyla deneyin."},
        {"baslik": "Aynı hesabın ESP32 / Arduino karşılığı", "dil": "cpp", "dosya": "rover_direksiyon.ino",
         "aciklama": "Açıları servolara, hızları motor sürücülerine yazmadan önce sınırlayın (±45°). Değerler cm cinsindendir.",
         "kod": """// Mars rover: 6 tekerlek hızı ve 4 köşe tekerlek açısı (R: dönüş yarıçapı, + sol, - sağ, 0 yerinde dönüş)
const float TRACK = 28.0, DF = 17.0, DR = 16.0;      // iz genişliği, ön ve arka köşe tekerlek mesafesi (cm)
// Tekerlek sırası: ön sol, ön sağ, orta sol, orta sağ, arka sol, arka sağ
const float WX[6] = {-TRACK / 2,  TRACK / 2, -TRACK / 2,  TRACK / 2, -TRACK / 2,  TRACK / 2};
const float WY[6] = {  DF,          DF,         0,          0,         -DR,         -DR};

void steering(float R, float angleDeg[6], float speed[6]) {
  float om = (R >= 0) ? 1.0 : -1.0;
  float vmax = 0.0001;
  for (uint8_t i = 0; i < 6; i++) {
    float vx = om * (-WY[i]);
    float vy = om * (WX[i] + R);
    float v  = hypotf(vx, vy);
    float d  = (v > 1e-6) ? atan2f(vx, vy) * 180.0 / PI : 0.0;
    if (d > 90.0)       { d -= 180.0; v = -v; }         // tekerlek geri gidiyor
    else if (d < -90.0) { d += 180.0; v = -v; }
    angleDeg[i] = d;
    speed[i]    = v;
    if (fabsf(v) > vmax) vmax = fabsf(v);
  }
  for (uint8_t i = 0; i < 6; i++) speed[i] /= vmax;     // en hızlı tekerlek = 1
}
"""},
    ],
    "test": [
        "Rocker ve bogie pivotları boşluksuz ve sürtünmesiz; diferansiyel kol doğru çalışıyor.",
        "Altı tekerlek düz zeminde aynı anda temas ediyor.",
        "Dört köşe tekerlek ± 45° dönüyor, ortalanmış.",
        "Sigorta ve şalter takılı; kısa devre yok; hiçbir parça ısınmıyor.",
        "Askıda motor ve direksiyon yönleri doğru.",
        "Küçük engelde (h ≤ D) gövde dengeli yükseliyor; rampada devrilmiyor.",
    ],
    "sorun": [
        ("Robot düz gitmiyor", "Tekerlek hizası / servo ortası hatalı", "Servoları yeniden ortalayın, hizayı ölçün"),
        ("Rocker bir yana sıkışıyor", "Pivot boşluğu veya sürtünme", "Rulman / cıvata sıkılığını ayarlayın, yağlayın"),
        ("Motor sürücü ısınıyor", "Akım yetersiz sürücü, ağır robot", "Daha yüksek akımlı sürücü, kütleyi azaltın"),
        ("Servolar resetleniyor / titriyor", "Buck akımı yetersiz", "Daha güçlü buck, kapasitör, kalın kablo"),
        ("Engelde tekerlek yerden kesiliyor", "Geometri hatalı veya CG çok yüksek", "Pivot konumlarını ve CG'yi analiz sayfasıyla kontrol edin"),
        ("Yerinde dönüşte tekerlekler sürtünüyor", "Köşe açıları veya hızlar hatalı", "R = 0 için hesaplanan açıları ve hız oranlarını uygulayın"),
    ],
    "guvenlik": [
        "Rocker-bogie eklemleri ve dişliler ezilme / sıkışma tehlikesi taşır; çalışırken el sokmayın.",
        "LiPo + yüksek akım: ana hatta sigorta ve şalter kullanın; kablo kesitini akıma göre seçin.",
        "İlk denemeleri robot askıdayken yapın; ağır robotu merdiven kenarında çalıştırmayın.",
    ],
    "gelistir": ["Enkoderle odometri ve yol takibi", "IMU ile eğim algılama ve otomatik yavaşlama", "Kamera ile engel / hedef tanıma", "Robot kol ekleyip örnek toplama"],
}
