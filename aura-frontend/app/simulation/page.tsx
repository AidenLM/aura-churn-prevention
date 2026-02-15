'use client';

import { useState } from 'react';
import { simulateROI, formatCurrency, formatNumber, type SimulationInput, type SimulationResult } from '@/lib/api';
import Link from 'next/link';
import { TooltipProvider, Tooltip } from '@/components/ui/tooltip';
import { Info } from 'lucide-react';

export default function SimulationPage() {
  const [formData, setFormData] = useState<SimulationInput>({
    risk_threshold: 0.7,
    campaign_budget: 100000,
  });

  const [result, setResult] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSimulate = async () => {
    setLoading(true);
    setError(null);

    try {
      const simulationResult = await simulateROI(formData);
      setResult(simulationResult);
    } catch (err) {
      setError('Simülasyon çalıştırılırken bir hata oluştu. Lütfen tekrar deneyin.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getROIColor = (roi: number) => {
    if (roi >= 200) return { bg: 'bg-[#E3FCEF]', text: 'text-[#00875A]', border: 'border-[#00875A]' };
    if (roi >= 100) return { bg: 'bg-[#FFF0B3]', text: 'text-[#FF991F]', border: 'border-[#FF991F]' };
    return { bg: 'bg-[#FFEBE6]', text: 'text-[#DE350B]', border: 'border-[#DE350B]' };
  };

  const getCoverageColor = (coverage: number) => {
    if (coverage >= 30) return 'bg-[#00875A]';
    if (coverage >= 15) return 'bg-[#FF991F]';
    return 'bg-[#DE350B]';
  };

  return (
    <TooltipProvider>
    <div className="min-h-screen bg-[#F4F5F7]">
      {/* Header */}
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-8 py-5 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/dashboard" className="text-[#5E6C84] hover:text-[#172B4D] transition-colors">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </Link>
            <div>
              <h1 className="text-[#172B4D] text-2xl font-bold">Kampanya Simülasyonu</h1>
              <p className="text-[#5E6C84] text-sm">ROI hesapla ve kampanya etkisini öngör</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 lg:px-8 py-6 lg:py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          {/* Left Side - Controls */}
          <div className="space-y-6">
            {/* Risk Threshold Control */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-[#0052CC]/10 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-[#0052CC]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-[#172B4D] text-lg font-semibold">Risk Eşiği</h3>
                  <p className="text-[#5E6C84] text-sm">Hedeflenecek minimum risk seviyesi</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-[#172B4D] text-sm font-medium">Risk Skoru</span>
                  <span className="text-[#0052CC] text-2xl font-bold">{(formData.risk_threshold * 100).toFixed(0)}%</span>
                </div>
                
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={formData.risk_threshold * 100}
                  onChange={(e) => setFormData(prev => ({ ...prev, risk_threshold: parseInt(e.target.value) / 100 }))}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-[#0052CC]"
                />
                
                <div className="flex justify-between text-xs text-[#5E6C84]">
                  <span>Düşük (0%)</span>
                  <span>Orta (50%)</span>
                  <span>Yüksek (100%)</span>
                </div>
              </div>
            </div>

            {/* Budget Control */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-[#00875A]/10 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-[#00875A]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-[#172B4D] text-lg font-semibold">Kampanya Bütçesi</h3>
                  <p className="text-[#5E6C84] text-sm">Toplam harcama limiti</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[#172B4D] text-sm font-medium">Bütçe</span>
                  <span className="text-[#00875A] text-2xl font-bold">{formatCurrency(formData.campaign_budget)}</span>
                </div>
                
                <input
                  type="number"
                  value={formData.campaign_budget}
                  onChange={(e) => setFormData(prev => ({ ...prev, campaign_budget: parseFloat(e.target.value) || 0 }))}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#0052CC] focus:ring-2 focus:ring-[#0052CC]/20 outline-none transition-colors text-[#172B4D] text-lg font-semibold"
                  min="0"
                  step="10000"
                />

                <div className="grid grid-cols-3 gap-2">
                  {[50000, 100000, 250000].map((amount) => (
                    <button
                      key={amount}
                      onClick={() => setFormData(prev => ({ ...prev, campaign_budget: amount }))}
                      className="px-3 py-2 rounded-lg border border-gray-300 hover:border-[#0052CC] hover:bg-[#0052CC]/5 text-[#172B4D] text-xs font-medium transition-colors"
                    >
                      {formatCurrency(amount)}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Simulate Button */}
            <button
              onClick={handleSimulate}
              disabled={loading}
              className="w-full px-6 py-4 rounded-lg bg-[#0052CC] hover:bg-[#0747A6] disabled:bg-gray-300 text-white text-base font-medium transition-colors shadow-sm disabled:cursor-not-allowed"
            >
              {loading ? 'Hesaplanıyor...' : 'Simülasyonu Çalıştır'}
            </button>

            {error && (
              <div className="bg-[#FFEBE6] border border-[#DE350B] rounded-lg p-4">
                <p className="text-[#DE350B] text-sm">{error}</p>
              </div>
            )}
          </div>

          {/* Right Side - Results */}
          <div className="space-y-6">
            {result ? (
              <>
                {/* Key Metrics Grid */}
                <div className="grid grid-cols-2 gap-4">
                  {/* Targeted Customers */}
                  <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                    <div className="flex items-center gap-2 mb-2">
                      <svg className="w-5 h-5 text-[#0052CC]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                      <span className="text-[#5E6C84] text-xs uppercase tracking-wider">Hedef Müşteri</span>
                    </div>
                    <p className="text-[#172B4D] text-3xl font-bold">{formatNumber(result.targeted_customers)}</p>
                  </div>

                  {/* Total Cost */}
                  <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                    <div className="flex items-center gap-2 mb-2">
                      <svg className="w-5 h-5 text-[#DE350B]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                      <span className="text-[#5E6C84] text-xs uppercase tracking-wider">Toplam Maliyet</span>
                    </div>
                    <p className="text-[#172B4D] text-3xl font-bold">{formatCurrency(result.total_cost)}</p>
                  </div>

                  {/* ROI */}
                  <div className={`rounded-lg border-2 p-6 shadow-sm ${getROIColor(result.roi).bg} ${getROIColor(result.roi).border}`}>
                    <div className="flex items-center gap-2 mb-2">
                      <svg className={`w-5 h-5 ${getROIColor(result.roi).text}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                      </svg>
                      <span className="text-[#5E6C84] text-xs uppercase tracking-wider">ROI</span>
                      <Tooltip id="roi" side="right">
                        <Info className="w-3.5 h-3.5 text-gray-400" />
                      </Tooltip>
                    </div>
                    <p className={`text-3xl font-bold ${getROIColor(result.roi).text}`}>%{result.roi.toFixed(1)}</p>
                  </div>

                  {/* Net Gain */}
                  <div className="bg-gradient-to-br from-[#00875A]/10 to-transparent rounded-lg border border-[#00875A]/30 p-6 shadow-sm">
                    <div className="flex items-center gap-2 mb-2">
                      <svg className="w-5 h-5 text-[#00875A]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span className="text-[#5E6C84] text-xs uppercase tracking-wider">Net Kazanç</span>
                    </div>
                    <p className="text-[#00875A] text-3xl font-bold">{formatCurrency(result.net_gain)}</p>
                  </div>
                </div>

                {/* Additional Metrics */}
                <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                  <h3 className="text-[#172B4D] text-sm font-semibold mb-4">Detaylı Metrikler</h3>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-[#5E6C84] text-sm">Müşteri Başı Maliyet</span>
                        <Tooltip id="campaign-cost" side="right">
                          <Info className="w-3.5 h-3.5 text-gray-400" />
                        </Tooltip>
                      </div>
                      <span className="text-[#172B4D] text-sm font-semibold">{formatCurrency(result.cost_per_customer)}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-[#5E6C84] text-sm">Beklenen Elde Tutma Oranı</span>
                        <Tooltip id="retention-rate" side="right">
                          <Info className="w-3.5 h-3.5 text-gray-400" />
                        </Tooltip>
                      </div>
                      <span className="text-[#172B4D] text-sm font-semibold">%{(result.expected_retention_rate * 100).toFixed(1)}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="text-[#5E6C84] text-sm">Öngörülen Gelir</span>
                        <Tooltip id="projected-revenue" side="right">
                          <Info className="w-3.5 h-3.5 text-gray-400" />
                        </Tooltip>
                      </div>
                      <span className="text-[#172B4D] text-sm font-semibold">{formatCurrency(result.projected_revenue)}</span>
                    </div>
                  </div>
                </div>

                {/* Coverage Visualization */}
                <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-[#172B4D] text-sm font-semibold">Müşteri Tabanı Kapsamı</h3>
                    <span className="text-[#172B4D] text-lg font-bold">%{result.coverage_percentage.toFixed(1)}</span>
                  </div>
                  <div className="w-full h-4 bg-gray-100 rounded-full overflow-hidden">
                    <div 
                      className={`h-full ${getCoverageColor(result.coverage_percentage)} transition-all duration-500`}
                      style={{width: `${Math.min(result.coverage_percentage, 100)}%`}}
                    />
                  </div>
                  <div className="flex justify-between text-xs text-[#5E6C84] mt-2">
                    <span>0%</span>
                    <span>50%</span>
                    <span>100%</span>
                  </div>
                </div>

                {/* Insights */}
                <div className="bg-gradient-to-br from-[#6554C0]/10 to-transparent rounded-lg border border-gray-200 p-6 shadow-sm">
                  <h3 className="text-[#172B4D] text-sm font-semibold mb-3 flex items-center gap-2">
                    <svg className="w-5 h-5 text-[#6554C0]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    Öneriler
                  </h3>
                  <div className="space-y-2 text-[#5E6C84] text-sm">
                    {result.roi >= 200 && (
                      <p>✓ Mükemmel ROI! Bu kampanya yüksek getiri sağlayacak.</p>
                    )}
                    {result.roi >= 100 && result.roi < 200 && (
                      <p>✓ İyi bir ROI. Kampanya karlı olacak.</p>
                    )}
                    {result.roi < 100 && (
                      <p>⚠ Düşük ROI. Bütçeyi artırmayı veya risk eşiğini ayarlamayı düşünün.</p>
                    )}
                    {result.coverage_percentage < 15 && (
                      <p>⚠ Düşük kapsam. Daha fazla müşteriye ulaşmak için risk eşiğini düşürün.</p>
                    )}
                    {result.coverage_percentage >= 30 && (
                      <p>✓ Geniş kapsam. Müşteri tabanınızın önemli bir kısmına ulaşıyorsunuz.</p>
                    )}
                  </div>
                </div>
              </>
            ) : (
              <div className="bg-white rounded-lg border border-gray-200 p-12 shadow-sm text-center">
                <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-10 h-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <p className="text-[#5E6C84] text-sm mb-2">Parametreleri ayarlayın</p>
                <p className="text-[#5E6C84] text-xs">Risk eşiği ve bütçe belirleyerek simülasyonu başlatın</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
    </TooltipProvider>
  );
}
