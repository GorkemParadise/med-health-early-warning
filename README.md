# Early Warning System for Mediterranean Health Risks - Hackathon

- **AI-powered early risk awareness platform for underserved Mediterranean regions.**

```
Akdeniz bölgesi, özellikle sağlık sistemlerini etkileyen ve savunmasız nüfus için eşitsizlikleri artıran doğal afetler, çevresel kırılganlıklar 
ve jeopolitik gerilimlerden kaynaklanan önemli zorluklarla karşı karşıyadır. 
COVID-19 pandemisi, acil durum hazırlığı ve müdahalesindeki zayıflıkları daha da ortaya çıkarmıştır. 
Bu proje, yapay zekayı (YZ) kullanarak acil sağlık sistemlerini geliştirmeyi, 
kaynakların daha iyi koordinasyonunu ve önceliklendirilmesini sağlamayı ve Lübnan, Filistin, İtalya, Türkiye ve İspanya'daki toplulukların dayanıklılığını güçlendirmeyi amaçlamaktadır.
```

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/React-18.2-61DAFB?style=for-the-badge&logo=react" alt="React"/>
  <img src="https://img.shields.io/badge/TypeScript-5.3-3178C6?style=for-the-badge&logo=typescript" alt="TypeScript"/>
  <img src="https://img.shields.io/badge/Accuracy-90%25+-green?style=for-the-badge" alt="Accuracy"/>
</p>

## Proje Hakkında

**MEDAIGENCY AI4PURPOSE Hackathon 2026** için geliştirilmiş yapay zeka destekli bir sağlık risk değerlendirme platformudur. Platform, 5 farklı hastalık için makine öğrenmesi tabanlı risk analizi sunmaktadır.

### Özellikler

- **5 AI Modeli**: Astım, Diyabet, Hipertansiyon, Parkinson, Hayvan Isırığı
- **%90+ Doğruluk**: Ensemble learning (Random Forest + Gradient Boosting)
- **Modern UI**: Glassmorphism tasarım, interaktif grafikler
- **Real-time**: Anında risk değerlendirme
- **Responsive**: Mobil uyumlu tasarım

## Mimari

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React + TypeScript)           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │  Hero   │  │ Models  │  │  Demo   │  │   Analytics     ││
│  │ Section │  │ Section │  │ Section │  │    Section      ││
│  └─────────┘  └─────────┘  └─────────┘  └─────────────────┘│
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST API
┌───────────────────────────▼─────────────────────────────────┐
│                     BACKEND (FastAPI)                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    API Endpoints                         ││
│  │  /api/predict/asthma    │  /api/predict/diabetes        ││
│  │  /api/predict/hypertension │ /api/predict/parkinson     ││
│  │  /api/predict/animal_bite  │ /api/statistics            ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    ML Models                             ││
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                 ││
│  │  │ Random   │ │ Gradient │ │ Scaler   │                 ││
│  │  │ Forest   │ │ Boosting │ │          │                 ││
│  │  └──────────┘ └──────────┘ └──────────┘                 ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 📊 Model Performansı

| Model | Doğruluk | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| 🫁 Astım | **94.8%** | 0.93 | 0.95 | 0.94 |
| 🩸 Diyabet | **92.5%** | 0.91 | 0.93 | 0.92 |
| ❤️ Hipertansiyon | **95.3%** | 0.88 | 0.90 | 0.89 |
| 🧠 Parkinson | **89.0%** | 0.83 | 0.86 | 0.84 |
| 🦂 Hayvan Isırığı | **93.5%** | 0.86 | 0.88 | 0.87 |

## Kurulum

### Gereksinimler

- Python 3.11+
- Node.js 18+
- npm veya yarn

### Backend Kurulumu

```bash
# Backend dizinine git
cd backend

# Sanal ortam oluştur
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Sunucuyu başlat
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Kurulumu

```bash
# Frontend dizinine git
cd frontend

# Bağımlılıkları yükle
npm install

# Geliştirme sunucusunu başlat
npm run dev
```


## Proje Yapısı

```
med-health-early-warning/
├── backend/
│   ├── main.py              # FastAPI uygulaması
│   ├── requirements.txt     # Python bağımlılıkları
│
├──│models/                  # Eğitilmiş ML modelleri
│   ├── animal/
│   ├── astım/
│   ├── city/
│   ├── diyabet/
│   └── hipertansiyon/
│   └── parkinson/
│
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Ana uygulama bileşeni
│   │   ├── main.tsx         # Giriş noktası
│   │   └── index.css        # Global stiller
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
└── README.md
```

## Güvenlik & Gizlilik

- Tüm veriler lokal olarak işlenir
- Hiçbir hasta verisi sunuculara gönderilmez
- HTTPS üzerinden güvenli iletişim
- CORS koruması aktif

## Yasal Uyarı

> **Bu platform sadece BİLGİLENDİRME amaçlıdır ve TIBBİ TANI KOYMAZ.**
> 
> Sağlık sorunlarınız için mutlaka bir sağlık profesyoneline danışın.
> Sonuçlar kesin tanı değildir ve klinik değerlendirmenin yerini tutmaz.
