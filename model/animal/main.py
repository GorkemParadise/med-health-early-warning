import os, pickle
import numpy as np
import pandas as pd
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class AnimalBiteRiskSystem:
    """Akdeniz Bölgesi Hayvan Isırığı/Sokması Risk Değerlendirme Sistemi"""
    
    # Sabitler
    ANIMALS = ['Yılan', 'Köpek', 'Arı/Eşek Arısı', 'Akrep', 'Kedi']
    ANIMALS_EN = ['Snake', 'Dog', 'Bee_Wasp', 'Scorpion', 'Cat']
    LOCATIONS = ['Kırsal', 'Şehir', 'Banliyö']
    SEASONS = ['İlkbahar', 'Yaz', 'Sonbahar', 'Kış']
    TIMES = ['Sabah (06-12)', 'Öğle (12-18)', 'Akşam (18-24)', 'Gece (00-06)']
    BODY_PARTS = ['Alt Ekstremite (Bacak/Ayak)', 'Üst Ekstremite (Kol)', 'El', 'Yüz/Baş', 'Boyun/Gövde']
    OCCUPATIONS = ['Çiftçi/Tarım İşçisi', 'Dış Mekan İşçisi', 'Öğrenci/Çocuk', 'Şehir İşçisi/Diğer']
    
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
        print("🐍 AKDENİZ BÖLGESİ HAYVAN ISIRIĞI/SOKMASI RİSK DEĞERLENDİRME SİSTEMİ")
        print("=" * 80)
        print("\n🔍 Lütfen aşağıdaki bilgileri giriniz:\n")
        
        try:
            name = input("👤 Hasta adı: ").strip() or "Hasta"
            
            print("\n📋 Demografik Bilgiler:")
            age = float(input("   Yaş: "))
            
            print("\n   Cinsiyet:")
            print("   0 = Kadın")
            print("   1 = Erkek")
            gender = int(input("   Seçiminiz (0/1): "))
            
            print("\nIsıran/Sokan Hayvan:")
            for i, animal in enumerate(self.ANIMALS):
                print(f"   {i} = {animal}")
            animal_type = int(input("   Seçiminiz (0-4): "))
            
            print("\ Olay Yeri:")
            for i, loc in enumerate(self.LOCATIONS):
                print(f"   {i} = {loc}")
            location = int(input("   Seçiminiz (0-2): "))
            
            print("\nMevsim:")
            for i, season in enumerate(self.SEASONS):
                print(f"   {i} = {season}")
            season = int(input("   Seçiminiz (0-3): "))
            
            print("\nGünün Zamanı:")
            for i, time in enumerate(self.TIMES):
                print(f"   {i} = {time}")
            time_of_day = int(input("   Seçiminiz (0-3): "))
            
            print("\nIsırık/Sokma Bölgesi:")
            for i, part in enumerate(self.BODY_PARTS):
                print(f"   {i} = {part}")
            body_part = int(input("   Seçiminiz (0-4): "))
            
            print("\nMeslek/Risk Grubu:")
            for i, occ in enumerate(self.OCCUPATIONS):
                print(f"   {i} = {occ}")
            occupation_risk = int(input("   Seçiminiz (0-3): "))
            
            print("\nAlerji ve Sağlık Durumu:")
            allergy_history = int(input("   Alerji öyküsü var mı? (0=Hayır, 1=Evet): "))
            previous_bite = int(input("   Daha önce hayvan ısırığı/sokması oldu mu? (0=Hayır, 1=Evet): "))
            chronic_disease = int(input("   Kronik hastalık var mı? (diyabet, kalp vb.) (0=Hayır, 1=Evet): "))
            
            print("\nMüdahale Bilgileri:")
            first_aid_applied = int(input("   İlk yardım uygulandı mı? (0=Hayır, 1=Evet): "))
            hospital_time = float(input("   Hastaneye ulaşım süresi (saat, örn: 1.5): "))
            
            patient_data = {
                'Age': age,
                'Gender': gender,
                'Location': location,
                'Season': season,
                'Time_of_Day': time_of_day,
                'Animal_Type': animal_type,
                'Body_Part': body_part,
                'Occupation_Risk': occupation_risk,
                'Allergy_History': allergy_history,
                'Previous_Bite': previous_bite,
                'First_Aid_Applied': first_aid_applied,
                'Hospital_Time_Hours': hospital_time,
                'Chronic_Disease': chronic_disease
            }
            
            return patient_data, name
            
        except ValueError:
            print("\n❌ Hatalı giriş! Lütfen sayısal değerler girin.")
            sys.exit(1)
    
    def assess(self, data):
        """Risk değerlendirmesi yap"""
        df = pd.DataFrame([data])
        feature_cols = ['Age', 'Gender', 'Location', 'Season', 'Time_of_Day', 'Animal_Type',
                        'Body_Part', 'Occupation_Risk', 'Allergy_History', 'Previous_Bite',
                        'First_Aid_Applied', 'Hospital_Time_Hours', 'Chronic_Disease']
        X_scaled = self.scaler.transform(df[feature_cols])
        
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
        
        animal = self.ANIMALS[data['Animal_Type']]
        severity_names = [
            "✅ Minimal Risk",
            "⚠️ Düşük Risk",
            "🚨 Orta Düzey Risk",
            "🚨🚨 Yüksek Risk - ACİL"
        ]
        
        print(f"\n🦎 ISIRAN/SOKAN HAYVAN: {animal}")
        print(f"🎯 SONUÇ: {severity_names[severity]}")
        print(f"📊 Genel Risk Skoru: {risk_score:.1f}/100")
        
        print(f"\n📈 Risk Dağılımı:")
        labels = ['Minimal', 'Düşük', 'Orta', 'Yüksek']
        for i, label in enumerate(labels):
            percentage = proba[i] * 100
            bar = "█" * int(percentage / 2)
            print(f"   {label:.<15} {percentage:>5.1f}% {bar}")
        
        # Hayvan türüne göre özel öneriler
        print("\n" + "=" * 80)
        print(f"🐍 {animal.upper()} ISIRIĞI/SOKMASI İÇİN ÖNERİLER")
        print("=" * 80)
        
        if data['Animal_Type'] == 0:  # Yılan
            self._snake_recommendations(severity, data)
        elif data['Animal_Type'] == 1:  # Köpek
            self._dog_recommendations(severity, data)
        elif data['Animal_Type'] == 2:  # Arı
            self._bee_recommendations(severity, data)
        elif data['Animal_Type'] == 3:  # Akrep
            self._scorpion_recommendations(severity, data)
        else:  # Kedi
            self._cat_recommendations(severity, data)
        
        # Risk faktörleri
        print("\n" + "=" * 80)
        print("⚠️ RİSK FAKTÖRLERİ ANALİZİ")
        print("=" * 80)
        self._analyze_risk_factors(data)
        
        print("\n" + "=" * 80)
        print("⚕️ UYARI: Bu rapor bilgilendirme amaçlıdır.")
        print("   Hayvan ısırığı/sokması durumunda MUTLAKA sağlık kuruluşuna başvurun!")
        print("   Özellikle yılan ve akrep ısırıklarında zaman kritiktir.")
        print("=" * 80 + "\n")
    
    def _snake_recommendations(self, severity, data):
        """Yılan ısırığı önerileri"""
        print("\n🐍 YILAN ISIRIĞI - KRİTİK BİLGİLER:")
        print("   • Sakin kalın, hareket etmeyin (zehir yayılımını artırır)")
        print("   • Isırık bölgesini kalp seviyesinin altında tutun")
        print("   • Sıkı giysi/takı çıkarın (şişme olabilir)")
        print("   • YAPMAYIN: Kesme, emme, turnike, buz uygulama")
        
        if severity >= 2:
            print("\n🚨 ACİL MÜDAHALE GEREKLİ:")
            print("   • HEMEN 112'yi arayın")
            print("   • En yakın ANTİVENOM bulunan hastaneye gidin")
            print("   • Mümkünse yılanın fotoğrafını çekin (tedavi için)")
            print("\n   ANTİVENOM GEREKLİ OLABİLİR!")
            print("   • Akdeniz'de: Engerek (Vipera), Kocabaş engerek yaygın")
            print("   • Altın süre: İlk 4-6 saat kritik")
        else:
            print("\n⚠️ YARDIM ALIN:")
            print("   • En yakın sağlık kuruluşuna gidin")
            print("   • Tetanos aşısı kontrolü")
            print("   • Gözlem için hastanede kalma gerekebilir")
    
    def _dog_recommendations(self, severity, data):
        """Köpek ısırığı önerileri"""
        print("\n🐕 KÖPEK ISIRIĞI - KRİTİK BİLGİLER:")
        print("   • Yarayı bol su ve sabunla 10-15 dk yıkayın")
        print("   • Antiseptik uygulayın")
        print("   • Temiz bezle kapatın")
        
        if severity >= 2:
            print("\n🚨 ACİL MÜDAHALE GEREKLİ:")
            print("   • KUDUZ RİSKİ DEĞERLENDİRMESİ ŞART!")
            print("   • Köpeğin sahipli/aşılı olup olmadığını öğrenin")
            print("   • Sahipsiz/şüpheli köpek: KUDUZ AŞISI GEREKEBİLİR")
            print("\n   KUDUZ AŞISI ŞEMASI:")
            print("   • 0, 3, 7, 14, 28. günlerde toplam 5 doz")
            print("   • İlk 24 saat içinde başlanmalı!")
        else:
            print("\n⚠️ YARDIM ALIN:")
            print("   • Sağlık kuruluşuna başvurun")
            print("   • Tetanos aşısı kontrolü")
            print("   • Antibiyotik tedavisi gerekebilir")
        
        print("\n   ENFEKSİYON BELİRTİLERİ (Takip edin):")
        print("   • Kızarıklık yayılması")
        print("   • Şişlik artışı")
        print("   • Ateş")
        print("   • Akıntı")
    
    def _bee_recommendations(self, severity, data):
        """Arı sokması önerileri"""
        print("\n🐝 ARI/EŞEK ARISI SOKMASI - KRİTİK BİLGİLER:")
        print("   • İğneyi KAZIYARAK çıkarın (sıkmayın)")
        print("   • Bölgeyi yıkayın")
        print("   • Buz uygulayın (15 dk)")
        print("   • Antihistaminik alabilirsiniz")
        
        if data['Allergy_History'] or severity >= 2:
            print("\n🚨🚨 ANAFİLAKSİ TEHLİKESİ!")
            print("   • HEMEN 112'yi arayın")
            print("   • EPİNEFRİN (EpiPen) varsa uygulayın")
            print("\n   ANAFİLAKSİ BELİRTİLERİ:")
            print("   • Nefes darlığı, hırıltı")
            print("   • Yüz/dudak/dil şişmesi")
            print("   • Yaygın kurdeşen")
            print("   • Baş dönmesi, bayılma hissi")
            print("   • Kalp çarpıntısı")
        else:
            print("\n⚠️ TAKİP EDİN:")
            print("   • Şişlik 24-48 saat içinde azalmalı")
            print("   • Ağrı kesici kullanabilirsiniz")
            print("   • Kaşıntı için antihistaminik")
    
    def _scorpion_recommendations(self, severity, data):
        """Akrep sokması önerileri"""
        print("\n🦂 AKREP SOKMASI - KRİTİK BİLGİLER:")
        print("   • Sokma bölgesini yıkayın")
        print("   • Buz uygulayın")
        print("   • Sakin kalın")
        print("   • YAPMAYIN: Kesme, emme, turnike")
        
        if severity >= 2:
            print("\n🚨 ACİL MÜDAHALE GEREKLİ:")
            print("   • HEMEN 112'yi arayın")
            print("   • En yakın ANTİVENOM bulunan hastaneye gidin")
            print("   • Akdeniz'de: Sarı akrep (Androctonus) tehlikeli!")
            print("\n   CİDDİ BELİRTİLER (Hemen hastaneye):")
            print("   • Kas spazmları, titreme")
            print("   • Terleme, salya artışı")
            print("   • Bulantı/kusma")
            print("   • Nefes güçlüğü")
            print("   • Kalp ritim bozukluğu")
        else:
            print("\n⚠️ GÖZLEM:")
            print("   • 24 saat gözlem önerilir")
            print("   • Çocuklar ve yaşlılar daha riskli")
            print("   • Belirtiler kötüleşirse hastaneye gidin")
    
    def _cat_recommendations(self, severity, data):
        """Kedi ısırığı önerileri"""
        print("\n🐱 KEDİ ISIRIĞI - KRİTİK BİLGİLER:")
        print("   • Yarayı bol su ve sabunla yıkayın")
        print("   • Antiseptik uygulayın")
        print("   • Kedi ısırıkları DERİN ve ENFEKSİYON riski YÜKSEK!")
        
        if severity >= 2:
            print("\n🚨 DOKTOR KONTROLÜ GEREKLİ:")
            print("   • Kedi ısırıkları %30-50 oranında enfekte olur!")
            print("   • Antibiyotik tedavisi genellikle gerekli")
            print("   • Kuduz riski değerlendirilmeli")
            print("\n   KEDİ TIRMAĞI HASTALIĞI (Bartonella):")
            print("   • Lenf bezi şişmesi")
            print("   • Ateş")
            print("   • Yorgunluk")
        else:
            print("\n⚠️ TAKİP:")
            print("   • Enfeksiyon belirtilerini izleyin")
            print("   • Tetanos aşısı kontrolü")
            print("   • 24-48 saat içinde kötüleşme: Doktora gidin")
    
    def _analyze_risk_factors(self, data):
        """Risk faktörlerini analiz et"""
        factors = []
        
        # Yaş
        if data['Age'] < 10:
            factors.append("🔴 Çocuk yaş grubu: Yüksek risk")
        elif data['Age'] > 65:
            factors.append("🔴 İleri yaş: Komplikasyon riski yüksek")
        
        # Vücut bölgesi
        if data['Body_Part'] == 3:  # Yüz
            factors.append("🔴 Yüz/baş bölgesi: Kritik - hızlı zehir yayılımı")
        elif data['Body_Part'] == 4:  # Boyun
            factors.append("🔴 Boyun bölgesi: Çok kritik - solunum yolu tehlikesi")
        
        # Alerji
        if data['Allergy_History'] and data['Animal_Type'] == 2:
            factors.append("🔴 Arı alerjisi: ANAFİLAKSİ RİSKİ!")
        elif data['Allergy_History']:
            factors.append("⚠️ Alerji öyküsü: Dikkatli takip")
        
        # Hastaneye ulaşım
        if data['Hospital_Time_Hours'] > 4:
            factors.append("🔴 Uzun hastane süresi (>4 saat): Gecikme riski!")
        elif data['Hospital_Time_Hours'] > 2:
            factors.append("⚠️ Hastaneye ulaşım 2+ saat: Hızlanın")
        
        # İlk yardım
        if not data['First_Aid_Applied']:
            factors.append("⚠️ İlk yardım uygulanmamış: Enfeksiyon riski artar")
        
        # Kronik hastalık
        if data['Chronic_Disease']:
            factors.append("⚠️ Kronik hastalık: Komplikasyon riski")
        
        # Konum
        if data['Location'] == 0:  # Kırsal
            factors.append("⚠️ Kırsal bölge: Antivenom erişimi zor olabilir")
        
        # Hayvan türü
        if data['Animal_Type'] == 0:  # Yılan
            factors.append("🔴 Yılan ısırığı: Antivenom gerekebilir")
        elif data['Animal_Type'] == 3:  # Akrep
            factors.append("🔴 Akrep sokması: Çocuklarda daha tehlikeli")
        
        if factors:
            for f in factors:
                print(f"   {f}")
        else:
            print("   ✅ Majör risk faktörü tespit edilmedi")


def main():
    """Ana program"""
    system = AnimalBiteRiskSystem()
    
    # Kullanıcıdan veri al
    patient_data, name = system.get_user_input()
    
    # Değerlendirme yap
    print("\n🔄 Analiz yapılıyor...")
    severity, proba, risk_score = system.assess(patient_data)
    
    # Raporu yazdır
    system.print_report(name, patient_data, severity, proba, risk_score)
    
    # Tekrar
    while True:
        choice = input("Başka bir vaka için değerlendirme yapmak ister misiniz? (e/h): ").lower()
        if choice == 'e':
            print("\n" * 2)
            patient_data, name = system.get_user_input()
            print("\n🔄 Analiz yapılıyor...")
            severity, proba, risk_score = system.assess(patient_data)
            system.print_report(name, patient_data, severity, proba, risk_score)
        else:
            print("\n👋 Sağlıklı günler dileriz! Dikkatli olun!")
            break


if __name__ == "__main__":
    main()
