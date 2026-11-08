"""Robot tanıtım verileri (hologramlardaki bilgi kartlarıyla uyumlu)."""
from __future__ import annotations

import pandas as pd

HOLO_FILES = {
    "araba": "robot_araba.html",
    "kol": "robot_kol.html",
    "hexapod": "hexapod.html",
    "quad": "quadcopter.html",
    "tank": "tank.html",
    "rover": "rover.html",
}

ROBOTS = {
    "araba": {
        "ad": "Çizgi İzleyen Robot Araba",
        "emoji": "🚗",
        "ozet": ("İki tekerlekli, diferansiyel sürüşlü bir mobil robot. Arduino Nano ile çalışır; "
                 "öndeki kızılötesi (IR) sensör dizisiyle zemindeki çizgiyi okur ve iki motorun hız farkıyla yönünü düzeltir."),
        "metrikler": [("Tekerlek", "2"), ("Motor", "2 × DC"), ("Denetleyici", "Arduino Nano")],
        "parcalar": [
            ("Akrilik şasi", "Robotun iskeleti; sensör ve ayak konumu uzun yuvalarla ayarlanır.", "Mavi akrilik plaka"),
            ("TT redüktörlü DC motor (2)", "Dişli kutusu hızı düşürür, torku artırır.", "Tipik 3–6 V"),
            ("Lastikli tekerlekler (2)", "Tutuş sağlar; iki tekerlek bağımsız sürülür, direksiyon gerekmez.", "Tipik Ø ≈ 65 mm"),
            ("Gri destek makaraları", "Önü taşır, sürtünmeyi azaltır, dengeyi korur.", "Fotoğraftan yorumlandı"),
            ("Kırmızı sürücü / genişletme kartı", "Nano'yu motorlara ve sensöre bağlar; genelde motor sürücü devresi içerir.", "Kit modeline göre değişir"),
            ("Yeşil vida terminalleri", "Pinleri lehimsiz, sökülebilir kablo bağlantısına açar.", "—"),
            ("Arduino Nano", "Robotun beyni: sensörü okur, motor hızlarına karar verir.", "ATmega328P, 5 V, 16 MHz, 32 KB flash, 14 dijital / 8 analog pin"),
            ("Şerit (jumper) kablo", "Sensör kartına 5 V, GND ve sinyal hatlarını taşır.", "Çok damarlı"),
            ("IR çizgi sensörü dizisi", "Her kanalda IR LED + alıcı; siyah çizgi ışığı emer, beyaz zemin yansıtır.", "Çok kanallı (modelde 5)"),
        ],
    },
    "kol": {
        "ad": "6 Eksenli Robot Kol",
        "emoji": "🦾",
        "ozet": ("Metal gövdeli, altı servolu masaüstü robot kol. Dönel taban, omuz, dirsek, iki eksenli bilek ve "
                 "parmaklı bir tutucudan oluşur; nesneleri alıp bırakabilir."),
        "metrikler": [("Serbestlik derecesi", "6"), ("Servo", "6"), ("Uç eleman", "Tutucu")],
        "parcalar": [
            ("Taban plakası ve vantuzlar", "Kolu dengeler ve masaya sabitler.", "Metal plaka, 4 vantuz"),
            ("Dönel tabla + taban servosu", "Kolu sağa sola döndürür (1. eksen).", "Yataklı tabla"),
            ("Kontrol kartı", "Servolara komut gönderir ve güç dağıtır.", "Model fotoğraftan anlaşılmıyor"),
            ("Omuz eklemi", "Kolu öne arkaya kaldırır (2. eksen).", "U braket + servo"),
            ("Üst kol", "Omuz ile dirsek arasındaki bağlantı; erişimi belirler.", "—"),
            ("Dirsek eklemi", "Ön kolu bükerek tutucuyu yaklaştırır / uzaklaştırır (3. eksen).", "—"),
            ("Ön kol", "Dirsek ile bilek arasında; bilek servosunu taşır.", "—"),
            ("Bilek", "Eğilme (4. eksen) ve kendi ekseninde dönme (5. eksen).", "2 servo"),
            ("Tutucu (gripper)", "Bir servo iki parmağı açıp kapatır (6. eksen).", "Parmak pedli"),
        ],
    },
    "hexapod": {
        "ad": "Altı Bacaklı Robot (Hexapod)",
        "emoji": "🕷️",
        "ozet": ("Altıgen gövdeli, altı bacaklı yürüyen robot. Bacak başına iki servo (kalça ve diz) bulunur; "
                 "kavisli pençe uçları ve kablosuz bağlantı anteni dikkat çeker."),
        "metrikler": [("Bacak", "6"), ("Servo", "12"), ("Yürüyüş", "Tripod")],
        "parcalar": [
            ("Gövde kabuğu", "Elektroniği korur; ön yüzde havalandırma ve port delikleri.", "Görünüşe göre 3D baskı"),
            ("Elektronik kart ve batarya", "Yürüyüş komutlarını servolara iletir ve enerji sağlar.", "Modeldeki iç parçalar tahminidir"),
            ("Anten", "Telefon / kumandadan kablosuz komut alır.", "Modül tipi belirsiz"),
            ("Kalça servoları", "Bacağı öne arkaya savurur (yatay hareket).", "6 adet"),
            ("Bacak braketi", "Diz servosunu tutar ve pençeyi taşır.", "—"),
            ("Diz servoları", "Pençeyi kaldırıp indirir (dikey hareket).", "6 adet"),
            ("Pençe bacaklar", "Kavisli, sivri uç; zeminde ince temas noktası oluşturur.", "—"),
            ("Servo kabloları", "Her servoyu karta bağlar: sinyal, güç, toprak.", "Çoğu servoda turuncu / kırmızı / kahverengi"),
        ],
    },
}


