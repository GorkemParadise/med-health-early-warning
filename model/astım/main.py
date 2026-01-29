import os, pickle
import numpy as np
import pandas as pd
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class AsthmaRiskSystem:
    """Astım Risk Değerlendirme Sistemi"""
    
    def __init__(self):
        model_dir = BASE_DIR
        try:
            with open(os.path.join(model_dir, "m1.pkl"), "rb") as f:
                self.m1 = pickle.load(f)

            with open(os.path.join(model_dir, "m2.pkl"), "rb") as f:
                self.m2 = pickle.load(f)

            with open(os.path.join(model_dir, "m3.pkl"), "rb") as f:
                self.m3 = pickle.load(f)

            with open(os.path.join(model_dir, "feature_columns.pkl"), "rb") as f:
                self.feature_cols = pickle.load(f)
            print("✅ Modeller başarıyla yüklendi!\n")
        except Exception as e:
            print(f"❌ Model yükleme hatası: {e}")
            print(f"Model klasörü: {model_dir}")
            sys.exit(1)
    
    def get_user_input(self):
        """Kullanıcıdan bilgileri al"""
        print("=" * 80)
        print("ASTIM HASTALIĞI RİSK DEĞERLENDİRME SİSTEMİ")
        print("=" * 80)
        print("\n📝 Lütfen aşağıdaki bilgileri giriniz:\n")
        
        try:
            # Temel Bilgiler
            name = input("👤 Hasta adı: ").strip() or "Hasta"
            age = int(input(" Yaş: "))
            
            print("\n👥 Cinsiyet:")
            print("  0 = Erkek")
            print("  1 = Kadın")
            gender = int(input("Seçim (0/1): "))
            
            print("\n🌍 Etnik Köken:")
            print("  0 = Kafkas")
            print("  1 = Afrikalı-Amerikalı")
            print("  2 = Asyalı")
            print("  3 = Diğer")
            ethnicity = int(input("Seçim (0-3): "))
            
            print("\n🎓 Eğitim Seviyesi:")
            print("  0 = İlkokul")
            print("  1 = Lise")
            print("  2 = Üniversite")
            print("  3 = Yüksek Lisans+")
            education = int(input("Seçim (0-3): "))
            
            bmi = float(input("\n⚖️  BMI (Vücut Kitle İndeksi): "))
            
            print("\n🚬 Sigara kullanıyor musunuz?")
            print("  0 = Hayır")
            print("  1 = Evet")
            smoking = int(input("Seçim (0/1): "))
            
            # Yaşam Tarzı (0-10 skala)
            print("\n" + "=" * 80)
            print("YAŞAM TARZI FAKTÖRLERİ (0-10 arası değerler girin)")
            print("=" * 80)
            
            physical_activity = float(input("\n🏃 Fiziksel Aktivite (0=Hiç, 10=Çok aktif): "))
            diet_quality = float(input("Diyet Kalitesi (0=Çok kötü, 10=Mükemmel): "))
            sleep_quality = float(input("Uyku Kalitesi (0=Çok kötü, 10=Mükemmel): "))
            
            # Çevresel Maruziyetler (0-10 skala)
            print("\n" + "=" * 80)
            print("ÇEVRESEL MARUZİYETLER (0-10 arası değerler girin)")
            print("=" * 80)
            
            pollution = float(input("\nHava Kirliliği Maruziyeti (0=Yok, 10=Çok yüksek): "))
            pollen = float(input("Polen Maruziyeti (0=Yok, 10=Çok yüksek): "))
            dust = float(input("Toz Maruziyeti (0=Yok, 10=Çok yüksek): "))
            
            # Tıbbi Geçmiş
            print("\n" + "=" * 80)
            print("TIBBİ GEÇMİŞ (0=Hayır, 1=Evet)")
            print("=" * 80)
            
            pet_allergy = int(input("\nEvcil hayvan alerjiniz var mı? (0/1): "))
            family_history = int(input("Ailede astım öyküsü var mı? (0/1): "))
            allergies = int(input("Alerji geçmişiniz var mı? (0/1): "))
            eczema = int(input("Egzama (atopik dermatit) var mı? (0/1): "))
            hay_fever = int(input("Saman nezlesi (alerjik rinit) var mı? (0/1): "))
            gerd = int(input("Gastroözofageal reflü var mı? (0/1): "))
            
            # Akciğer Fonksiyon Testleri
            print("\n" + "=" * 80)
            print("AKCİĞER FONKSİYON TESTLERİ")
            print("=" * 80)
            print("(Bilinmiyorsa tahmine dayalı değerler girebilirsiniz)")
            print("Derin bir nefes alıp verirken ne kadar rahat hissediyorsunuz? FEV1 ve FVC değerlerinizi bilmiyorsanız, lütfen tahmini değerler girin.\n")
            fev1 = float(input("\n🫁 FEV1 (1. saniye zorlu ekspirasyon hacmi - Litre, normal: 2.5-4.0): "))
            fvc = float(input("🫁 FVC (Zorlu vital kapasite - Litre, normal: 3.0-5.0): "))
            
            # Semptomlar
            print("\n" + "=" * 80)
            print("SEMPTOMLAR (0=Yok, 1=Var)")
            print("=" * 80)
            
            wheezing = int(input("\nHırıltılı solunum (wheezing)? (0/1): "))
            shortness = int(input("Nefes darlığı? (0/1): "))
            chest_tight = int(input("Göğüs sıkışması? (0/1): "))
            coughing = int(input("Öksürük? (0/1): "))
            night_symptoms = int(input("Gece atakları? (0/1): "))
            exercise_induced = int(input("Egzersiz ile tetiklenen semptomlar? (0/1): "))
            
            # Veriyi hazırla
            patient_data = {
                'Age': age,
                'Gender': gender,
                'Ethnicity': ethnicity,
                'EducationLevel': education,
                'BMI': bmi,
                'Smoking': smoking,
                'PhysicalActivity': physical_activity,
                'DietQuality': diet_quality,
                'SleepQuality': sleep_quality,
                'PollutionExposure': pollution,
                'PollenExposure': pollen,
                'DustExposure': dust,
                'PetAllergy': pet_allergy,
                'FamilyHistoryAsthma': family_history,
                'HistoryOfAllergies': allergies,
                'Eczema': eczema,
                'HayFever': hay_fever,
                'GastroesophagealReflux': gerd,
                'LungFunctionFEV1': fev1,
                'LungFunctionFVC': fvc,
                'Wheezing': wheezing,
                'ShortnessOfBreath': shortness,
                'ChestTightness': chest_tight,
                'Coughing': coughing,
                'NighttimeSymptoms': night_symptoms,
                'ExerciseInduced': exercise_induced
            }
            
            return patient_data, name
            
        except ValueError:
            print("\n❌ Hatalı giriş! Lütfen sayısal değerler girin.")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\n👋 Program sonlandırıldı.")
            sys.exit(0)
    
    def assess(self, data):
        """Risk değerlendirmesi yap"""
        df = pd.DataFrame([data])
        df = df[self.feature_cols]
        X_scaled = self.m3.transform(df)
        
        # Tahminler
        m1_proba = self.m1.predict_proba(X_scaled)[0]
        m2_proba = self.m2.predict_proba(X_scaled)[0]
        ensemble_proba = (m1_proba + m2_proba) / 2
        
        has_asthma = int(np.argmax(ensemble_proba))
        risk_percentage = float(ensemble_proba[1]) * 100
        
        return has_asthma, ensemble_proba, risk_percentage
    
    def print_report(self, name, data, has_asthma, proba, risk_percentage):
        """Raporu yazdır"""
        print("\n\n" + "=" * 80)
        print(f"ASTIM RİSK DEĞERLENDİRME RAPORU - {name}")
        print("=" * 80)
        
        # Hasta Bilgileri
        print(f"\n📋 HASTA BİLGİLERİ:")
        print(f"   Yaş: {data['Age']}")
        print(f"   Cinsiyet: {'Erkek' if data['Gender'] == 0 else 'Kadın'}")
        print(f"   BMI: {data['BMI']:.1f}")
        print(f"   Sigara: {'Evet ❌' if data['Smoking'] == 1 else 'Hayır ✅'}")
        
        # Sonuç
        print(f"\n🎯 TAHMİN SONUCU:")
        if has_asthma == 1:
            print(f"   Durum: ⚠️ ASTIM RİSKİ TESPİT EDİLDİ")
        else:
            print(f"   Durum: ✅ ASTIM RİSKİ DÜŞÜK")
        
        print(f"   Risk Yüzdesi: {risk_percentage:.1f}%")
        
        # Risk seviyesi
        if risk_percentage < 20:
            risk_level = "🟢 Çok Düşük Risk"
            urgency = "Düşük"
        elif risk_percentage < 50:
            risk_level = "🟡 Düşük-Orta Risk"
            urgency = "Orta"
        elif risk_percentage < 75:
            risk_level = "🟠 Orta-Yüksek Risk"
            urgency = "Yüksek"
        else:
            risk_level = "🔴 Yüksek Risk"
            urgency = "ÇOK YÜKSEK"
        
        print(f"   Risk Seviyesi: {risk_level}")
        print(f"   Aciliyet: {urgency}")
        
        # Olasılık Dağılımı
        print(f"\nOLASILIK DAĞILIMI:")
        no_asthma_pct = proba[0] * 100
        has_asthma_pct = proba[1] * 100
        
        no_bar = "█" * int(no_asthma_pct / 2)
        has_bar = "█" * int(has_asthma_pct / 2)
        
        print(f"   Astım Yok....... {no_asthma_pct:>5.1f}% {no_bar}")
        print(f"   Astım Var........ {has_asthma_pct:>5.1f}% {has_bar}")
        
        # Öneriler
        print("\n" + "=" * 80)
        print("ÖNERİLER VE TAKİP PLANI")
        print("=" * 80)
        
        if risk_percentage < 20:
            print("\n✅ DURUM: Çok düşük risk")
            print("\n   ÖNERİLER:")
            print("   • Yıllık rutin kontrol yeterli")
            print("   • Düzenli egzersiz yapın")
            print("   • Tetikleyicilerden kaçının (polen, toz, duman)")
            print("   • Dengeli beslenme")
            print("   • Stres yönetimi")
        
        elif risk_percentage < 50:
            print("\n⚠️  DURUM: Düşük-Orta risk - TAKİP ÖNERİLİR")
            print("\n   DOKTOR: 6 ayda bir kontrol önerilir")
            print("\n   ÖNERİLER:")
            print("   • Göğüs hastalıkları uzmanı ile görüşün")
            print("   • Peak flow metre kullanımı")
            print("   • Tetikleyicilerden uzak durun")
            print("   • Acil durum planı hazırlayın")
            print("   • Fiziksel aktiviteye devam edin")
        
        elif risk_percentage < 75:
            print("\n🚨 DURUM: Orta-Yüksek risk - TIBBİ TAKİP GEREKLİ")
            print("\n   DOKTOR: 3 ayda bir kontrol ZORUNLU")
            print("\n   TEDAVİ:")
            print("   • Kontrol edici ilaç tedavisi önerilir")
            print("   • İnhaler kortikosteroidler değerlendirilmeli")
            print("   • Uzun etkili beta-2 agonistler")
            print("\n   ÖNERİLER:")
            print("   • Peak flow günlük takip")
            print("   • Tetikleyicilerden MUTLAKA kaçının")
            print("   • Acil eylem planı hazır olmalı")
            print("   • Destek gruplarına katılın")
        
        else:
            print("\n🚨🚨 DURUM: Yüksek risk - ACİL TIBBİ MÜDAHALE")
            print("\n   DOKTOR: HEMEN göğüs hastalıkları uzmanına başvurun")
            print("\n   TEDAVİ:")
            print("   • Yüksek doz inhaler kortikosteroidler")
            print("   • Uzun etkili beta-2 agonistler")
            print("   • Kısa etkili bronkodilatörler (kurtarıcı)")
            print("   • Oral kortikosteroidler (gerekirse)")
            print("   • Biyolojik ajanlar (şiddetli astımda)")
            print("\n   ACİL ÖNLEMLER:")
            print("   • Astım acil eylem planı EDİNİN")
            print("   • Tetikleyicilerden TAM kaçınma")
            print("   • Peak flow günlük takip ZORUNLU")
            print("   • İnhaler tekniği eğitimi alın")
        
        # Risk Faktörleri
        print("\n" + "=" * 80)
        print("RİSK FAKTÖRLERİ ANALİZİ")
        print("=" * 80)
        
        factors = []
        if data['Smoking'] == 1:
            factors.append("🔴 SİGARA İÇİYORSUNUZ - HEMEN BIRAKIN!")
        if data['FamilyHistoryAsthma'] == 1:
            factors.append("⚠️ Ailede astım öyküsü var")
        if data['HistoryOfAllergies'] == 1:
            factors.append("⚠️ Alerji geçmişi mevcut")
        if data['PetAllergy'] == 1:
            factors.append("⚠️ Evcil hayvan alerjisi var")
        if data['Eczema'] == 1:
            factors.append("⚠️ Egzama (atopik dermatit) mevcut")
        if data['HayFever'] == 1:
            factors.append("⚠️ Saman nezlesi var")
        if data['BMI'] > 30:
            factors.append("⚠️ Yüksek BMI (obezite riski)")
        if data['PollutionExposure'] > 7:
            factors.append("🔴 Yüksek hava kirliliği maruziyeti")
        if data['PollenExposure'] > 7:
            factors.append("⚠️ Yüksek polen maruziyeti")
        if data['DustExposure'] > 7:
            factors.append("⚠️ Yüksek toz maruziyeti")
        
        # Semptomlar
        symptoms = []
        if data['Wheezing'] == 1:
            symptoms.append("Hırıltılı solunum")
        if data['ShortnessOfBreath'] == 1:
            symptoms.append("Nefes darlığı")
        if data['ChestTightness'] == 1:
            symptoms.append("Göğüs sıkışması")
        if data['Coughing'] == 1:
            symptoms.append("Öksürük")
        if data['NighttimeSymptoms'] == 1:
            symptoms.append("Gece semptomları")
        if data['ExerciseInduced'] == 1:
            symptoms.append("Egzersiz ile tetiklenen")
        
        if symptoms:
            factors.append(f"🔴 Aktif semptomlar: {', '.join(symptoms)}")
        
        if factors:
            for factor in factors:
                print(f"   {factor}")
        else:
            print("   ✅ Önemli risk faktörü tespit edilmedi")
        
        # Akciğer Fonksiyonları
        print("\n" + "=" * 80)
        print("AKCİĞER FONKSİYON TESTLERİ")
        print("=" * 80)
        print(f"\n   FEV1: {data['LungFunctionFEV1']:.2f} L")
        print(f"   FVC: {data['LungFunctionFVC']:.2f} L")
        
        if data['LungFunctionFVC'] > 0:
            fev1_fvc = data['LungFunctionFEV1'] / data['LungFunctionFVC']
            print(f"   FEV1/FVC Oranı: {fev1_fvc:.2f}")
            
            if fev1_fvc < 0.7:
                print(f"   ⚠️ FEV1/FVC < 0.7: Obstrüksiyon belirtisi!")
            else:
                print(f"   ✅ FEV1/FVC Normal")
        
        print("\n" + "=" * 80)
        print("⚕️ UYARI: Bu rapor bilgilendirme amaçlıdır.")
        print("   Kesin tanı için mutlaka göğüs hastalıkları uzmanına başvurunuz.")
        print("=" * 80 + "\n")


