import { getDashboardSummary, formatNumber, formatPercentage } from '@/lib/api';
import Link from 'next/link';
import Image from 'next/image';

export default async function Home() {
  // Fetch real data from API
  const dashboardData = await getDashboardSummary();
  return (
    <div className="min-h-screen bg-[#0a0a1f] relative overflow-hidden">
      {/* Vaultflow-style gradient orbs */}
      <div className="absolute top-0 left-0 w-full h-full">
        <div className="absolute top-0 right-1/4 w-[800px] h-[800px] bg-gradient-to-br from-pink-500 to-purple-600 rounded-full opacity-20 blur-[150px] animate-[floatOrb_25s_ease-in-out_infinite]" />
        <div className="absolute top-1/3 left-1/4 w-[600px] h-[600px] bg-gradient-to-br from-purple-600 to-blue-600 rounded-full opacity-25 blur-[120px] animate-[floatOrb_20s_ease-in-out_infinite_reverse]" />
      </div>
      
      {/* Content */}
      <div className="relative z-10">
        {/* Navigation - Vaultflow style */}
        <nav className="flex items-center justify-between px-8 py-5 max-w-7xl mx-auto border-b border-white/5">
          <Link href="/" className="flex items-center gap-3">
            <Image src="/logo-transparent.png" alt="AURA Logo" width={280} height={112} className="h-28 w-auto" priority />
          </Link>
          <div className="hidden md:flex items-center gap-8 text-white/70 text-sm font-medium">
            <a href="#" className="hover:text-white transition">Özellikler</a>
            <a href="#" className="hover:text-white transition">Fiyatlandırma</a>
            <a href="#" className="hover:text-white transition">Blog</a>
            <a href="#" className="hover:text-white transition">Hakkımızda</a>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/dashboard" className="px-5 py-2.5 text-white text-sm font-medium hover:bg-white/5 rounded-full border border-white/10 transition">
              Dashboard
            </Link>
            <Link href="/dashboard" className="px-5 py-2.5 bg-white text-[#0a0a1f] text-sm font-medium rounded-full hover:bg-white/90 transition">
              Ücretsiz Dene
            </Link>
          </div>
        </nav>

        {/* Hero Section - Vaultflow style */}
        <div className="max-w-7xl mx-auto px-8 pt-24 pb-20">
          {/* Announcement Badge */}
          <div className="flex justify-center mb-12 animate-[fadeInUp_0.8s_ease-out]">
            <div className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-white/5 border border-white/10 text-white/80 text-sm backdrop-blur-sm">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
              Yeni • Yapay Zeka Destekli Müşteri Kayıp Önleme Sistemi
            </div>
          </div>

          {/* Main Heading */}
          <div className="text-center space-y-6 mb-16">
            <h1 className="text-6xl md:text-7xl lg:text-8xl font-bold text-white leading-[1.1] max-w-5xl mx-auto animate-[fadeInUp_0.8s_ease-out_0.1s] opacity-0 [animation-fill-mode:forwards]">
              Müşteri kaybını
              <br />
              <span className="text-white/40">önlemek artık çok kolay</span>
            </h1>

            {/* Subtitle */}
            <p className="text-lg md:text-xl text-white/50 max-w-2xl mx-auto leading-relaxed animate-[fadeInUp_0.8s_ease-out_0.2s] opacity-0 [animation-fill-mode:forwards]">
              XGBoost ve SHAP teknolojileriyle müşteri davranışlarını analiz edin. 
              Risk faktörlerini önceden tespit edin, akıllı kampanyalarla müşterilerinizi koruyun.
            </p>

            {/* CTA Buttons */}
            <div className="flex items-center justify-center gap-4 pt-4 animate-[fadeInUp_0.8s_ease-out_0.3s] opacity-0 [animation-fill-mode:forwards]">
              <Link href="/dashboard" className="px-8 py-4 bg-white text-[#0a0a1f] rounded-full font-medium hover:bg-white/90 transition hover:scale-105">
                Ücretsiz Deneyin
              </Link>
              <Link href="/dashboard" className="px-8 py-4 text-white rounded-full font-medium border border-white/10 hover:bg-white/5 transition">
                Demo İzleyin
              </Link>
            </div>
          </div>

          {/* Dashboard Mockup - Vaultflow style */}
          <div className="relative max-w-5xl mx-auto animate-[fadeInUp_1s_ease-out_0.4s] opacity-0 [animation-fill-mode:forwards]">
            {/* Glow effect */}
            <div className="absolute inset-0 bg-gradient-to-t from-purple-500/30 via-transparent to-transparent blur-3xl" />
            
            {/* Dashboard Container */}
            <div className="relative bg-gradient-to-br from-white/[0.07] to-white/[0.02] backdrop-blur-2xl rounded-3xl border border-white/10 p-1 shadow-2xl">
              {/* Inner Dashboard */}
              <div className="bg-[#0f0f23] rounded-2xl overflow-hidden">
                {/* Dashboard Header */}
                <div className="flex items-center justify-between px-6 py-4 border-b border-white/5">
                  <div className="flex items-center gap-4">
                    <button className="p-2 hover:bg-white/5 rounded-lg transition">
                      <div className="w-5 h-5 grid grid-cols-2 gap-0.5">
                        <div className="w-2 h-2 bg-white/40 rounded-sm" />
                        <div className="w-2 h-2 bg-white/40 rounded-sm" />
                        <div className="w-2 h-2 bg-white/40 rounded-sm" />
                        <div className="w-2 h-2 bg-white/40 rounded-sm" />
                      </div>
                    </button>
                    <div className="flex items-center gap-6 text-sm">
                      <a href="#" className="text-white font-medium border-b-2 border-purple-500 pb-4">Dashboard</a>
                      <a href="#" className="text-white/40 hover:text-white/70 transition">Dijital Takip</a>
                      <a href="#" className="text-white/40 hover:text-white/70 transition">Analitik</a>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-white/40 text-sm">May 2023</span>
                    <button className="p-2 hover:bg-white/5 rounded-lg transition">
                      <div className="w-4 h-4 border border-white/40 rounded" />
                    </button>
                  </div>
                </div>

                {/* Dashboard Content */}
                <div className="p-6">
                  <div className="grid grid-cols-12 gap-6">
                    {/* Left Sidebar */}
                    <div className="col-span-2 space-y-3">
                      <div className="w-10 h-10 bg-purple-500/20 rounded-xl flex items-center justify-center">
                        <div className="w-5 h-5 bg-purple-500 rounded-lg" />
                      </div>
                      <div className="w-10 h-10 bg-purple-500/10 rounded-xl flex items-center justify-center hover:bg-purple-500/20 transition cursor-pointer">
                        <div className="w-5 h-5 border-2 border-purple-400 rounded-lg" />
                      </div>
                      <div className="w-10 h-10 bg-pink-500/10 rounded-xl flex items-center justify-center hover:bg-pink-500/20 transition cursor-pointer">
                        <div className="w-5 h-5 border-2 border-pink-400 rounded-lg" />
                      </div>
                    </div>

                    {/* Main Content */}
                    <div className="col-span-7 space-y-6">
                      {/* Header */}
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <Image src="/logo-transparent.png" alt="AURA" width={160} height={64} className="h-16 w-auto" />
                          <div>
                            <div className="text-white/40 text-xs">Müşteri Risk Analizi</div>
                          </div>
                          <button className="ml-2 w-6 h-6 bg-white/5 hover:bg-white/10 rounded-lg flex items-center justify-center transition">
                            <span className="text-white/60 text-lg">+</span>
                          </button>
                        </div>
                      </div>

                      {/* Total Visits */}
                      <div>
                        <div className="flex items-center gap-2 mb-4">
                          <span className="text-white/50 text-sm">Toplam Müşteri Aktivitesi</span>
                          <div className="w-4 h-4 bg-white/5 rounded-full flex items-center justify-center">
                            <span className="text-white/40 text-xs">?</span>
                          </div>
                        </div>
                        
                        {/* Chart */}
                        <div className="relative h-64 bg-gradient-to-b from-purple-500/10 to-transparent rounded-2xl p-4">
                          {/* Tooltip */}
                          <div className="absolute top-8 left-1/2 -translate-x-1/2 bg-[#1a1a2e] border border-white/10 rounded-lg px-4 py-2 shadow-xl">
                            <div className="text-white/50 text-xs mb-1">Bu Ay</div>
                            <div className="text-white text-2xl font-bold">{formatNumber(dashboardData.total_customers)}</div>
                            <div className="text-white/40 text-xs">Aktif Müşteri</div>
                          </div>

                          {/* Chart Lines */}
                          <svg className="w-full h-full" viewBox="0 0 600 200">
                            {/* Grid lines */}
                            <line x1="0" y1="40" x2="600" y2="40" stroke="rgba(255,255,255,0.05)" strokeWidth="1" />
                            <line x1="0" y1="80" x2="600" y2="80" stroke="rgba(255,255,255,0.05)" strokeWidth="1" />
                            <line x1="0" y1="120" x2="600" y2="120" stroke="rgba(255,255,255,0.05)" strokeWidth="1" />
                            <line x1="0" y1="160" x2="600" y2="160" stroke="rgba(255,255,255,0.05)" strokeWidth="1" />
                            
                            {/* Main purple line */}
                            <path
                              d="M 0 150 Q 100 120, 200 100 T 400 80 T 600 90"
                              fill="none"
                              stroke="url(#purpleGradient)"
                              strokeWidth="3"
                              strokeLinecap="round"
                            />
                            
                            {/* Fill area */}
                            <path
                              d="M 0 150 Q 100 120, 200 100 T 400 80 T 600 90 L 600 200 L 0 200 Z"
                              fill="url(#purpleFill)"
                              opacity="0.3"
                            />
                            
                            {/* Dot indicator */}
                            <circle cx="300" cy="90" r="6" fill="white" />
                            <circle cx="300" cy="90" r="3" fill="#8b5cf6" />
                            
                            <defs>
                              <linearGradient id="purpleGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stopColor="#8b5cf6" />
                                <stop offset="100%" stopColor="#6366f1" />
                              </linearGradient>
                              <linearGradient id="purpleFill" x1="0%" y1="0%" x2="0%" y2="100%">
                                <stop offset="0%" stopColor="#8b5cf6" stopOpacity="0.4" />
                                <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0" />
                              </linearGradient>
                            </defs>
                          </svg>
                        </div>
                      </div>
                    </div>

                    {/* Right Sidebar */}
                    <div className="col-span-3 space-y-4">
                      {/* Stats */}
                      <div className="space-y-3">
                        <div className="text-white/50 text-xs">Risk Dağılımı</div>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span className="text-white/60 text-xs">Düşük Risk</span>
                            <div className="flex-1 mx-2 h-1 bg-white/5 rounded-full overflow-hidden">
                              <div className="h-full bg-green-500 rounded-full" style={{width: `${(dashboardData.risk_distribution.low / dashboardData.total_customers * 100)}%`}} />
                            </div>
                            <span className="text-white/40 text-xs">{dashboardData.risk_distribution.low}</span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-white/60 text-xs">Orta Risk</span>
                            <div className="flex-1 mx-2 h-1 bg-white/5 rounded-full overflow-hidden">
                              <div className="h-full bg-yellow-500 rounded-full" style={{width: `${(dashboardData.risk_distribution.medium / dashboardData.total_customers * 100)}%`}} />
                            </div>
                            <span className="text-white/40 text-xs">{dashboardData.risk_distribution.medium}</span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span className="text-white/60 text-xs">Yüksek Risk</span>
                            <div className="flex-1 mx-2 h-1 bg-white/5 rounded-full overflow-hidden">
                              <div className="h-full bg-red-500 rounded-full" style={{width: `${(dashboardData.risk_distribution.high / dashboardData.total_customers * 100)}%`}} />
                            </div>
                            <span className="text-white/40 text-xs">{dashboardData.risk_distribution.high}</span>
                          </div>
                        </div>
                      </div>

                      {/* Circular Progress */}
                      <div className="bg-gradient-to-br from-purple-500/10 to-transparent rounded-2xl p-6 flex flex-col items-center justify-center">
                        <div className="text-white/50 text-xs mb-3">Kayıp Riski</div>
                        <div className="relative w-24 h-24">
                          <svg className="w-full h-full -rotate-90">
                            <circle cx="48" cy="48" r="40" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="8" />
                            <circle cx="48" cy="48" r="40" fill="none" stroke="url(#circleGradient)" strokeWidth="8" strokeDasharray="251" strokeDashoffset={251 - (251 * dashboardData.monthly_churn_rate / 100)} strokeLinecap="round" />
                            <defs>
                              <linearGradient id="circleGradient">
                                <stop offset="0%" stopColor="#ef4444" />
                                <stop offset="100%" stopColor="#f97316" />
                              </linearGradient>
                            </defs>
                          </svg>
                          <div className="absolute inset-0 flex items-center justify-center">
                            <span className="text-white font-bold text-xl">{formatPercentage(dashboardData.monthly_churn_rate)}</span>
                          </div>
                        </div>
                        <div className="text-white/40 text-xs mt-2">{formatNumber(dashboardData.high_risk_count)} Müşteri</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Social Proof */}
          <div className="text-center mt-20 space-y-8 animate-[fadeInUp_1s_ease-out_0.6s] opacity-0 [animation-fill-mode:forwards]">
            <p className="text-white/40 text-sm">
              Türkiye'nin önde gelen telekom şirketleri tarafından güvenilir
            </p>
            <div className="flex items-center justify-center gap-12 flex-wrap opacity-40">
              <div className="text-white font-bold text-xl">TURKCELL</div>
              <div className="text-white font-bold text-xl">VODAFONE</div>
              <div className="text-white font-bold text-xl">TÜRK TELEKOM</div>
              <div className="text-white font-bold text-xl">SUPERONLINE</div>
              <div className="text-white font-bold text-xl">MILLENICOM</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
