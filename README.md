# 🧾 SOAP Invoice Service

Python ile geliştirilmiş, SOAP protokolü kullanan fatura oluşturma servisi. Flask tabanlı SOAP server, Zeep tabanlı client ve SQLAlchemy ORM ile SQLite veritabanından oluşmaktadır.

---

## 📌 Proje Hakkında

Bu proje, Türkiye'deki kurumsal ve fintech sektöründe yaygın olarak kullanılan SOAP/Web Services teknolojisini öğrenmek ve uygulamak amacıyla geliştirilmiştir. Client tarafından gönderilen fatura bilgileri XML formatında SOAP server'a iletilir, server tarafında işlenerek veritabanına kaydedilir ve benzersiz bir fatura numarası üretilir.

---

## 🏗️ Mimari

```
client.py
    └── XML isteği gönderir (Zeep)
            ↓
server.py
    └── SOAP isteğini dinler, XML'i parse eder (Flask + lxml)
            ↓
service.py
    └── İş mantığı: fatura oluşturur, toplam tutar hesaplar
            ↓
database.py + models.py
    └── SQLAlchemy ORM ile SQLite veritabanına kaydeder
```

---

## 📁 Dosya Yapısı

```
create_invoice/
├── server.py        # Flask tabanlı SOAP sunucusu, WSDL tanımı
├── service.py       # Fatura oluşturma iş mantığı
├── database.py      # Veritabanı bağlantısı ve session yönetimi
├── models.py        # SQLAlchemy ORM tablo tanımı
├── client.py        # Zeep tabanlı SOAP client (test amaçlı)
├── invoice.wsdl     # Web servis tanım dosyası
├── .gitignore
└── README.md
```

---

## 🔧 Kurulum

```bash
# Repoyu klonla
git clone https://github.com/gulerdeniz/create_invoice.git
cd create_invoice

# Sanal ortam oluştur
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Bağımlılıkları yükle
pip install flask zeep lxml sqlalchemy
```

---

## 🚀 Kullanım

**1. Server'ı başlat:**
```bash
python server.py
```

**2. Yeni bir terminalde client'ı çalıştır:**
```bash
python client.py
```

**3. Çıktı:**
```
Fatura No: f47ac10b-58cc-4372-a567-0e02b2c3d479
```

---

## 📋 WSDL ve SOAP Akışı

WSDL (Web Service Description Language) servisin "menüsü" gibidir. Client önce WSDL'i okur, hangi fonksiyonların mevcut olduğunu ve hangi parametrelerin gerektiğini öğrenir.

`GET http://localhost:8000/soap?wsdl` → WSDL döner

`POST http://localhost:8000/soap` → Fatura isteği işlenir

---

## 🗃️ Veritabanı Şeması

`fatura_bilgileri` tablosu:

| Kolon | Tip | Açıklama |
|---|---|---|
| id | Integer | Otomatik artan birincil anahtar |
| fatura_no | String | UUID ile üretilen benzersiz fatura numarası |
| tarih | Date | Otomatik atanan işlem tarihi |
| alici_isim | String | Alıcı adı |
| satici_firma | String | Satıcı firma adı |
| urun_adi | String | Ürün adı |
| miktar | Integer | Adet |
| fiyat | Float | Birim fiyat |
| kdv_orani | Float | KDV oranı (örn: 0.20 = %20) |
| toplam_tutar | Float | fiyat × miktar × (1 + kdv_orani) |

---

## 🛠️ Kullanılan Teknolojiler

- **Python** — Ana programlama dili
- **Flask** — SOAP sunucusu için HTTP framework
- **Zeep** — SOAP client kütüphanesi
- **lxml** — XML parse işlemleri
- **SQLAlchemy** — ORM ve veritabanı yönetimi
- **SQLite** — Yerel veritabanı
- **SOAP/Web Services** — Servis iletişim protokolü
- **WSDL** — Web servis tanım dili
- **UUID** — Benzersiz fatura numarası üretimi

---

## 👤 Geliştirici

**Deniz Güler**
[GitHub](https://github.com/gulerdeniz) | Manisa, Türkiye
