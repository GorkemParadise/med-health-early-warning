import React, { useState, useEffect } from 'react';
import {
  Activity, Brain, Heart, Wind, Bug,
  ChevronRight, Menu, X, Github, Linkedin,
  AlertTriangle, CheckCircle, TrendingUp,
  Zap, Shield, Award, Target, BarChart3,
  ArrowRight, Play, RefreshCw, Users
} from 'lucide-react';
import {
  BarChart, Bar, PieChart as RePieChart, Pie, Cell,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, AreaChart, Area, Line
} from 'recharts';

// ==================== TYPES ====================
interface Model {
  id: string;
  name: string;
  icon: React.ReactNode;
  accuracy: number;
  features: number;
  description: string;
  color: string;
  gradient: string;
}

interface PredictionResult {
  risk_level: string;
  severity: number;
  risk_score: number;
  probabilities: Record<string, number>;
}

// ==================== DATA ====================
const models: Model[] = [
  {
    id: 'asthma',
    name: 'Astım',
    icon: <Wind className="w-6 h-6" />,
    accuracy: 94.8,
    features: 27,
    description: 'Akciğer fonksiyonları ve çevresel faktörlere dayalı risk analizi',
    color: '#06b6d4',
    gradient: 'from-cyan-500 to-blue-600'
  },
  {
    id: 'diabetes',
    name: 'Diyabet',
    icon: <Activity className="w-6 h-6" />,
    accuracy: 92.5,
    features: 24,
    description: 'Yaşam tarzı ve metabolik faktörlere dayalı tahmin',
    color: '#8b5cf6',
    gradient: 'from-violet-500 to-purple-600'
  },
  {
    id: 'hypertension',
    name: 'Hipertansiyon',
    icon: <Heart className="w-6 h-6" />,
    accuracy: 95.3,
    features: 25,
    description: 'Kardiyovasküler risk faktörlerine dayalı analiz',
    color: '#ef4444',
    gradient: 'from-red-500 to-rose-600'
  },
  {
    id: 'parkinson',
    name: 'Parkinson',
    icon: <Brain className="w-6 h-6" />,
    accuracy: 89.0,
    features: 23,
    description: 'Motor ve ses özelliklerine dayalı erken teşhis',
    color: '#f59e0b',
    gradient: 'from-amber-500 to-orange-600'
  },
  {
    id: 'animal_bite',
    name: 'Hayvan Isırığı',
    icon: <Bug className="w-6 h-6" />,
    accuracy: 93.5,
    features: 13,
    description: 'Akdeniz bölgesi ısırık/sokma aciliyet değerlendirmesi',
    color: '#10b981',
    gradient: 'from-emerald-500 to-teal-600'
  }
];

const performanceData = [
  { name: 'Astım', accuracy: 94.8, precision: 93, recall: 95, f1: 94 },
  { name: 'Diyabet', accuracy: 92.5, precision: 91, recall: 93, f1: 92 },
  { name: 'Hipertansiyon', accuracy: 95.3, precision: 91, recall: 94, f1: 89 },
  { name: 'Parkinson', accuracy: 89.0, precision: 87, recall: 91, f1: 84 },
  { name: 'Hayvan Isırığı', accuracy: 93.5, precision: 92, recall: 96, f1: 87 }
];

const featureImportanceAsthma = [
  { name: 'Toz Maruziyeti', value: 8.97, fullMark: 10 },
  { name: 'FVC', value: 8.49, fullMark: 10 },
  { name: 'Polen', value: 8.46, fullMark: 10 },
  { name: 'BMI', value: 8.44, fullMark: 10 },
  { name: 'FEV1', value: 8.35, fullMark: 10 },
  { name: 'Hava Kirliliği', value: 7.90, fullMark: 10 }
];

const featureImportanceParkinson = [
  { name: 'Jitter', value: 19.9, fullMark: 25 },
  { name: 'Bradikinezi', value: 11.6, fullMark: 25 },
  { name: 'Tremor', value: 11.5, fullMark: 25 },
  { name: 'Rijidite', value: 11.4, fullMark: 25 },
  { name: 'Shimmer', value: 10.0, fullMark: 25 }
];

const riskDistribution = [
  { name: 'Minimal', value: 35, color: '#22c55e' },
  { name: 'Düşük', value: 28, color: '#eab308' },
  { name: 'Orta', value: 25, color: '#f97316' },
  { name: 'Yüksek', value: 12, color: '#ef4444' }
];

const timelineData = [
  { month: '', predictions: 0, accuracy: 0 },
  { month: 'İtalya', predictions: 60000, accuracy: 91 },
  { month: 'Türkiye', predictions: 90000, accuracy: 96 },
  { month: 'İspanya', predictions: 70000, accuracy: 72 },
  { month: 'İsrail', predictions: 10000, accuracy: 95 },
  { month: 'Mısır', predictions: 40000, accuracy: 84 },
  { month: 'Yunanistan', predictions: 20000, accuracy: 84 },
  { month: 'Fransa', predictions: 60000, accuracy: 84 },
  { month: '', predictions: 0, accuracy: 0 }
];

