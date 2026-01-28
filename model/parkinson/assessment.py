import os, pickle
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ParkinsonRiskAssessment:
    """Parkinson Hastalığı Risk Değerlendirme Sistemi"""
    
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
            'risk_yok': ensemble_proba[0] * 100,
            'hafif': ensemble_proba[1] * 100,
            'orta': ensemble_proba[2] * 100,
            'ileri': ensemble_proba[3] * 100
        }
        
        overall_risk = (ensemble_proba[1] * 33 + ensemble_proba[2] * 66 + ensemble_proba[3] * 100)
        assessment = self._generate_assessment(predicted_severity, risk_percentages, 
                                                overall_risk, patient_data)
        return assessment
    
    def _generate_assessment(self, severity, percentages, overall_risk, patient_data):
        """Değerlendirme ve öneriler oluştur"""
        
        severity_names = {
            0: "Parkinson Riski Yok / Minimal",
            1: "Hafif Parkinson Belirtileri",
            2: "Orta Düzey Parkinson",
            3: "İleri Parkinson"
        }
        
        result = {
            'tahmin': severity_names[severity],
            'seviye': severity,
            'genel_risk_skoru': round(overall_risk, 1),
            'risk_dagilimi': {
                'Risk Yok': round(percentages['risk_yok'], 1),
                'Hafif': round(percentages['hafif'], 1),
                'Orta': round(percentages['orta'], 1),
                'İleri': round(percentages['ileri'], 1)
            }
        }
        
        if severity == 0:
            result['doktor_onerisi'] = '❌ Acil doktor kontrolü gerekmiyor'
            result['tedavi_onerisi'] = '✅ Önleyici yaşam tarzı değişiklikleri'
            result['takip'] = 'Yıllık kontrol yeterli'
            result['aciliyet'] = 'Düşük'
            result['detaylar'] = [
                '• Düzenli egzersiz yapın (haftada 3-4 gün, 30 dakika)',
                '• Dengeli beslenme (Akdeniz diyeti önerilir)',
                '• Zihinsel aktiviteler (bulmaca, okuma, sosyal aktiviteler)',
                '• Uyku düzenine dikkat edin (7-8 saat)',
                '• Kafa travmalarından korunun'
            ]
            
        elif severity == 1:
            result['doktor_onerisi'] = '⚠️ Nöroloji uzmanına başvurun (1-2 ay içinde)'
            result['tedavi_onerisi'] = '💊 İLAÇ TEDAVİSİ ÖNERİLİYOR'
            result['takip'] = '3-6 ayda bir kontrol'
            result['aciliyet'] = 'Orta'
            result['detaylar'] = [
                '• Levodopa veya dopamin agonistleri değerlendirilmeli',
                '• MAO-B inhibitörleri (Rasajilin, Selejilin) düşünülebilir',
                '• Fizik tedavi ve rehabilitasyon programı başlatın',
                '• Egzersiz programı (özellikle denge ve kuvvet egzersizleri)',
                '• Konuşma terapisi değerlendirmesi',
                '• 3 ayda bir nöroloji kontrolü yapılmalı'
            ]
            
        elif severity == 2:
            result['doktor_onerisi'] = '🚨 ACİL nöroloji uzmanı konsültasyonu (1-2 hafta içinde)'
            result['tedavi_onerisi'] = '💊💊 YAKIN TAKİP + İLAÇ TEDAVİSİ GEREKLİ'
            result['takip'] = 'Aylık kontrol zorunlu'
            result['aciliyet'] = 'Yüksek'
            result['detaylar'] = [
                '• Kombine ilaç tedavisi gerekebilir (Levodopa + COMT inhibitörü)',
                '• İlaç dozları ve zamanlaması optimize edilmeli',
                '• Fizik tedavi ve rehabilitasyon YOĞUNLAŞTIRILMALI',
                '• Konuşma ve yutma terapisi',
                '• Günlük yaşam aktiviteleri için ergoterapi',
                '• Motor dalgalanmaları ve diskinezi izlenmeli',
                '• Aylık nöroloji kontrolü ZORUNLU',
                '• Destek gruplarına katılım önerilir'
            ]
            
        else: # severity == 3
            result['doktor_onerisi'] = '🚨🚨 ACİL hareket bozuklukları merkezine sevk (HEMEN)'
            result['tedavi_onerisi'] = '🏥 CERRAHİ DEĞERLENDİRME + YOĞUN İLAÇ TEDAVİSİ'
            result['takip'] = 'Haftalık/iki haftada bir kontrol'
            result['aciliyet'] = 'ÇOK YÜKSEK - ACİL'
            result['detaylar'] = [
                '• DBS (Derin Beyin Stimülasyonu) ameliyatı değerlendirilmeli',
                '• Apomorfin infüzyon pompası düşünülebilir',
                '• Duodopa (jejunostomi) değerlendirmesi',
                '• Maksimum ilaç tedavisi optimize edilmeli',
                '• Yoğun fizik tedavi ve rehabilitasyon ZORUNLU',
                '• Bakım veren eğitimi ve desteği',
                '• Beslenme desteği (gerekirse NGT)',
                '• Psikiyatri konsültasyonu (depresyon/anksiyete için)',
                '• Evde bakım hizmetleri düzenlemesi',
                '• Haftalık/iki haftada bir hareket bozuklukları uzmanı takibi'
            ]
        
        # Risk faktörleri analizi
        result['risk_faktorleri'] = self._analyze_risk_factors(patient_data)
        
        return result
    
    def _analyze_risk_factors(self, data):
        """Risk faktörlerini analiz et"""
        factors = []
        
        if data['age'] > 70:
            factors.append('⚠️ İleri yaş (70+): Parkinson riski artırır')
        
        if data['tremor_score'] > 3:
            factors.append('🔴 Yüksek tremor skoru: Major semptom')
        
        if data['rigidity'] > 3:
            factors.append('🔴 Yüksek rijidite: Kas sertliği belirgin')
        
        if data['bradykinesia'] > 3:
            factors.append('🔴 Belirgin bradykinezi: Hareket yavaşlığı')
        
        if data['postural_instability'] > 2.5:
            factors.append('⚠️ Postural instabilite: Düşme riski yüksek')
        
        if data['motor_updrs'] > 40:
            factors.append('🔴 Yüksek motor UPDRS: İleri motor belirtiler')
        
        if data['jitter'] > 0.01:
            factors.append('⚠️ Yüksek jitter: Ses bozuklukları')
        
        if data['levodopa_response'] < 50:
            factors.append('🔴 Düşük levodopa yanıtı: Tedavi zorluğu')
        
        if data['disease_duration'] > 5:
            factors.append('⚠️ Uzun hastalık süresi: Progresyon riski')
        
        if not factors:
            factors.append('✅ Major risk faktörü tespit edilmedi')
        
        return factors
    
    def generate_report(self, patient_data, patient_name="Hasta"):
        """Detaylı rapor oluştur"""
        assessment = self.assess_risk(patient_data)
        
        print("\n" + "=" * 80)
        print(f"PARKINSON HASTALIĞI RİSK DEĞERLENDİRME RAPORU - {patient_name}")
        print("=" * 80)
        
        print(f"\n📋 HASTA BİLGİLERİ:")
        print(f"   Yaş: {patient_data['age']:.0f}")
        print(f"   Hastalık Süresi: {patient_data['disease_duration']:.1f} yıl")
        
        print(f"\n🎯 TAHMİN SONUCU:")
        print(f"   Durum: {assessment['tahmin']}")
        print(f"   Genel Risk Skoru: {assessment['genel_risk_skoru']:.1f}/100")
        print(f"   Aciliyet Seviyesi: {assessment['aciliyet']}")
        
        print(f"\n📊 RİSK DAĞILIMI:")
        for risk_type, percentage in assessment['risk_dagilimi'].items():
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            print(f"   {risk_type:.<20} {percentage:>5.1f}% {bar}")
        
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
        print(f"   Motor UPDRS: {patient_data['motor_updrs']:.1f}")
        print(f"   Tremor Skoru: {patient_data['tremor_score']:.1f}/5")
        print(f"   Rijidite: {patient_data['rigidity']:.1f}/5")
        print(f"   Bradikinezi: {patient_data['bradykinesia']:.1f}/5")
        print(f"   Postural İnstabilite: {patient_data['postural_instability']:.1f}/5")
        print(f"   Levodopa Yanıtı: {patient_data['levodopa_response']:.1f}%")
        
        print("\n" + "=" * 80)
        print("⚕️ BU RAPOR BİLGİLENDİRME AMAÇLIDIR. MUTLAKA BİR NÖROLOJI UZMANI İLE")
        print("   GÖRÜŞÜNÜZ. KESİN TANI İÇİN KLİNİK DEĞERLENDİRME GEREKLİDİR.")
        print("=" * 80)
        
        return assessment


