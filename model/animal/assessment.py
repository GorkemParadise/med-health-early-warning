import os, pickle
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class AnimalBiteRiskAssessment:
    """Akdeniz Bölgesi Hayvan Isırığı/Sokması Risk Değerlendirme Sistemi"""
    
    # Sabitler
    ANIMALS = ['Yılan', 'Köpek', 'Arı/Eşek Arısı', 'Akrep', 'Kedi']
    ANIMALS_EN = ['Snake', 'Dog', 'Bee_Wasp', 'Scorpion', 'Cat']
    LOCATIONS = ['Kırsal', 'Şehir', 'Banliyö']
    SEASONS = ['İlkbahar', 'Yaz', 'Sonbahar', 'Kış']
    TIMES = ['Sabah', 'Öğle', 'Akşam', 'Gece']
    BODY_PARTS = ['Alt Ekstremite', 'Üst Ekstremite', 'El', 'Yüz/Baş', 'Boyun/Gövde']
    OCCUPATIONS = ['Çiftçi/Tarım', 'Dış Mekan İşçisi', 'Öğrenci/Çocuk', 'Şehir İşçisi']
    
    def __init__(self):
        with open(os.path.join(BASE_DIR, "m1.pkl"), "rb") as f:
            self.rf_model = pickle.load(f)
        with open(os.path.join(BASE_DIR, "m2.pkl"), "rb") as f:
            self.gb_model = pickle.load(f)
        with open(os.path.join(BASE_DIR, "m3.pkl"), "rb") as f:
            self.scaler = pickle.load(f)
    
    def assess_risk(self, patient_data):
        """Risk değerlendirmesi yap"""
        feature_cols = ['Age', 'Gender', 'Location', 'Season', 'Time_of_Day', 'Animal_Type',
                        'Body_Part', 'Occupation_Risk', 'Allergy_History', 'Previous_Bite',
                        'First_Aid_Applied', 'Hospital_Time_Hours', 'Chronic_Disease']
        
        df = pd.DataFrame([patient_data])
        X_scaled = self.scaler.transform(df[feature_cols])
        
        rf_proba = self.rf_model.predict_proba(X_scaled)[0]
        gb_proba = self.gb_model.predict_proba(X_scaled)[0]
        ensemble_proba = (rf_proba + gb_proba) / 2
        predicted_severity = np.argmax(ensemble_proba)
        
        risk_percentages = {
            'minimal': ensemble_proba[0] * 100,
            'dusuk': ensemble_proba[1] * 100,
            'orta': ensemble_proba[2] * 100,
            'yuksek': ensemble_proba[3] * 100
        }
        
        overall_risk = (ensemble_proba[1] * 25 + ensemble_proba[2] * 60 + ensemble_proba[3] * 100)
        assessment = self._generate_assessment(predicted_severity, risk_percentages, 
                                                overall_risk, patient_data)
        return assessment
    
    def _generate_assessment(self, severity, percentages, overall_risk, data):
        """Değerlendirme ve öneriler oluştur"""
        
        animal = self.ANIMALS[data['Animal_Type']]
        
        severity_names = {
            0: f"{animal} Isırığı/Sokması - Minimal Risk",
            1: f"{animal} Isırığı/Sokması - Düşük Risk",
            2: f"{animal} Isırığı/Sokması - Orta Düzey Risk",
            3: f"{animal} Isırığı/Sokması - Yüksek Risk"
        }
        
        result = {
            'tahmin': severity_names[severity],
            'seviye': severity,
            'hayvan': animal,
            'genel_risk_skoru': round(overall_risk, 1),
            'risk_dagilimi': {
                'Minimal': round(percentages['minimal'], 1),
                'Düşük': round(percentages['dusuk'], 1),
                'Orta': round(percentages['orta'], 1),
                'Yüksek': round(percentages['yuksek'], 1)
            }
        }
        
        # Hayvan türüne göre özel tedavi
        result['tedavi'] = self._get_animal_treatment(data['Animal_Type'], severity, data)
        
        # Genel aciliyet
        if severity == 0:
            result['aciliyet'] = 'Düşük'
            result['takip'] = 'Evde gözlem yeterli, belirtiler kötüleşirse başvurun'
        elif severity == 1:
            result['aciliyet'] = 'Orta'
            result['takip'] = '24 saat içinde sağlık kuruluşuna başvurun'
        elif severity == 2:
            result['aciliyet'] = 'Yüksek'
            result['takip'] = 'HEMEN sağlık kuruluşuna başvurun'
        else:
            result['aciliyet'] = 'ÇOK YÜKSEK - ACİL'
            result['takip'] = '112\'yi HEMEN arayın!'
        
        # Risk faktörleri
        result['risk_faktorleri'] = self._analyze_risk_factors(data)
        
        return result
    
    def _get_animal_treatment(self, animal_type, severity, data):
        """Hayvan türüne göre tedavi önerileri"""
        treatments = {
            0: {  # Yılan
                'ilk_yardim': [
                    '• Sakin kalın, hareket etmeyin',
                    '• Isırık bölgesini kalp altında tutun',
                    '• Sıkı giysi/takı çıkarın',
                    '• YAPMAYIN: Kesme, emme, turnike, buz'
                ],
                'tibbi': [
                    '• ANTİVENOM değerlendirmesi',
                    '• Tetanos profilaksisi',
                    '• Yara bakımı ve antibiyotik',
                    '• Vital bulgular takibi',
                    '• Koagülasyon testleri'
                ],
                'uyari': 'Akdeniz\'de engerek yılanları yaygın. İlk 4-6 saat kritik!'
            },
            1: {  # Köpek
                'ilk_yardim': [
                    '• Yarayı 10-15 dk su ve sabunla yıkayın',
                    '• Antiseptik uygulayın',
                    '• Temiz bezle kapatın',
                    '• Kanama varsa baskı uygulayın'
                ],
                'tibbi': [
                    '• KUDUZ RİSKİ değerlendirmesi',
                    '• Kuduz aşısı (gerekirse)',
                    '• Tetanos profilaksisi',
                    '• Antibiyotik tedavisi',
                    '• Yara debridmanı (gerekirse)'
                ],
                'uyari': 'Sahipsiz köpek ısırığında KUDUZ AŞISI gerekebilir!'
            },
            2: {  # Arı
                'ilk_yardim': [
                    '• İğneyi KAZIYARAK çıkarın (sıkmayın)',
                    '• Bölgeyi yıkayın',
                    '• Buz uygulayın (15 dk)',
                    '• Antihistaminik alabilirsiniz'
                ],
                'tibbi': [
                    '• ANAFİLAKSİ takibi',
                    '• EPİNEFRİN (şok durumunda)',
                    '• Kortikosteroid',
                    '• Antihistaminik IV',
                    '• Sıvı resüsitasyonu'
                ],
                'uyari': 'Alerji öyküsü varsa ANAFİLAKSİ riski çok yüksek!'
            },
            3: {  # Akrep
                'ilk_yardim': [
                    '• Sokma bölgesini yıkayın',
                    '• Buz uygulayın',
                    '• Sakin kalın',
                    '• YAPMAYIN: Kesme, emme, turnike'
                ],
                'tibbi': [
                    '• ANTİVENOM değerlendirmesi',
                    '• Ağrı yönetimi',
                    '• Kas gevşetici (spazm için)',
                    '• Kardiyak monitörizasyon',
                    '• Solunum desteği (gerekirse)'
                ],
                'uyari': 'Sarı akrep (Androctonus) Akdeniz\'de tehlikeli! Çocuklarda daha ciddi.'
            },
            4: {  # Kedi
                'ilk_yardim': [
                    '• Yarayı bol su ve sabunla yıkayın',
                    '• Antiseptik uygulayın',
                    '• Derin ısırıklarda dikkat (enfeksiyon riski yüksek)',
                    '• Temiz bezle kapatın'
                ],
                'tibbi': [
                    '• Antibiyotik tedavisi (genellikle gerekli)',
                    '• Tetanos profilaksisi',
                    '• Kuduz değerlendirmesi',
                    '• Pasteurella enfeksiyonu takibi',
                    '• Kedi tırmığı hastalığı (Bartonella) taraması'
                ],
                'uyari': 'Kedi ısırıkları %30-50 oranında enfekte olur!'
            }
        }
        
        return treatments.get(animal_type, treatments[1])
    
    def _analyze_risk_factors(self, data):
        """Risk faktörlerini analiz et"""
        factors = []
        
        if data['Age'] < 10:
            factors.append('🔴 Çocuk yaş grubu: Vücut ağırlığına göre yüksek toksin dozu')
        elif data['Age'] > 65:
            factors.append('🔴 İleri yaş: Komplikasyon riski yüksek')
        
        if data['Body_Part'] == 3:
            factors.append('🔴 Yüz/baş bölgesi ısırığı: Hızlı sistemik yayılım')
        elif data['Body_Part'] == 4:
            factors.append('🔴 Boyun bölgesi: Solunum yolu tehlikesi')
        elif data['Body_Part'] == 2:
            factors.append('⚠️ El ısırığı: Fonksiyon kaybı riski')
        
        if data['Allergy_History'] and data['Animal_Type'] == 2:
            factors.append('🔴🔴 Arı alerjisi: ANAFİLAKSİ RİSKİ ÇOK YÜKSEK!')
        elif data['Allergy_History']:
            factors.append('⚠️ Alerji öyküsü mevcut')
        
        if data['Hospital_Time_Hours'] > 4:
            factors.append('🔴 Hastaneye ulaşım >4 saat: Ciddi gecikme!')
        elif data['Hospital_Time_Hours'] > 2:
            factors.append('⚠️ Hastaneye ulaşım >2 saat: Antivenom gecikmesi riski')
        
        if data['First_Aid_Applied'] == 0:
            factors.append('⚠️ İlk yardım uygulanmamış')
        
        if data['Chronic_Disease']:
            factors.append('⚠️ Kronik hastalık: İyileşme süreci uzayabilir')
        
        if data['Location'] == 0:
            factors.append('⚠️ Kırsal bölge: Sağlık hizmetine erişim zor')
        
        if data['Animal_Type'] == 0:
            factors.append('🔴 Yılan ısırığı: Antivenom gerekebilir')
        elif data['Animal_Type'] == 3:
            factors.append('🔴 Akrep sokması: Nörotoksik etki riski')
        
        if data['Season'] == 1:  # Yaz
            if data['Animal_Type'] in [0, 2, 3]:
                factors.append('⚠️ Yaz mevsimi: Bu hayvan aktivitesi yüksek')
        
        if not factors:
            factors.append('✅ Majör risk faktörü tespit edilmedi')
        
        return factors
    
    def generate_report(self, patient_data, patient_name="Hasta"):
        """Detaylı rapor oluştur"""
        assessment = self.assess_risk(patient_data)
        
        animal = self.ANIMALS[patient_data['Animal_Type']]
        location = self.LOCATIONS[patient_data['Location']]
        season = self.SEASONS[patient_data['Season']]
        body_part = self.BODY_PARTS[patient_data['Body_Part']]
        
        print("\n" + "=" * 80)
        print(f"🐍 HAYVAN ISIRIĞI/SOKMASI RİSK DEĞERLENDİRME RAPORU - {patient_name}")
        print("=" * 80)
        
        print(f"\n📋 OLAY BİLGİLERİ:")
        print(f"   Hayvan: {animal}")
        print(f"   Yaş: {patient_data['Age']}")
        print(f"   Cinsiyet: {'Erkek' if patient_data['Gender'] else 'Kadın'}")
        print(f"   Konum: {location}")
        print(f"   Mevsim: {season}")
        print(f"   Isırık Bölgesi: {body_part}")
        print(f"   Hastaneye Ulaşım: {patient_data['Hospital_Time_Hours']:.1f} saat")
        
        print(f"\n🎯 TAHMİN SONUCU:")
        print(f"   Durum: {assessment['tahmin']}")
        print(f"   Genel Risk Skoru: {assessment['genel_risk_skoru']:.1f}/100")
        print(f"   Aciliyet: {assessment['aciliyet']}")
        
        print(f"\n📊 RİSK DAĞILIMI:")
        for risk_type, percentage in assessment['risk_dagilimi'].items():
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            print(f"   {risk_type:.<15} {percentage:>5.1f}% {bar}")
        
        print(f"\n🩹 İLK YARDIM:")
        for item in assessment['tedavi']['ilk_yardim']:
            print(f"   {item}")
        
        print(f"\n🏥 TIBBİ TEDAVİ:")
        for item in assessment['tedavi']['tibbi']:
            print(f"   {item}")
        
        print(f"\n⚠️ UYARI:")
        print(f"   {assessment['tedavi']['uyari']}")
        
        print(f"\n📅 TAKİP:")
        print(f"   {assessment['takip']}")
        
        print(f"\n🔍 RİSK FAKTÖRLERİ:")
        for factor in assessment['risk_faktorleri']:
            print(f"   {factor}")
        
        # Akdeniz bölgesi özel bilgiler
        print("\n" + "-" * 40)
        print("🌊 AKDENİZ BÖLGESİ ÖZEL BİLGİLER:")
        if patient_data['Animal_Type'] == 0:  # Yılan
            print("   • Yaygın türler: Engerek, Kocabaş engerek")
            print("   • En riskli dönem: Nisan-Ekim")
            print("   • Antivenom: Devlet hastanelerinde mevcut")
        elif patient_data['Animal_Type'] == 3:  # Akrep
            print("   • Yaygın tür: Sarı akrep (Androctonus crassicauda)")
            print("   • En riskli dönem: Mayıs-Eylül")
            print("   • Çocuklarda ölüm riski daha yüksek")
        elif patient_data['Animal_Type'] == 2:  # Arı
            print("   • Yaygın: Bal arısı, Eşek arısı, Yaban arısı")
            print("   • En riskli dönem: Nisan-Eylül")
            print("   • EpiPen bulundurma önerilir (alerji varsa)")
        
        print("\n" + "=" * 80)
        print("⚕️ BU RAPOR BİLGİLENDİRME AMAÇLIDIR.")
        print("   Hayvan ısırığı/sokması durumunda MUTLAKA sağlık kuruluşuna başvurun!")
        print("=" * 80)
        
        return assessment


