import os, pickle
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class HypertensionRiskAssessment:
    """Hipertansiyon (Yüksek Tansiyon) Risk Değerlendirme Sistemi"""
    
    def __init__(self):
        with open(os.path.join(BASE_DIR, "m1.pkl"), "rb") as f:
            self.rf_model = pickle.load(f)

        with open(os.path.join(BASE_DIR, "m2.pkl"), "rb") as f:
            self.gb_model = pickle.load(f)

        with open(os.path.join(BASE_DIR, "m3.pkl"), "rb") as f:
            self.scaler = pickle.load(f)
    
    def assess_risk(self, patient_data):
        """
        Hasta verisini analiz et ve risk değerlendirmesi yap
        
        Parameters:
        -----------
        patient_data : dict
            Hasta verileri
            
        Returns:
        --------
        dict : Risk değerlendirmesi ve öneriler
        """
        df = pd.DataFrame([patient_data])
        X_scaled = self.scaler.transform(df)
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
        
        overall_risk = (ensemble_proba[1] * 30 + ensemble_proba[2] * 65 + ensemble_proba[3] * 100)
        assessment = self._generate_assessment(predicted_severity, risk_percentages, 
                                                overall_risk, patient_data)
        return assessment
    
    def _generate_assessment(self, severity, percentages, overall_risk, patient_data):
        """Değerlendirme ve öneriler oluştur"""
        
        severity_names = {
            0: "Hipertansiyon Riski Minimal",
            1: "Düşük Risk (Prehipertansiyon Eğilimi)",
            2: "Orta Düzey Risk (Hipertansiyon - Kontrollü)",
            3: "Yüksek Risk (İleri Hipertansiyon)"
        }
        
        result = {
            'tahmin': severity_names[severity],
            'seviye': severity,
            'genel_risk_skoru': round(overall_risk, 1),
            'risk_dagilimi': {
                'Minimal': round(percentages['minimal'], 1),
                'Düşük (Prehipertansiyon)': round(percentages['dusuk'], 1),
                'Orta (Kontrollü HT)': round(percentages['orta'], 1),
                'Yüksek (İleri HT)': round(percentages['yuksek'], 1)
            }
        }
        
        if severity == 0:
            result['doktor_onerisi'] = '❌ Acil doktor kontrolü gerekmiyor'
            result['tedavi_onerisi'] = '✅ Sağlıklı yaşam tarzını sürdürün'
            result['takip'] = 'Yıllık tansiyon kontrolü yeterli'
            result['aciliyet'] = 'Düşük'
            result['detaylar'] = [
                '• Düşük tuzlu beslenmeye devam edin (<6g/gün)',
                '• Düzenli egzersiz yapın (haftada 150 dakika)',
                '• İdeal kilonuzu koruyun (BMI 18.5-24.9)',
                '• Yılda en az 2 kez tansiyon ölçtürün',
                '• Stresi yönetin, yeterli uyuyun (7-8 saat)',
                '• Sigara ve aşırı alkolden kaçının'
            ]
            
        elif severity == 1:
            result['doktor_onerisi'] = '⚠️ 3-6 ay içinde kardiyoloji kontrolü'
            result['tedavi_onerisi'] = '🏃 YAŞAM TARZI DEĞİŞİKLİĞİ ZORUNLU'
            result['takip'] = '3 ayda bir kontrol'
            result['aciliyet'] = 'Orta'
            result['detaylar'] = [
                '• Evde düzenli tansiyon takibi başlayın (sabah-akşam)',
                '• DASH diyetine geçin (meyve, sebze, az yağlı süt ürünleri)',
                '• Günlük tuz alımını <6g\'a düşürün',
                '• %5-10 kilo vermeye çalışın',
                '• Günde 30-45 dakika tempolu yürüyüş yapın',
                '• Stresi azaltın (meditasyon, derin nefes, yoga)',
                '• Alkol tüketimini sınırlayın (E:<2, K:<1 kadeh/gün)',
                '• Kafein alımını azaltın',
                '• Holter tansiyon monitörizasyonu yaptırın',
                '• 3 ayda bir kardiyoloji kontrolü'
            ]
            
        elif severity == 2:
            result['doktor_onerisi'] = '🚨 1-2 AY içinde kardiyoloji uzmanına başvurun'
            result['tedavi_onerisi'] = '💊 İLAÇ TEDAVİSİ + YAŞAM TARZI DEĞİŞİKLİĞİ'
            result['takip'] = 'Aylık kontrol ZORUNLU'
            result['aciliyet'] = 'Yüksek'
            result['detaylar'] = [
                '• 24 saat ambulatuvar tansiyon izlemi (Holter) yaptırın',
                '• Ekokardiyografi (kalp ultrason) çekilmeli',
                '• Böbrek fonksiyonları kontrol edilmeli (kreatinin, BUN)',
                '• Göz dibi muayenesi (hipertansif retinopati)',
                '• İlaç tedavisi başlanabilir (ACE inhibitörü, ARB)',
                '• Gerekirse kombinasyon tedavisi uygulanabilir',
                '• Günlük tuz <5g KESİNLİKLE',
                '• DASH diyeti KESİNLİKLE uygulanmalı',
                '• Günde 2 kez evde tansiyon ölçümü (kayıt tutun)',
                '• Kilo kontrolü (BMI <25 hedef)',
                '• Sigara BIRAKILMALI',
                '• Aylık kardiyoloji kontrolü ZORUNLU'
            ]
            
        else:  # severity == 3
            result['doktor_onerisi'] = '🚨🚨 HEMEN kardiyoloji uzmanına başvurun!'
            result['tedavi_onerisi'] = '🏥 YOĞUN TEDAVİ + HEDEF ORGAN KORUMA'
            result['takip'] = 'Haftalık/2 haftada bir kontrol'
            result['aciliyet'] = 'ÇOK YÜKSEK - ACİL'
            result['detaylar'] = [
                '• ACİL: Tam kardiyak değerlendirme',
                '• Ekokardiyografi (sol ventrikül hipertrofisi?)',
                '• Böbrek fonksiyonları ve proteinüri taraması',
                '• Hedef organ hasarı taraması',
                '• Retinopati taraması (göz dibi)',
                '• Karotis Doppler (boyun damarları)',
                '• Kombine antihipertansif tedavi gerekli',
                '• İlaç dozları optimize edilmeli',
                '• Dirençli hipertansiyon değerlendirmesi',
                '• Sekonder hipertansiyon araştırması',
                '• Kalp: Sol ventrikül hipertrofisi takibi',
                '• Böbrek: GFR ve proteinüri takibi',
                '• Beyin: İnme risk değerlendirmesi',
                '• Haftalık/2 haftada bir kontrol ZORUNLU'
            ]
        
        # Risk faktörleri analizi
        result['risk_faktorleri'] = self._analyze_risk_factors(patient_data)
        
        return result
    
    def _analyze_risk_factors(self, data):
        """Risk faktörlerini analiz et"""
        factors = []
        
        if data['Age'] > 65:
            factors.append('🔴 İleri yaş (65+): Hipertansiyon için major risk faktörü')
        elif data['Age'] > 50:
            factors.append('⚠️ Orta yaş (50+): Risk artmaya başlıyor')
        
        if data['BMI'] > 30:
            factors.append('🔴 Obezite (BMI>30): Tansiyonu önemli ölçüde artırır')
        elif data['BMI'] > 25:
            factors.append('⚠️ Fazla kilo (BMI>25): Risk faktörü')
        
        if data['Salt_Intake'] > 10:
            factors.append('🔴 Çok yüksek tuz alımı (>10g): ACİL olarak azaltın!')
        elif data['Salt_Intake'] > 6:
            factors.append('⚠️ Yüksek tuz alımı (>6g): 6g altına düşürün')
        
        if data['Stress_Score'] > 7:
            factors.append('🔴 Yüksek stres seviyesi: Tansiyonu tetikler')
        elif data['Stress_Score'] > 4:
            factors.append('⚠️ Orta düzey stres: Stres yönetimi önemli')
        
        if data['Sleep_Duration'] < 6:
            factors.append('⚠️ Yetersiz uyku (<6 saat): Kardiyovasküler riski artırır')
        elif data['Sleep_Duration'] > 9:
            factors.append('⚠️ Aşırı uyku (>9 saat): Sağlık durumunu kontrol ettirin')
        
        if data['BP_History_Encoded'] == 2:
            factors.append('🔴 Hipertansiyon geçmişi: Yakın takip ve tedavi gerekli')
        elif data['BP_History_Encoded'] == 1:
            factors.append('⚠️ Prehipertansiyon geçmişi: Dikkatli olun')
        
        if data['Family_History_Encoded'] == 1:
            factors.append('⚠️ Ailede hipertansiyon: Genetik yatkınlık mevcut')
        
        if data['Exercise_Level_Encoded'] == 0:
            factors.append('⚠️ Hareketsiz yaşam: Düzenli egzersiz başlayın')
        
        if data['Smoking_Encoded'] == 1:
            factors.append('🔴 Sigara kullanımı: Damar sertliği ve tansiyon artışı - BIRAKIN!')
        
        if not factors:
            factors.append('✅ Major risk faktörü tespit edilmedi')
        
        return factors
    
    def _calculate_bmi_status(self, bmi):
        """BMI durumunu hesapla"""
        if bmi < 18.5:
            return 'Zayıf', '⚠️'
        elif bmi < 25:
            return 'Normal', '✅'
        elif bmi < 30:
            return 'Fazla Kilolu', '⚠️'
        elif bmi < 35:
            return 'Obez (Sınıf 1)', '🔴'
        elif bmi < 40:
            return 'Obez (Sınıf 2)', '🔴'
        else:
            return 'Morbid Obez (Sınıf 3)', '🚨'
    
    def _get_bp_history_text(self, encoded):
        """BP geçmişi kodunu metne çevir"""
        bp_map = {0: 'Normal', 1: 'Prehipertansiyon', 2: 'Hipertansiyon'}
        return bp_map.get(int(encoded), 'Bilinmiyor')
    
    def _get_exercise_text(self, encoded):
        """Egzersiz kodunu metne çevir"""
        ex_map = {0: 'Düşük', 1: 'Orta', 2: 'Yüksek'}
        return ex_map.get(int(encoded), 'Bilinmiyor')
    
    def generate_report(self, patient_data, patient_name="Hasta"):
        """Detaylı rapor oluştur"""
        assessment = self.assess_risk(patient_data)
        
        print("\n" + "=" * 80)
        print(f"HİPERTANSİYON RİSK DEĞERLENDİRME RAPORU - {patient_name}")
        print("=" * 80)
        
        print(f"\n📋 HASTA BİLGİLERİ:")
        print(f"   Yaş: {patient_data['Age']:.0f}")
        bmi_status, bmi_icon = self._calculate_bmi_status(patient_data['BMI'])
        print(f"   BMI: {patient_data['BMI']:.1f} - {bmi_status} {bmi_icon}")
        print(f"   Günlük Tuz Alımı: {patient_data['Salt_Intake']:.1f}g")
        print(f"   Tansiyon Geçmişi: {self._get_bp_history_text(patient_data['BP_History_Encoded'])}")
        
        print(f"\n🎯 TAHMİN SONUCU:")
        print(f"   Durum: {assessment['tahmin']}")
        print(f"   Genel Risk Skoru: {assessment['genel_risk_skoru']:.1f}/100")
        print(f"   Aciliyet Seviyesi: {assessment['aciliyet']}")
        
        print(f"\n📊 RİSK DAĞILIMI:")
        for risk_type, percentage in assessment['risk_dagilimi'].items():
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            print(f"   {risk_type:.<30} {percentage:>5.1f}% {bar}")
        
        print(f"\n👨‍⚕️ DOKTOR ÖNERİSİ:")
        print(f"   {assessment['doktor_onerisi']}")
        
        print(f"\n💊 TEDAVİ ÖNERİSİ:")
        print(f"   {assessment['tedavi_onerisi']}")
        
        print(f"\n📅 TAKİP PLANI:")
        print(f"   {assessment['takip']}")
        
        print(f"\n📝 DETAYLI ÖNERİLER:")
        for detail in assessment['detaylar']:
            print(f"   {detail}")
        
        print(f"\n⚠️ RİSK FAKTÖRLERİ ANALİZİ:")
        for factor in assessment['risk_faktorleri']:
            print(f"   {factor}")
        
        print(f"\n🔬 ÖLÇÜM SONUÇLARI:")
        print(f"   Yaş: {patient_data['Age']:.0f}")
        print(f"   BMI: {patient_data['BMI']:.1f}")
        print(f"   Tuz Alımı: {patient_data['Salt_Intake']:.1f}g/gün")
        print(f"   Stres Skoru: {patient_data['Stress_Score']:.0f}/10")
        print(f"   Uyku Süresi: {patient_data['Sleep_Duration']:.1f} saat")
        print(f"   Egzersiz: {self._get_exercise_text(patient_data['Exercise_Level_Encoded'])}")
        print(f"   Sigara: {'Evet' if patient_data['Smoking_Encoded'] else 'Hayır'}")
        print(f"   Aile Öyküsü: {'Evet' if patient_data['Family_History_Encoded'] else 'Hayır'}")
        
        print("\n" + "-" * 40)
        print("📏 TANSİYON DEĞERLERİ REFERANSI:")
        print("   Normal:          <120/80 mmHg")
        print("   Yüksek-Normal:   120-129/<80 mmHg")
        print("   Evre 1 HT:       130-139/80-89 mmHg")
        print("   Evre 2 HT:       ≥140/90 mmHg")
        print("   Hipertansif Kriz: >180/120 mmHg ⚠️")
        
        print("\n" + "=" * 80)
        print("⚕️ BU RAPOR BİLGİLENDİRME AMAÇLIDIR. KESİN TANI İÇİN MUTLAKA")
        print("   KARDİYOLOJİ VEYA DAHİLİYE UZMANI İLE GÖRÜŞÜNÜZ.")
        print("   HİPERTANSİYON TANISI İÇİN DÜZENLİ TANSİYON ÖLÇÜMÜ ŞARTTIR.")
        print("=" * 80)
        
        return assessment