# ÖRNEK KULLANIM - 5 FARKLI DURUM
if __name__ == "__main__":
    system = ParkinsonRiskAssessment()
    
    # ÖRNEK 1: Minimal Risk
    print("\n\n🟢 ÖRNEK 1: MİNİMAL RİSK (Sağlıklı Birey)")
    patient1 = {
        'age': 58,
        'motor_updrs': 15,
        'total_updrs': 20,
        'jitter': 0.003,
        'shimmer': 0.02,
        'nhr': 0.015,
        'hnr': 25,
        'tremor_score': 0.5,
        'rigidity': 0.3,
        'bradykinesia': 0.4,
        'postural_instability': 0.2,
        'disease_duration': 0,
        'levodopa_response': 80
    }
    system.generate_report(patient1, "Ahmet Bey (58)")
    
    # ÖRNEK 2: Hafif Parkinson
    print("\n\n🟡 ÖRNEK 2: HAFİF PARKINSON BELİRTİLERİ")
    patient2 = {
        'age': 65,
        'motor_updrs': 28,
        'total_updrs': 38,
        'jitter': 0.0065,
        'shimmer': 0.035,
        'nhr': 0.025,
        'hnr': 18,
        'tremor_score': 2.1,
        'rigidity': 1.8,
        'bradykinesia': 2.3,
        'postural_instability': 1.2,
        'disease_duration': 1.5,
        'levodopa_response': 75
    }
    system.generate_report(patient2, "Mehmet Bey (65)")
    
    # ÖRNEK 3: Orta Düzey Parkinson
    print("\n\n🟠 ÖRNEK 3: ORTA DÜZEY PARKINSON")
    patient3 = {
        'age': 70,
        'motor_updrs': 45,
        'total_updrs': 60,
        'jitter': 0.011,
        'shimmer': 0.055,
        'nhr': 0.045,
        'hnr': 14,
        'tremor_score': 3.5,
        'rigidity': 3.2,
        'bradykinesia': 3.8,
        'postural_instability': 2.9,
        'disease_duration': 4.5,
        'levodopa_response': 58
    }
    system.generate_report(patient3, "Ayşe Hanım (70)")
    
    # ÖRNEK 4: İleri Parkinson
    print("\n\n🔴 ÖRNEK 4: İLERİ PARKINSON")
    patient4 = {
        'age': 75,
        'motor_updrs': 68,
        'total_updrs': 95,
        'jitter': 0.016,
        'shimmer': 0.078,
        'nhr': 0.068,
        'hnr': 9,
        'tremor_score': 4.5,
        'rigidity': 4.3,
        'bradykinesia': 4.7,
        'postural_instability': 4.2,
        'disease_duration': 9.5,
        'levodopa_response': 35
    }
    system.generate_report(patient4, "Fatma Hanım (75)")
    
    # ÖRNEK 5: Sınırda Durum
    print("\n\n🟡 ÖRNEK 5: SINIRDA DURUM (Yakın takip gerekli)")
    patient5 = {
        'age': 62,
        'motor_updrs': 32,
        'total_updrs': 42,
        'jitter': 0.008,
        'shimmer': 0.04,
        'nhr': 0.03,
        'hnr': 16,
        'tremor_score': 2.5,
        'rigidity': 2.2,
        'bradykinesia': 2.8,
        'postural_instability': 1.8,
        'disease_duration': 2.0,
        'levodopa_response': 68
    }
    system.generate_report(patient5, "Ali Bey (62)")