ROBOTS["quad"] = {
    "ad": "Quadcopter (Dört Pervaneli Drone)",
    "emoji": "🚁",
    "ozet": ("X şasili, dört fırçasız motorlu çok rotorlu hava aracı. Uçuş kontrol kartı IMU ile yatışı ölçer ve "
             "dört motorun hızını sürekli ayarlayarak dengede kalır. Motor çiftleri zıt yönde dönerek gövdenin dönmesini dengeler."),
    "metrikler": [("Motor", "4 × BLDC"), ("Kontrol girişi", "4"), ("Serbestlik", "6")],
    "parcalar": [
        ("Gövde plakaları", "Kartları ve bataryayı taşıyan üst/alt plaka; ara parçalar sertlik sağlar.", "Genellikle karbon fiber"),
        ("Kollar (X şasi)", "Motorları gövdeden uzaklaştırır; uçlardaki LED yönü gösterir.", "Ön yeşil, arka kırmızı (tipik)"),
        ("Fırçasız (BLDC) motorlar", "Pervaneleri döndürür; çiftler zıt yönde dönerek tepki momentlerini dengeler.", "4 adet"),
        ("ESC (hız kontrolcü)", "Bataryanın DC gücünü motor için üç fazlı sinyale çevirir.", "Her motor için 1 adet"),
        ("Pervaneler", "İtki üretir; itki yaklaşık dönüş hızının karesiyle artar.", "2 CW + 2 CCW"),
        ("Uçuş kontrol kartı", "IMU ile yatışı ölçer, PID ile motor hızlarını günceller.", "Tipik yapı gösterildi"),
        ("LiPo batarya", "Enerji kaynağı; kapasite (mAh) uçuş süresini belirler.", "Ağırlık uçuş süresini kısaltır"),
        ("Kamera ve gimbal", "Görüntü alır; gimbal titreşimi azaltır.", "Modelde basitleştirildi"),
        ("GPS / pusula", "Konum ve yön bilgisi verir.", "Konum tutma için"),
        ("İniş takımı", "İniş darbesini karşılar, alt parçaları korur.", "—"),
    ],
}

ROBOTS["tank"] = {
    "ad": "Paletli Tank Robot",
    "emoji": "🚜",
    "ozet": ("İki palet grubuyla hareket eden, direksiyonsuz bir mobil robot. Palet hız farkıyla (skid steer) döner, yerinde "
             "dönebilir; geniş temas alanı sayesinde yumuşak ve engebeli zeminde tekerleğe göre daha iyi tutunur."),
    "metrikler": [("Palet", "2"), ("Motor", "2 × DC"), ("Sürüş", "Skid steer")],
    "parcalar": [
        ("Gövde", "Elektronik, motor ve bataryayı taşır; iki palet grubunu bağlar.", "—"),
        ("Palet bandı", "Zeminle geniş temas oluşturan halka; üstteki bloklar tutunmayı artırır.", "Lastik / plastik"),
        ("Tahrik dişlisi", "Motorun gücünü palete aktarır; dişler palet bloklarına kavrar.", "Modelde arkada"),
        ("Avara ve yol tekerlekleri", "Paleti gergin tutar ve ağırlığı palet boyunca dağıtır.", "1 avara + 4 yol tekerleği (her yanda)"),
        ("Motorlar ve dişli kutuları", "Her palet kendi motoruyla sürülür; hız farkı dönüşü sağlar.", "2 adet"),
        ("Kontrol kartı ve batarya", "Motor hızlarını ayarlar; ağır batarya aşağıda tutulur.", "Model belirsiz"),
        ("Kamera kulesi", "Dönebilen kule; kamera ve sensör taşır.", "Örnek amaçlı"),
    ],
}