def main():
    """Ana program"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "   🫁 ASTIM HASTALIĞI RİSK DEĞERLENDİRME SİSTEMİ".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("║" + "   Yapay Zeka Destekli Tıbbi Tarama Sistemi".center(78) + "║")
    print("║" + "   Model Doğruluğu: %95".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print("\n")
    
    system = AsthmaRiskSystem()
    
    # Kullanıcıdan veri al
    patient_data, name = system.get_user_input()
    
    # Değerlendirme yap
    print("\n🔄 Analiz yapılıyor...")
    print("   M1 - Random Forest modeli çalışıyor...")
    print("   M2 - Gradient Boosting modeli çalışıyor...")
    print("   Ensemble tahmin hesaplanıyor...")
    
    has_asthma, proba, risk_percentage = system.assess(patient_data)
    system.print_report(name, patient_data, has_asthma, proba, risk_percentage)
    
    while True:
        try:
            choice = input("Başka bir hasta için değerlendirme yapmak ister misiniz? (e/h): ").lower()
            if choice == 'e':
                print("\n" * 2)
                patient_data, name = system.get_user_input()
                print("\n🔄 Analiz yapılıyor...")
                has_asthma, proba, risk_percentage = system.assess(patient_data)
                system.print_report(name, patient_data, has_asthma, proba, risk_percentage)
            else:
                print("\n👋 Sağlıklı günler dileriz!")
                print("⚕️ Unutmayın: Düzenli sağlık kontrolleri önemlidir.\n")
                break
        except KeyboardInterrupt:
            print("\n\n👋 Program sonlandırıldı.")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program sonlandırıldı.")
        sys.exit(0)