# ÖRNEK KULLANIM - 5 FARKLI SENARYO
if __name__ == "__main__":
    system = AnimalBiteRiskAssessment()
    
    # ÖRNEK 1: Yılan Isırığı - Yüksek Risk
    print("\n\n🐍 ÖRNEK 1: YILAN ISIRIĞI - KIRSAL BÖLGE")
    patient1 = {
        'Age': 45,
        'Gender': 1,  # Erkek
        'Location': 0,  # Kırsal
        'Season': 1,  # Yaz
        'Time_of_Day': 2,  # Akşam
        'Animal_Type': 0,  # Yılan
        'Body_Part': 0,  # Alt ekstremite
        'Occupation_Risk': 0,  # Çiftçi
        'Allergy_History': 0,
        'Previous_Bite': 0,
        'First_Aid_Applied': 0,
        'Hospital_Time_Hours': 3.5,
        'Chronic_Disease': 0
    }
    system.generate_report(patient1, "Mehmet Bey (45) - Çiftçi")
    
    # ÖRNEK 2: Köpek Isırığı - Çocuk
    print("\n\n🐕 ÖRNEK 2: KÖPEK ISIRIĞI - ÇOCUK")
    patient2 = {
        'Age': 7,
        'Gender': 1,  # Erkek
        'Location': 1,  # Şehir
        'Season': 2,  # Sonbahar
        'Time_of_Day': 1,  # Öğle
        'Animal_Type': 1,  # Köpek
        'Body_Part': 3,  # Yüz
        'Occupation_Risk': 2,  # Öğrenci/Çocuk
        'Allergy_History': 0,
        'Previous_Bite': 0,
        'First_Aid_Applied': 1,
        'Hospital_Time_Hours': 0.5,
        'Chronic_Disease': 0
    }
    system.generate_report(patient2, "Ali (7) - Öğrenci")
    
    # ÖRNEK 3: Arı Sokması - Alerji Öyküsü
    print("\n\n🐝 ÖRNEK 3: ARI SOKMASI - ALERJİ ÖYKÜSÜ VAR")
    patient3 = {
        'Age': 35,
        'Gender': 0,  # Kadın
        'Location': 2,  # Banliyö
        'Season': 1,  # Yaz
        'Time_of_Day': 1,  # Öğle
        'Animal_Type': 2,  # Arı
        'Body_Part': 1,  # Üst ekstremite
        'Occupation_Risk': 3,  # Şehir işçisi
        'Allergy_History': 1,  # ALERJİ VAR!
        'Previous_Bite': 1,
        'First_Aid_Applied': 1,
        'Hospital_Time_Hours': 0.75,
        'Chronic_Disease': 0
    }
    system.generate_report(patient3, "Ayşe Hanım (35) - Arı Alerjisi")
    
    # ÖRNEK 4: Akrep Sokması - Yaşlı
    print("\n\n🦂 ÖRNEK 4: AKREP SOKMASI - YAŞLI HASTA")
    patient4 = {
        'Age': 72,
        'Gender': 0,  # Kadın
        'Location': 0,  # Kırsal
        'Season': 1,  # Yaz
        'Time_of_Day': 3,  # Gece
        'Animal_Type': 3,  # Akrep
        'Body_Part': 2,  # El
        'Occupation_Risk': 0,  # Çiftçi
        'Allergy_History': 0,
        'Previous_Bite': 0,
        'First_Aid_Applied': 0,
        'Hospital_Time_Hours': 4.5,
        'Chronic_Disease': 1  # Kronik hastalık var
    }
    system.generate_report(patient4, "Fatma Nine (72)")
    
    # ÖRNEK 5: Kedi Isırığı - Düşük Risk
    print("\n\n🐱 ÖRNEK 5: KEDİ ISIRIĞI - DÜŞÜK RİSK")
    patient5 = {
        'Age': 28,
        'Gender': 0,  # Kadın
        'Location': 1,  # Şehir
        'Season': 3,  # Kış
        'Time_of_Day': 0,  # Sabah
        'Animal_Type': 4,  # Kedi
        'Body_Part': 2,  # El
        'Occupation_Risk': 3,  # Şehir işçisi
        'Allergy_History': 0,
        'Previous_Bite': 0,
        'First_Aid_Applied': 1,
        'Hospital_Time_Hours': 1.0,
        'Chronic_Disease': 0
    }
    system.generate_report(patient5, "Zeynep Hanım (28)")
