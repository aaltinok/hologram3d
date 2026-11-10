# MERAL Robotik Kulübü · 3D Robot Hologram Laboratuvarı

Kulübün altı robotunu (çizgi izleyen araba, 6 eksenli robot kol, altı bacaklı robot, quadcopter, paletli tank robot,
Mars rover tipi robot) mavi **blueprint** temalı etkileşimli 3D hologramlarla tanıtan ve her robot için temel robotik
hesaplamaları gösteren, karanlık / bilimsel temalı bir Streamlit uygulaması.

## Özellikler
- **🛠️ Nasıl yapılır? rehberi (her robot sayfasında):** genel bilgi ve beceriler, araç listesi, malzeme listesi (BOM) ve kontrol listesi,
  **adım adım montaj** (hologramda parçalar sırayla belirir, güncel adımın parçaları vurgulanır, etiketle gösterilir),
  **patlatılmış görünüm** kaydırıcısı, **otomatik montaj animasyonu**, blueprint **kablolama şeması** + bağlantı tablosu,
  indirilebilir **örnek kodlar**, test listesi, sorun giderme tablosu, güvenlik uyarıları ve geliştirme fikirleri.
- **Hologramlar:** her hologramda *PATLAT* düğmesi (katmanlı patlatılmış görünüm) ve parça seçince 3B etiket (callout) bulunur.
- **Genel Bakış:** altı hologram, üçerli iki satır (telefonda alt alta). Yeni robotlar bir onay kutusuyla gizlenebilir.
- **Her robot için:** 360° dönen hologram, parça seçince vurgulama + bilgi kartı, tel kafes görünümü, parça kataloğu tablosu.
- **Robot araba:** diferansiyel sürüş kinematiği (v, ω, dönüş yarıçapı, yörünge) ve PD kontrollü çizgi izleme simülasyonu.
- **Robot kol:** düzlemsel 3R ileri kinematik, çalışma uzayı, Jacobian / manipülabilite (tekillik uyarısı), analitik ters kinematik.
- **Altı bacaklı:** tripod / ripple / wave yürüyüş çizelgesi, destek bacağı sayısı, statik kararlılık, ayak yörüngesi, gövde hızı.
- **Quadcopter:** itki/ağırlık oranı, asılı kalma gazı ve uçuş süresi (momentum teorisi), roll ekseni PD basamak yanıtı, X şasi motor karıştırıcı.
- **Paletli tank:** kayma faktörlü skid-steer kinematiği, yerinde dönüş / eğim için gereken tahrik torku, çekiş sınırı.
- **Mars rover (rocker-bogie):** engel aşma simülasyonu (ortalama kuralı, h/D oranı), yanal / boyuna devrilme ve kayma eşikleri.
- **Karşılaştırma:** teknik tablo, radar ve çubuk grafik.

## Kurulum ve çalıştırma
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Tarayıcıda `http://localhost:8501` açılır. Tema `.streamlit/config.toml` içinde tanımlıdır (karanlık).

### Docker
```bash
docker build -t meral-robot-hologram .
docker run -p 8501:8501 meral-robot-hologram
```

## Testler
```bash
pip install pytest
python -m pytest -q
```

## Dosya yapısı
```
app.py                      Streamlit arayüzü
robot_lab/kinematics.py     Araba, kol, hexapod hesaplamaları (saf NumPy)
robot_lab/physics.py        Quadcopter, tank, rover hesaplamaları (saf NumPy)
robot_lab/guides.py         6 robotun yapım rehberi içeriği (adımlar, BOM, kod, test, sorun giderme)
robot_lab/guide_ui.py       Rehber arayüzü (stepper, kontrol listeleri, kod indirme)
robot_lab/diagrams.py       Blueprint kablolama şeması (SVG) üretici
robot_lab/plots.py          Plotly grafikleri
robot_lab/data.py           Parça ve karşılaştırma verileri
robot_lab/ui.py             Tema CSS'i, hologram gömme yardımcıları
assets/holograms/*.html     three.js blueprint hologramları (6 robot)
tests/                      Birim testleri (kinematik, fizik, veri/varlık, rehber bütünlüğü, şema geçerliliği)
.streamlit/config.toml      Karanlık tema
```

## Notlar
- Hologramlar three.js (r128) kütüphanesini **CDN'den** yükler; ilk açılışta internet gerekir.
- 3D modeller robot fotoğraflarına bakılarak yaklaşık çizilmiştir, ölçüler birebir değildir.
- Parça bilgilerindeki değerler bu tür kitlerde tipiktir; kendi robotunuzun modeline göre değişebilir.
- Hologramlar tek renkli mavi blueprint temasındadır; parçalar renk yerine açık/koyu mavi tonlarla ayrılır.
- Quadcopter, tank ve rover modelleri genel / tipik tasarımlardır (belirli bir ürünün birebir kopyası değildir).
- Yapım rehberleri genel / tipik kit ve parçalara göredir; kendi kitinizin kılavuzu ve parça veri sayfaları önceliklidir. Örnek kodlar derlenmeden önce pin ve kalibrasyon değerleri kontrol edilmelidir.
- Quadcopter uçuşunda yerel mevzuata (SHGM) uyun; LiPo ve yüksek akımlı sistemlerde güvenlik uyarılarını dikkate alın.
- Radar grafiği öznel, eğitim amaçlı bir değerlendirmedir.
- Kol uzunlukları, eklem sınırları, tekerlek aralığı ve sensör yerleşimi tahmini varsayımlardır; arayüzden değiştirilebilir.

MERAL Robotik Kulübü
