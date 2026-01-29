# Parkinson Hastalığı Risk Değerlendirme Sistemi 

## Genel Bakış

Bu sistem, hastaların Parkinson hastalığı riskini ve şiddetini değerlendirmek için makine öğrenimi modellerini kullanır. Sistem, klinik parametrelere dayanarak hastaları 4 kategoriye ayırır ve tedavi önerileri sunar.

## Özellikler

- **%85 doğruluk oranı** ile risk tahmini
- **4 seviye risk sınıflandırması**: Yok, Hafif, Orta, İleri
- **Kişiselleştirilmiş tedavi önerileri**
- **Detaylı risk faktörü analizi**
- **İlaç, cerrahi ve rehabilitasyon önerileri**

## Risk Seviyeleri

### 0️ Minimal Risk (Risk Yok)
- **Risk Skoru**: 0-25/100
- **Öneri**: Yıllık kontrol
- **Tedavi**: Önleyici yaşam tarzı değişiklikleri
- **Takip**: Yıllık

### 1️ Hafif Parkinson
- **Risk Skoru**: 25-50/100
- **Öneri**: 1-2 ay içinde nöroloji uzmanına başvuru
- **Tedavi**: İlaç tedavisi (Levodopa/Dopamin agonistleri)
- **Takip**: 3-6 ayda bir

### 2️ Orta Düzey Parkinson
- **Risk Skoru**: 50-75/100
- **Öneri**: 1-2 HAFTA içinde ACİL nöroloji konsültasyonu
- **Tedavi**: Kombine ilaç tedavisi + Yoğun rehabilitasyon
- **Takip**: AYLIK kontrol ZORUNLU

### 3️ İleri Parkinson
- **Risk Skoru**: 75-100/100
- **Öneri**: HEMEN hareket bozuklukları merkezine sevk
- **Tedavi**: Cerrahi değerlendirme (DBS) + Maksimum ilaç tedavisi
- **Takip**: Haftalık/2 haftada bir

## Değerlendirme Parametreleri

### Motor Belirtiler (0-5 skala)
- **Tremor (Titreme)**: El, kol veya bacaklarda titreme
- **Rijidite (Kas Sertliği)**: Kasların sertleşmesi
- **Bradikinezi (Yavaş Hareket)**: Hareket başlatma ve yürütme zorluğu
- **Postural İnstabilite**: Denge problemleri