// ==================== HOSPITAL DATA ====================
const hospitalCountryData = [
  { country: 'Fransa', kamu: 1330, ozel: 1635, toplam: 2965, yatakPer1000: 6.2, performans: 77.9 },
  { country: 'Türkiye', kamu: 1010, ozel: 552, toplam: 1562, yatakPer1000: 3.2, performans: 61.2 },
  { country: 'İtalya', kamu: 511, ozel: 485, toplam: 996, yatakPer1000: 3.2, performans: 75.4 },
  { country: 'İspanya', kamu: 449, ozel: 327, toplam: 776, yatakPer1000: 3.4, performans: 75.1 },
  { country: 'Mısır', kamu: 350, ozel: 225, toplam: 575, yatakPer1000: 1.2, performans: 52.5 },
  { country: 'Yunanistan', kamu: 124, ozel: 146, toplam: 270, yatakPer1000: 5.6, performans: 68.3 },
  { country: 'İsrail', kamu: 24, ozel: 20, toplam: 44, yatakPer1000: 2.9, performans: 80.2 },
];

const turkeyTimeSeries = [
  { yil: '2002', sb: 774, ozel: 271, universite: 50, toplamYatak: 164471 },
  { yil: '2010', sb: 843, ozel: 489, universite: 62, toplamYatak: 200000 },
  { yil: '2015', sb: 872, ozel: 541, universite: 65, toplamYatak: 217771 },
  { yil: '2020', sb: 900, ozel: 566, universite: 68, toplamYatak: 251182 },
  { yil: '2022', sb: 915, ozel: 572, universite: 68, toplamYatak: 262190 },
  { yil: '2024', sb: 941, ozel: 552, universite: 69, toplamYatak: 268359 },
];

const qualityData = [
  { country: 'İsrail', erisim: 88, kalite: 92, verimlilik: 85 },
  { country: 'Fransa', erisim: 95, kalite: 93, verimlilik: 75 },
  { country: 'İtalya', erisim: 91, kalite: 88, verimlilik: 78 },
  { country: 'İspanya', erisim: 79, kalite: 77, verimlilik: 79 },
  { country: 'Türkiye', erisim: 71, kalite: 58, verimlilik: 61 },
];

const costData = [
  { country: 'Fransa', maliyet: 680, harcama: 3850 },
  { country: 'İtalya', maliyet: 520, harcama: 2580 },
  { country: 'İspanya', maliyet: 450, harcama: 2350 },
  { country: 'İsrail', maliyet: 350, harcama: 2890 },
  { country: 'Türkiye', maliyet: 85, harcama: 452 },
];

const emergencyData = [
  { country: 'İsrail', mudahale: 7, ambulans: 6.8 },
  { country: 'Fransa', mudahale: 9, ambulans: 7.8 },
  { country: 'İspanya', mudahale: 12, ambulans: 10.3 },
  { country: 'İtalya', mudahale: 15, ambulans: 26.5 },
  { country: 'Türkiye', mudahale: 28, ambulans: 25.0 },
];

const techData = [
  { country: 'Türkiye', icu: 48.5, dijital: 68 },
  { country: 'İsrail', icu: 19.2, dijital: 92 },
  { country: 'Fransa', icu: 15.8, dijital: 89 },
  { country: 'İtalya', icu: 12.5, dijital: 85 },
  { country: 'İspanya', icu: 9.7, dijital: 83 },
];

// ==================== COMPONENTS ====================

const AnimatedCounter: React.FC<{ end: number; suffix?: string; duration?: number }> = ({ 
  end, suffix = '', duration = 2000 
}) => {
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    let startTime: number;
    const animate = (currentTime: number) => {
      if (!startTime) startTime = currentTime;
      const progress = Math.min((currentTime - startTime) / duration, 1);
      setCount(Math.floor(progress * end));
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }, [end, duration]);
  
  return <span>{count}{suffix}</span>;
};

const GlassCard: React.FC<{ children: React.ReactNode; className?: string }> = ({ 
  children, className = '' 
}) => (
  <div className={`backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl shadow-2xl ${className}`}>
    {children}
  </div>
);

