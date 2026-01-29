#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Astım Hastalığı Risk Değerlendirme Sistemi
"""

import os, pickle
import numpy as np
import pandas as pd
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class AsthmaRiskAssessment:
    """Astım Hastalığı Risk Değerlendirme Sistemi"""
    
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
            sys.exit(1)
    
    def assess_risk(self, patient_data):
        """Hasta verisini analiz et ve risk değerlendirmesi yap"""
        # DataFrame oluştur
        df = pd.DataFrame([patient_data])
        
        # Özellikleri sırala
        df = df[self.feature_cols]
        
        # Normalizasyon
        X_scaled = self.m3.transform(df)
        
        # Tahminler
        m1_proba = self.m1.predict_proba(X_scaled)[0]
        m2_proba = self.m2.predict_proba(X_scaled)[0]
        
        # Ensemble tahmin
        ensemble_proba = (m1_proba + m2_proba) / 2
        predicted_asthma = int(np.argmax(ensemble_proba))
        
        # Risk yüzdesi
        asthma_risk = float(ensemble_proba[1]) * 100
        
        return {
            'has_asthma': predicted_asthma,
            'risk_percentage': round(asthma_risk, 1),
            'probabilities': {
                'no_asthma': round(float(ensemble_proba[0]) * 100, 1),
                'has_asthma': round(float(ensemble_proba[1]) * 100, 1)
            },
            'model_predictions': {
                'm1_rf': {
                    'no_asthma': round(float(m1_proba[0]) * 100, 1),
                    'has_asthma': round(float(m1_proba[1]) * 100, 1)
                },
                'm2_gb': {
                    'no_asthma': round(float(m2_proba[0]) * 100, 1),
                    'has_asthma': round(float(m2_proba[1]) * 100, 1)
                }
            }
        }
    
    def generate_recommendations(self, assessment, patient_data):
        """Değerlendirme ve öneriler oluştur"""
        risk = assessment['risk_percentage']
        has_asthma = assessment['has_asthma']
        
        recommendations = {
            'risk_level': '',
            'urgency': '',
            'doctor_visit': '',
            'treatment': '',
            'lifestyle': [],
            'risk_factors': [],
            'medications': []
        }
        
        # Risk seviyesini belirle
        if risk < 20:
            recommendations['risk_level'] = 'Çok Düşük Risk'
            recommendations['urgency'] = 'Düşük'
            recommendations['doctor_visit'] = 'Rutin kontrol yeterli (yıllık)'
            recommendations['treatment'] = 'Önleyici tedbirler'
            recommendations['lifestyle'] = [
                '✅ Düzenli egzersiz yapın (haftada 3-4 gün)',
                '✅ Tetikleyicilerden kaçının (polen, toz, duman)',
                '✅ Dengeli beslenme',
                '✅ Stres yönetimi',
                '✅ Uyku düzenine dikkat edin (7-8 saat)'
            ]
        elif risk < 50:
            recommendations['risk_level'] = 'Düşük Risk'
            recommendations['urgency'] = 'Orta'
            recommendations['doctor_visit'] = '6 ayda bir kontrol önerilir'
            recommendations['treatment'] = 'Takip ve önleyici tedbirler'
            recommendations['lifestyle'] = [
                '⚠️ Tetikleyicilerden uzak durun',
                '⚠️ Düzenli doktor kontrolü',
                '⚠️ Peak flow metre kullanımı',
                '⚠️ Acil durum planı hazırlayın',
                '✅ Fiziksel aktivite devam ettirin'
            ]
        elif risk < 75:
            recommendations['risk_level'] = 'Orta Risk'
            recommendations['urgency'] = 'Yüksek'
            recommendations['doctor_visit'] = '3 ayda bir kontrol GEREKLİ'
            recommendations['treatment'] = 'Kontrol edici ilaç tedavisi önerilir'
            recommendations['lifestyle'] = [
                '🚨 Göğüs hastalıkları uzmanına başvurun',
                '🚨 İlaç tedavisi gerekebilir',
                '⚠️ Tetikleyicilerden MUTLAKA kaçının',
                '⚠️ Peak flow takibi YAP',
                '⚠️ Acil eylem planı HAZIR olmalı'
            ]
            recommendations['medications'] = [
                '💊 İnhaler kortikoste roidler (kontrol edici)',
                '💊 Uzun etkili beta-2 agonistler',
                '💊 Kısa etkili beta-2 agonistler (acil durumlar için)',
                '💊 Leukotriene antagonistleri'
            ]
        else:
            recommendations['risk_level'] = 'Yüksek Risk'
            recommendations['urgency'] = 'ÇOK YÜKSEK - ACİL'
            recommendations['doctor_visit'] = 'HEMEN göğüs hastalıkları uzmanına başvurun'
            recommendations['treatment'] = 'ACİL tıbbi değerlendirme ve tedavi gerekli'
            recommendations['lifestyle'] = [
                '🚨🚨 HEMEN doktor randevusu alın',
                '🚨 Astım acil eylem planı EDİNİN',
                '🚨 Tetikleyicilerden TAM kaçınma',
                '⚠️ Peak flow günlük takip',
                '⚠️ İnhaler tekniği eğitimi alın'
            ]
            recommendations['medications'] = [
                '💊💊 Yüksek doz inhaler kortikosteroidler',
                '💊 Uzun etkili beta-2 agonistler',
                '💊 Kısa etkili bronkodilatörler (kurtarıcı)',
                '💊 Oral kortikosteroidler (gerekirse)',
                '💊 Biyolojik ajanlar (şiddetli astımda)'
            ]
        
        # Risk faktörlerini analiz et
        if patient_data.get('Smoking', 0) == 1:
            recommendations['risk_factors'].append('🔴 SİGARA İÇİYORSUNUZ - HEMEN BIRAKIN!')
        
        if patient_data.get('FamilyHistoryAsthma', 0) == 1:
            recommendations['risk_factors'].append('⚠️ Ailede astım öyküsü var')
        
        if patient_data.get('HistoryOfAllergies', 0) == 1:
            recommendations['risk_factors'].append('⚠️ Alerji geçmişi mevcut')
        
        if patient_data.get('PetAllergy', 0) == 1:
            recommendations['risk_factors'].append('⚠️ Evcil hayvan alerjisi var')
        
        if patient_data.get('Eczema', 0) == 1:
            recommendations['risk_factors'].append('⚠️ Egzama (atopik dermatit) mevcut')
        
        if patient_data.get('HayFever', 0) == 1:
            recommendations['risk_factors'].append('⚠️ Saman nezlesi (alerjik rinit) var')
        
        if patient_data.get('BMI', 25) > 30:
            recommendations['risk_factors'].append('⚠️ Yüksek BMI (obezite riski)')
        
        if patient_data.get('PollutionExposure', 0) > 7:
            recommendations['risk_factors'].append('🔴 Yüksek hava kirliliği maruziyeti')
        
        if patient_data.get('PollenExposure', 0) > 7:
            recommendations['risk_factors'].append('⚠️ Yüksek polen maruziyeti')
        
        if patient_data.get('DustExposure', 0) > 7:
            recommendations['risk_factors'].append('⚠️ Yüksek toz maruziyeti')
        
        # Semptomları kontrol et
        symptoms = []
        if patient_data.get('Wheezing', 0) == 1:
            symptoms.append('Hırıltılı solunum')
        if patient_data.get('ShortnessOfBreath', 0) == 1:
            symptoms.append('Nefes darlığı')
        if patient_data.get('ChestTightness', 0) == 1:
            symptoms.append('Göğüs sıkışması')
        if patient_data.get('Coughing', 0) == 1:
            symptoms.append('Öksürük')
        if patient_data.get('NighttimeSymptoms', 0) == 1:
            symptoms.append('Gece semptomları')
        if patient_data.get('ExerciseInduced', 0) == 1:
            symptoms.append('Egzersiz ile tetiklenen semptomlar')
        
        if symptoms:
            recommendations['risk_factors'].append(f'🔴 Aktif semptomlar: {", ".join(symptoms)}')
        
        if not recommendations['risk_factors']:
            recommendations['risk_factors'].append('✅ Önemli risk faktörü tespit edilmedi')
        
        return recommendations
    
    def generate_report(self, patient_data, patient_name="Hasta"):
        """Detaylı rapor oluştur"""
        assessment = self.assess_risk(patient_data)
        recommendations = self.generate_recommendations(assessment, patient_data)
        
        print("\n" + "=" * 80)
        print(f"ASTIM HASTALIĞI RİSK DEĞERLENDİRME RAPORU - {patient_name}")
        print("=" * 80)
        
        print(f"\n📋 HASTA BİLGİLERİ:")
        print(f"   Yaş: {patient_data.get('Age', 'N/A')}")
        print(f"   Cinsiyet: {'Erkek' if patient_data.get('Gender', 0) == 0 else 'Kadın'}")
        print(f"   BMI: {patient_data.get('BMI', 0):.1f}")
        print(f"   Sigara: {'Evet ❌' if patient_data.get('Smoking', 0) == 1 else 'Hayır ✅'}")
        
        print(f"\n🎯 TAHMİN SONUCU:")
        print(f"   Durum: {'⚠️ ASTIM RİSKİ VAR' if assessment['has_asthma'] == 1 else '✅ ASTIM RİSKİ YOK'}")
        print(f"   Risk Yüzdesi: {assessment['risk_percentage']:.1f}%")
        print(f"   Risk Seviyesi: {recommendations['risk_level']}")
        print(f"   Aciliyet: {recommendations['urgency']}")
        
        print(f"\n📊 OLASILIK DAĞILIMI:")
        print(f"   Astım Yok..... {assessment['probabilities']['no_asthma']:>6.1f}%")
        print(f"   Astım Var...... {assessment['probabilities']['has_asthma']:>6.1f}%")
        
        print(f"\n👨‍⚕️ DOKTOR ÖNERİSİ:")
        print(f"   {recommendations['doctor_visit']}")
        
        print(f"\n💊 TEDAVİ ÖNERİSİ:")
        print(f"   {recommendations['treatment']}")
        
        if recommendations['medications']:
            print(f"\n💊 İLAÇ SEÇENEKLERİ:")
            for med in recommendations['medications']:
                print(f"   {med}")
        
        print(f"\n📝 YAŞAM TARZI ÖNERİLERİ:")
        for rec in recommendations['lifestyle']:
            print(f"   {rec}")
        
        print(f"\n⚠️ RİSK FAKTÖRLERİ:")
        for factor in recommendations['risk_factors']:
            print(f"   {factor}")
        
        print(f"\n🔬 AKCİĞER FONKSİYON TESTLERİ:")
        print(f"   FEV1 (1. saniye zorlu ekspirasyon): {patient_data.get('LungFunctionFEV1', 0):.2f}")
        print(f"   FVC (zorlu vital kapasite): {patient_data.get('LungFunctionFVC', 0):.2f}")
        fev1_fvc = patient_data.get('LungFunctionFEV1', 0) / patient_data.get('LungFunctionFVC', 1) if patient_data.get('LungFunctionFVC', 0) > 0 else 0
        print(f"   FEV1/FVC Oranı: {fev1_fvc:.2f}")
        if fev1_fvc < 0.7:
            print(f"   ⚠️ FEV1/FVC < 0.7: Obstrüksiyon belirtisi!")
        
        print("\n" + "=" * 80)
        print("⚕️ BU RAPOR BİLGİLENDİRME AMAÇLIDIR.")
        print("   KESİN TANI İÇİN MUTLAKA BİR GÖĞÜS HASTALI KLARI UZMANI İLE GÖRÜŞÜNÜZ.")
        print("=" * 80)
        
        return {'assessment': assessment, 'recommendations': recommendations}


# ÖRNEK KULLANIM
if __name__ == "__main__":
    system = AsthmaRiskAssessment()
    
    # ÖRNEK 1: Düşük Risk
    print("\n\n🟢 ÖRNEK 1: DÜŞÜK RİSK (Sağlıklı Birey)")
    patient1 = {
        'Age': 28,
        'Gender': 1,
        'Ethnicity': 1,
        'EducationLevel': 2,
        'BMI': 22.5,
        'Smoking': 0,
        'PhysicalActivity': 7.5,
        'DietQuality': 8.0,
        'SleepQuality': 7.5,
        'PollutionExposure': 2.0,
        'PollenExposure': 3.0,
        'DustExposure': 2.5,
        'PetAllergy': 0,
        'FamilyHistoryAsthma': 0,
        'HistoryOfAllergies': 0,
        'Eczema': 0,
        'HayFever': 0,
        'GastroesophagealReflux': 0,
        'LungFunctionFEV1': 3.5,
        'LungFunctionFVC': 4.2,
        'Wheezing': 0,
        'ShortnessOfBreath': 0,
        'ChestTightness': 0,
        'Coughing': 0,
        'NighttimeSymptoms': 0,
        'ExerciseInduced': 0
    }
    system.generate_report(patient1, "Ayşe Hanım (28)")
    
    # ÖRNEK 2: Orta Risk
    print("\n\n🟡 ÖRNEK 2: ORTA RİSK")
    patient2 = {
        'Age': 35,
        'Gender': 0,
        'Ethnicity': 2,
        'EducationLevel': 1,
        'BMI': 28.5,
        'Smoking': 0,
        'PhysicalActivity': 4.0,
        'DietQuality': 5.5,
        'SleepQuality': 6.0,
        'PollutionExposure': 6.5,
        'PollenExposure': 7.0,
        'DustExposure': 6.0,
        'PetAllergy': 1,
        'FamilyHistoryAsthma': 1,
        'HistoryOfAllergies': 1,
        'Eczema': 0,
        'HayFever': 1,
        'GastroesophagealReflux': 0,
        'LungFunctionFEV1': 2.8,
        'LungFunctionFVC': 3.9,
        'Wheezing': 1,
        'ShortnessOfBreath': 0,
        'ChestTightness': 1,
        'Coughing': 1,
        'NighttimeSymptoms': 1,
        'ExerciseInduced': 1
    }
    system.generate_report(patient2, "Mehmet Bey (35)")
    
    # ÖRNEK 3: Yüksek Risk
    print("\n\n🔴 ÖRNEK 3: YÜKSEK RİSK")
    patient3 = {
        'Age': 42,
        'Gender': 1,
        'Ethnicity': 0,
        'EducationLevel': 1,
        'BMI': 32.0,
        'Smoking': 1,
        'PhysicalActivity': 2.0,
        'DietQuality': 3.5,
        'SleepQuality': 4.5,
        'PollutionExposure': 8.5,
        'PollenExposure': 8.0,
        'DustExposure': 8.5,
        'PetAllergy': 1,
        'FamilyHistoryAsthma': 1,
        'HistoryOfAllergies': 1,
        'Eczema': 1,
        'HayFever': 1,
        'GastroesophagealReflux': 1,
        'LungFunctionFEV1': 2.0,
        'LungFunctionFVC': 3.2,
        'Wheezing': 1,
        'ShortnessOfBreath': 1,
        'ChestTightness': 1,
        'Coughing': 1,
        'NighttimeSymptoms': 1,
        'ExerciseInduced': 1
    }
    system.generate_report(patient3, "Fatma Hanım (42)")
