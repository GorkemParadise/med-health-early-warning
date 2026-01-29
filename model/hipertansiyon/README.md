# Hipertansiyon (Yüksek Tansiyon) Risk Değerlendirme Sistemi

## Veri Seti

- **Kaynak:** Hipertansiyon Risk Faktörleri Veri Seti
- **Boyut:** 1,985 kayıt
- **Özellikler:** 10 sağlık ve yaşam tarzı faktörü

## Risk Seviyeleri

| Seviye | Açıklama | Aciliyet |
|--------|----------|----------|
| 0 - Minimal | Hipertansiyon riski yok/çok düşük | Düşük |
| 1 - Düşük | Prehipertansiyon eğilimi | Orta |
| 2 - Orta | Kontrollü hipertansiyon | Yüksek |
| 3 - Yüksek | İleri hipertansiyon | Çok Yüksek |

## Kullanım

### Yöntem 1: Interaktif Mod (main.py)

```bash
python main.py
```

Kullanıcıdan adım adım bilgi alır ve risk raporu oluşturur.

### Yöntem 2: API Kullanımı (assessment.py)

```python
from assessment import HypertensionRiskAssessment

# Sistemi başlat
system = HypertensionRiskAssessment()

# Hasta verisi hazırla
patient_data = {
    'Age': 55,                      # Yaş
    'Salt_Intake': 8.5,             # Günlük tuz alımı (gram)
    'Stress_Score': 6,              # Stres puanı (0-10)
    'Sleep_Duration': 6.5,          # Uyku süresi (saat)
    'BMI': 28.0,                    # Vücut Kitle İndeksi
    'BP_History_Encoded': 1,        # 0=Normal, 1=Prehipertansiyon, 2=Hipertansiyon
    'Medication_Encoded': 0,        # 0=Yok, 1=Diğer, 2=Diüretik, 3=ACE, 4=Beta Bloker
    'Family_History_Encoded': 1,    # 0=Hayır, 1=Evet
    'Exercise_Level_Encoded': 1,    # 0=Düşük, 1=Orta, 2=Yüksek
    'Smoking_Encoded': 0            # 0=Hayır, 1=Evet
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

## Veri Alanları

| Alan | Açıklama | Değer Aralığı |
|------|----------|---------------|
| Age | Yaş | 18-90 |
| Salt_Intake | Günlük tuz alımı (gram) | 2-15 |
| Stress_Score | Stres puanı | 0-10 |
| Sleep_Duration | Günlük uyku süresi (saat) | 2-12 |
| BMI | Vücut Kitle İndeksi | 15-45 |
| BP_History_Encoded | Tansiyon geçmişi | 0=Normal, 1=Pre-HT, 2=HT |
| Medication_Encoded | İlaç kullanımı | 0-4 |
| Family_History_Encoded | Aile öyküsü | 0=Hayır, 1=Evet |
| Exercise_Level_Encoded | Egzersiz seviyesi | 0=Düşük, 1=Orta, 2=Yüksek |
| Smoking_Encoded | Sigara kullanımı | 0=Hayır, 1=Evet |

## Çıktı Örneği

```
================================================================================
HİPERTANSİYON RİSK DEĞERLENDİRME RAPORU - Test Hastası
================================================================================

🎯 TAHMİN SONUCU:
   Durum: Orta Düzey Risk (Hipertansiyon - Kontrollü)
   Genel Risk Skoru: 62.5/100
   Aciliyet Seviyesi: Yüksek

📊 RİSK DAĞILIMI:
   Minimal.......................  12.3%
   Düşük (Prehipertansiyon)......  18.5%
   Orta (Kontrollü HT)...........  45.2%
   Yüksek (İleri HT).............  24.0%

👨‍⚕️ DOKTOR ÖNERİSİ:
   🚨 1-2 AY içinde kardiyoloji uzmanına başvurun
```

## Tansiyon Değerleri Referansı

| Kategori | Sistolik | Diastolik |
|----------|----------|-----------|
| Normal | <120 | <80 |
| Yüksek-Normal | 120-129 | <80 |
| Evre 1 HT | 130-139 | 80-89 |
| Evre 2 HT | ≥140 | ≥90 |
| Hipertansif Kriz | >180 | >120 |

## Önemli Uyarılar

1. **Bu sistem TIBBİ TANI KOYMAZ!**
2. Sonuçlar sadece BİLGİLENDİRME amaçlıdır
3. Kesin tanı için mutlaka kardiyoloji uzmanına başvurun
4. Hipertansiyon tanısı için düzenli tansiyon ölçümü şarttır
5. Evde tansiyon takibi önerilir

## DASH Diyeti Önerileri

Hipertansiyon riski olanlar için önerilen DASH diyeti:
- Bol meyve ve sebze
- Az yağlı süt ürünleri
- Tam tahıllar
- Az kırmızı et, şeker ve tuz
- Potasyum, magnezyum ve kalsiyum açısından zengin besinler

---
