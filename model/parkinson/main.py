import os, pickle
import numpy as np
import pandas as pd
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ParkinsonRiskSystem:
    """Basitleştirilmiş Parkinson Risk Değerlendirme"""
    
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
        print("PARKINSON HASTALIĞI RİSK DEĞERLENDİRME SİSTEMİ")
        print("=" * 80)
        print("\n📝 Lütfen aşağıdaki bilgileri giriniz:\n")
        
        try:
            name = input("👤 Hasta adı: ").strip() or "Hasta"
            age = float(input("Yaş (50-85): "))
            
            print("\n Motor Belirtiler (0-5 arası, 0=Yok, 5=Çok şiddetli):")
            tremor = float(input("    Tremor (titreme): "))
            rigidity = float(input("    Rijidite (kas sertliği): "))
            bradykinesia = float(input("    Bradikinezi (yavaş hareket): "))
            postural = float(input("    Denge problemi: "))
            
            motor_updrs = float(input("\nMotor UPDRS skoru veya Son 1 haftada hareket etmek sizin için ne kadar zorlayıcıydı? (0-100, ortalama 30): "))
            disease_duration = float(input("  Hastalık süresi (yıl, 0=yeni): "))
            levodopa_response = float(input(" Levodopa tedavi yanıtı (0-100%, ortalama 60): "))
            
            print("\n Analiz yapılıyor...")
            jitter = 0.003 + (tremor / 500)
            shimmer = 0.02 + (tremor / 100)
            nhr = 0.015 + (tremor / 200)
            hnr = 25 - (tremor * 3)
            total_updrs = motor_updrs * 1.3
            
            patient_data = {
                'age': age,
                'motor_updrs': motor_updrs,
                'total_updrs': total_updrs,
                'jitter': jitter,
                'shimmer': shimmer,
                'nhr': nhr,
                'hnr': hnr,
                'tremor_score': tremor,
                'rigidity': rigidity,
                'bradykinesia': bradykinesia,
                'postural_instability': postural,
                'disease_duration': disease_duration,
                'levodopa_response': levodopa_response
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
        risk_score = (ensemble_proba[1] * 33 + ensemble_proba[2] * 66 + ensemble_proba[3] * 100)
        
        return severity, ensemble_proba, risk_score
    
    def print_report(self, name, data, severity, proba, risk_score):
        """Raporu yazdır"""
        print("\n\n" + "=" * 80)
        print(f"RİSK DEĞERLENDİRME RAPORU - {name}")
        print("=" * 80)
        
        severity_names = [
            "✅ Parkinson Riski Minimal",
            "⚠️ Hafif Parkinson Belirtileri",
            "🚨 Orta Düzey Parkinson",
            "🚨🚨 İleri Parkinson"
        ]
        
        print(f"\n SONUÇ: {severity_names[severity]}")
        print(f" Genel Risk Skoru: {risk_score:.1f}/100")
        
        print(f"\n Risk Dağılımı:")
        labels = ['Risk Yok', 'Hafif', 'Orta', 'İleri']
        for i, label in enumerate(labels):
            percentage = proba[i] * 100
            bar = "█" * int(percentage / 2)
            print(f"   {label:.<15} {percentage:>5.1f}% {bar}")
        
        # Öneriler
        print("\n" + "=" * 80)
        print("ÖNERİLER VE TAKİP PLANI")
        print("=" * 80)
        
        if severity == 0:
            print("\n✅ DURUM: Minimal risk")
            print("\n   ÖNERİLER:")
            print("   • Yıllık kontrol yeterli")
            print("   • Düzenli egzersiz (haftada 3-4 gün)")
            print("   • Dengeli beslenme")
            print("   • Zihinsel aktiviteler")
            
        elif severity == 1:
            print("\n⚠️ DURUM: Hafif belirtiler - İLAÇ TEDAVİSİ ÖNERİLİYOR")
            print("\n  DOKTOR: 1-2 ay içinde nöroloji uzmanına başvurun")
            print("\n  TEDAVİ:")
            print("   • Levodopa veya dopamin agonistleri değerlendirilmeli")
            print("   • MAO-B inhibitörleri düşünülebilir")
            print("\n   REHABİLİTASYON:")
            print("   • Fizik tedavi programı başlatın")
            print("   • Denge ve kuvvet egzersizleri")
            print("   • Konuşma terapisi değerlendirmesi")
            print("\n   TAKİP: 3-6 ayda bir kontrol")
            
        elif severity == 2:
            print("\n🚨 DURUM: Orta düzey - YAKIN TAKİP GEREKLİ")
            print("\n   DOKTOR: 1-2 HAFTA içinde ACİL nöroloji konsültasyonu")
            print("\n   TEDAVİ:")
            print("   • Kombine ilaç tedavisi (Levodopa + COMT inhibitörü)")
            print("   • İlaç dozları optimize edilmeli")
            print("   • Motor dalgalanmaları izlenmeli")
            print("\n   REHABİLİTASYON:")
            print("   • Fizik tedavi YOĞUNLAŞTIRILMALI")
            print("   • Konuşma ve yutma terapisi")
            print("   • Ergoterapi (günlük aktiviteler için)")
            print("   • Destek gruplarına katılım")
            print("\n   TAKİP: AYLIK kontrol ZORUNLU")
            
        else:  # severity == 3
            print("\n🚨🚨 DURUM: İleri düzey - CERRAHİ DEĞERLENDİRME")
            print("\n   DOKTOR: HEMEN hareket bozuklukları merkezine sevk")
            print("\n   CERRAHİ:")
            print("   • DBS (Derin Beyin Stimülasyonu) ameliyatı değerlendirilmeli")
            print("   • Apomorfin pompası düşünülebilir")
            print("   • Duodopa (jejunostomi) değerlendirmesi")
            print("\n   TEDAVİ:")
            print("   • Maksimum ilaç tedavisi")
            print("   • Psikiyatri konsültasyonu")
            print("\n   BAKIM:")
            print("   • Yoğun rehabilitasyon")
            print("   • Bakım veren eğitimi")
            print("   • Evde bakım hizmetleri")
            print("\n   TAKİP: Haftalık/2 haftada bir")
        
        # Risk faktörleri
        print("\n" + "=" * 80)
        print("RİSK FAKTÖRLERİ")
        print("=" * 80)
        
        factors = []
        if data['age'] > 70:
            factors.append("🔴 İleri yaş (70+)")
        if data['tremor_score'] > 3:
            factors.append("🔴 Yüksek tremor")
        if data['rigidity'] > 3:
            factors.append("🔴 Yüksek rijidite")
        if data['bradykinesia'] > 3:
            factors.append("🔴 Belirgin bradikinezi")
        if data['postural_instability'] > 2.5:
            factors.append("⚠️ Postural instabilite")
        if data['motor_updrs'] > 40:
            factors.append("🔴 Yüksek motor UPDRS")
        if data['disease_duration'] > 5:
            factors.append("⚠️ Uzun hastalık süresi")
        if data['levodopa_response'] < 50:
            factors.append("🔴 Düşük tedavi yanıtı")
        
        if factors:
            for factor in factors:
                print(f"   {factor}")
        else:
            print("   ✅ Major risk faktörü tespit edilmedi")
        
        print("\n" + "=" * 80)
        print("⚕️ UYARI: Bu rapor bilgilendirme amaçlıdır.")
        print("   Kesin tanı için mutlaka bir nöroloji uzmanına başvurunuz.")
        print("=" * 80 + "\n")


def main():
    """Ana program"""
    system = ParkinsonRiskSystem()
    
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