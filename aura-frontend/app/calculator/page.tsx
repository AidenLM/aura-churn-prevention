'use client';

import { useState } from 'react';
import Image from 'next/image';
import { calculateRisk, formatCurrency, type RiskCalculationInput, type RiskCalculationResult } from '@/lib/api';
import Link from 'next/link';
import { TooltipProvider } from '@/components/ui/tooltip/TooltipProvider';
import { Tooltip } from '@/components/ui/tooltip/Tooltip';
import { Info } from 'lucide-react';

export default function CalculatorPage() {
  const [formData, setFormData] = useState<RiskCalculationInput>({
    gender: 'Male',
    senior_citizen: 0,
    partner: 'No',
    dependents: 'No',
    tenure: 12,
    contract: 'Month-to-month',
    paperless_billing: 'Yes',
    payment_method: 'Electronic check',
    monthly_charges: 70.0,
    total_charges: 840.0,
    phone_service: 'Yes',
    multiple_lines: 'No',
    internet_service: 'Fiber optic',
    online_security: 'No',
    online_backup: 'No',
    device_protection: 'No',
    tech_support: 'No',
    streaming_tv: 'No',
    streaming_movies: 'No',
  });

  const [result, setResult] = useState<RiskCalculationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const calculatedResult = await calculateRisk(formData);
      setResult(calculatedResult);
    } catch (err) {
      setError('Risk hesaplanırken bir hata oluştu. Lütfen tekrar deneyin.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: keyof RiskCalculationInput, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const getRiskColor = (level: string) => {
    switch (level?.toLowerCase()) {
      case 'high': return { bg: 'bg-[#FFEBE6]', text: 'text-[#DE350B]', border: 'border-[#DE350B]' };
      case 'medium': return { bg: 'bg-[#FFF0B3]', text: 'text-[#FF991F]', border: 'border-[#FF991F]' };
      case 'low': return { bg: 'bg-[#E3FCEF]', text: 'text-[#00875A]', border: 'border-[#00875A]' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-600', border: 'border-gray-300' };
    }
  };

  return (
    <TooltipProvider>
      <div className="min-h-screen bg-[#F4F5F7]">
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-8 py-5 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="text-[#5E6C84] hover:text-[#172B4D] transition-colors">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </Link>
            <div>
              <h1 className="text-[#172B4D] text-2xl font-bold">Risk Hesaplama</h1>
              <p className="text-[#5E6C84] text-sm">Müşteri profili için kayıp riski hesapla</p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 lg:px-8 py-6 lg:py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6">
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit} className="space-y-4 lg:space-y-6">
              {/* Demografik Bilgiler */}
              <div className="bg-white rounded-lg border border-gray-200 p-4 lg:p-8 shadow-sm">
                <h3 className="text-[#172B4D] text-lg font-semibold mb-6 flex items-center gap-3">
                  <div className="w-10 h-10 bg-[#0052CC]/10 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-[#0052CC]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  Demografik Bilgiler
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Cinsiyet
                      <Tooltip id="gender" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.gender} onChange={(e) => handleInputChange('gender', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Male">Erkek</option>
                      <option value="Female">Kadın</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Yaşlı Vatandaş
                      <Tooltip id="senior-citizen" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.senior_citizen} onChange={(e) => handleInputChange('senior_citizen', parseInt(e.target.value))} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value={0}>Hayır</option>
                      <option value={1}>Evet</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Eş Durumu
                      <Tooltip id="partner" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.partner} onChange={(e) => handleInputChange('partner', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Yes">Evet</option>
                      <option value="No">Hayır</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Bakmakla Yükümlü
                      <Tooltip id="dependents" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.dependents} onChange={(e) => handleInputChange('dependents', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Yes">Evet</option>
                      <option value="No">Hayır</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Hesap Bilgileri */}
              <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
                <h3 className="text-[#172B4D] text-lg font-semibold mb-6 flex items-center gap-3">
                  <div className="w-10 h-10 bg-[#00875A]/10 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-[#00875A]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  Hesap Bilgileri
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Müşteri Süresi (ay)
                      <Tooltip id="tenure" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <input type="number" value={formData.tenure} onChange={(e) => handleInputChange('tenure', parseInt(e.target.value))} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" min="0" required />
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Sözleşme Tipi
                      <Tooltip id="contract-type" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.contract} onChange={(e) => handleInputChange('contract', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Month-to-month">Aylık</option>
                      <option value="One year">1 Yıl</option>
                      <option value="Two year">2 Yıl</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Kağıtsız Fatura
                      <Tooltip id="paperless-billing" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.paperless_billing} onChange={(e) => handleInputChange('paperless_billing', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Yes">Evet</option>
                      <option value="No">Hayır</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Ödeme Yöntemi
                      <Tooltip id="payment-method" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.payment_method} onChange={(e) => handleInputChange('payment_method', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Electronic check">Elektronik Çek</option>
                      <option value="Mailed check">Posta Çeki</option>
                      <option value="Bank transfer (automatic)">Otomatik Banka Transferi</option>
                      <option value="Credit card (automatic)">Otomatik Kredi Kartı</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Aylık Ücret ($)
                      <Tooltip id="monthly-charges" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <input type="number" value={formData.monthly_charges} onChange={(e) => handleInputChange('monthly_charges', parseFloat(e.target.value))} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" min="0" step="0.01" required />
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Toplam Ücret ($)
                      <Tooltip id="total-charges" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <input type="number" value={formData.total_charges} onChange={(e) => handleInputChange('total_charges', parseFloat(e.target.value))} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" min="0" step="0.01" required />
                  </div>
                </div>
              </div>

              {/* Telefon Hizmetleri */}
              <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
                <h3 className="text-[#172B4D] text-lg font-semibold mb-6 flex items-center gap-3">
                  <div className="w-10 h-10 bg-[#6554C0]/10 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-[#6554C0]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  Telefon Hizmetleri
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Telefon Hizmeti
                      <Tooltip id="phone-service" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.phone_service} onChange={(e) => handleInputChange('phone_service', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Yes">Evet</option>
                      <option value="No">Hayır</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Çoklu Hat
                      <Tooltip id="multiple-lines" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.multiple_lines} onChange={(e) => handleInputChange('multiple_lines', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Yes">Evet</option>
                      <option value="No">Hayır</option>
                      <option value="No phone service">Telefon Hizmeti Yok</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* İnternet Hizmetleri */}
              <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
                <h3 className="text-[#172B4D] text-lg font-semibold mb-6 flex items-center gap-3">
                  <div className="w-10 h-10 bg-[#FF991F]/10 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-[#FF991F]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                    </svg>
                  </div>
                  İnternet Hizmetleri
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      İnternet Hizmeti
                      <Tooltip id="internet-service" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.internet_service} onChange={(e) => handleInputChange('internet_service', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="DSL">DSL</option>
                      <option value="Fiber optic">Fiber Optik</option>
                      <option value="No">Hayır</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Online Güvenlik
                      <Tooltip id="online-security" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.online_security} onChange={(e) => handleInputChange('online_security', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Yes">Evet</option>
                      <option value="No">Hayır</option>
                      <option value="No internet service">İnternet Hizmeti Yok</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Online Yedekleme
                      <Tooltip id="online-backup" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.online_backup} onChange={(e) => handleInputChange('online_backup', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Yes">Evet</option>
                      <option value="No">Hayır</option>
                      <option value="No internet service">İnternet Hizmeti Yok</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Cihaz Koruma
                      <Tooltip id="device-protection" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.device_protection} onChange={(e) => handleInputChange('device_protection', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Yes">Evet</option>
                      <option value="No">Hayır</option>
                      <option value="No internet service">İnternet Hizmeti Yok</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Teknik Destek
                      <Tooltip id="tech-support" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.tech_support} onChange={(e) => handleInputChange('tech_support', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Yes">Evet</option>
                      <option value="No">Hayır</option>
                      <option value="No internet service">İnternet Hizmeti Yok</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      TV Yayını
                      <Tooltip id="streaming-tv" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.streaming_tv} onChange={(e) => handleInputChange('streaming_tv', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Yes">Evet</option>
                      <option value="No">Hayır</option>
                      <option value="No internet service">İnternet Hizmeti Yok</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-[#172B4D] text-sm font-medium mb-2 flex items-center gap-2">
                      Film Yayını
                      <Tooltip id="streaming-movies" side="right">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </label>
                    <select value={formData.streaming_movies} onChange={(e) => handleInputChange('streaming_movies', e.target.value)} className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D]" required>
                      <option value="Yes">Evet</option>
                      <option value="No">Hayır</option>
                      <option value="No internet service">İnternet Hizmeti Yok</option>
                    </select>
                  </div>
                </div>
              </div>

              <button type="submit" disabled={loading} className="w-full px-6 py-4 rounded-lg bg-[#0052CC] hover:bg-[#0747A6] disabled:bg-gray-300 text-white text-base font-medium transition-colors shadow-sm disabled:cursor-not-allowed">
                {loading ? 'Hesaplanıyor...' : 'Risk Hesapla'}
              </button>

              {error && (
                <div className="bg-[#FFEBE6] border border-[#DE350B] rounded-lg p-4">
                  <p className="text-[#DE350B] text-sm">{error}</p>
                </div>
              )}
            </form>
          </div>

          {/* Results - Right Side */}
          <div className="space-y-6">
            {result ? (
              <>
                <div className={`rounded-lg border-2 p-8 shadow-sm ${getRiskColor(result.risk_level).bg} ${getRiskColor(result.risk_level).border}`}>
                  <div className="text-center">
                    <p className="text-[#5E6C84] text-sm uppercase tracking-wider mb-4 flex items-center justify-center gap-2">
                      Risk Skoru
                      <Tooltip id="risk-score" side="bottom">
                        <Info className="w-4 h-4 text-gray-400" />
                      </Tooltip>
                    </p>
                    <div className="relative w-32 h-32 mx-auto mb-4">
                      <svg className="w-full h-full transform -rotate-90">
                        <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="8" fill="none" className="text-gray-200" />
                        <circle cx="64" cy="64" r="56" stroke="currentColor" strokeWidth="8" fill="none" strokeDasharray={`${2 * Math.PI * 56}`} strokeDashoffset={`${2 * Math.PI * 56 * (1 - result.risk_score)}`} className={getRiskColor(result.risk_level).text} strokeLinecap="round" />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className={`text-4xl font-bold ${getRiskColor(result.risk_level).text}`}>
                          {(result.risk_score * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                    <span className={`inline-block px-4 py-2 rounded-lg ${getRiskColor(result.risk_level).bg} ${getRiskColor(result.risk_level).text} border ${getRiskColor(result.risk_level).border} text-sm font-semibold`}>
                      {result.risk_level} Risk
                    </span>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-[#6554C0]/10 to-transparent rounded-lg border border-gray-200 p-6 shadow-sm">
                  <h3 className="text-[#172B4D] text-sm font-semibold mb-3 flex items-center gap-2">
                    <svg className="w-5 h-5 text-[#6554C0]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    AI Analizi
                    <Tooltip id="ai-insights" side="bottom">
                      <Info className="w-4 h-4 text-gray-400" />
                    </Tooltip>
                  </h3>
                  <p className="text-[#5E6C84] text-sm leading-relaxed">{result.ai_analysis}</p>
                </div>
              </>
            ) : (
              <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm text-center">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                </div>
                <p className="text-[#5E6C84] text-sm">Formu doldurun ve risk hesaplayın</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
    </TooltipProvider>
  );
}
