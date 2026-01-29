import os, pickle
import numpy as np
import pandas as pd
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class HypertensionRiskSystem:
    """Basitleştirilmiş Hipertansiyon Risk Değerlendirme"""
    
    def __init__(self):
        try:
            with open(os.path.join(BASE_DIR, "m1.pkl"), "rb") as f:
                self.rf_model = pickle.load(f)
            with open(os.path.join(BASE_DIR, "m2.pkl"), "rb") as f:
                self.gb_model = pickle.load(f)
            with open(os.path.join(BASE_DIR, "m3.pkl"), "rb") as f:
                self.scaler = pickle.load(f)
            print("✅ Modeller başarıyla yüklendi!\n")
        except Exception as e:
            print(f"❌ Model yükleme hatası: {e}")
            sys.exit(1)
    
    def get_user_input(self):
        """Kullanıcıdan bilgileri al"""
        print("=" * 80)
        print("HİPERTANSİYON (YÜKSEK TANSİYON) RİSK DEĞERLENDİRME SİSTEMİ")
        print("=" * 80)
        print("\n🔍 Lütfen aşağıdaki bilgileri giriniz:\n")
        
        try:
            name = input("👤 Hasta adı: ").strip() or "Hasta"
            
            print("\n📋 Demografik Bilgiler:")
            age = float(input("   Yaş (18-90): "))
            
            print("\n📊 Fiziksel Ölçümler:")
            bmi = float(input("   BMI (Vücut Kitle İndeksi, örn: 25): "))
            
            print("\n🍽️ Beslenme ve Yaşam Tarzı:")
            salt_intake = float(input("   Günlük tuz alımı (gram, 2-15 arası, ortalama 6-8): "))
            
            print("\n😰 Stres Seviyesi:")
            stress_score = float(input("   Stres puanı (0=Stressiz, 10=Çok stresli): "))
            
            print("\n😴 Uyku Düzeni:")
            sleep_duration = float(input("   Günlük uyku süresi (saat, örn: 7): "))
            
            print("\n📈 Tansiyon Geçmişi:")
            print("   0 = Normal")
            print("   1 = Prehipertansiyon (yüksek-normal)")
            print("   2 = Hipertansiyon (yüksek tansiyon)")
            bp_history = float(input("   Tansiyon geçmişi (0/1/2): "))
            
            print("\n💊 Mevcut İlaç Kullanımı:")
            print("   0 = İlaç kullanmıyor")
            print("   1 = Diğer ilaçlar")
            print("   2 = Diüretik")
            print("   3 = ACE İnhibitörü")
            print("   4 = Beta Bloker")
            medication = float(input("   İlaç durumu (0-4): "))
            
            print("\n👨‍👩‍👧‍👦 Aile Geçmişi:")
            family_history = float(input("   Ailede hipertansiyon var mı? (0=Hayır, 1=Evet): "))
            
            print("\n🏃 Egzersiz Düzeyi:")
            print("   0 = Düşük (hareketsiz)")
            print("   1 = Orta (haftada 2-3 gün)")
            print("   2 = Yüksek (haftada 4+ gün)")
            exercise_level = float(input("   Egzersiz seviyesi (0/1/2): "))
            
            print("\n🚬 Sigara Kullanımı:")
            smoking = float(input("   Sigara içiyor musunuz? (0=Hayır, 1=Evet): "))
            
            patient_data = {
                'Age': age,
                'Salt_Intake': salt_intake,
                'Stress_Score': stress_score,
                'Sleep_Duration': sleep_duration,
                'BMI': bmi,
                'BP_History_Encoded': bp_history,
                'Medication_Encoded': medication,
                'Family_History_Encoded': family_history,
                'Exercise_Level_Encoded': exercise_level,
                'Smoking_Encoded': smoking
            }
            
            return patient_data, name
            
        except ValueError:
            print("\n❌ Hatalı giriş! Lütfen sayısal değerler girin.")
            sys.exit(1)
    
    def assess(self, data):
        """Risk değerlendirmesi yap"""
        df = pd.DataFrame([data])
        X_scaled = self.scaler.transform(df)
        
        rf_proba = self.rf_model.predict_proba(X_scaled)[0]
        gb_proba = self.gb_model.predict_proba(X_scaled)[0]
        ensemble_proba = (rf_proba + gb_proba) / 2
        
        severity = np.argmax(ensemble_proba)
        risk_score = (ensemble_proba[1] * 30 + ensemble_proba[2] * 65 + ensemble_proba[3] * 100)
        
        return severity, ensemble_proba, risk_score
    
    def print_report(self, name, data, severity, proba, risk_score):
        """Raporu yazdır"""
        print("\n\n" + "=" * 80)
        print(f"RİSK DEĞERLENDİRME RAPORU - {name}")
        print("=" * 80)
        
        severity_names = [
            "✅ Hipertansiyon Riski Minimal",
            "⚠️ Düşük Risk (Prehipertansiyon Eğilimi)",
            "🚨 Orta Düzey Risk (Hipertansiyon Mevcut - Kontrollü)",
            "🚨🚨 Yüksek Risk (İleri Hipertansiyon)"
        ]
        
        print(f"\n🎯 SONUÇ: {severity_names[severity]}")
        print(f"📊 Genel Risk Skoru: {risk_score:.1f}/100")
        
        print(f"\n📈 Risk Dağılımı:")
        labels = ['Minimal', 'Düşük (Prehipertansiyon)', 'Orta (Kontrollü HT)', 'Yüksek (İleri HT)']
        for i, label in enumerate(labels):
            percentage = proba[i] * 100
            bar = "█" * int(percentage / 2)
            print(f"   {label:.<30} {percentage:>5.1f}% {bar}")
        
        # Öneriler
        print("\n" + "=" * 80)
        print("ÖNERİLER VE TAKİP PLANI")
        print("=" * 80)
        
        if severity == 0:
            print("\n✅ DURUM: Minimal risk")
            print("\n   ÖNERİLER:")
            print("   • Yıllık tansiyon kontrolü yeterli")
            print("   • Düşük tuzlu beslenmeye devam edin")
            print("   • Düzenli egzersiz (haftada 150 dk)")
            print("   • İdeal kilonuzu koruyun")
            print("   • Stresi yönetin, yeterli uyuyun")
            print("   • Sigara ve aşırı alkolden kaçının")
            
        elif severity == 1:
            print("\n⚠️ DURUM: Prehipertansiyon eğilimi - YAŞAM TARZI DEĞİŞİKLİĞİ")
            print("\n   DOKTOR: 3-6 ay içinde kardiyoloji kontrolü")
            print("\n   TESTLER:")
            print("   • Evde düzenli tansiyon takibi başlayın")
            print("   • Holter tansiyon monitörizasyonu")
            print("   • Böbrek fonksiyon testleri")
            print("   • EKG kontrolü")
            print("\n   YAŞAM TARZI (ZORUNLU):")
            print("   • DASH diyeti uygulayın")
            print("   • Günlük tuz alımını <6g'a düşürün")
            print("   • %5-10 kilo vermeye çalışın")
            print("   • Günde 30-45 dk yürüyüş")
            print("   • Stresi azaltın (meditasyon, yoga)")
            print("   • Alkol tüketimini sınırlayın")
            print("\n   TAKİP: 3 ayda bir kontrol")
            
        elif severity == 2:
            print("\n🚨 DURUM: Hipertansiyon mevcut - YAKIN TAKİP GEREKLİ")
            print("\n   DOKTOR: 1-2 AY içinde kardiyoloji uzmanına başvurun")
            print("\n   ACİL TESTLER:")
            print("   • 24 saat ambulatuvar tansiyon izlemi")
            print("   • Ekokardiyografi (kalp ultrason)")
            print("   • Böbrek fonksiyonları (kreatinin, BUN)")
            print("   • Göz dibi muayenesi")
            print("   • Lipid profili")
            print("\n   TEDAVİ:")
            print("   • İlaç tedavisi değerlendirilmeli")
            print("   • ACE inhibitörü veya ARB başlanabilir")
            print("   • Gerekirse kombinasyon tedavisi")
            print("\n   YAŞAM TARZI (ZORUNLU):")
            print("   • Günlük tuz <5g")
            print("   • DASH diyeti KESİNLİKLE uygulanmalı")
            print("   • Günde 2 kez evde tansiyon ölçümü")
            print("   • Kilo kontrolü (BMI <25 hedef)")
            print("   • Sigara BIRAKILMALI")
            print("\n   TAKİP: Aylık kontrol ZORUNLU")
            
        else:  # severity == 3
            print("\n🚨🚨 DURUM: İleri hipertansiyon - ACİL DEĞERLENDİRME")
            print("\n   DOKTOR: HEMEN kardiyoloji uzmanına başvurun!")
            print("\n   ACİL TESTLER:")
            print("   • Tam kardiyak değerlendirme")
            print("   • Ekokardiyografi")
            print("   • Böbrek fonksiyonları")
            print("   • Hedef organ hasarı taraması")
            print("   • Retinopati taraması (göz)")
            print("   • Karotis Doppler")
            print("\n   TEDAVİ:")
            print("   • Kombine antihipertansif tedavi")
            print("   • İlaç dozları optimize edilmeli")
            print("   • Dirençli hipertansiyon değerlendirmesi")
            print("   • Sekonder hipertansiyon araştırması")
            print("\n   HEDEF ORGAN KORUMA:")
            print("   • Kalp: Sol ventrikül hipertrofisi takibi")
            print("   • Böbrek: Proteinüri, GFR takibi")
            print("   • Beyin: İnme risk değerlendirmesi")
            print("   • Göz: Hipertansif retinopati")
            print("\n   TAKİP: Haftalık/2 haftada bir kontrol")
        
        # Risk faktörleri
        print("\n" + "=" * 80)
        print("RİSK FAKTÖRLERİ ANALİZİ")
        print("=" * 80)
        
        factors = []
        
        if data['Age'] > 65:
            factors.append("🔴 İleri yaş (65+): Major risk faktörü")
        elif data['Age'] > 50:
            factors.append("⚠️ Orta yaş (50+): Risk artıyor")
            
        if data['BMI'] > 30:
            factors.append("🔴 Obezite (BMI>30): Tansiyonu artırır")
        elif data['BMI'] > 25:
            factors.append("⚠️ Fazla kilo (BMI>25): Risk faktörü")
            
        if data['Salt_Intake'] > 10:
            factors.append("🔴 Çok yüksek tuz alımı (>10g): ACİL azaltın!")
        elif data['Salt_Intake'] > 6:
            factors.append("⚠️ Yüksek tuz alımı (>6g): Azaltın")
            
        if data['Stress_Score'] > 7:
            factors.append("🔴 Yüksek stres: Tansiyonu tetikler")
        elif data['Stress_Score'] > 4:
            factors.append("⚠️ Orta düzey stres: Yönetin")
            
        if data['Sleep_Duration'] < 6:
            factors.append("⚠️ Yetersiz uyku (<6 saat): Riski artırır")
            
        if data['BP_History_Encoded'] == 2:
            factors.append("🔴 Hipertansiyon geçmişi: Yakın takip gerekli")
        elif data['BP_History_Encoded'] == 1:
            factors.append("⚠️ Prehipertansiyon geçmişi: Dikkatli olun")
            
        if data['Family_History_Encoded'] == 1:
            factors.append("⚠️ Aile öyküsü: Genetik yatkınlık mevcut")
            
        if data['Exercise_Level_Encoded'] == 0:
            factors.append("⚠️ Hareketsiz yaşam: Egzersiz başlayın")
            
        if data['Smoking_Encoded'] == 1:
            factors.append("🔴 Sigara kullanımı: BIRAKIN!")
        
        if factors:
            for factor in factors:
                print(f"   {factor}")
        else:
            print("   ✅ Major risk faktörü tespit edilmedi")
        
        # Tansiyon değerleri referans
        print("\n" + "-" * 40)
        print("📏 TANSİYON DEĞERLERİ REFERANSI:")
        print("   Normal:          <120/80 mmHg")
        print("   Yüksek-Normal:   120-129/<80 mmHg")
        print("   Evre 1 HT:       130-139/80-89 mmHg")
        print("   Evre 2 HT:       ≥140/90 mmHg")
        print("   Hipertansif Kriz: >180/120 mmHg ⚠️")
        
        print("\n" + "=" * 80)
        print("⚕️ UYARI: Bu rapor bilgilendirme amaçlıdır.")
        print("   Kesin tanı için mutlaka bir kardiyoloji veya dahiliye")
        print("   uzmanına başvurunuz. Düzenli tansiyon ölçümü şarttır.")
        print("=" * 80 + "\n")


def main():
    """Ana program"""
    system = HypertensionRiskSystem()
    
    # Kullanıcıdan veri al
    patient_data, name = system.get_user_input()
    
    # Değerlendirme yap
    print("\n🔄 Analiz yapılıyor...")
    severity, proba, risk_score = system.assess(patient_data)
    
    # Raporu yazdır
    system.print_report(name, patient_data, severity, proba, risk_score)
    
    # Tekrar sormak ister mi?
    while True:
        choice = input("Başka bir hasta için değerlendirme yapmak ister misiniz? (e/h): ").lower()
        if choice == 'e':
            print("\n" * 2)
            patient_data, name = system.get_user_input()
            print("\n🔄 Analiz yapılıyor...")
            severity, proba, risk_score = system.assess(patient_data)
            system.print_report(name, patient_data, severity, proba, risk_score)
        else:
            print("\n👋 Sağlıklı günler dileriz!")
            break


if __name__ == "__main__":
    main()