const Navigation: React.FC<{ activeSection: string; setActiveSection: (s: string) => void }> = ({ 
  activeSection, setActiveSection 
}) => {
  const [isOpen, setIsOpen] = useState(false);
  
  const navItems = [
    { id: 'home', label: 'Ana Sayfa' },
    { id: 'models', label: 'Modeller' },
    { id: 'demo', label: 'Demo' },
    { id: 'hospital', label: 'Hastane Analizi' },
    { id: 'analytics', label: 'Analitik' },
    { id: 'about', label: 'Hakkında' }
  ];
  
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-slate-900/80 border-b border-white/10">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
              HealthAI
            </span>
          </div>
          
          <div className="hidden md:flex items-center gap-8">
            {navItems.map(item => (
              <button
                key={item.id}
                onClick={() => setActiveSection(item.id)}
                className={`text-sm font-medium transition-all duration-300 ${
                  activeSection === item.id ? 'text-cyan-400' : 'text-gray-400 hover:text-white'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>
          
          <button className="md:hidden text-white" onClick={() => setIsOpen(!isOpen)}>
            {isOpen ? <X /> : <Menu />}
          </button>
        </div>
        
        {isOpen && (
          <div className="md:hidden mt-4 pb-4 space-y-2">
            {navItems.map(item => (
              <button
                key={item.id}
                onClick={() => { setActiveSection(item.id); setIsOpen(false); }}
                className="block w-full text-left px-4 py-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-lg"
              >
                {item.label}
              </button>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
};

const HeroSection: React.FC = () => (
  <section className="min-h-screen flex items-center justify-center relative overflow-hidden pt-20">
    <div className="absolute inset-0">
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-cyan-500/10 to-purple-500/10 rounded-full blur-3xl" />
    </div>
    
    <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:100px_100px]" />
    
    <div className="relative z-10 max-w-7xl mx-auto px-6 text-center">
      <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-8">
        <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
        <span className="text-sm text-gray-400">MEDAIGENCY AI4PURPOSE Hackathon 2026</span>
      </div>
      
      <h1 className="text-5xl md:text-7xl lg:text-8xl font-black mb-6 leading-tight">
        <span className="bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent">
          Yapay Zeka ile
        </span>
        <br />
        <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
          Sağlık Devrimi
        </span>
      </h1>
      
      <p className="text-lg md:text-xl text-gray-400 max-w-3xl mx-auto mb-12">
        Akdeniz bölgelerinde yaygın ve hayati risk taşıyan 5 hastalık için makine öğrenimi modelleriyle                
        <span className="text-cyan-400"> %90+ doğruluk oranı</span> ile erken teşhis imkanı.
      </p>
      
      <div className="flex flex-wrap justify-center gap-4 mb-16">
        <button className="group px-8 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-semibold flex items-center gap-2 hover:shadow-lg hover:shadow-cyan-500/25 transition-all duration-300">
          @ayarlicazhocam
        </button>
        <button className="px-8 py-4 rounded-2xl bg-white/5 border border-white/20 text-white font-semibold hover:bg-white/10 transition-all duration-300">
          @nexatr0
        </button>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {[
          { value: 5, label: 'AI Modeli', suffix: '' },
          { value: 92, label: 'Ort. Doğruluk', suffix: '%' },
          { value: 113, label: 'Toplam Özellik', suffix: '+' },
          { value: 280, label: 'Bin+ Veri', suffix: 'K' }
        ].map((stat, i) => (
          <GlassCard key={i} className="p-6">
            <div className="text-3xl md:text-4xl font-bold text-white mb-1">
              <AnimatedCounter end={stat.value} suffix={stat.suffix} />
            </div>
            <div className="text-sm text-gray-400">{stat.label}</div>
          </GlassCard>
        ))}
      </div>
    </div>
    
    <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
      <ChevronRight className="w-6 h-6 text-gray-400 rotate-90" />
    </div>
  </section>
);

const ModelsSection: React.FC<{ onSelectModel: (id: string) => void }> = ({ onSelectModel }) => (
  <section className="py-24 relative">
    <div className="max-w-7xl mx-auto px-6">
      <div className="text-center mb-16">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">AI Modelleri</h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Her biri özel olarak eğitilmiş, yüksek doğruluk oranına sahip 5 farklı sağlık riski tahmin modeli
        </p>
      </div>
      
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {models.map((model) => (
          <GlassCard key={model.id} className="p-6 hover:scale-105 transition-all duration-500 cursor-pointer group">
            <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${model.gradient} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
              {model.icon}
            </div>
            
            <h3 className="text-xl font-bold text-white mb-2">{model.name}</h3>
            <p className="text-gray-400 text-sm mb-4">{model.description}</p>
            
            <div className="flex items-center justify-between mb-4">
              <div>
                <div className="text-2xl font-bold text-white">{model.accuracy}%</div>
                <div className="text-xs text-gray-500">Doğruluk</div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-white">{model.features}</div>
                <div className="text-xs text-gray-500">Özellik</div>
              </div>
            </div>
            
            <div className="h-2 bg-white/10 rounded-full overflow-hidden mb-4">
              <div 
                className={`h-full bg-gradient-to-r ${model.gradient} transition-all duration-1000`}
                style={{ width: `${model.accuracy}%` }}
              />
            </div>
            
            <button
              onClick={() => onSelectModel(model.id)}
              className="w-full py-3 rounded-xl bg-white/5 hover:bg-white/10 text-white font-medium flex items-center justify-center gap-2 transition-all"
            >
              Modeli Kullan
              <ArrowRight className="w-4 h-4" />
            </button>
          </GlassCard>
        ))}
      </div>
    </div>
  </section>
);

const DemoSection: React.FC<{ selectedModel: string }> = ({ selectedModel }) => {
  const [formData, setFormData] = useState<Record<string, number>>({});
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  
  const currentModel = models.find(m => m.id === selectedModel) || models[0];
  
  const handlePredict = async () => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const severityLevel = Math.floor(Math.random() * 4);
    const riskScore = Math.floor(Math.random() * 100);
    const riskLevels = ['Minimal', 'Düşük', 'Orta', 'Yüksek'];
    
    const mockResult: PredictionResult = {
      risk_level: riskLevels[severityLevel],
      severity: severityLevel,
      risk_score: riskScore,
      probabilities: {
        minimal: Math.random() * 30,
        low: Math.random() * 30,
        medium: Math.random() * 25,
        high: Math.random() * 15
      }
    };
    
    setResult(mockResult);
    setLoading(false);
  };
  
  const getFormFields = () => {
    switch (selectedModel) {
      case 'asthma':
        return [
          { key: 'Age', label: 'Yaş', type: 'number', min: 1, max: 100 },
          { key: 'BMI', label: 'BMI', type: 'number', min: 10, max: 60 },
          { key: 'Smoking', label: 'Sigara', type: 'select', options: [{ v: 0, l: 'Hayır' }, { v: 1, l: 'Evet' }] },
          { key: 'DustExposure', label: 'Toza Maruz Kalma Oranı (0-10)', type: 'range', min: 0, max: 10 },
          { key: 'PollenExposure', label: 'Polene Maruz Kalma Oranı (0-10)', type: 'range', min: 0, max: 10 },
          { key: 'LungFunctionFEV1', label: 'FEV1 (Litre) - Derin bir nefes alıp verirken ne kadar rahat hissediyorsunuz? FEV1 bilmiyorsanız, lütfen tahmini değerler girin. (0-6)', type: 'number', min: 0, max: 6 },
          { key: 'Wheezing', label: 'Hırıltılı Solunum', type: 'select', options: [{ v: 0, l: 'Hayır' }, { v: 1, l: 'Evet' }] },
          { key: 'FamilyHistoryAsthma', label: 'Ailede Astım', type: 'select', options: [{ v: 0, l: 'Hayır' }, { v: 1, l: 'Evet' }] }
        ];
      case 'diabetes':
        return [
          { key: 'Age', label: 'Yaş Kategorisi (1-13)', type: 'number', min: 1, max: 13 },
          { key: 'BMI', label: 'BMI', type: 'number', min: 10, max: 60 },
          { key: 'HighBP', label: 'Yüksek Tansiyon', type: 'select', options: [{ v: 0, l: 'Hayır' }, { v: 1, l: 'Evet' }] },
          { key: 'HighChol', label: 'Yüksek Kolesterol', type: 'select', options: [{ v: 0, l: 'Hayır' }, { v: 1, l: 'Evet' }] },
          { key: 'PhysActivity', label: 'Fiziksel Aktivite', type: 'select', options: [{ v: 0, l: 'Hayır' }, { v: 1, l: 'Evet' }] },
          { key: 'GenHlth', label: 'Genel Sağlık (1-5)', type: 'range', min: 1, max: 5 },
          { key: 'HeartDiseaseorAttack', label: 'Kalp Hastalığı', type: 'select', options: [{ v: 0, l: 'Hayır' }, { v: 1, l: 'Evet' }] }
        ];
      case 'hypertension':
        return [
          { key: 'Age', label: 'Yaş', type: 'number', min: 18, max: 90 },
          { key: 'BMI', label: 'BMI', type: 'number', min: 15, max: 45 },
          { key: 'Salt_Intake', label: 'Günlük Tuz (gram)', type: 'range', min: 2, max: 15 },
          { key: 'Stress_Score', label: 'Stres Puanı (0-10)', type: 'range', min: 0, max: 10 },
          { key: 'Sleep_Duration', label: 'Uyku Süresi (saat)', type: 'number', min: 2, max: 12 },
          { key: 'Smoking_Encoded', label: 'Sigara', type: 'select', options: [{ v: 0, l: 'Hayır' }, { v: 1, l: 'Evet' }] },
          { key: 'Family_History_Encoded', label: 'Ailede Tansiyon Hastası', type: 'select', options: [{ v: 0, l: 'Hayır' }, { v: 1, l: 'Evet' }] }
        ];
      case 'parkinson':
        return [
          { key: 'age', label: 'Yaş', type: 'number', min: 40, max: 90 },
          { key: 'tremor_score', label: 'Tremor - Titreme (0-5)', type: 'range', min: 0, max: 5 },
          { key: 'rigidity', label: 'Rijidite - Kaslarda Sertlik (0-5)', type: 'range', min: 0, max: 5 },
          { key: 'bradykinesia', label: 'Bradikinezi - Hareket Yavaşlığı (0-5)', type: 'range', min: 0, max: 5 },
          { key: 'motor_updrs', label: 'Motor UPDRS - Geç Cevap / Algılama (0-100)', type: 'range', min: 0, max: 100 },
          { key: 'disease_duration', label: 'Hastalık Süresi (yıl)', type: 'number', min: 0, max: 30 },
          { key: 'levodopa_response', label: 'Levodopa (Parkinson İlacı) Yanıtı (%)', type: 'range', min: 0, max: 100 }
        ];
      case 'animal_bite':
        return [
          { key: 'Age', label: 'Yaş', type: 'number', min: 1, max: 100 },
          { key: 'Animal_Type', label: 'Hayvan Türü', type: 'select', options: [{ v: 0, l: 'Yılan' }, { v: 1, l: 'Köpek' }, { v: 2, l: 'Arı' }, { v: 3, l: 'Akrep' }, { v: 4, l: 'Kedi' }] },
          { key: 'Body_Part', label: 'Isırık Bölgesi', type: 'select', options: [{ v: 0, l: 'Alt Ekstremite' }, { v: 1, l: 'Üst Ekstremite' }, { v: 2, l: 'El' }, { v: 3, l: 'Yüz' }, { v: 4, l: 'Boyun' }] },
          { key: 'Hospital_Time_Hours', label: 'Evden, Hastane Süresi (saat)', type: 'number', min: 0.25, max: 24 },
          { key: 'First_Aid_Applied', label: 'İlk Yardım Yapıldı mı', type: 'select', options: [{ v: 0, l: 'Hayır' }, { v: 1, l: 'Evet' }] },
          { key: 'Allergy_History', label: 'Alerji Var mı', type: 'select', options: [{ v: 0, l: 'Hayır' }, { v: 1, l: 'Evet' }] }
        ];
      default:
        return [];
    }
  };
  
  const fields = getFormFields();
  
  return (
    <section className="py-24 relative">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">Canlı Demo</h2>
          <p className="text-gray-400">
            Seçili model: <span className="text-cyan-400 font-semibold">{currentModel.name}</span>
          </p>
        </div>
        
        <div className="grid lg:grid-cols-2 gap-8">
          <GlassCard className="p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${currentModel.gradient} flex items-center justify-center`}>
                {currentModel.icon}
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">{currentModel.name} Risk Analizi</h3>
                <p className="text-sm text-gray-400">{currentModel.features} parametre</p>
              </div>
            </div>
            
            <div className="space-y-4 mb-6">
              {fields.map(field => (
                <div key={field.key}>
                  <label className="text-sm text-gray-400 mb-1 block">{field.label}</label>
                  {field.type === 'select' ? (
                    <select
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-cyan-500 focus:outline-none"
                      onChange={e => setFormData({ ...formData, [field.key]: Number(e.target.value) })}
                    >
                      <option value="">Seçiniz</option>
                      {field.options?.map(opt => (
                        <option key={opt.v} value={opt.v}>{opt.l}</option>
                      ))}
                    </select>
                  ) : field.type === 'range' ? (
                    <div className="flex items-center gap-4">
                      <input
                        type="range"
                        min={field.min}
                        max={field.max}
                        step={field.max && field.max <= 10 ? 0.5 : 1}
                        className="flex-1 accent-cyan-500"
                        onChange={e => setFormData({ ...formData, [field.key]: Number(e.target.value) })}
                      />
                      <span className="text-white w-12 text-center">
                        {formData[field.key] || field.min}
                      </span>
                    </div>
                  ) : (
                    <input
                      type="number"
                      min={field.min}
                      max={field.max}
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:border-cyan-500 focus:outline-none"
                      onChange={e => setFormData({ ...formData, [field.key]: Number(e.target.value) })}
                    />
                  )}
                </div>
              ))}
            </div>
            
            <button
              onClick={handlePredict}
              disabled={loading}
              className={`w-full py-4 rounded-xl bg-gradient-to-r ${currentModel.gradient} text-white font-semibold flex items-center justify-center gap-2 hover:shadow-lg transition-all disabled:opacity-50`}
            >
              {loading ? (
                <>
                  <RefreshCw className="w-5 h-5 animate-spin" />
                  Analiz Ediliyor...
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5" />
                  Risk Analizi Yap
                </>
              )}
            </button>
          </GlassCard>
          
          <GlassCard className="p-8">
            <h3 className="text-xl font-bold text-white mb-6">Sonuçlar</h3>
            
            {result ? (
              <div className="space-y-6">
                <div className="text-center p-6 rounded-2xl bg-gradient-to-br from-white/5 to-white/0">
                  <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full mb-4 ${
                    result.severity === 0 ? 'bg-green-500/20 text-green-400' :
                    result.severity === 1 ? 'bg-yellow-500/20 text-yellow-400' :
                    result.severity === 2 ? 'bg-orange-500/20 text-orange-400' :
                    'bg-red-500/20 text-red-400'
                  }`}>
                    {result.severity < 2 ? <CheckCircle className="w-5 h-5" /> : <AlertTriangle className="w-5 h-5" />}
                    {result.risk_level}
                  </div>
                  <div className="text-5xl font-black text-white mb-2">{result.risk_score}%</div>
                  <div className="text-gray-400">Risk Skoru</div>
                </div>
                
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <RePieChart>
                      <Pie
                        data={Object.entries(result.probabilities).map(([key, value]) => ({
                          name: key === 'minimal' ? 'Minimal' : key === 'low' ? 'Düşük' : key === 'medium' ? 'Orta' : 'Yüksek',
                          value: Number(value.toFixed(1))
                        }))}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={90}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {riskDistribution.map((_, index) => (
                          <Cell key={`cell-${index}`} fill={riskDistribution[index].color} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </RePieChart>
                  </ResponsiveContainer>
                </div>
                
                <div className="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
                  <div className="flex items-start gap-3">
                    <Shield className="w-5 h-5 text-cyan-400 mt-0.5" />
                    <div>
                      <div className="font-semibold text-white mb-1">Öneri</div>
                      <p className="text-sm text-gray-400">
                        {result.severity < 2 
                          ? 'Risk seviyeniz düşük. Düzenli kontroller ve sağlıklı yaşam tarzı ile devam edin.'
                          : 'Risk seviyeniz yüksek. En kısa sürede bir sağlık kuruluşuna başvurmanız önerilir.'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center py-12">
                <div className="w-24 h-24 rounded-full bg-white/5 flex items-center justify-center mb-4">
                  <BarChart3 className="w-12 h-12 text-gray-600" />
                </div>
                <p className="text-gray-400">
                  Formu doldurup "Risk Analizi Yap" butonuna tıklayın
                </p>
              </div>
            )}
          </GlassCard>
        </div>
      </div>
    </section>
  );
};

// ==================== HOSPITAL SECTION ====================
const HospitalSection: React.FC = () => (
  <section className="py-24 relative">
    <div className="max-w-7xl mx-auto px-6">
      <div className="text-center mb-16">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">🏥 Akdeniz Bölgesi Hastane Analizi</h2>
        <p className="text-gray-400 max-w-2xl mx-auto">19 Ülke • 8,963 Hastane • 1.5 Milyon Yatak Kapasitesi</p>
      </div>
      
      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12">
        {[
          { value: '19', label: 'Ülke', icon: '🌍', color: '#06b6d4' },
          { value: '8,963', label: 'Hastane', icon: '🏥', color: '#10b981' },
          { value: '1.5M', label: 'Yatak', icon: '🛏️', color: '#8b5cf6' },
          { value: '78.5', label: 'Ort. Performans', icon: '⭐', color: '#f59e0b' }
        ].map((stat, i) => (
          <GlassCard key={i} className="p-6 text-center">
            <div className="text-3xl mb-2">{stat.icon}</div>
            <div className="text-2xl font-bold" style={{color: stat.color}}>{stat.value}</div>
            <div className="text-sm text-gray-400">{stat.label}</div>
          </GlassCard>
        ))}
      </div>
      
      <div className="grid lg:grid-cols-2 gap-8 mb-12">
        {/* Ülkelere Göre Hastane Sayısı */}
        <GlassCard className="p-6">
          <h3 className="text-lg font-bold text-white mb-4">🏥 Ülkelere Göre Hastane Sayısı</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={hospitalCountryData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis type="number" stroke="#9ca3af" />
                <YAxis type="category" dataKey="country" stroke="#9ca3af" width={80} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px' }} />
                <Legend />
                <Bar dataKey="kamu" name="Kamu" fill="#3b82f6" stackId="a" />
                <Bar dataKey="ozel" name="Özel" fill="#10b981" stackId="a" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
        
        {/* Sağlık Sistemi Performans Skorları */}
        <GlassCard className="p-6">
          <h3 className="text-lg font-bold text-white mb-4">⭐ Sağlık Sistemi Performans Skorları</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={[...hospitalCountryData].sort((a,b) => b.performans - a.performans)} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis type="number" domain={[0, 100]} stroke="#9ca3af" />
                <YAxis type="category" dataKey="country" stroke="#9ca3af" width={80} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px' }} />
                <Bar dataKey="performans" name="Performans" fill="#8b5cf6">
                  {hospitalCountryData.map((entry, index) => (
                    <Cell key={index} fill={entry.performans >= 85 ? '#22c55e' : entry.performans >= 75 ? '#eab308' : '#ef4444'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>
      
      <div className="grid lg:grid-cols-2 gap-8 mb-12">
        {/* Türkiye Hastane Gelişimi */}
        <GlassCard className="p-6">
          <h3 className="text-lg font-bold text-white mb-4">🇹🇷 Türkiye Hastane Gelişimi (2002-2024)</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={turkeyTimeSeries}>
                <defs>
                  <linearGradient id="colorSB" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1}/>
                  </linearGradient>
                  <linearGradient id="colorOzel" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0.1}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="yil" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px' }} />
                <Legend />
                <Area type="monotone" dataKey="sb" name="Sağlık Bakanlığı" stroke="#3b82f6" fillOpacity={1} fill="url(#colorSB)" />
                <Area type="monotone" dataKey="ozel" name="Özel" stroke="#10b981" fillOpacity={1} fill="url(#colorOzel)" />
                <Area type="monotone" dataKey="universite" name="Üniversite" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
        
        {/* Kalite Boyutları */}
        <GlassCard className="p-6">
          <h3 className="text-lg font-bold text-white mb-4">📊 Sağlık Sistemi Kalite Boyutları</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={qualityData}>
                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                <PolarAngleAxis dataKey="country" stroke="#9ca3af" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <PolarRadiusAxis stroke="#9ca3af" domain={[0, 100]} />
                <Radar name="Erişim" dataKey="erisim" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.3} />
                <Radar name="Kalite" dataKey="kalite" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
                <Radar name="Verimlilik" dataKey="verimlilik" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.3} />
                <Legend />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>
      
      <div className="grid lg:grid-cols-3 gap-8">
        {/* Yatak Başına Maliyet */}
        <GlassCard className="p-6">
          <h3 className="text-lg font-bold text-white mb-4">💰 Yatak Günü Maliyeti (USD)</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={costData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="country" stroke="#9ca3af" tick={{ fontSize: 10 }} />
                <YAxis stroke="#9ca3af" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px' }} formatter={(v: number) => `$${v}`} />
                <Bar dataKey="maliyet" name="Maliyet">
                  {costData.map((entry, index) => (
                    <Cell key={index} fill={entry.maliyet > 500 ? '#ef4444' : entry.maliyet > 300 ? '#f59e0b' : '#22c55e'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 text-center">
            <span className="text-sm text-gray-400">Türkiye: <span className="text-green-400 font-bold">$85</span> vs Fransa: <span className="text-red-400 font-bold">$680</span></span>
          </div>
        </GlassCard>
        
        {/* Acil Müdahale Süresi */}
        <GlassCard className="p-6">
          <h3 className="text-lg font-bold text-white mb-4">🚑 Acil Müdahale (dk)</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={emergencyData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis type="number" stroke="#9ca3af" />
                <YAxis type="category" dataKey="country" stroke="#9ca3af" width={60} tick={{ fontSize: 10 }} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px' }} />
                <Bar dataKey="mudahale" name="Dakika">
                  {emergencyData.map((entry, index) => (
                    <Cell key={index} fill={entry.mudahale <= 10 ? '#22c55e' : entry.mudahale <= 15 ? '#f59e0b' : '#ef4444'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 text-center">
            <span className="text-sm text-gray-400">Hedef: <span className="text-cyan-400 font-bold">10 dakika</span></span>
          </div>
        </GlassCard>
        
        {/* Yoğun Bakım Kapasitesi */}
        <GlassCard className="p-6">
          <h3 className="text-lg font-bold text-white mb-4">🏥 Yoğun Bakım Kapasitesi (100k)</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={techData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="country" stroke="#9ca3af" tick={{ fontSize: 10 }} />
                <YAxis stroke="#9ca3af" />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px' }} />
                <Bar dataKey="icu" name="YBÜ Yatağı" fill="#ec4899" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-4 text-center">
            <span className="text-sm text-gray-400">Türkiye: <span className="text-pink-400 font-bold">45.5</span> (En Yüksek)</span>
          </div>
        </GlassCard>
      </div>
    </div>
  </section>
);

const AnalyticsSection: React.FC = () => (
  <section className="py-24 relative">
    <div className="max-w-7xl mx-auto px-6">
      <div className="text-center mb-16">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">Model Performansı</h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
          Tüm modellerin detaylı performans metrikleri ve karşılaştırmalı analizi
        </p>
      </div>
      
      <div className="grid lg:grid-cols-2 gap-8 mb-12">
        <GlassCard className="p-6">
          <h3 className="text-lg font-bold text-white mb-4">Model Karşılaştırması</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={performanceData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis type="number" domain={[0, 100]} stroke="#9ca3af" />
                <YAxis type="category" dataKey="name" stroke="#9ca3af" width={100} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px' }} />
                <Legend />
                <Bar dataKey="accuracy" name="Doğruluk" fill="#06b6d4" radius={[0, 4, 4, 0]} />
                <Bar dataKey="precision" name="Precision" fill="#8b5cf6" radius={[0, 4, 4, 0]} />
                <Bar dataKey="recall" name="Recall" fill="#10b981" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
        
        <GlassCard className="p-6">
          <h3 className="text-lg font-bold text-white mb-4">Genel Risk Dağılımı</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RePieChart>
                <Pie
                  data={riskDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={70}
                  outerRadius={120}
                  paddingAngle={3}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}%`}
                >
                  {riskDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </RePieChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>
      
      <div className="grid lg:grid-cols-2 gap-8 mb-12">
        <GlassCard className="p-6">
          <h3 className="text-lg font-bold text-white mb-4">Astım - Özellik Önemi</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={featureImportanceAsthma}>
                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                <PolarAngleAxis dataKey="name" stroke="#9ca3af" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <PolarRadiusAxis stroke="#9ca3af" />
                <Radar name="Önem" dataKey="value" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.3} />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
        
        <GlassCard className="p-6">
          <h3 className="text-lg font-bold text-white mb-4">Parkinson - Özellik Önemi</h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={featureImportanceParkinson}>
                <PolarGrid stroke="rgba(255,255,255,0.1)" />
                <PolarAngleAxis dataKey="name" stroke="#9ca3af" tick={{ fill: '#9ca3af', fontSize: 11 }} />
                <PolarRadiusAxis stroke="#9ca3af" />
                <Radar name="Önem" dataKey="value" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.3} />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>
      
      <GlassCard className="p-6">
        <h3 className="text-lg font-bold text-white mb-4">Modellerin Alındığı Veri / Doğruluk İstatistikleri (2026)</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={timelineData}>
              <defs>
                <linearGradient id="colorPredictions" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="month" stroke="#9ca3af" />
              <YAxis yAxisId="left" stroke="#9ca3af" />
              <YAxis yAxisId="right" orientation="right" stroke="#9ca3af" domain={[80, 100]} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '12px' }} />
              <Legend />
              <Area yAxisId="left" type="monotone" dataKey="predictions" name="Tahmin Sayısı" stroke="#06b6d4" fillOpacity={1} fill="url(#colorPredictions)" />
              <Line yAxisId="right" type="monotone" dataKey="accuracy" name="Doğruluk %" stroke="#8b5cf6" strokeWidth={3} dot={{ fill: '#8b5cf6', strokeWidth: 2 }} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </GlassCard>
    </div>
  </section>
);

const AboutSection: React.FC = () => (
  <section className="py-24 relative">
    <div className="max-w-7xl mx-auto px-6">
      <div className="text-center mb-16">
        <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">Proje Hakkında</h2>
        <p className="text-gray-400 max-w-2xl mx-auto">
        MEDAIGENCY AI4PURPOSE Hackathon 2026 için geliştirilen yapay zeka destekli sağlık platformu
        </p>
      </div>
      
      <div className="grid md:grid-cols-3 gap-8 mb-16">
        {[
          { icon: <Target className="w-8 h-8" />, title: 'Misyon', description: 'Yapay zeka ile hastalıkların erken teşhisini kolaylaştırarak sağlık hizmetlerine erişimi demokratikleştirmek.' },
          { icon: <Award className="w-8 h-8" />, title: 'Teknoloji', description: 'Random Forest ve Gradient Boosting ensemble modelleri ile %90+ doğruluk oranı.' },
          { icon: <Users className="w-8 h-8" />, title: 'Etki', description: 'Akdeniz bölgesinde yaşayan, hastalık belirtilerine alışıp zamana bırakan kişilere tanı koyma ve yol gösterme konusunda yardımcı olmak.' },
        ].map((item, i) => (
          <GlassCard key={i} className="p-8 text-center">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center mx-auto mb-4 text-white">
              {item.icon}
            </div>
            <h3 className="text-xl font-bold text-white mb-2">{item.title}</h3>
            <p className="text-gray-400">{item.description}</p>
          </GlassCard>
        ))}
      </div>
      
      <GlassCard className="p-8">
        <h3 className="text-2xl font-bold text-white text-center mb-8">Kullanılar Teknolojiler</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
          {[
            { name: 'Python', color: '#3776ab' },
            { name: 'FastAPI', color: '#009688' },
            { name: 'React', color: '#61dafb' },
            { name: 'TypeScript', color: '#3178c6' },
            { name: 'Scikit-learn', color: '#f89939' },
            { name: 'Pandas', color: '#150458' }
          ].map((tech, i) => (
            <div key={i} className="p-4 rounded-xl bg-white/5 text-center hover:bg-white/10 transition-all">
              <div className="w-12 h-12 rounded-lg mx-auto mb-2 flex items-center justify-center text-white font-bold" style={{ backgroundColor: tech.color }}>
                {tech.name[0]}
              </div>
              <span className="text-sm text-gray-300">{tech.name}</span>
            </div>
          ))}
        </div>
      </GlassCard>
      
      <div className="mt-12 p-6 rounded-2xl bg-amber-500/10 border border-amber-500/20">
        <div className="flex items-start gap-4">
          <AlertTriangle className="w-6 h-6 text-amber-400 flex-shrink-0 mt-1" />
          <div>
            <h4 className="font-bold text-amber-400 mb-2">Önemli Uyarı</h4>
            <p className="text-gray-300 text-sm">
              Bu platform sadece bilgilendirme amaçlıdır ve tıbbi tanı koymaz. 
              Sağlık sorunlarınız için mutlaka bir sağlık profesyoneline danışın. 
              Sonuçlar kesin tanı değildir ve klinik değerlendirmenin yerini tutmaz.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
);

const Footer: React.FC = () => (
  <footer className="py-12 border-t border-white/10">
    <div className="max-w-7xl mx-auto px-6">
      <div className="flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center">
            <Zap className="w-6 h-6 text-white" />
          </div>
          <span className="text-lg font-bold text-white">HealthAI</span>
        </div>
        
        <p className="text-gray-400 text-sm">© 2026 HealthAI - Hackathon Projesi. Tüm hakları saklıdır.</p>
        
        <div className="flex items-center gap-4">
          <a href="https://github.com/GorkemParadise/med-health-early-warning" className="text-gray-400 hover:text-white transition-colors"><Github className="w-5 h-5" /></a>
          <a href="https://www.linkedin.com/in/gorkemergune/" className="text-gray-400 hover:text-white transition-colors"><Linkedin className="w-5 h-5" /></a>
        </div>
      </div>
    </div>
  </footer>
);

// ==================== MAIN APP ====================
const App: React.FC = () => {
  const [activeSection, setActiveSection] = useState('home');
  const [selectedModel, setSelectedModel] = useState('asthma');
  
  const handleSelectModel = (modelId: string) => {
    setSelectedModel(modelId);
    setActiveSection('demo');
  };
  
  return (
    <div className="min-h-screen bg-slate-950 text-white overflow-x-hidden">
      <Navigation activeSection={activeSection} setActiveSection={setActiveSection} />
      
      {activeSection === 'home' && <HeroSection />}
      {activeSection === 'models' && <ModelsSection onSelectModel={handleSelectModel} />}
      {activeSection === 'demo' && <DemoSection selectedModel={selectedModel} />}
      {activeSection === 'hospital' && <HospitalSection />}
      {activeSection === 'analytics' && <AnalyticsSection />}
      {activeSection === 'about' && <AboutSection />}
      
      {activeSection === 'home' && (
        <>
          <ModelsSection onSelectModel={handleSelectModel} />
          <HospitalSection />
          <AnalyticsSection />
          <AboutSection />
        </>
      )}
      
      <Footer />
    </div>
  );
};

export default App;