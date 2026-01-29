import os, pickle
import numpy as np
import pandas as pd
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class DiabetesRiskSystem:
    """Basitleştirilmiş Diyabet Risk Değerlendirme"""
    
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
        print("DİYABET HASTALIĞI RİSK DEĞERLENDİRME SİSTEMİ")
        print("=" * 80)
        print("\n🔍 Lütfen aşağıdaki bilgileri giriniz:\n")
        
        try:
            name = input("👤 Hasta adı: ").strip() or "Hasta"
            
            print("\n📋 Demografik Bilgiler:")
            age_input = float(input("   Yaş (18-80): "))
            # Yaş kategorisine dönüştür (1-13 arası, her 5 yıl için 1)
            age = min(13, max(1, int((age_input - 18) / 5) + 1))
            
            sex = float(input("   Cinsiyet (0=Kadın, 1=Erkek): "))
            
            print("\n📊 Fiziksel Ölçümler:")
            bmi = float(input("   BMI (Vücut Kitle İndeksi, örn: 25): "))
            
            print("\n❤️ Sağlık Durumu (0=Hayır, 1=Evet):")
            high_bp = float(input("   Yüksek tansiyon var mı?: "))
            high_chol = float(input("   Yüksek kolesterol var mı?: "))
            chol_check = float(input("   Son 5 yılda kolesterol kontrolü yapıldı mı?: "))
            stroke = float(input("   Daha önce inme geçirdiniz mi?: "))
            heart_disease = float(input("   Kalp hastalığı veya kalp krizi var mı?: "))
            
            print("\n🏃 Yaşam Tarzı (0=Hayır, 1=Evet):")
            smoker = float(input("   En az 100 sigara içtiniz mi (yaşam boyu)?: "))
            phys_activity = float(input("   Son 30 günde fiziksel aktivite yaptınız mı?: "))
            fruits = float(input("   Her gün meyve tüketiyor musunuz?: "))
            veggies = float(input("   Her gün sebze tüketiyor musunuz?: "))
            hvy_alcohol = float(input("   Ağır alkol tüketimi var mı? (E:>14, K:>7 içki/hafta): "))
            
            print("\n🏥 Sağlık Erişimi (0=Hayır, 1=Evet):")
            any_healthcare = float(input("   Sağlık sigortanız var mı?: "))
            no_doc_cost = float(input("   Maliyet nedeniyle doktora gidemediğiniz oldu mu?: "))
            
            print("\n📈 Genel Sağlık Durumu:")
            gen_hlth = float(input("   Genel sağlık durumu (1=Mükemmel, 5=Kötü): "))
            ment_hlth = float(input("   Son 30 günde kaç gün mental sağlık sorunu yaşadınız? (0-30): "))
            phys_hlth = float(input("   Son 30 günde kaç gün fiziksel sağlık sorunu yaşadınız? (0-30): "))
            diff_walk = float(input("   Yürümekte veya merdiven çıkmakta zorluk var mı? (0/1): "))
            
            print("\n📚 Sosyoekonomik Durum:")
            education = float(input("   Eğitim seviyesi (1=İlkokul...6=Üniversite+): "))
            income = float(input("   Gelir seviyesi (1=Düşük...8=Yüksek): "))
            
            patient_data = {
                'HighBP': high_bp,
                'HighChol': high_chol,
                'CholCheck': chol_check,
                'BMI': bmi,
                'Smoker': smoker,
                'Stroke': stroke,
                'HeartDiseaseorAttack': heart_disease,
                'PhysActivity': phys_activity,
                'Fruits': fruits,
                'Veggies': veggies,
                'HvyAlcoholConsump': hvy_alcohol,
                'AnyHealthcare': any_healthcare,
                'NoDocbcCost': no_doc_cost,
                'GenHlth': gen_hlth,
                'MentHlth': ment_hlth,
                'PhysHlth': phys_hlth,
                'DiffWalk': diff_walk,
                'Sex': sex,
                'Age': age,
                'Education': education,
                'Income': income
            }
            
            # Gerçek yaşı da sakla (raporlama için)
            patient_data['_real_age'] = age_input
            
            return patient_data, name
            
        except ValueError:
            print("\n❌ Hatalı giriş! Lütfen sayısal değerler girin.")
            sys.exit(1)
    
    def assess(self, data):
        """Risk değerlendirmesi yap"""
        # _real_age'i çıkar
        data_copy = {k: v for k, v in data.items() if not k.startswith('_')}
        df = pd.DataFrame([data_copy])
        X_scaled = self.scaler.transform(df)
        
        rf_proba = self.rf_model.predict_proba(X_scaled)[0]
        gb_proba = self.gb_model.predict_proba(X_scaled)[0]
        ensemble_proba = (rf_proba + gb_proba) / 2
        
        severity = np.argmax(ensemble_proba)
        risk_score = (ensemble_proba[1] * 25 + ensemble_proba[2] * 60 + ensemble_proba[3] * 100)
        
        return severity, ensemble_proba, risk_score
    
    def print_report(self, name, data, severity, proba, risk_score):
        """Raporu yazdır"""
        print("\n\n" + "=" * 80)
        print(f"RİSK DEĞERLENDİRME RAPORU - {name}")
        print("=" * 80)
        
        severity_names = [
            "✅ Diyabet Riski Minimal",
            "⚠️ Düşük Diyabet Riski (Dikkatli Olun)",
            "🚨 Orta Düzey Risk (Prediyabet Olabilir)",
            "🚨🚨 Yüksek Risk (Diyabet Olabilir)"
        ]
        
        print(f"\n🎯 SONUÇ: {severity_names[severity]}")
        print(f"📊 Genel Risk Skoru: {risk_score:.1f}/100")
        
        print(f"\n📈 Risk Dağılımı:")
        labels = ['Minimal', 'Düşük', 'Orta (Prediyabet)', 'Yüksek (Diyabet)']
        for i, label in enumerate(labels):
            percentage = proba[i] * 100
            bar = "█" * int(percentage / 2)
            print(f"   {label:.<25} {percentage:>5.1f}% {bar}")
        
        # Öneriler
        print("\n" + "=" * 80)
        print("ÖNERİLER VE TAKİP PLANI")
        print("=" * 80)
        
        if severity == 0:
            print("\n✅ DURUM: Minimal risk")
            print("\n   ÖNERİLER:")
            print("   • Yıllık check-up yeterli")
            print("   • Sağlıklı beslenmeye devam edin")
            print("   • Düzenli egzersiz (haftada 150 dk)")
            print("   • İdeal kilonuzu koruyun")
            print("   • Yılda bir açlık kan şekeri ölçümü")
            
        elif severity == 1:
            print("\n⚠️ DURUM: Düşük risk - YAŞAM TARZI DEĞİŞİKLİĞİ ÖNERİLİYOR")
            print("\n   DOKTOR: 6 ay içinde check-up yaptırın")
            print("\n   TESTLER:")
            print("   • Açlık kan şekeri (FPG)")
            print("   • HbA1c testi")
            print("   • Lipid profili")
            print("\n   YAŞAM TARZI:")
            print("   • %5-7 kilo vermeye çalışın")
            print("   • Günde 30 dk yürüyüş")
            print("   • Şekerli içeceklerden kaçının")
            print("   • Tam tahıl tüketimini artırın")
            print("   • Porsiyonları küçültün")
            print("\n   TAKİP: 6 ayda bir kontrol")
            
        elif severity == 2:
            print("\n🚨 DURUM: Orta düzey risk - PREDİYABET OLABİLİR")
            print("\n   DOKTOR: 1-2 AY içinde endokrinoloji/dahiliye uzmanına başvurun")
            print("\n   ACİL TESTLER:")
            print("   • Oral Glukoz Tolerans Testi (OGTT)")
            print("   • HbA1c testi")
            print("   • Açlık insülin seviyesi")
            print("   • Böbrek fonksiyon testleri")
            print("\n   TEDAVİ:")
            print("   • Metformin başlanabilir (doktor kararıyla)")
            print("   • Diyabet eğitimi alın")
            print("   • Diyetisyen danışmanlığı")
            print("\n   YAŞAM TARZI DEĞİŞİKLİKLERİ:")
            print("   • %7-10 kilo verme hedefi")
            print("   • Günde 45-60 dk egzersiz")
            print("   • Karbonhidrat sayımı öğrenin")
            print("   • Evde kan şekeri takibi başlayın")
            print("\n   TAKİP: 3 ayda bir kontrol ZORUNLU")
            
        else:  # severity == 3
            print("\n🚨🚨 DURUM: Yüksek risk - DİYABET OLABİLİR")
            print("\n   DOKTOR: HEMEN endokrinoloji uzmanına başvurun!")
            print("\n   ACİL TESTLER:")
            print("   • Açlık kan şekeri (FPG)")
            print("   • HbA1c testi")
            print("   • Tam idrar tahlili (idrarda şeker/protein)")
            print("   • Böbrek fonksiyonları")
            print("   • Göz dibi muayenesi")
            print("   • Ayak muayenesi")
            print("\n   OLASI TEDAVİ:")
            print("   • Oral antidiyabetikler (Metformin vb.)")
            print("   • Gerekirse insülin tedavisi")
            print("   • Tansiyon/kolesterol ilaçları")
            print("\n   YAŞAM TARZI (ZORUNLU):")
            print("   • Diyabet diyeti BAŞLAYIN")
            print("   • Günde 2-3 kez kan şekeri ölçümü")
            print("   • Egzersiz programı (doktor onaylı)")
            print("   • Sigara/alkol bırakma")
            print("\n   KOMPLİKASYON TAKİBİ:")
            print("   • Yılda 1 göz muayenesi")
            print("   • Düzenli ayak bakımı")
            print("   • Böbrek fonksiyon takibi")
            print("\n   TAKİP: Haftalık/aylık kontrol (doktor belirleyecek)")
        
        # Risk faktörleri
        print("\n" + "=" * 80)
        print("RİSK FAKTÖRLERİ ANALİZİ")
        print("=" * 80)
        
        factors = []
        real_age = data.get('_real_age', data['Age'] * 5 + 18)
        
        if real_age > 45:
            factors.append("🔴 45 yaş üstü: Diyabet riski artıyor")
        if data['BMI'] > 30:
            factors.append("🔴 Obezite (BMI>30): Major risk faktörü")
        elif data['BMI'] > 25:
            factors.append("⚠️ Fazla kilo (BMI>25): Risk artırıcı")
        if data['HighBP'] == 1:
            factors.append("🔴 Yüksek tansiyon: Diyabet riskini artırır")
        if data['HighChol'] == 1:
            factors.append("🔴 Yüksek kolesterol: Metabolik sendrom işareti")
        if data['HeartDiseaseorAttack'] == 1:
            factors.append("🔴 Kalp hastalığı: Diyabetle güçlü ilişkili")
        if data['PhysActivity'] == 0:
            factors.append("⚠️ Fiziksel inaktivite: Egzersiz başlayın")
        if data['Smoker'] == 1:
            factors.append("⚠️ Sigara kullanımı: İnsülin direncini artırır")
        if data['GenHlth'] >= 4:
            factors.append("⚠️ Kötü genel sağlık algısı")
        if data['DiffWalk'] == 1:
            factors.append("⚠️ Hareket kısıtlılığı")
        if data['Fruits'] == 0 and data['Veggies'] == 0:
            factors.append("⚠️ Yetersiz meyve/sebze tüketimi")
        
        if factors:
            for factor in factors:
                print(f"   {factor}")
        else:
            print("   ✅ Major risk faktörü tespit edilmedi")
        
        # BMI yorumu
        print("\n" + "-" * 40)
        print("📏 BMI DEĞERLENDİRMESİ:")
        bmi = data['BMI']
        if bmi < 18.5:
            print(f"   BMI: {bmi:.1f} - Zayıf")
        elif bmi < 25:
            print(f"   BMI: {bmi:.1f} - Normal ✅")
        elif bmi < 30:
            print(f"   BMI: {bmi:.1f} - Fazla Kilolu ⚠️")
        elif bmi < 35:
            print(f"   BMI: {bmi:.1f} - Obez (Sınıf 1) 🔴")
        elif bmi < 40:
            print(f"   BMI: {bmi:.1f} - Obez (Sınıf 2) 🔴")
        else:
            print(f"   BMI: {bmi:.1f} - Morbid Obez (Sınıf 3) 🚨")
        
        print("\n" + "=" * 80)
        print("⚕️ UYARI: Bu rapor bilgilendirme amaçlıdır.")
        print("   Kesin tanı için mutlaka bir endokrinoloji veya dahiliye")
        print("   uzmanına başvurunuz. Diyabet tanısı SADECE kan testleriyle konur.")
        print("=" * 80 + "\n")


def main():
    """Ana program"""
    system = DiabetesRiskSystem()
    
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
