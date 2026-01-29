#  Astım Hastalığı Risk Değerlendirme Sistemi

## Model Performansı

**%95 Doğruluk Oranı**
- M1 (Random Forest): %94.8
- M2 (Gradient Boosting): %94.6  
- Ensemble: %94.8

## Dataset Bilgileri

- **Toplam Hasta**: 2,392
- **Özellik Sayısı**: 26
- **Astım Vakaları**: 124 (%5.2)
- **Sağlıklı Bireyler**: 2,268 (%94.8)

## Önemli Risk Faktörleri

1. **Toz Maruziyeti** (8.82%)
2. **Polen Maruziyeti** (8.55%)
3. **BMI** (8.49%)
4. **Akciğer Fonksiyonu FVC** (8.44%)
5. **Akciğer Fonksiyonu FEV1** (8.22%)
6. **Fiziksel Aktivite** (7.82%)
7. **Hava Kirliliği** (7.82%)
8. **Uyku Kalitesi** (7.55%)
9. **Diyet Kalitesi** (7.48%)
10. **Yaş** (7.44%)

## 🎯 Değerlendirme Parametreleri

### Demografik Bilgiler
- **Yaş**: Tüm yaş grupları
- **Cinsiyet**: Erkek/Kadın
- **Etnik Köken**: Çeşitli
- **Eğitim Seviyesi**: 0-3
- **BMI**: Vücut Kitle İndeksi

### Yaşam Tarzı Faktörleri
- **Sigara Kullanımı**: Evet/Hayır
- **Fiziksel Aktivite**: 0-10 skala
- **Diyet Kalitesi**: 0-10 skala
- **Uyku Kalitesi**: 0-10 skala

### Çevresel Maruziyetler
- **Hava Kirliliği**: 0-10 skala
- **Polen Maruziyeti**: 0-10 skala
- **Toz Maruziyeti**: 0-10 skala

### Tıbbi Geçmiş
- **Evcil Hayvan Alerjisi**: Evet/Hayır
- **Ailede Astım Öyküsü**: Evet/Hayır
- **Alerji Geçmişi**: Evet/Hayır
- **Egzama**: Evet/Hayır
- **Saman Nezlesi**: Evet/Hayır
- **Gastroözofageal Reflü**: Evet/Hayır

### Akciğer Fonksiyon Testleri
- **FEV1**: 1. saniye zorlu ekspirasyon hacmi
- **FVC**: Zorlu vital kapasite
- **FEV1/FVC Oranı**: < 0.7 obstrüksiyon belirtisi

### Semptomlar
- **Hırıltılı Solunum (Wheezing)**: Evet/Hayır
- **Nefes Darlığı**: Evet/Hayır
- **Göğüs Sıkışması**: Evet/Hayır
- **Öksürük**: Evet/Hayır
- **Gece Semptomları**: Evet/Hayır
- **Egzersizle Tetiklenen**: Evet/Hayır

## 🚀 Hızlı Kullanım

### 1. Model Eğitimi (Zaten yapıldı)
```bash
python asthma_model_training.py
```

### 2. Değerlendirme Sistemi
```bash
python assessment.py
```

### 3. Programatik Kullanım
```python
from assessment import AsthmaRiskAssessment

system = AsthmaRiskAssessment()

patient_data = {
    'Age': 28,
    'Gender': 1,  # 0: Erkek, 1: Kadın
    'Ethnicity': 1,
    'EducationLevel': 2,
    'BMI': 22.5,
    'Smoking': 0,  # 0: Hayır, 1: Evet
    'PhysicalActivity': 7.5,  # 0-10
    'DietQuality': 8.0,  # 0-10
    'SleepQuality': 7.5,  # 0-10
    'PollutionExposure': 2.0,  # 0-10
    'PollenExposure': 3.0,  # 0-10
    'DustExposure': 2.5,  # 0-10
    'PetAllergy': 0,  # 0: Hayır, 1: Evet
    'FamilyHistoryAsthma': 0,
    'HistoryOfAllergies': 0,
    'Eczema': 0,
    'HayFever': 0,
    'GastroesophagealReflux': 0,
    'LungFunctionFEV1': 3.5,  # Litre
    'LungFunctionFVC': 4.2,  # Litre
    'Wheezing': 0,
    'ShortnessOfBreath': 0,
    'ChestTightness': 0,
    'Coughing': 0,
    'NighttimeSymptoms': 0,
    'ExerciseInduced': 0
}

result = system.generate_report(patient_data, "Ayşe Hanım")
```

## 📊 Risk Seviyeleri

### 🟢 Çok Düşük Risk (0-20%)
- **Öneri**: Rutin yıllık kontrol
- **Tedavi**: Önleyici tedbirler
- **Takip**: Yıllık

### 🟡 Düşük Risk (20-50%)
- **Öneri**: 6 ayda bir kontrol
- **Tedavi**: Takip ve önleyici tedbirler
- **Takip**: 6 ayda bir

### 🟠 Orta Risk (50-75%)
- **Öneri**: 3 ayda bir kontrol GEREKLİ
- **Tedavi**: Kontrol edici ilaç tedavisi
- **Takip**: 3 ayda bir
- **İlaçlar**: İnhaler kortikosteroidler, beta-2 agonistler

### 🔴 Yüksek Risk (75-100%)
- **Öneri**: HEMEN göğüs hastalıkları uzmanı
- **Tedavi**: ACİL tıbbi değerlendirme
- **Takip**: Çok sık (aylık veya daha sık)
- **İlaçlar**: Yüksek doz inhaler, oral kortikosteroidler, biyolojik ajanlar

