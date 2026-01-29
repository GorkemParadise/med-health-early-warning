import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line, ScatterChart, Scatter, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ComposedChart, Area } from 'recharts';

const MediterraneanHospitalDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');

  // Ülke verileri
  const countryData = [
    { country: 'Fransa', kamu: 1330, ozel: 1635, toplam: 2965, yatak: 412788, yatakPer1000: 6.2, ozelOran: 55.1, performans: 87.9 },
    { country: 'Türkiye', kamu: 1010, ozel: 552, toplam: 1562, yatak: 268359, yatakPer1000: 3.2, ozelOran: 35.3, performans: 71.2 },
    { country: 'İtalya', kamu: 511, ozel: 485, toplam: 996, yatak: 189600, yatakPer1000: 3.2, ozelOran: 48.7, performans: 85.4 },
    { country: 'İspanya', kamu: 449, ozel: 327, toplam: 776, yatak: 160000, yatakPer1000: 3.4, ozelOran: 42.1, performans: 85.1 },
    { country: 'Mısır', kamu: 350, ozel: 225, toplam: 575, yatak: 125000, yatakPer1000: 1.2, ozelOran: 39.1, performans: 62.5 },
    { country: 'Fas', kamu: 220, ozel: 135, toplam: 355, yatak: 35000, yatakPer1000: 0.9, ozelOran: 38.0, performans: 58.2 },
    { country: 'Portekiz', kamu: 208, ozel: 115, toplam: 323, yatak: 35754, yatakPer1000: 3.5, ozelOran: 35.6, performans: 81.5 },
    { country: 'Yunanistan', kamu: 124, ozel: 146, toplam: 270, yatak: 58000, yatakPer1000: 5.6, ozelOran: 54.1, performans: 78.3 },
    { country: 'İsrail', kamu: 24, ozel: 20, toplam: 44, yatak: 28800, yatakPer1000: 2.9, ozelOran: 45.5, performans: 90.2 },
  ];

  // Türkiye zaman serisi
  const turkeyTimeSeries = [
    { yil: 2002, sb: 774, ozel: 271, universite: 50, toplamYatak: 164471 },
    { yil: 2020, sb: 900, ozel: 566, universite: 68, toplamYatak: 251182 },
    { yil: 2021, sb: 908, ozel: 571, universite: 68, toplamYatak: 254497 },
    { yil: 2022, sb: 915, ozel: 572, universite: 68, toplamYatak: 262190 },
    { yil: 2023, sb: 933, ozel: 565, universite: 68, toplamYatak: 266594 },
    { yil: 2024, sb: 941, ozel: 552, universite: 69, toplamYatak: 268359 },
  ];

  // Kalite skorları
  const qualityData = [
    { country: 'İsrail', erisim: 90, kalite: 92, verimlilik: 85, memnuniyet: 88, performans: 90.2 },
    { country: 'Fransa', erisim: 95, kalite: 93, verimlilik: 75, memnuniyet: 82, performans: 87.9 },
    { country: 'İtalya', erisim: 92, kalite: 88, verimlilik: 78, memnuniyet: 84, performans: 85.4 },
    { country: 'İspanya', erisim: 91, kalite: 87, verimlilik: 79, memnuniyet: 85, performans: 85.1 },
    { country: 'Portekiz', erisim: 89, kalite: 84, verimlilik: 77, memnuniyet: 81, performans: 81.5 },
    { country: 'Yunanistan', erisim: 88, kalite: 82, verimlilik: 72, memnuniyet: 76, performans: 78.3 },
    { country: 'Türkiye', erisim: 75, kalite: 68, verimlilik: 71, memnuniyet: 72, performans: 71.2 },
  ];

  // Teknoloji verileri
  const techData = [
    { country: 'İtalya', mri: 35.5, ct: 34.7, icu: 12.5, dijital: 85 },
    { country: 'Yunanistan', mri: 31.9, ct: 40.3, icu: 8.9, dijital: 71 },
    { country: 'İspanya', mri: 16.1, ct: 19.1, icu: 9.7, dijital: 83 },
    { country: 'Portekiz', mri: 14.8, ct: 30.6, icu: 8.1, dijital: 75 },
    { country: 'Fransa', mri: 14.4, ct: 17.5, icu: 15.8, dijital: 89 },
    { country: 'Türkiye', mri: 13.9, ct: 19.2, icu: 45.5, dijital: 68 },
    { country: 'İsrail', mri: 12.1, ct: 15.8, icu: 18.2, dijital: 92 },
  ];

  // Maliyet verileri
  const costData = [
    { country: 'Fransa', maliyet: 680, harcama: 3850 },
    { country: 'İtalya', maliyet: 520, harcama: 2580 },
    { country: 'İspanya', maliyet: 450, harcama: 2350 },
    { country: 'Portekiz', maliyet: 420, harcama: 1680 },
    { country: 'Yunanistan', maliyet: 380, harcama: 1245 },
    { country: 'İsrail', maliyet: 350, harcama: 2890 },
    { country: 'Türkiye', maliyet: 85, harcama: 452 },
  ];

  // Acil servis verileri
  const emergencyData = [
    { country: 'İsrail', mudahale: 7, bekleme: 35, ambulans: 6.8 },
    { country: 'Fransa', mudahale: 8, bekleme: 38, ambulans: 7.8 },
    { country: 'İspanya', mudahale: 10, bekleme: 52, ambulans: 6.3 },
    { country: 'İtalya', mudahale: 12, bekleme: 45, ambulans: 6.5 },
    { country: 'Portekiz', mudahale: 13, bekleme: 58, ambulans: 11.0 },
    { country: 'Yunanistan', mudahale: 15, bekleme: 92, ambulans: 8.3 },
    { country: 'Türkiye', mudahale: 18, bekleme: 85, ambulans: 5.0 },
  ];

  // Yatak fonksiyonları
  const bedFunctionData = [
    { name: 'Tedavi', value: 787600, color: '#3498db' },
    { name: 'Rehabilitasyon', value: 134156, color: '#2ecc71' },
    { name: 'Psikiyatri', value: 91440, color: '#9b59b6' },
    { name: 'Uzun Süreli', value: 43616, color: '#e74c3c' },
  ];

  const COLORS = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#e91e63', '#00bcd4'];

  const tabs = [
    { id: 'overview', label: '📊 Genel Bakış', icon: '🏥' },
    { id: 'quality', label: '⭐ Kalite', icon: '📈' },
    { id: 'turkey', label: '🇹🇷 Türkiye', icon: '📉' },
    { id: 'technology', label: '🔬 Teknoloji', icon: '💻' },
    { id: 'finance', label: '💰 Finans', icon: '💵' },
    { id: 'emergency', label: '🚑 Acil', icon: '⚕️' },
  ];

  // Özet istatistikler
  const stats = [
    { label: 'Toplam Ülke', value: '19', icon: '🌍', color: '#3498db' },
    { label: 'Toplam Hastane', value: '8,963', icon: '🏥', color: '#2ecc71' },
    { label: 'Toplam Yatak', value: '1.5M', icon: '🛏️', color: '#9b59b6' },
    { label: 'Ort. Performans', value: '78.5', icon: '⭐', color: '#f39c12' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      {/* Header */}
      <div className="bg-white rounded-2xl shadow-lg p-6 mb-6">
        <h1 className="text-3xl font-bold text-center bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          🌊 Akdeniz Bölgesi Hastane Sistemleri Analizi
        </h1>
        <p className="text-center text-gray-500 mt-2">19 Ülke • 8,963 Hastane • 1.5 Milyon Yatak Kapasitesi</p>
      </div>

      {/* Özet Kartlar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        {stats.map((stat, idx) => (
          <div key={idx} className="bg-white rounded-xl shadow-md p-4 flex items-center space-x-4 hover:shadow-lg transition-shadow">
            <div className="text-4xl">{stat.icon}</div>
            <div>
              <p className="text-2xl font-bold" style={{ color: stat.color }}>{stat.value}</p>
              <p className="text-sm text-gray-500">{stat.label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Tab Navigation */}
      <div className="bg-white rounded-xl shadow-md p-2 mb-6 flex flex-wrap gap-2 justify-center">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded-lg font-medium transition-all ${
              activeTab === tab.id
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content Area */}
      <div className="space-y-6">
        {activeTab === 'overview' && (
          <>
            {/* Hastane Sayıları */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">🏥 Ülkelere Göre Hastane Sayısı</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={countryData.sort((a, b) => b.toplam - a.toplam)} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="country" type="category" width={80} />
                    <Tooltip />
                    <Bar dataKey="toplam" fill="#3498db" name="Toplam Hastane" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">🏛️ Kamu vs Özel Hastane</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={countryData.slice(0, 6)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="country" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="kamu" fill="#3498db" name="Kamu" />
                    <Bar dataKey="ozel" fill="#e74c3c" name="Özel" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Yatak ve Performans */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">🛏️ 1000 Kişi Başına Yatak</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={countryData.sort((a, b) => b.yatakPer1000 - a.yatakPer1000)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="country" angle={-45} textAnchor="end" height={80} />
                    <YAxis domain={[0, 7]} />
                    <Tooltip />
                    <Bar dataKey="yatakPer1000" fill="#2ecc71" name="Yatak/1000 Nüfus">
                      {countryData.map((entry, index) => (
                        <Cell key={index} fill={entry.yatakPer1000 >= 3 ? '#2ecc71' : '#e74c3c'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">🏥 Yatak Fonksiyonları Dağılımı</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={bedFunctionData}
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {bedFunctionData.map((entry, index) => (
                        <Cell key={index} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => value.toLocaleString()} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </>
        )}

        {activeTab === 'quality' && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">⭐ Genel Performans Skorları</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={qualityData.sort((a, b) => b.performans - a.performans)} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" domain={[60, 100]} />
                    <YAxis dataKey="country" type="category" width={80} />
                    <Tooltip />
                    <Bar dataKey="performans" fill="#f39c12" name="Performans Skoru">
                      {qualityData.map((entry, index) => (
                        <Cell key={index} fill={entry.performans >= 80 ? '#2ecc71' : entry.performans >= 70 ? '#f39c12' : '#e74c3c'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">📊 Kalite Boyutları Karşılaştırması</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={qualityData.slice(0, 5)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="country" />
                    <YAxis domain={[60, 100]} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="erisim" fill="#3498db" name="Erişim" />
                    <Bar dataKey="kalite" fill="#2ecc71" name="Kalite" />
                    <Bar dataKey="verimlilik" fill="#e74c3c" name="Verimlilik" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-lg font-bold mb-4 text-gray-700">😊 Hasta Memnuniyeti vs Performans</h3>
              <ResponsiveContainer width="100%" height={350}>
                <ScatterChart>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="memnuniyet" name="Memnuniyet" domain={[70, 90]} />
                  <YAxis dataKey="performans" name="Performans" domain={[65, 95]} />
                  <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                  <Scatter data={qualityData} fill="#9b59b6">
                    {qualityData.map((entry, index) => (
                      <Cell key={index} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Scatter>
                </ScatterChart>
              </ResponsiveContainer>
              <div className="flex flex-wrap justify-center gap-2 mt-2">
                {qualityData.map((item, idx) => (
                  <span key={idx} className="px-2 py-1 rounded text-xs text-white" style={{ backgroundColor: COLORS[idx % COLORS.length] }}>
                    {item.country}
                  </span>
                ))}
              </div>
            </div>
          </>
        )}

        {activeTab === 'turkey' && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">🇹🇷 Türkiye Hastane Gelişimi (2002-2024)</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={turkeyTimeSeries}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="yil" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="sb" stroke="#3498db" strokeWidth={3} name="Sağlık Bakanlığı" />
                    <Line type="monotone" dataKey="ozel" stroke="#e74c3c" strokeWidth={3} name="Özel" />
                    <Line type="monotone" dataKey="universite" stroke="#f39c12" strokeWidth={3} name="Üniversite" />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">📈 Yatak Kapasitesi Gelişimi</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <ComposedChart data={turkeyTimeSeries}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="yil" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="toplamYatak" fill="#3498db" stroke="#3498db" fillOpacity={0.3} name="Toplam Yatak" />
                  </ComposedChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Türkiye İstatistik Kartları */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-4 text-white">
                <p className="text-sm opacity-80">Hastane Artışı</p>
                <p className="text-2xl font-bold">+35.1%</p>
                <p className="text-xs">2002-2024</p>
              </div>
              <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-4 text-white">
                <p className="text-sm opacity-80">Yatak Artışı</p>
                <p className="text-2xl font-bold">+63.2%</p>
                <p className="text-xs">2002-2024</p>
              </div>
              <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-4 text-white">
                <p className="text-sm opacity-80">Özel Hastane</p>
                <p className="text-2xl font-bold">+281</p>
                <p className="text-xs">Yeni hastane</p>
              </div>
              <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-4 text-white">
                <p className="text-sm opacity-80">YBÜ Kapasitesi</p>
                <p className="text-2xl font-bold">45.5</p>
                <p className="text-xs">/ 100k nüfus</p>
              </div>
            </div>
          </>
        )}

        {activeTab === 'technology' && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">🔬 MRI ve CT Yoğunluğu</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={techData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="country" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="mri" fill="#3498db" name="MRI/Milyon" />
                    <Bar dataKey="ct" fill="#e74c3c" name="CT/Milyon" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">💻 Dijital Sağlık İndeksi</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={techData.sort((a, b) => b.dijital - a.dijital)} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" domain={[60, 100]} />
                    <YAxis dataKey="country" type="category" width={80} />
                    <Tooltip />
                    <Bar dataKey="dijital" fill="#9b59b6" name="Dijital İndeks">
                      {techData.map((entry, index) => (
                        <Cell key={index} fill={entry.dijital >= 85 ? '#2ecc71' : entry.dijital >= 75 ? '#f39c12' : '#e74c3c'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-lg font-bold mb-4 text-gray-700">🏥 Yoğun Bakım Kapasitesi (100k Nüfus Başına)</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={techData.sort((a, b) => b.icu - a.icu)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="country" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="icu" fill="#e91e63" name="YBÜ Yatağı" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </>
        )}

        {activeTab === 'finance' && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">💵 Yatak Günü Başına Maliyet (USD)</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={costData.sort((a, b) => b.maliyet - a.maliyet)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="country" />
                    <YAxis />
                    <Tooltip formatter={(value) => `$${value}`} />
                    <Bar dataKey="maliyet" fill="#f39c12" name="Maliyet">
                      {costData.map((entry, index) => (
                        <Cell key={index} fill={entry.maliyet > 500 ? '#e74c3c' : entry.maliyet > 300 ? '#f39c12' : '#2ecc71'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">💰 Kişi Başı Sağlık Harcaması (USD)</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={costData.sort((a, b) => b.harcama - a.harcama)} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="country" type="category" width={80} />
                    <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                    <Bar dataKey="harcama" fill="#2ecc71" name="Harcama/Kişi" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Maliyet Karşılaştırma Kartları */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white rounded-xl shadow-md p-4 text-center">
                <p className="text-sm text-gray-500">En Pahalı</p>
                <p className="text-xl font-bold text-red-500">Fransa</p>
                <p className="text-2xl font-bold">$680/gün</p>
              </div>
              <div className="bg-white rounded-xl shadow-md p-4 text-center">
                <p className="text-sm text-gray-500">En Ucuz</p>
                <p className="text-xl font-bold text-green-500">Türkiye</p>
                <p className="text-2xl font-bold">$85/gün</p>
              </div>
              <div className="bg-white rounded-xl shadow-md p-4 text-center">
                <p className="text-sm text-gray-500">Fark</p>
                <p className="text-xl font-bold text-purple-500">8x</p>
                <p className="text-sm">Maliyet farkı</p>
              </div>
              <div className="bg-white rounded-xl shadow-md p-4 text-center">
                <p className="text-sm text-gray-500">Toplam Bütçe</p>
                <p className="text-xl font-bold text-blue-500">$290.6B</p>
                <p className="text-sm">Kamu harcaması</p>
              </div>
            </div>
          </>
        )}

        {activeTab === 'emergency' && (
          <>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">🚑 Acil Müdahale Süresi (Dakika)</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={emergencyData.sort((a, b) => a.mudahale - b.mudahale)} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis dataKey="country" type="category" width={80} />
                    <Tooltip />
                    <Bar dataKey="mudahale" name="Müdahale Süresi">
                      {emergencyData.map((entry, index) => (
                        <Cell key={index} fill={entry.mudahale <= 10 ? '#2ecc71' : entry.mudahale <= 15 ? '#f39c12' : '#e74c3c'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="bg-white rounded-xl shadow-md p-6">
                <h3 className="text-lg font-bold mb-4 text-gray-700">⏱️ Acil Serviste Bekleme Süresi</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={emergencyData.sort((a, b) => a.bekleme - b.bekleme)}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="country" angle={-45} textAnchor="end" height={80} />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="bekleme" fill="#e74c3c" name="Bekleme (dk)">
                      {emergencyData.map((entry, index) => (
                        <Cell key={index} fill={entry.bekleme <= 45 ? '#2ecc71' : entry.bekleme <= 60 ? '#f39c12' : '#e74c3c'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-lg font-bold mb-4 text-gray-700">🚐 Ambulans Kapsama Oranı (100k Nüfus)</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={emergencyData.sort((a, b) => b.ambulans - a.ambulans)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="country" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="ambulans" fill="#2ecc71" name="Ambulans/100k" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </>
        )}
      </div>

      {/* Footer */}
      <div className="mt-8 text-center text-gray-500 text-sm">
        <p>📊 Veri Kaynakları: T.C. Sağlık Bakanlığı, Eurostat, WHO, Ulusal Sağlık Bakanlıkları</p>
        <p>🗓️ Analiz Tarihi: Ocak 2026 | 19 Akdeniz Ülkesi</p>
      </div>
    </div>
  );
};

export default MediterraneanHospitalDashboard;