### Klinik Ölçümler
- **Motor UPDRS**: 0-100 arası (Unified Parkinson's Disease Rating Scale)
- **Hastalık Süresi**: Semptomların başlangıcından itibaren yıl
- **Levodopa Yanıtı**: 0-100% tedaviye yanıt

### Ses Özellikleri (Otomatik hesaplanır)
- **Jitter**: Ses frekans değişkenliği
- **Shimmer**: Ses genlik değişkenliği
- **NHR**: Gürültü-harmonik oranı
- **HNR**: Harmonik-gürültü oranı

## Kullanım

### Yöntem 1: İnteraktif Kullanım (En Kolay)

```bash
python main.py
```

Program sırayla soracak:
1. Hasta adı
2. Yaş
3. Motor belirtiler (tremor, rijidite, vb.)
4. UPDRS skoru
5. Hastalık süresi
6. Levodopa yanıtı

### Yöntem 2: Python Kodu ile

```python
from assessment import ParkinsonRiskAssessment

# Sistemi başlat
system = ParkinsonRiskAssessment()

# Hasta verilerini hazırla
hasta_verileri = {
    'age': 65,
    'motor_updrs': 28,
    'total_updrs': 38,
    'jitter': 0.0065,
    'shimmer': 0.035,
    'nhr': 0.025,
    'hnr': 18,
    'tremor_score': 2.1,
    'rigidity': 1.8,
    'bradykinesia': 2.3,
    'postural_instability': 1.2,
    'disease_duration': 1.5,
    'levodopa_response': 75
}

# Rapor oluştur
system.generate_report(hasta_verileri, "Ahmet Bey")
```

## 📁 Dosya Yapısı

```
parkinson_model/
├── parkinson_model.py              # Model eğitim scripti
├── parkinson_assessment.py         # Risk değerlendirme sistemi
├── parkinson_interactive.py        # İnteraktif kullanıcı arayüzü
├── parkinson_rf_model.pkl          # Random Forest modeli
├── parkinson_gb_model.pkl          # Gradient Boosting modeli
├── parkinson_scaler.pkl            # Veri normalizasyon scaler'ı
├── parkinson_dataset.csv           # Eğitim verileri
└── README.md                       # Bu dosya
```

## 🔍 Model Detayları

### Kullanılan Algoritmalar
1. **Random Forest Classifier**: 200 ağaç, max_depth=15
2. **Gradient Boosting Classifier**: 150 ağaç, learning_rate=0.1
3. **Ensemble Method**: İki modelin ortalaması

### Performans Metrikleri
- **Doğruluk (Accuracy)**: ~85%
- **Precision**: 0.79-0.86
- **Recall**: 0.81-0.85
- **F1-Score**: 0.80-0.83

### En Önemli Özellikler (Feature Importance)
1. Jitter (19.9%)
2. Bradikinezi (11.6%)
3. Tremor Skoru (11.5%)
4. Rijidite (11.4%)
5. Shimmer (10.0%)

## ⚠️ Önemli Notlar

### ⚕️ Tıbbi Uyarı
- Bu sistem **BİLGİLENDİRME** amaçlıdır
- Kesin tanı için **MUTLAKA** nöroloji uzmanına başvurun
- Klinik değerlendirme gereklidir
- Tedavi kararları sadece uzman hekim tarafından verilmelidir

### Veri Gizliliği
- Hasta verileri sadece analiz sırasında kullanılır
- Veriler harici sunuculara gönderilmez
- Gizlilik ve güvenlik önceliklidir

### Limitasyonler
- Model sentetik verilerle eğitilmiştir
- Gerçek klinik uygulamada validasyon gereklidir
- Sadece belirli parametreleri değerlendirir
- Diğer nörolojik hastalıklarla ayırıcı tanı yapmaz

## Klinik Referanslar

### UPDRS (Unified Parkinson's Disease Rating Scale)
- **0-32**: Hafif
- **33-58**: Orta
- **59-108**: Şiddetli
- **109+**: Çok şiddetli

### Hoehn & Yahr Evreleme
- **Evre 1**: Tek taraflı belirtiler
- **Evre 2**: İki taraflı belirtiler
- **Evre 3**: Postural instabilite
- **Evre 4**: Ciddi sakatlık
- **Evre 5**: Tekerlekli sandalye/yatağa bağımlı

## Tedavi Seçenekleri

### İlaç Tedavisi
- **Levodopa**: Altın standart tedavi
- **Dopamin Agonistleri**: Pramipeksol, Ropinirol
- **MAO-B İnhibitörleri**: Rasajilin, Selejilin
- **COMT İnhibitörleri**: Entakapon, Tolkapon

### Cerrahi Tedavi
- **DBS (Derin Beyin Stimülasyonu)**: STN veya GPi hedefleme
- **Apomorfin Pompası**: Sürekli infüzyon
- **Duodopa**: Jejunal Levodopa infüzyonu

### Rehabilitasyon
- **Fizik Tedavi**: Denge, kuvvet, esneklik
- **Konuşma Terapisi**: Disartri, yutma
- **Ergoterapi**: Günlük yaşam aktiviteleri

## Destek ve İletişim

Bu sistem, Parkinson hastalığı ile mücadele eden hastalara ve ailelerine yardımcı olmak için geliştirilmiştir.

**Acil Durumlar İçin**:
- 112 - Acil Sağlık Hizmetleri
- En yakın hastane acil servisi

**Destek Grupları**:
- Türkiye Parkinson Hastalığı Derneği
- Nöroloji klinikleri hasta destek programları

## Versiyon Geçmişi

**v1.0.0** (2026-01-30)
- İlk versiyon
- Random Forest + Gradient Boosting ensemble
- 4 seviye risk sınıflandırması
- Detaylı tedavi önerileri
- İnteraktif kullanıcı arayüzü

---

**⚕️ Sağlığınız bizim için önemli. Lütfen düzenli kontrolleri ihmal etmeyin.**