ROBOTS["rover"] = {
    "ad": "Mars Rover Tipi Robot (Rocker-Bogie)",
    "emoji": "🪐",
    "ozet": ("Altı tekerlekli, rocker-bogie süspansiyonlu arazi robotu. Yaylar olmadan engebeli zeminde tüm tekerleklerin temasını "
             "korur; ön ve arka köşe tekerlekleri döner, böylece robot yerinde dönebilir."),
    "metrikler": [("Tekerlek", "6"), ("Sürüş motoru", "6"), ("Direksiyon", "4")],
    "parcalar": [
        ("Gövde (sıcak elektronik kutusu)", "Elektronik ve bataryayı toz ve soğuktan korur.", "—"),
        ("Güneş paneli", "Enerji kaynağı.", "Bazı gezginler nükleer güç kullanır"),
        ("Direk ve kamera başı", "Stereo kameralarla çevreyi görüntüler.", "Kendi ekseninde döner"),
        ("Yüksek kazançlı anten", "Dünya ile veri ve komut alışverişi.", "Yönlendirilebilir çanak"),
        ("Rocker (ana salıncak)", "Ön tekerleği ve bogie'yi taşır.", "Her yanda 1 adet"),
        ("Bogie (küçük salıncak)", "Orta ve arka tekerleği taşır, yükü dengeler.", "Her yanda 1 adet"),
        ("Diferansiyel kol", "Rocker'ları bağlar; gövde eğimi iki yanın ortalaması olur.", "Yay gerektirmez"),
        ("Tekerlekler (6)", "Her biri ayrı motorla sürülür; çıkıntılar tutunmayı artırır.", "6 sürüş motoru"),
        ("Direksiyon motorları (4)", "Köşe tekerlekleri döndürür; yerinde dönüş sağlar.", "Ön ve arka köşeler"),
    ],
}


def parts_df(key: str) -> pd.DataFrame:
    return pd.DataFrame(ROBOTS[key]["parcalar"], columns=["Parça", "Görev", "Not"])


COMPARE_ROWS = [
    {"Robot": "Çizgi izleyen araba", "Hareket tipi": "Tekerlekli (diferansiyel sürüş)", "Aktüatör": "2 DC redüktörlü motor",
     "Aktüatör sayısı": 2, "Denetleyici": "Arduino Nano", "Algılama": "IR çizgi sensörü dizisi",
     "Tipik kullanım": "Çizgi izleme yarışmaları, kontrol eğitimi"},
    {"Robot": "6 eksenli robot kol", "Hareket tipi": "Sabit tabanlı manipülatör", "Aktüatör": "6 servo",
     "Aktüatör sayısı": 6, "Denetleyici": "Servo kontrol kartı (model belirsiz)", "Algılama": "Fotoğrafta görünmüyor",
     "Tipik kullanım": "Al-bırak, kinematik eğitimi"},
    {"Robot": "Altı bacaklı robot", "Hareket tipi": "Bacaklı (hexapod)", "Aktüatör": "12 servo (bacak başına 2)",
     "Aktüatör sayısı": 12, "Denetleyici": "Belirsiz (kablosuz anten var)", "Algılama": "Fotoğrafta görünmüyor",
     "Tipik kullanım": "Engebeli zemin, yürüyüş algoritmaları"},
    {"Robot": "Quadcopter", "Hareket tipi": "Havada (çok rotorlu)", "Aktüatör": "4 BLDC motor + ESC",
     "Aktüatör sayısı": 4, "Denetleyici": "Uçuş kontrol kartı (IMU)", "Algılama": "IMU; GPS ve kamera (tipik)",
     "Tipik kullanım": "Havadan görüntüleme, keşif"},
    {"Robot": "Paletli tank robot", "Hareket tipi": "Paletli (skid steer)", "Aktüatör": "2 DC motor",
     "Aktüatör sayısı": 2, "Denetleyici": "Motor sürücü + denetleyici (model belirsiz)", "Algılama": "Kamera kulesi (örnek)",
     "Tipik kullanım": "Engebeli zemin, gözetleme, eğitim"},
    {"Robot": "Mars rover tipi robot", "Hareket tipi": "6 tekerlekli rocker-bogie", "Aktüatör": "6 sürüş + 4 direksiyon motoru",
     "Aktüatör sayısı": 10, "Denetleyici": "Ana bilgisayar (örnek)", "Algılama": "Stereo kamera direği",
     "Tipik kullanım": "Engebeli arazide keşif"},
]

# Öznel, eğitim amaçlı nitel değerlendirme (1–10). Ölçüm değildir.
RADAR_AXES = ["Hız", "Arazi uyumu", "Manipülasyon", "Kontrol karmaşıklığı", "Mekanik karmaşıklık", "Başlangıç dostu"]
RADAR_SCORES = {
    "Çizgi izleyen araba": [8, 3, 1, 3, 2, 9],
    "6 eksenli robot kol": [4, 1, 9, 7, 7, 5],
    "Altı bacaklı robot": [4, 8, 2, 8, 8, 3],
    "Quadcopter": [9, 6, 1, 9, 4, 3],
    "Paletli tank robot": [3, 7, 1, 3, 4, 8],
    "Mars rover tipi robot": [2, 9, 2, 6, 8, 3],
}
