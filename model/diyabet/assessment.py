import os, pickle
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class DiabetesRiskAssessment:
    """Diyabet Hastalığı Risk Değerlendirme Sistemi"""
    
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
        # _real_age gibi ekstra alanları çıkar
        data_clean = {k: v for k, v in patient_data.items() if not k.startswith('_')}
        df = pd.DataFrame([data_clean])
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
        
        overall_risk = (ensemble_proba[1] * 25 + ensemble_proba[2] * 60 + ensemble_proba[3] * 100)
        assessment = self._generate_assessment(predicted_severity, risk_percentages, 
                                                overall_risk, patient_data)
        return assessment
    
    def _generate_assessment(self, severity, percentages, overall_risk, patient_data):
        """Değerlendirme ve öneriler oluştur"""
        
        severity_names = {
            0: "Diyabet Riski Minimal",
            1: "Düşük Diyabet Riski",
            2: "Orta Düzey Risk (Prediyabet Olabilir)",
            3: "Yüksek Risk (Diyabet Olabilir)"
        }
        
        result = {
            'tahmin': severity_names[severity],
            'seviye': severity,
            'genel_risk_skoru': round(overall_risk, 1),
            'risk_dagilimi': {
                'Minimal': round(percentages['minimal'], 1),
                'Düşük': round(percentages['dusuk'], 1),
                'Orta (Prediyabet)': round(percentages['orta'], 1),
                'Yüksek (Diyabet)': round(percentages['yuksek'], 1)
            }
        }
        
        if severity == 0:
            result['doktor_onerisi'] = '❌ Acil doktor kontrolü gerekmiyor'
            result['tedavi_onerisi'] = '✅ Sağlıklı yaşam tarzını sürdürün'
            result['takip'] = 'Yıllık check-up yeterli'
            result['aciliyet'] = 'Düşük'
            result['detaylar'] = [
                '• Düzenli egzersiz yapın (haftada 150 dakika)',
                '• Dengeli beslenmeye devam edin',
                '• İdeal kilonuzu koruyun (BMI 18.5-24.9)',
                '• Yılda bir açlık kan şekeri kontrolü',
                '• Bol su için, şekerli içeceklerden kaçının',
                '• Stres yönetimi ve yeterli uyku'
            ]
            
        elif severity == 1:
            result['doktor_onerisi'] = '⚠️ 6 ay içinde check-up yaptırın'
            result['tedavi_onerisi'] = '🏃 YAŞAM TARZI DEĞİŞİKLİĞİ ÖNERİLİYOR'
            result['takip'] = '6 ayda bir kontrol'
            result['aciliyet'] = 'Orta'
            result['detaylar'] = [
                '• Açlık kan şekeri (FPG) ve HbA1c testi yaptırın',
                '• %5-7 kilo vermeye çalışın',
                '• Günde 30 dakika yürüyüş yapın',
                '• Şekerli içecekleri tamamen bırakın',
                '• Tam tahıllı gıdaları tercih edin',
                '• Porsiyon kontrolü yapın',
                '• Lipid profili kontrolü',
                '• 6 ayda bir doktor kontrolü'
            ]
            
        elif severity == 2:
            result['doktor_onerisi'] = '🚨 1-2 AY içinde endokrinoloji/dahiliye uzmanına başvurun'
            result['tedavi_onerisi'] = '💊 PREDİYABET TEDAVİSİ GEREKEBİLİR'
            result['takip'] = '3 ayda bir kontrol ZORUNLU'
            result['aciliyet'] = 'Yüksek'
            result['detaylar'] = [
                '• Oral Glukoz Tolerans Testi (OGTT) yaptırın',
                '• HbA1c testi ve açlık insülin ölçümü',
                '• Metformin başlanabilir (doktor kararıyla)',
                '• Diyabet eğitim programına katılın',
                '• Diyetisyen danışmanlığı alın',
                '• %7-10 kilo verme hedefleyin',
                '• Günde 45-60 dakika egzersiz yapın',
                '• Karbonhidrat sayımını öğrenin',
                '• Evde kan şekeri takibi başlayın',
                '• Böbrek fonksiyonları takibi',
                '• 3 ayda bir HbA1c kontrolü ZORUNLU'
            ]
            
        else:  # severity == 3
            result['doktor_onerisi'] = '🚨🚨 HEMEN endokrinoloji uzmanına başvurun!'
            result['tedavi_onerisi'] = '🏥 DİYABET TEDAVİSİ GEREKİYOR OLABİLİR'
            result['takip'] = 'Haftalık/aylık kontrol (doktor belirleyecek)'
            result['aciliyet'] = 'ÇOK YÜKSEK - ACİL'
            result['detaylar'] = [
                '• ACİL: Açlık kan şekeri ve HbA1c testi',
                '• Tam idrar tahlili (idrarda şeker/protein)',
                '• Böbrek fonksiyon testleri',
                '• Göz dibi muayenesi (retinopati taraması)',
                '• Ayak muayenesi (nöropati taraması)',
                '• Oral antidiyabetik ilaçlar başlanabilir',
                '• Gerekirse insülin tedavisi',
                '• Tansiyon ve kolesterol takibi',
                '• Diyabet diyetine HEMEN başlayın',
                '• Günde 2-3 kez kan şekeri ölçümü',
                '• Sigara ve alkolü bırakın',
                '• Yılda 1 göz ve ayak muayenesi',
                '• Düzenli böbrek fonksiyon takibi'
            ]
        
        # Risk faktörleri analizi
        result['risk_faktorleri'] = self._analyze_risk_factors(patient_data)
        
        return result
    
    def _analyze_risk_factors(self, data):
        """Risk faktörlerini analiz et"""
        factors = []
        
        # Yaş hesaplama
        real_age = data.get('_real_age', data['Age'] * 5 + 18)
        
        if real_age > 45:
            factors.append('⚠️ 45 yaş üstü: Diyabet riski artıyor')
        if real_age > 65:
            factors.append('🔴 65 yaş üstü: Yüksek risk grubu')
        
        if data['BMI'] > 35:
            factors.append('🔴 İleri derece obezite (BMI>35): Çok yüksek risk')
        elif data['BMI'] > 30:
            factors.append('🔴 Obezite (BMI>30): Major risk faktörü')
        elif data['BMI'] > 25:
            factors.append('⚠️ Fazla kilo (BMI>25): Risk artırıcı')
        
        if data['HighBP'] == 1:
            factors.append('🔴 Yüksek tansiyon: Diyabet riskini 2 kat artırır')
        
        if data['HighChol'] == 1:
            factors.append('🔴 Yüksek kolesterol: Metabolik sendrom bileşeni')
        
        if data['HeartDiseaseorAttack'] == 1:
            factors.append('🔴 Kalp hastalığı: Diyabetle çok güçlü ilişkili')
        
        if data['Stroke'] == 1:
            factors.append('🔴 İnme öyküsü: Yüksek kardiyovasküler risk')
        
        if data['PhysActivity'] == 0:
            factors.append('⚠️ Fiziksel inaktivite: İnsülin direncini artırır')
        
        if data['Smoker'] == 1:
            factors.append('⚠️ Sigara kullanımı: İnsülin direncini %30-40 artırır')
        
        if data['HvyAlcoholConsump'] == 1:
            factors.append('⚠️ Ağır alkol tüketimi: Pankreas hasarı riski')
        
        if data['GenHlth'] >= 4:
            factors.append('⚠️ Kötü genel sağlık algısı')
        
        if data['DiffWalk'] == 1:
            factors.append('⚠️ Hareket kısıtlılığı: Egzersiz zorlaşır')
        
        if data['Fruits'] == 0 and data['Veggies'] == 0:
            factors.append('⚠️ Yetersiz meyve ve sebze tüketimi')
        
        if data['AnyHealthcare'] == 0:
            factors.append('⚠️ Sağlık sigortası yok: Takip zorlaşabilir')
        
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
    
    def generate_report(self, patient_data, patient_name="Hasta"):
        """Detaylı rapor oluştur"""
        assessment = self.assess_risk(patient_data)
        real_age = patient_data.get('_real_age', patient_data['Age'] * 5 + 18)
        
        print("\n" + "=" * 80)
        print(f"DİYABET HASTALIĞI RİSK DEĞERLENDİRME RAPORU - {patient_name}")
        print("=" * 80)
        
        print(f"\n📋 HASTA BİLGİLERİ:")
        print(f"   Yaş: {real_age:.0f}")
        print(f"   Cinsiyet: {'Erkek' if patient_data['Sex'] == 1 else 'Kadın'}")
        bmi_status, bmi_icon = self._calculate_bmi_status(patient_data['BMI'])
        print(f"   BMI: {patient_data['BMI']:.1f} - {bmi_status} {bmi_icon}")
        
        print(f"\n🎯 TAHMİN SONUCU:")
        print(f"   Durum: {assessment['tahmin']}")
        print(f"   Genel Risk Skoru: {assessment['genel_risk_skoru']:.1f}/100")
        print(f"   Aciliyet Seviyesi: {assessment['aciliyet']}")
        
        print(f"\n📊 RİSK DAĞILIMI:")
        for risk_type, percentage in assessment['risk_dagilimi'].items():
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            print(f"   {risk_type:.<25} {percentage:>5.1f}% {bar}")
        
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
        print(f"   BMI: {patient_data['BMI']:.1f}")
        print(f"   Yüksek Tansiyon: {'Evet' if patient_data['HighBP'] else 'Hayır'}")
        print(f"   Yüksek Kolesterol: {'Evet' if patient_data['HighChol'] else 'Hayır'}")
        print(f"   Kalp Hastalığı: {'Evet' if patient_data['HeartDiseaseorAttack'] else 'Hayır'}")
        print(f"   Fiziksel Aktivite: {'Evet' if patient_data['PhysActivity'] else 'Hayır'}")
        print(f"   Sigara: {'Evet' if patient_data['Smoker'] else 'Hayır'}")
        print(f"   Genel Sağlık: {patient_data['GenHlth']}/5")
        
        print("\n" + "=" * 80)
        print("⚕️ BU RAPOR BİLGİLENDİRME AMAÇLIDIR. KESİN TANI İÇİN MUTLAKA")
        print("   ENDOKRİNOLOJİ VEYA DAHİLİYE UZMANI İLE GÖRÜŞÜNÜZ.")
        print("   DİYABET TANISI SADECE KAN TESTLERİYLE KONUR:")
        print("   • Açlık Kan Şekeri (FPG) ≥ 126 mg/dL")
        print("   • HbA1c ≥ %6.5")
        print("   • OGTT 2. saat ≥ 200 mg/dL")
        print("=" * 80)
        
        return assessment


