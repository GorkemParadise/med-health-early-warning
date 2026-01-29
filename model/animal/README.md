# Akdeniz Bölgesi Hayvan Isırığı/Sokması Risk Değerlendirme Sistemi

## Veri Seti

- **Kaynak:** WHO, CDC, NCBI, Nature Communications epidemiyolojik verileri
- **Boyut:** 5,000 sentetik kayıt (gerçek epidemiyolojik dağılımlara dayalı)
- **Özellikler:** 13 risk faktörü

## Desteklenen Hayvan Türleri

| Hayvan | Akdeniz Riski | Kritik Dönem |
|--------|---------------|--------------|
| 🐍 Yılan (Engerek) | Yüksek | Nisan-Ekim |
| 🐕 Köpek | Orta | Tüm yıl |
| 🐝 Arı/Eşek Arısı | Orta-Yüksek | Nisan-Eylül |
| 🦂 Akrep | Yüksek | Mayıs-Eylül |
| 🐱 Kedi | Düşük-Orta | Tüm yıl |

## Risk Seviyeleri

| Seviye | Açıklama | Aksiyon |
|--------|----------|---------|
| 0 - Minimal | Ciddi risk yok | Evde gözlem |
| 1 - Düşük | Dikkat gerekli | 24 saat içinde başvuru |
| 2 - Orta | Tıbbi müdahale gerekli | HEMEN başvuru |
| 3 - Yüksek | ACİL DURUM | 112'yi arayın! |

## Kullanım

### Yöntem 1: Interaktif Mod (main.py)

```bash
python main.py
```

Kullanıcıdan adım adım bilgi alır ve risk raporu oluşturur.

### Yöntem 2: API Kullanımı (assessment.py)

```python
from assessment import AnimalBiteRiskAssessment

# Sistemi başlat
system = AnimalBiteRiskAssessment()

# Hasta verisi hazırla
patient_data = {
    'Age': 45,                    # Yaş
    'Gender': 1,                  # 0=Kadın, 1=Erkek
    'Location': 0,                # 0=Kırsal, 1=Şehir, 2=Banliyö
    'Season': 1,                  # 0=İlkbahar, 1=Yaz, 2=Sonbahar, 3=Kış
    'Time_of_Day': 2,             # 0=Sabah, 1=Öğle, 2=Akşam, 3=Gece
    'Animal_Type': 0,             # 0=Yılan, 1=Köpek, 2=Arı, 3=Akrep, 4=Kedi
    'Body_Part': 0,               # 0=Alt ext, 1=Üst ext, 2=El, 3=Yüz, 4=Boyun
    'Occupation_Risk': 0,         # 0=Çiftçi, 1=Dış mekan, 2=Öğrenci, 3=Şehir
    'Allergy_History': 0,         # 0=Hayır, 1=Evet
    'Previous_Bite': 0,           # 0=Hayır, 1=Evet
    'First_Aid_Applied': 1,       # 0=Hayır, 1=Evet
    'Hospital_Time_Hours': 2.0,   # Hastaneye ulaşım süresi
    'Chronic_Disease': 0          # 0=Hayır, 1=Evet
}

# Rapor oluştur
system.generate_report(patient_data, "Test Hastası")

# Veya sadece değerlendirme al
result = system.assess_risk(patient_data)
print(f"Risk Skoru: {result['genel_risk_skoru']}")
print(f"Tahmin: {result['tahmin']}")
print(f"Aciliyet: {result['aciliyet']}")
```

### Yöntem 3: Örnek Vakaları Çalıştır

```bash
python assessment.py
```

5 farklı senaryo için örnek çıktı görüntüler.

## 📋 Veri Alanları

| Alan | Açıklama | Değer Aralığı |
|------|----------|---------------|
| Age | Yaş | 1-90 |
| Gender | Cinsiyet | 0=Kadın, 1=Erkek |
| Location | Konum | 0=Kırsal, 1=Şehir, 2=Banliyö |
| Season | Mevsim | 0-3 (İlkbahar-Kış) |
| Time_of_Day | Günün zamanı | 0-3 (Sabah-Gece) |
| Animal_Type | Hayvan türü | 0-4 |
| Body_Part | Isırık bölgesi | 0-4 |
| Occupation_Risk | Meslek riski | 0-3 |
| Allergy_History | Alerji öyküsü | 0/1 |
| Previous_Bite | Önceki ısırık | 0/1 |
| First_Aid_Applied | İlk yardım | 0/1 |
| Hospital_Time_Hours | Hastane süresi | 0.25-12 saat |
| Chronic_Disease | Kronik hastalık | 0/1 |


## Hayvan Türlerine Göre Tedavi

### Yılan Isırığı
- **İlk Yardım:** Sakin kal, hareket etme, kalp altında tut
- **YAPMA:** Kesme, emme, turnike, buz
- **Tedavi:** Antivenom (ilk 4-6 saat kritik)
- **Akdeniz türleri:** Engerek, Kocabaş engerek

### Köpek Isırığı
- **İlk Yardım:** 10-15 dk sabunlu su ile yıka
- **Tedavi:** Kuduz aşısı (şüpheli köpek), antibiyotik
- **Kritik:** Sahipsiz köpek = Kuduz riski!

### Arı/Eşek Arısı Sokması
- **İlk Yardım:** İğneyi kazı (sıkma!), buz, antihistaminik
- **Tedavi:** Epinefrin (anafilaksi), kortikosteroid
- **Kritik:** Alerji öyküsü = ANAFİLAKSİ RİSKİ!

### Akrep Sokması
- **İlk Yardım:** Yıka, buz, sakin kal
- **Tedavi:** Antivenom, kas gevşetici
- **Akdeniz türü:** Sarı akrep (çocuklarda tehlikeli!)

### Kedi Isırığı
- **İlk Yardım:** Bol su ve sabunla yıka
- **Tedavi:** Antibiyotik (enfeksiyon riski %30-50!)
- **Kritik:** Derin ısırıklar = Yüksek enfeksiyon

## ⚠️ Önemli Uyarılar

1. **Bu sistem TIBBİ TANI KOYMAZ!**
2. Hayvan ısırığı/sokması durumunda MUTLAKA sağlık kuruluşuna başvurun
3. Yılan ve akrep ısırıklarında ZAMAN KRİTİKTİR
4. Arı alerjisi olanlar EpiPen bulundurmalı
5. Kuduz şüphesi varsa 24 saat içinde aşı başlanmalı

## 📞 Acil Numaralar

- **112** - Acil Yardım
- **182** - Zehir Danışma
- **Antivenom:** Devlet hastaneleri, üniversite hastaneleri

**Not:** Bu sistem epidemiyolojik verilere dayalı risk tahmini yapar ancak klinik değerlendirmenin yerini tutmaz. Her hayvan ısırığı/sokması vakasında profesyonel sağlık hizmeti alınmalıdır.

## 📊 Akdeniz Bölgesi İstatistikleri

| İstatistik | Değer |
|------------|-------|
| Yılan ısırığı (yıllık) | ~5,000 vaka |
| Köpek ısırığı (yıllık) | ~100,000+ vaka |
| Arı sokması (yıllık) | ~50,000+ vaka |
| Akrep sokması (yıllık) | ~10,000 vaka |
| Ölüm (tüm türler) | ~10-20/yıl |

*Kaynak: WHO, Sağlık Bakanlığı verileri*
