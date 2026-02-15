import { getDashboardSummary, formatNumber, formatPercentage } from '@/lib/api';
import Link from 'next/link';
import Image from 'next/image';
import RiskDistributionChart from './components/RiskDistributionChart';
import TopRiskyCustomersChart from './components/TopRiskyCustomersChart';
import { TooltipProvider, Tooltip } from '@/components/ui/tooltip';
import { Info } from 'lucide-react';

export default async function DashboardPage() {
  const data = await getDashboardSummary();
  
  return (
    <TooltipProvider>
      <div className="min-h-screen bg-[#F4F5F7] flex flex-col lg:flex-row">
      {/* Sidebar - Hidden on mobile, visible on desktop */}
      <aside className="hidden lg:flex w-64 bg-white border-r border-gray-200 flex-col shadow-sm">
        {/* Logo */}
        <div className="p-6 border-b border-gray-200">
          <Link href="/" className="flex items-center gap-3">
            <Image src="/logo-transparent.png" alt="AURA Logo" width={240} height={96} className="h-24 w-auto" priority />
          </Link>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1">
          <Link href="/dashboard" className="flex items-center gap-3 px-4 py-2.5 rounded-lg bg-[#0052CC]/10 text-[#0052CC] font-medium text-sm transition-colors">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
            <span>Dashboard</span>
          </Link>

          <Link href="/reports" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[#5E6C84] hover:text-[#172B4D] hover:bg-gray-100 font-medium text-sm transition-colors">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>Raporlar</span>
          </Link>

          <Link href="/customers" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[#5E6C84] hover:text-[#172B4D] hover:bg-gray-100 font-medium text-sm transition-colors">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <span>Müşteriler</span>
          </Link>

          <Link href="/calculator" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[#5E6C84] hover:text-[#172B4D] hover:bg-gray-100 font-medium text-sm transition-colors">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
            <span>Risk Hesapla</span>
          </Link>

          <Link href="/simulation" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[#5E6C84] hover:text-[#172B4D] hover:bg-gray-100 font-medium text-sm transition-colors">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>ROI Simülasyonu</span>
          </Link>
        </nav>

        {/* User Profile */}
        <div className="p-4 border-t border-gray-200">
          <div className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
            <div className="w-9 h-9 bg-gradient-to-br from-[#0052CC] to-[#0065FF] rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-semibold">JD</span>
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-[#172B4D] text-sm font-medium truncate">John Doe</div>
              <div className="text-[#5E6C84] text-xs truncate">Admin</div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header - Jira Style */}
        <header className="border-b border-gray-200 bg-white shadow-sm">
          <div className="px-4 lg:px-8 py-4 lg:py-5 flex items-center justify-between">
            <div className="flex items-center gap-4">
              {/* Mobile Logo */}
              <div className="lg:hidden flex items-center gap-2">
                <Image src="/logo-transparent.png" alt="AURA" width={180} height={72} className="h-18 w-auto" priority />
              </div>
              <div>
                <h1 className="text-[#172B4D] text-xl lg:text-2xl font-bold mb-0 lg:mb-1">Hoş geldin, John</h1>
                <p className="text-[#5E6C84] text-xs lg:text-sm hidden sm:block">Müşteri kayıp riskini analiz et ve önlem al</p>
              </div>
            </div>
            <div className="flex items-center gap-2 lg:gap-3">
              <button className="hidden sm:flex px-3 lg:px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 text-[#172B4D] text-xs lg:text-sm font-medium transition-colors">
                Rapor İndir
              </button>
              <button className="px-3 lg:px-4 py-2 rounded-lg bg-[#0052CC] hover:bg-[#0747A6] text-white text-xs lg:text-sm font-medium transition-colors shadow-sm">
                Yeni Analiz
              </button>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <main className="flex-1 p-4 lg:p-8 overflow-auto">
          {/* Stats Cards - Jira Colors */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-5 mb-6 lg:mb-8">
            {/* Total Customers */}
            <div className="bg-white rounded-lg border border-gray-200 p-4 lg:p-6 hover:shadow-md transition-all group">
              <div className="flex items-start justify-between mb-4 lg:mb-6">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-[#5E6C84] text-xs font-medium uppercase tracking-wider">Toplam Müşteri</span>
                    <Tooltip id="total-customers" side="right">
                      <Info className="w-3.5 h-3.5 text-[#5E6C84] hover:text-[#0052CC] cursor-help transition-colors" />
                    </Tooltip>
                  </div>
                  <div className="text-[#172B4D] text-2xl lg:text-3xl font-bold mt-2">{formatNumber(data.total_customers)}</div>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="text-[#00875A] text-xs lg:text-sm font-medium">+8.2%</span>
                    <span className="text-[#5E6C84] text-xs">bu ay</span>
                  </div>
                </div>
                <div className="w-10 lg:w-12 h-10 lg:h-12 bg-[#0052CC]/10 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                  <svg className="w-5 lg:w-6 h-5 lg:h-6 text-[#0052CC]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                </div>
              </div>
            </div>

            {/* High Risk */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all group">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-[#5E6C84] text-xs font-medium uppercase tracking-wider">Yüksek Risk</span>
                    <Tooltip id="high-risk-count" side="right">
                      <Info className="w-3.5 h-3.5 text-[#5E6C84] hover:text-[#0052CC] cursor-help transition-colors" />
                    </Tooltip>
                  </div>
                  <div className="text-[#172B4D] text-3xl font-bold mt-2">{formatNumber(data.high_risk_count)}</div>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="text-[#DE350B] text-sm font-medium">-3.1%</span>
                    <span className="text-[#5E6C84] text-xs">bu ay</span>
                  </div>
                </div>
                <div className="w-12 h-12 bg-[#DE350B]/10 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                  <svg className="w-6 h-6 text-[#DE350B]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Average Risk */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all group">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <span className="text-[#5E6C84] text-xs font-medium uppercase tracking-wider">Ortalama Risk</span>
                  <div className="text-[#172B4D] text-3xl font-bold mt-2">{data.average_risk.toFixed(2)}</div>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="text-[#FF991F] text-sm font-medium">0-1 skalası</span>
                  </div>
                </div>
                <div className="w-12 h-12 bg-[#FF991F]/10 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                  <svg className="w-6 h-6 text-[#FF991F]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Churn Rate */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-all group">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-[#5E6C84] text-xs font-medium uppercase tracking-wider">Aylık Kayıp</span>
                    <Tooltip id="churn-rate" side="right">
                      <Info className="w-3.5 h-3.5 text-[#5E6C84] hover:text-[#0052CC] cursor-help transition-colors" />
                    </Tooltip>
                  </div>
                  <div className="text-[#172B4D] text-3xl font-bold mt-2">{formatPercentage(data.monthly_churn_rate)}</div>
                  <div className="flex items-center gap-2 mt-2">
                    <span className="text-[#6554C0] text-sm font-medium">Tahmini</span>
                  </div>
                </div>
                <div className="w-12 h-12 bg-[#6554C0]/10 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform">
                  <svg className="w-6 h-6 text-[#6554C0]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* Main Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6 mb-6 lg:mb-8">
            {/* Risk Distribution - Takes 2 columns on desktop, full width on mobile */}
            <div className="lg:col-span-2 bg-white rounded-lg border border-gray-200 p-4 lg:p-8 shadow-sm">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                  <h2 className="text-[#172B4D] text-xl font-semibold">Risk Dağılımı</h2>
                  <Tooltip id="risk-distribution" side="right">
                    <Info className="w-4 h-4 text-[#5E6C84] hover:text-[#0052CC] cursor-help transition-colors" />
                  </Tooltip>
                </div>
                <button className="text-[#0052CC] hover:text-[#0747A6] text-sm font-medium transition-colors">
                  Detaylar →
                </button>
              </div>
              
              {/* Recharts Bar Chart */}
              <RiskDistributionChart data={data.risk_distribution} />
              
              {/* Summary Stats Below Chart */}
              <div className="grid grid-cols-3 gap-4 mt-6 pt-6 border-t border-gray-200">
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <div className="w-3 h-3 rounded-full bg-[#00875A]"></div>
                    <span className="text-[#5E6C84] text-xs font-medium">Düşük</span>
                  </div>
                  <p className="text-[#172B4D] text-lg font-bold">{formatNumber(data.risk_distribution.low)}</p>
                  <p className="text-[#5E6C84] text-xs">({((data.risk_distribution.low / data.total_customers) * 100).toFixed(0)}%)</p>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <div className="w-3 h-3 rounded-full bg-[#FF991F]"></div>
                    <span className="text-[#5E6C84] text-xs font-medium">Orta</span>
                  </div>
                  <p className="text-[#172B4D] text-lg font-bold">{formatNumber(data.risk_distribution.medium)}</p>
                  <p className="text-[#5E6C84] text-xs">({((data.risk_distribution.medium / data.total_customers) * 100).toFixed(0)}%)</p>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center gap-2 mb-1">
                    <div className="w-3 h-3 rounded-full bg-[#DE350B]"></div>
                    <span className="text-[#5E6C84] text-xs font-medium">Yüksek</span>
                  </div>
                  <p className="text-[#172B4D] text-lg font-bold">{formatNumber(data.risk_distribution.high)}</p>
                  <p className="text-[#5E6C84] text-xs">({((data.risk_distribution.high / data.total_customers) * 100).toFixed(0)}%)</p>
                </div>
              </div>
            </div>

            {/* Top Risky Customers */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-[#172B4D] text-lg font-semibold">En Riskli Müşteriler</h2>
              </div>
              
              {/* Recharts Horizontal Bar Chart */}
              <TopRiskyCustomersChart customers={data.top_risky_customers} />
              
              {/* View All Link */}
              <div className="mt-6 pt-4 border-t border-gray-200">
                <Link 
                  href="/customers" 
                  className="flex items-center justify-center gap-2 text-[#0052CC] hover:text-[#0747A6] text-sm font-medium transition-colors"
                >
                  <span>Tüm Müşterileri Gör</span>
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </Link>
              </div>
            </div>
          </div>

          {/* How We Calculate Section */}
          <div className="bg-gradient-to-br from-[#6554C0]/5 via-[#0052CC]/5 to-transparent rounded-xl border border-gray-200 p-8 lg:p-10 shadow-sm mb-8">
            <div className="flex items-start gap-4 mb-8">
              <div className="w-14 h-14 bg-gradient-to-br from-[#6554C0] to-[#0052CC] rounded-xl flex items-center justify-center flex-shrink-0 shadow-lg">
                <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div className="flex-1">
                <h2 className="text-[#172B4D] text-2xl font-bold mb-2">Nasıl Hesaplıyoruz?</h2>
                <p className="text-[#5E6C84] text-sm leading-relaxed">AURA, gelişmiş makine öğrenmesi algoritmaları kullanarak müşteri kayıp riskini tahmin eder</p>
              </div>
            </div>

            {/* ML Pipeline Steps */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {/* Step 1 */}
              <div className="relative">
                <div className="bg-white rounded-lg p-6 border border-gray-200 hover:shadow-md transition-all h-full">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-8 h-8 bg-[#0052CC] rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-white text-sm font-bold">1</span>
                    </div>
                    <h3 className="text-[#172B4D] font-semibold text-sm">Veri Toplama</h3>
                  </div>
                  <p className="text-[#5E6C84] text-xs leading-relaxed">19 farklı müşteri özelliği analiz edilir: sözleşme tipi, ödeme yöntemi, hizmet kullanımı, demografik bilgiler</p>
                </div>
                {/* Arrow */}
                <div className="hidden lg:block absolute top-1/2 -right-3 transform -translate-y-1/2 z-10">
                  <svg className="w-6 h-6 text-[#0052CC]" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>

              {/* Step 2 */}
              <div className="relative">
                <div className="bg-white rounded-lg p-6 border border-gray-200 hover:shadow-md transition-all h-full">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-8 h-8 bg-[#00875A] rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-white text-sm font-bold">2</span>
                    </div>
                    <h3 className="text-[#172B4D] font-semibold text-sm">Ensemble Model</h3>
                  </div>
                  <p className="text-[#5E6C84] text-xs leading-relaxed">3 güçlü algoritma birlikte çalışır: Random Forest, Gradient Boosting, Logistic Regression (Voting Classifier)</p>
                </div>
                {/* Arrow */}
                <div className="hidden lg:block absolute top-1/2 -right-3 transform -translate-y-1/2 z-10">
                  <svg className="w-6 h-6 text-[#00875A]" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>

              {/* Step 3 */}
              <div className="relative">
                <div className="bg-white rounded-lg p-6 border border-gray-200 hover:shadow-md transition-all h-full">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-8 h-8 bg-[#FF991F] rounded-lg flex items-center justify-center flex-shrink-0">
                      <span className="text-white text-sm font-bold">3</span>
                    </div>
                    <h3 className="text-[#172B4D] font-semibold text-sm">SHAP Analizi</h3>
                  </div>
                  <p className="text-[#5E6C84] text-xs leading-relaxed">Her özelliğin risk skoruna etkisi hesaplanır. Hangi faktörlerin riski artırdığı açıklanır</p>
                </div>
                {/* Arrow */}
                <div className="hidden lg:block absolute top-1/2 -right-3 transform -translate-y-1/2 z-10">
                  <svg className="w-6 h-6 text-[#FF991F]" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>

              {/* Step 4 */}
              <div className="bg-white rounded-lg p-6 border border-gray-200 hover:shadow-md transition-all h-full">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-8 h-8 bg-[#6554C0] rounded-lg flex items-center justify-center flex-shrink-0">
                    <span className="text-white text-sm font-bold">4</span>
                  </div>
                  <h3 className="text-[#172B4D] font-semibold text-sm">Aksiyon Önerisi</h3>
                </div>
                <p className="text-[#5E6C84] text-xs leading-relaxed">AI, risk seviyesine göre özelleştirilmiş kampanya ve elde tutma stratejileri önerir</p>
              </div>
            </div>

            {/* Model Performance Metrics */}
            <div className="bg-white/50 rounded-lg p-6 border border-gray-200">
              <h3 className="text-[#172B4D] font-semibold text-sm mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-[#0052CC]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Model Performansı
              </h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-[#0052CC] text-2xl font-bold mb-1">82.4%</div>
                  <div className="text-[#5E6C84] text-xs">Doğruluk (Accuracy)</div>
                </div>
                <div className="text-center">
                  <div className="text-[#00875A] text-2xl font-bold mb-1">0.87</div>
                  <div className="text-[#5E6C84] text-xs">ROC-AUC Skoru</div>
                </div>
                <div className="text-center">
                  <div className="text-[#FF991F] text-2xl font-bold mb-1">78.5%</div>
                  <div className="text-[#5E6C84] text-xs">Precision</div>
                </div>
                <div className="text-center">
                  <div className="text-[#6554C0] text-2xl font-bold mb-1">81.2%</div>
                  <div className="text-[#5E6C84] text-xs">Recall</div>
                </div>
              </div>
            </div>

            {/* Key Features */}
            <div className="mt-6 pt-6 border-t border-gray-200">
              <h3 className="text-[#172B4D] font-semibold text-sm mb-4">Analiz Edilen Özellikler (19 Adet)</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
                {[
                  'Müşteri Süresi',
                  'Sözleşme Tipi',
                  'Aylık Ücret',
                  'Toplam Ücret',
                  'Ödeme Yöntemi',
                  'İnternet Hizmeti',
                  'Teknik Destek',
                  'Çevrimiçi Güvenlik',
                  'Çevrimiçi Yedekleme',
                  'Cihaz Koruma',
                  'Streaming TV',
                  'Streaming Film',
                  'Kağıtsız Fatura',
                  'Aile Durumu',
                  'Yaşlı Vatandaş',
                  'Telefon Hizmeti',
                  'Çoklu Hat',
                  'Cinsiyet',
                  'Partner Durumu'
                ].map((feature, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-xs">
                    <div className="w-1.5 h-1.5 rounded-full bg-[#0052CC] flex-shrink-0"></div>
                    <span className="text-[#5E6C84]">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Feature Cards - Jira Colors */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
            {/* Customer Analysis */}
            <Link href="/customers" className="group relative bg-gradient-to-br from-[#0052CC]/10 to-transparent rounded-lg border border-gray-200 p-8 hover:shadow-md hover:border-[#0052CC]/30 transition-all overflow-hidden">
              <div className="relative">
                <div className="w-14 h-14 bg-[#0052CC]/10 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <svg className="w-7 h-7 text-[#0052CC]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <h3 className="text-[#172B4D] font-semibold text-xl mb-3">Müşteri Analizi</h3>
                <p className="text-[#5E6C84] text-sm leading-relaxed mb-4">Detaylı müşteri risk analizi görüntüle</p>
                <div className="flex items-center gap-2 text-[#0052CC] text-sm font-medium">
                  <span>Analiz Et</span>
                  <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </Link>

            {/* Risk Calculator */}
            <Link href="/calculator" className="group relative bg-gradient-to-br from-[#00875A]/10 to-transparent rounded-lg border border-gray-200 p-8 hover:shadow-md hover:border-[#00875A]/30 transition-all overflow-hidden">
              <div className="relative">
                <div className="w-14 h-14 bg-[#00875A]/10 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <svg className="w-7 h-7 text-[#00875A]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                  </svg>
                </div>
                <h3 className="text-[#172B4D] font-semibold text-xl mb-3">Risk Hesapla</h3>
                <p className="text-[#5E6C84] text-sm leading-relaxed mb-4">Yeni müşteri profili için risk hesapla</p>
                <div className="flex items-center gap-2 text-[#00875A] text-sm font-medium">
                  <span>Hesapla</span>
                  <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </Link>

            {/* ROI Simulation */}
            <Link href="/simulation" className="group relative bg-gradient-to-br from-[#6554C0]/10 to-transparent rounded-lg border border-gray-200 p-8 hover:shadow-md hover:border-[#6554C0]/30 transition-all overflow-hidden">
              <div className="relative">
                <div className="w-14 h-14 bg-[#6554C0]/10 rounded-lg flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                  <svg className="w-7 h-7 text-[#6554C0]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-[#172B4D] font-semibold text-xl mb-3">ROI Simülasyonu</h3>
                <p className="text-[#5E6C84] text-sm leading-relaxed mb-4">Kampanya ROI'sini simüle et</p>
                <div className="flex items-center gap-2 text-[#6554C0] text-sm font-medium">
                  <span>Simüle Et</span>
                  <svg className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </Link>
          </div>
        </main>
      </div>
      </div>
    </TooltipProvider>
  );
}