## 💊 İlaç Tedavi Seçenekleri

### Kontrol Edici İlaçlar (Uzun Süreli)
1. **İnhaler Kortikosteroidler**: İltihabı azaltır
   - Budesonid, Flutikazon, Beklometazon
   
2. **Uzun Etkili Beta-2 Agonistler (LABA)**: Hava yollarını açar
   - Formoterol, Salmeterol
   
3. **Leukotriene Antagonistleri**: İltihap azaltıcı
   - Montelukast

4. **Biyolojik Ajanlar** (Şiddetli astımda):
   - Omalizumab, Mepolizumab, Benralizumab

### Kurtarıcı İlaçlar (Acil Durumlarda)
1. **Kısa Etkili Beta-2 Agonistler (SABA)**:
   - Salbutamol (Ventolin)
   - Terbutalin

## 🏥 Acil Durum Belirtileri

**HEMEN 112 ARAYIN:**
- ❌ Dudaklar veya tırnaklar mavileşiyor
- ❌ Konuşmak çok zor
- ❌ Nefes almak için boğuşma
- ❌ Kurtarıcı ilaç işe yaramıyor
- ❌ Peak flow çok düşük (kırmızı bölge)
- ❌ Zihinsel karışıklık veya uykululuk

## 📁 Dosya Yapısı

```
asthma_models/
├── asthma_m1_rf.pkl           # M1 - Random Forest model
├── asthma_m2_gb.pkl           # M2 - Gradient Boosting model
├── asthma_m3_scaler.pkl       # M3 - Standard Scaler
├── feature_columns.pkl         # Özellik listesi
├── asthma_dataset.csv         # Tam dataset (2392 hasta)
└── model_info.json            # Model performans bilgileri

asthma_model_training.py       # Model eğitim scripti
asthma_assessment.py           # Değerlendirme sistemi
```

## 🎯 Örnek Senaryolar

### Senaryo 1: Sağlıklı Birey ✅
```
Yaş: 28, Kadın
BMI: 22.5
Sigara: Hayır
Fiziksel Aktivite: 7.5/10
Alerji Geçmişi: Hayır
Semptomlar: Yok
FEV1/FVC: 0.83 (Normal)

→ Sonuç: %7.4 risk - Rutin kontrol yeterli
```

### Senaryo 2: Orta Risk ⚠️
```
Yaş: 35, Erkek
BMI: 28.5
Sigara: Hayır
Aile Öyküsü: Var
Alerji: Var
Semptomlar: Hırıltı, öksürük, gece semptomları
FEV1/FVC: 0.72

→ Sonuç: %35-50 risk - 3 ayda bir kontrol + ilaç
```

### Senaryo 3: Yüksek Risk 🚨
```
Yaş: 42, Kadın
BMI: 32 (Obez)
Sigara: EVET
Çevresel Maruziyet: Yüksek
Tüm Semptomlar: Var
FEV1/FVC: 0.62 (Obstrüksiyon!)

→ Sonuç: HEMEN doktor + yoğun tedavi
```

## ⚠️ Önemli Notlar

1. **Model Sınırlamaları**:
   - Dataset dengesiz (%95 sağlıklı, %5 astım)
   - Gerçek klinik tanı için yeterli değil
   - Uzman hekim görüşü ZORUNLU

2. **Kullanım Amaçları**:
   - ✅ Erken tarama
   - ✅ Risk faktörü belirleme
   - ✅ Eğitim ve farkındalık
   - ❌ Kesin tanı koymak
   - ❌ Tedavi kararı vermek

3. **Güvenlik**:
   - Hasta verileri gizli tutulmalı
   - KVKK/HIPAA uyumlu olmalı
   - Profesyonel kullanım için validasyon gerekli

## 📞 Acil Durumlar

- **112**: Acil Sağlık Hizmetleri
- **En yakın hastane**: Göğüs Hastalıkları
- **Astım Okulu**: Eğitim programları

## 🔬 İleri Testler

Doktor önerebileceği testler:
- Spirometri (Akciğer fonksiyon testi)
- Bronkodilatör yanıt testi
- Metakolin challenge test
- Alerji testleri (skin prick test)
- FeNO (Exhaled nitric oxide)
- Göğüs röntgeni

## 💪 Önerilen Yaşam Tarzı Değişiklikleri

1. **Tetikleyicilerden Kaçının**:
   - Sigara dumanı
   - Hava kirliliği
   - Polen (mevsimsel)
   - Toz ve küf
   - Evcil hayvan tüyleri
   - Soğuk hava

2. **Düzenli Egzersiz**:
   - Yüzme (en iyi)
   - Yürüyüş
   - Yoga
   - Egzersiz öncesi inhaler kullanın

3. **Beslenme**:
   - Antioksidan açısından zengin
   - Omega-3 yağ asitleri
   - C ve E vitamini
   - Aşırı kilolardan kaçının

4. **Stres Yönetimi**:
   - Nefes egzersizleri
   - Meditasyon
   - Yeterli uyku

## 📚 Kaynaklar

- GINA (Global Initiative for Asthma) Kılavuzu
- Türk Toraks Derneği Astım Tanı ve Tedavi Rehberi
- WHO Astım Bilgi Sayfaları

---

**⚕️ Bu sistem bilgilendirme amaçlıdır. Astım tanısı ve tedavisi için mutlaka göğüs hastalıkları uzmanına başvurun.**