# ÖRNEK KULLANIM - 5 FARKLI DURUM
if __name__ == "__main__":
    system = DiabetesRiskAssessment()
    
    # ÖRNEK 1: Minimal Risk (Sağlıklı Genç)
    print("\n\n🟢 ÖRNEK 1: MİNİMAL RİSK (Sağlıklı Birey)")
    patient1 = {
        'HighBP': 0,
        'HighChol': 0,
        'CholCheck': 1,
        'BMI': 22.5,
        'Smoker': 0,
        'Stroke': 0,
        'HeartDiseaseorAttack': 0,
        'PhysActivity': 1,
        'Fruits': 1,
        'Veggies': 1,
        'HvyAlcoholConsump': 0,
        'AnyHealthcare': 1,
        'NoDocbcCost': 0,
        'GenHlth': 1,
        'MentHlth': 0,
        'PhysHlth': 0,
        'DiffWalk': 0,
        'Sex': 0,
        'Age': 5,  # ~40 yaş
        'Education': 6,
        'Income': 7,
        '_real_age': 35
    }
    system.generate_report(patient1, "Ayşe Hanım (35)")
    
    # ÖRNEK 2: Düşük Risk (Risk Faktörlü Sağlıklı)
    print("\n\n🟡 ÖRNEK 2: DÜŞÜK RİSK (Dikkat Gerektiren)")
    patient2 = {
        'HighBP': 0,
        'HighChol': 1,
        'CholCheck': 1,
        'BMI': 27.5,
        'Smoker': 1,
        'Stroke': 0,
        'HeartDiseaseorAttack': 0,
        'PhysActivity': 0,
        'Fruits': 0,
        'Veggies': 1,
        'HvyAlcoholConsump': 0,
        'AnyHealthcare': 1,
        'NoDocbcCost': 0,
        'GenHlth': 3,
        'MentHlth': 5,
        'PhysHlth': 3,
        'DiffWalk': 0,
        'Sex': 1,
        'Age': 7,  # ~50 yaş
        'Education': 5,
        'Income': 5,
        '_real_age': 48
    }
    system.generate_report(patient2, "Mehmet Bey (48)")
    
    # ÖRNEK 3: Orta Risk (Prediyabet Adayı)
    print("\n\n🟠 ÖRNEK 3: ORTA RİSK (Prediyabet Olabilir)")
    patient3 = {
        'HighBP': 1,
        'HighChol': 1,
        'CholCheck': 1,
        'BMI': 31.5,
        'Smoker': 1,
        'Stroke': 0,
        'HeartDiseaseorAttack': 0,
        'PhysActivity': 0,
        'Fruits': 0,
        'Veggies': 0,
        'HvyAlcoholConsump': 0,
        'AnyHealthcare': 1,
        'NoDocbcCost': 0,
        'GenHlth': 4,
        'MentHlth': 10,
        'PhysHlth': 15,
        'DiffWalk': 1,
        'Sex': 0,
        'Age': 9,  # ~60 yaş
        'Education': 4,
        'Income': 4,
        '_real_age': 58
    }
    system.generate_report(patient3, "Fatma Hanım (58)")
    
    # ÖRNEK 4: Yüksek Risk (Diyabet Olabilir)
    print("\n\n🔴 ÖRNEK 4: YÜKSEK RİSK (Diyabet Olabilir)")
    patient4 = {
        'HighBP': 1,
        'HighChol': 1,
        'CholCheck': 1,
        'BMI': 38.2,
        'Smoker': 1,
        'Stroke': 0,
        'HeartDiseaseorAttack': 1,
        'PhysActivity': 0,
        'Fruits': 0,
        'Veggies': 0,
        'HvyAlcoholConsump': 0,
        'AnyHealthcare': 1,
        'NoDocbcCost': 0,
        'GenHlth': 5,
        'MentHlth': 15,
        'PhysHlth': 20,
        'DiffWalk': 1,
        'Sex': 1,
        'Age': 11,  # ~70 yaş
        'Education': 3,
        'Income': 3,
        '_real_age': 67
    }
    system.generate_report(patient4, "Ali Bey (67)")
    
    # ÖRNEK 5: Sınırda Durum
    print("\n\n🟡 ÖRNEK 5: SINIRDA DURUM (Yakın Takip Gerekli)")
    patient5 = {
        'HighBP': 1,
        'HighChol': 0,
        'CholCheck': 1,
        'BMI': 29.0,
        'Smoker': 0,
        'Stroke': 0,
        'HeartDiseaseorAttack': 0,
        'PhysActivity': 1,
        'Fruits': 1,
        'Veggies': 1,
        'HvyAlcoholConsump': 0,
        'AnyHealthcare': 1,
        'NoDocbcCost': 0,
        'GenHlth': 3,
        'MentHlth': 5,
        'PhysHlth': 5,
        'DiffWalk': 0,
        'Sex': 0,
        'Age': 8,  # ~55 yaş
        'Education': 5,
        'Income': 6,
        '_real_age': 52
    }
    system.generate_report(patient5, "Zeynep Hanım (52)")
