# 📊 Olist E-Commerce Data Analytics Pipeline 

Bu proje, Brezilya merkezli e-ticaret platformu Olist'in verilerini kullanarak uçtan uca bir veri analitiği ve iş zekası (BI) mimarisi sunmaktadır. Kaggle API kullanılarak otomatik çekilen veriler, Python ile işlenmiş, PostgreSQL üzerinde Yıldız Şema (Star Schema) modeline dönüştürülmüş ve Power BI ile görselleştirilmiştir.

## 🏗️ Proje Mimarisi

1. **Extract (Veri Çekme):** Kaggle API kullanılarak ham veriler otomatik olarak `data/raw/` klasörüne indirilir.
2. **Transform (Veri Temizleme & Özellik Çıkarımı):** Python (Pandas & NumPy) kullanılarak veri tipleri düzeltilmiş, eksik veriler (örn. ürün kategorileri) doldurulmuş ve `delivery_duration_days`, `is_delayed` gibi yeni analitik metrikler üretilmiştir. Portekizce kategoriler İngilizceye çevrilerek veri zenginleştirilmiştir.
3. **Load (Veritabanı Yükleme):** SQLAlchemy ve psycopg2 kullanılarak temizlenmiş veriler PostgreSQL veritabanına aktarılmıştır.
4. **Data Warehousing (Yıldız Şema):** PostgreSQL üzerinde DDL komutlarıyla boyut (Dimension) ve gerçek (Fact) tabloları oluşturularak ilişkisel model kurulmuştur.
5. **Business Intelligence (İş Zekası):** Karmaşık SQL dönüşümleri (View katmanı) üzerinden Power BI Import moduyla bağlanılmış, DAX fonksiyonları kullanılarak interaktif bir dashboard tasarlanmıştır.

## 📁 Dosya Yapısı

```text
olist-ecommerce-analytics/
├── data/                  # Ham ve işlenmiş veriler (Git'te yok)
├── notebooks/             
│   └── 01_EDA.ipynb       # Keşifçi Veri Analizi ve İstatistiksel Dağılımlar
├── scripts/
│   ├── extract_load.py    # Kaggle API entegrasyonu
│   ├── data_cleaning.py   # Pandas ile ETL (Transform) süreçleri
│   └── load_to_postgres.py# SQLAlchemy ile DB aktarımı
├── sql/
│   ├── 01_create_schema.sql  # Star Schema tasarımı
│   └── 02_create_views.sql   # Power BI için sanal tablolar (Views)
├── dashboard/             
│   └── olist_dashboard.pbix  # Power BI Dashboard dosyası
├── .env                   # DB şifreleri (Git'te yok)
└── requirements.txt       # Proje bağımlılıkları
🛠️ Kullanılan Teknolojiler
Python: Pandas, NumPy, SQLAlchemy, python-dotenv

Veritabanı: PostgreSQL, pgAdmin (Star Schema, CTEs, Views)

İş Zekası: Power BI (DAX, Data Modeling)

Versiyon Kontrol: Git & GitHub

🚀 Kurulum ve Çalıştırma
Repoyu klonlayın ve bağımlılıkları yükleyin:
git clone https://github.com/deryaKhrimn/olist-ecommerce-analytics.git
cd olist-ecommerce-analytics
pip install -r requirements.txt

Ana dizinde bir .env dosyası oluşturun ve PostgreSQL şifrenizi ekleyin: DB_PASS=sifreniz

Kaggle API Token dosyanızı (kaggle.json) doğru dizine yerleştirin. Sırasıyla ETL scriptlerini çalıştırın:
python scripts/extract_load.py
python scripts/data_cleaning.py
python scripts/load_to_postgres.py

sql/ klasöründeki scriptleri PostgreSQL üzerinde çalıştırarak veri ambarını kurun.

dashboard/olist_dashboard.pbix dosyasını Power BI Desktop ile açın.

📈 Temel İçgörüler (Key Insights)
Lojistik Performansı: Gerçekleşen teslimat süreleri ile tahmin edilen süreler arasındaki sapmalar vw_delivery_analysis üzerinden tespit edilmiştir.

Ödeme Davranışları: Müşterilerin tercih ettiği ödeme yöntemlerine göre sepet ortalamasındaki (AOV) değişimler analiz edilmiştir.

📊 Dashboard Görünümleri
1. Genel Satış ve Ciro Analizi

2. Operasyon ve Lojistik Performansı