# ÖRNEK KULLANIM - 5 FARKLI DURUM
if __name__ == "__main__":
    system = HypertensionRiskAssessment()
    
    # ÖRNEK 1: Minimal Risk (Sağlıklı Genç)
    print("\n\n🟢 ÖRNEK 1: MİNİMAL RİSK (Sağlıklı Birey)")
    patient1 = {
        'Age': 32,
        'Salt_Intake': 5.0,
        'Stress_Score': 3,
        'Sleep_Duration': 7.5,
        'BMI': 22.5,
        'BP_History_Encoded': 0,  # Normal
        'Medication_Encoded': 0,  # None
        'Family_History_Encoded': 0,  # Hayır
        'Exercise_Level_Encoded': 2,  # High
        'Smoking_Encoded': 0  # Non-smoker
    }
    system.generate_report(patient1, "Ayşe Hanım (32)")
    
    # ÖRNEK 2: Düşük Risk (Prehipertansiyon Eğilimli)
    print("\n\n🟡 ÖRNEK 2: DÜŞÜK RİSK (Prehipertansiyon Eğilimi)")
    patient2 = {
        'Age': 48,
        'Salt_Intake': 8.5,
        'Stress_Score': 6,
        'Sleep_Duration': 6.0,
        'BMI': 27.5,
        'BP_History_Encoded': 1,  # Prehipertansiyon
        'Medication_Encoded': 0,  # None
        'Family_History_Encoded': 1,  # Evet
        'Exercise_Level_Encoded': 1,  # Moderate
        'Smoking_Encoded': 0  # Non-smoker
    }
    system.generate_report(patient2, "Mehmet Bey (48)")
    
    # ÖRNEK 3: Orta Risk (Kontrollü Hipertansiyon)
    print("\n\n🟠 ÖRNEK 3: ORTA RİSK (Kontrollü Hipertansiyon)")
    patient3 = {
        'Age': 58,
        'Salt_Intake': 9.0,
        'Stress_Score': 7,
        'Sleep_Duration': 5.5,
        'BMI': 29.5,
        'BP_History_Encoded': 2,  # Hipertansiyon
        'Medication_Encoded': 3,  # ACE Inhibitor
        'Family_History_Encoded': 1,  # Evet
        'Exercise_Level_Encoded': 0,  # Low
        'Smoking_Encoded': 0  # Non-smoker
    }
    system.generate_report(patient3, "Fatma Hanım (58)")
    
    # ÖRNEK 4: Yüksek Risk (İleri Hipertansiyon)
    print("\n\n🔴 ÖRNEK 4: YÜKSEK RİSK (İleri Hipertansiyon)")
    patient4 = {
        'Age': 68,
        'Salt_Intake': 12.0,
        'Stress_Score': 9,
        'Sleep_Duration': 5.0,
        'BMI': 32.5,
        'BP_History_Encoded': 2,  # Hipertansiyon
        'Medication_Encoded': 4,  # Beta Blocker
        'Family_History_Encoded': 1,  # Evet
        'Exercise_Level_Encoded': 0,  # Low
        'Smoking_Encoded': 1  # Smoker
    }
    system.generate_report(patient4, "Ali Bey (68)")
    
    # ÖRNEK 5: Sınırda Durum
    print("\n\n🟡 ÖRNEK 5: SINIRDA DURUM (Yakın Takip Gerekli)")
    patient5 = {
        'Age': 52,
        'Salt_Intake': 7.5,
        'Stress_Score': 5,
        'Sleep_Duration': 6.5,
        'BMI': 26.0,
        'BP_History_Encoded': 1,  # Prehipertansiyon
        'Medication_Encoded': 0,  # None
        'Family_History_Encoded': 1,  # Evet
        'Exercise_Level_Encoded': 1,  # Moderate
        'Smoking_Encoded': 1  # Smoker
    }
    system.generate_report(patient5, "Zeynep Hanım (52)")
