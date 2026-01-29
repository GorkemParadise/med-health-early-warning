# Diyabet Hastalığı Risk Değerlendirme Sistemi

Bu proje, makine öğrenmesi kullanarak diyabet hastalığı risk değerlendirmesi yapan bir sistemdir. Kullanıcıdan alınan sağlık bilgilerine göre kişinin diyabet riskini tahmin eder ve detaylı öneriler sunar.

## Veri Seti

- **Kaynak:** CDC Behavioral Risk Factor Surveillance System (BRFSS)
- **Boyut:** 253,680 kayıt
- **Özellikler:** 21 sağlık ve yaşam tarzı faktörü

## Risk Seviyeleri

| Seviye | Açıklama | Aciliyet |
|--------|----------|----------|
| 0 - Minimal | Diyabet riski yok/çok düşük | Düşük |
| 1 - Düşük | Risk faktörleri var, dikkat gerekli | Orta |
| 2 - Orta | Prediyabet olabilir | Yüksek |
| 3 - Yüksek | Diyabet olabilir | Çok Yüksek |

## Kullanım

### Yöntem 1: Interaktif Mod (main.py)

```bash
python main.py
```

Kullanıcıdan adım adım bilgi alır ve risk raporu oluşturur.

### Yöntem 2: API Kullanımı (assessment.py)

```python
from assessment import DiabetesRiskAssessment

# Sistemi başlat
system = DiabetesRiskAssessment()

# Hasta verisi hazırla
patient_data = {
    'HighBP': 1,              # Yüksek tansiyon (0/1)
    'HighChol': 1,            # Yüksek kolesterol (0/1)
    'CholCheck': 1,           # Son 5 yılda kolesterol kontrolü (0/1)
    'BMI': 32.5,              # Vücut Kitle İndeksi
    'Smoker': 1,              # Sigara (0/1)
    'Stroke': 0,              # İnme geçmişi (0/1)
    'HeartDiseaseorAttack': 0, # Kalp hastalığı (0/1)
    'PhysActivity': 0,        # Fiziksel aktivite (0/1)
    'Fruits': 1,              # Günlük meyve tüketimi (0/1)
    'Veggies': 1,             # Günlük sebze tüketimi (0/1)
    'HvyAlcoholConsump': 0,   # Ağır alkol (0/1)
    'AnyHealthcare': 1,       # Sağlık sigortası (0/1)
    'NoDocbcCost': 0,         # Maliyet engeli (0/1)
    'GenHlth': 3,             # Genel sağlık (1-5)
    'MentHlth': 5,            # Mental sağlık günleri (0-30)
    'PhysHlth': 10,           # Fiziksel sağlık günleri (0-30)
    'DiffWalk': 0,            # Yürüme zorluğu (0/1)
    'Sex': 1,                 # Cinsiyet (0=Kadın, 1=Erkek)
    'Age': 9,                 # Yaş kategorisi (1-13)
    'Education': 5,           # Eğitim (1-6)
    'Income': 6,              # Gelir (1-8)
    '_real_age': 58           # Gerçek yaş (opsiyonel)
}

# Rapor oluştur
system.generate_report(patient_data, "Test Hastası")

# Veya sadece değerlendirme al
result = system.assess_risk(patient_data)
print(f"Risk Skoru: {result['genel_risk_skoru']}")
print(f"Tahmin: {result['tahmin']}")
```

### Yöntem 3: Örnek Hastaları Çalıştır

```bash
python assessment.py
```

5 farklı risk seviyesinde örnek hasta çıktısı görüntüler.

## 📋 Veri Alanları

| Alan | Açıklama | Değer Aralığı |
|------|----------|---------------|
| HighBP | Yüksek tansiyon | 0=Hayır, 1=Evet |
| HighChol | Yüksek kolesterol | 0=Hayır, 1=Evet |
| CholCheck | Kolesterol kontrolü (5 yıl) | 0=Hayır, 1=Evet |
| BMI | Vücut Kitle İndeksi | 12-98 |
| Smoker | Sigara (100+ sigara içmiş) | 0=Hayır, 1=Evet |
| Stroke | İnme geçmişi | 0=Hayır, 1=Evet |
| HeartDiseaseorAttack | Kalp hastalığı/krizi | 0=Hayır, 1=Evet |
| PhysActivity | Fiziksel aktivite (30 gün) | 0=Hayır, 1=Evet |
| Fruits | Günlük meyve | 0=Hayır, 1=Evet |
| Veggies | Günlük sebze | 0=Hayır, 1=Evet |
| HvyAlcoholConsump | Ağır alkol | 0=Hayır, 1=Evet |
| AnyHealthcare | Sağlık sigortası | 0=Hayır, 1=Evet |
| NoDocbcCost | Maliyet nedeniyle doktora gidememe | 0=Hayır, 1=Evet |
| GenHlth | Genel sağlık durumu | 1=Mükemmel, 5=Kötü |
| MentHlth | Kötü mental sağlık günleri | 0-30 |
| PhysHlth | Kötü fiziksel sağlık günleri | 0-30 |
| DiffWalk | Yürüme/merdiven zorluğu | 0=Hayır, 1=Evet |
| Sex | Cinsiyet | 0=Kadın, 1=Erkek |
| Age | Yaş kategorisi | 1-13 (her 5 yıl) |
| Education | Eğitim seviyesi | 1-6 |
| Income | Gelir seviyesi | 1-8 |


## Çıktı Örneği

```
================================================================================
DİYABET HASTALIĞI RİSK DEĞERLENDİRME RAPORU - Test Hastası
================================================================================

🎯 TAHMİN SONUCU:
   Durum: Orta Düzey Risk (Prediyabet Olabilir)
   Genel Risk Skoru: 58.5/100
   Aciliyet Seviyesi: Yüksek

📊 RİSK DAĞILIMI:
   Minimal..................  15.2%
   Düşük....................  22.3%
   Orta (Prediyabet)........  38.5%
   Yüksek (Diyabet).........  24.0%

👨‍⚕️ DOKTOR ÖNERİSİ:
   🚨 1-2 AY içinde endokrinoloji/dahiliye uzmanına başvurun
```

## ⚠️ Önemli Uyarılar

1. **Bu sistem TIBBİ TANI KOYMAZ!**
2. Sonuçlar sadece BİLGİLENDİRME amaçlıdır
3. Kesin tanı için mutlaka doktora başvurun
4. Diyabet tanısı SADECE kan testleriyle konur:
   - Açlık Kan Şekeri (FPG) ≥ 126 mg/dL
   - HbA1c ≥ %6.5
   - OGTT 2. saat ≥ 200 mg/dL


---

**Not:** Bu sistem, CDC BRFSS veri seti kullanılarak eğitilmiştir. Model, risk faktörlerine göre tahmin yapar ancak klinik testlerin yerini tutmaz.
