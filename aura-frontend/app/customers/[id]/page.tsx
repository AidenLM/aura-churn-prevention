import { getCustomerById, formatCurrency } from '@/lib/api';
import Link from 'next/link';
import { TooltipProvider, Tooltip } from '@/components/ui/tooltip';
import { Info } from 'lucide-react';

export default async function CustomerDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const customer = await getCustomerById(id);
  
  // Risk level colors (Jira style)
  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high': return { bg: 'bg-[#FFEBE6]', text: 'text-[#DE350B]', border: 'border-[#DE350B]' };
      case 'medium': return { bg: 'bg-[#FFF0B3]', text: 'text-[#FF991F]', border: 'border-[#FF991F]' };
      case 'low': return { bg: 'bg-[#E3FCEF]', text: 'text-[#00875A]', border: 'border-[#00875A]' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-600', border: 'border-gray-300' };
    }
  };

  const riskColors = getRiskColor(customer.risk_level);
  
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
              <h1 className="text-[#172B4D] text-2xl font-bold">Müşteri Detayı</h1>
              <p className="text-[#5E6C84] text-sm">Risk analizi ve öneriler</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button className="px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 text-[#172B4D] text-sm font-medium transition-colors">
              Rapor İndir
            </button>
            <button className="px-4 py-2 rounded-lg bg-[#0052CC] hover:bg-[#0747A6] text-white text-sm font-medium transition-colors shadow-sm">
              Kampanya Gönder
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 lg:px-8 py-6 lg:py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6">
          {/* Left Column - Customer Info */}
          <div className="lg:col-span-2 space-y-6">
            {/* Customer Header Card */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="flex items-start gap-6">
                <div className="w-20 h-20 bg-gradient-to-br from-[#0052CC] to-[#0065FF] rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-white text-2xl font-bold">{customer.customer_id.charAt(0)}</span>
                </div>
                <div className="flex-1">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h2 className="text-[#172B4D] text-2xl font-bold mb-1">Müşteri {customer.customer_id}</h2>
                      <p className="text-[#5E6C84] text-sm">ID: {customer.customer_id}</p>
                    </div>
                    <span className={`px-4 py-2 rounded-lg ${riskColors.bg} ${riskColors.text} border ${riskColors.border} text-sm font-semibold`}>
                      {customer.risk_level} Risk
                    </span>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-[#5E6C84] text-xs mb-1">Sözleşme Tipi</p>
                      <p className="text-[#172B4D] text-sm font-medium">{customer.contract_type}</p>
                    </div>
                    <div>
                      <p className="text-[#5E6C84] text-xs mb-1">İnternet Hizmeti</p>
                      <p className="text-[#172B4D] text-sm font-medium">{customer.plan_type}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                <div className="flex items-center gap-2 mb-2">
                  <p className="text-[#5E6C84] text-xs uppercase tracking-wider">Risk Skoru</p>
                  <Tooltip id="risk-score" side="right">
                    <Info className="w-3.5 h-3.5 text-gray-400" />
                  </Tooltip>
                </div>
                <p className="text-[#172B4D] text-3xl font-bold mb-1">{(customer.risk_score * 100).toFixed(0)}%</p>
                <div className="w-full h-2 bg-gray-100 rounded-full overflow-hidden mt-3">
                  <div 
                    className={`h-full ${customer.risk_level.toLowerCase() === 'high' ? 'bg-[#DE350B]' : customer.risk_level.toLowerCase() === 'medium' ? 'bg-[#FF991F]' : 'bg-[#00875A]'} rounded-full transition-all`}
                    style={{width: `${customer.risk_score * 100}%`}}
                  />
                </div>
              </div>

              <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                <p className="text-[#5E6C84] text-xs uppercase tracking-wider mb-2">Müşteri Süresi</p>
                <p className="text-[#172B4D] text-3xl font-bold mb-1">{customer.tenure}</p>
                <p className="text-[#5E6C84] text-sm">ay</p>
              </div>

              <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                <p className="text-[#5E6C84] text-xs uppercase tracking-wider mb-2">Aylık Ücret</p>
                <p className="text-[#172B4D] text-3xl font-bold mb-1">{formatCurrency(customer.monthly_charge)}</p>
                <p className="text-[#5E6C84] text-sm">{customer.plan_type}</p>
              </div>
            </div>

            {/* AI Insights */}
            <div className="bg-gradient-to-br from-[#6554C0]/10 to-transparent rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="flex items-start gap-4 mb-6">
                <div className="w-12 h-12 bg-[#6554C0]/10 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-6 h-6 text-[#6554C0]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-3">
                    <h3 className="text-[#172B4D] text-lg font-semibold">AI Analizi</h3>
                    <Tooltip id="ai-insights" side="right">
                      <Info className="w-4 h-4 text-gray-400" />
                    </Tooltip>
                  </div>
                  
                  {(() => {
                    const sections = customer.ai_insights.split('|||');
                    const riskAssessment = sections[0] || '';
                    const mlFeatures = sections[1] || '';
                    const keyFactors = sections[2] || '';
                    const actions = sections[3] || '';
                    
                    return (
                      <div className="space-y-4">
                        {/* Risk Assessment */}
                        {riskAssessment && (
                          <div className="bg-white/50 rounded-lg p-4 border border-gray-100">
                            <p className="text-[#172B4D] text-sm font-medium leading-relaxed">{riskAssessment}</p>
                          </div>
                        )}
                        
                        {/* ML Model Features */}
                        {mlFeatures && (
                          <div className="bg-gradient-to-r from-[#6554C0]/5 to-transparent rounded-lg p-4 border border-[#6554C0]/20">
                            <div className="flex items-center gap-2 mb-2">
                              <svg className="w-4 h-4 text-[#6554C0]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                              </svg>
                              <span className="text-[#6554C0] text-xs font-semibold uppercase tracking-wider">Makine Öğrenmesi Analizi</span>
                            </div>
                            <p className="text-[#172B4D] text-sm leading-relaxed">{mlFeatures}</p>
                          </div>
                        )}
                        
                        {/* Key Factors */}
                        {keyFactors && (
                          <div className="bg-white/50 rounded-lg p-4 border border-gray-100">
                            <p className="text-[#5E6C84] text-sm leading-relaxed">{keyFactors}</p>
                          </div>
                        )}
                        
                        {/* Recommended Actions */}
                        {actions && (
                          <div className="bg-gradient-to-r from-[#0052CC]/5 to-transparent rounded-lg p-4 border border-[#0052CC]/20">
                            <h4 className="text-[#0052CC] text-xs font-semibold uppercase tracking-wider mb-3">Önerilen Aksiyonlar</h4>
                            <div className="grid grid-cols-1 gap-2">
                              {actions.split('|').filter(a => a.trim()).map((action, idx) => {
                                if (idx % 2 === 0) {
                                  const title = action.trim();
                                  const desc = actions.split('|')[idx + 1]?.trim();
                                  return (
                                    <div key={idx} className="flex items-start gap-2">
                                      <div className="w-1.5 h-1.5 rounded-full bg-[#0052CC] mt-1.5 flex-shrink-0"></div>
                                      <div className="flex-1">
                                        <span className="text-[#172B4D] text-sm font-semibold">{title}:</span>
                                        <span className="text-[#5E6C84] text-sm ml-1">{desc}</span>
                                      </div>
                                    </div>
                                  );
                                }
                                return null;
                              })}
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })()}
                </div>
              </div>
            </div>

            {/* SHAP Feature Importance */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="flex items-center gap-2 mb-6">
                <h3 className="text-[#172B4D] text-lg font-semibold">Risk Faktörleri (SHAP Analizi)</h3>
                <Tooltip id="shap-values" side="right">
                  <Info className="w-4 h-4 text-gray-400" />
                </Tooltip>
              </div>
              <p className="text-[#5E6C84] text-xs mb-4">Her faktörün risk skoruna etkisi ve gerçek değerler</p>
              <div className="space-y-4">
                {(() => {
                  const topFeatures = customer.shap_values.slice(0, 8);
                  const maxImportance = Math.max(...topFeatures.map(f => Math.abs(f.importance)));
                  
                  // Map feature names to actual values
                  const getActualValue = (featureName: string) => {
                    switch(featureName) {
                      case 'tenure': return `${customer.tenure} ay`;
                      case 'contract': return customer.contract_type;
                      case 'monthly_charges': return formatCurrency(customer.monthly_charge);
                      case 'total_charges': return formatCurrency(customer.monthly_charge * customer.tenure);
                      case 'payment_method': return customer.contract_type;
                      case 'internet_service': return customer.plan_type;
                      case 'tech_support': return '';
                      case 'online_security': return '';
                      case 'online_backup': return '';
                      case 'device_protection': return '';
                      case 'streaming_tv': return '';
                      case 'streaming_movies': return '';
                      case 'paperless_billing': return '';
                      case 'family_status': return '';
                      case 'senior_citizen': return '';
                      case 'phone_service': return '';
                      case 'multiple_lines': return '';
                      case 'gender': return '';
                      case 'partner': return '';
                      default: return '';
                    }
                  };
                  
                  return topFeatures.map((feature, index) => {
                    const normalizedWidth = (Math.abs(feature.importance) / maxImportance) * 50;
                    const impactLabel = feature.direction === 'positive' ? 'Riski Artırıyor' : 'Riski Azaltıyor';
                    const actualValue = getActualValue(feature.feature_name);
                    
                    return (
                      <div key={index}>
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex-1">
                            <span className="text-[#172B4D] text-sm font-medium">{feature.display_name_tr}</span>
                            {actualValue && (
                              <span className="ml-2 text-[#5E6C84] text-xs font-semibold">
                                {actualValue}
                              </span>
                            )}
                            <span className={`ml-2 text-xs ${feature.direction === 'positive' ? 'text-[#DE350B]' : 'text-[#00875A]'}`}>
                              ({impactLabel})
                            </span>
                          </div>
                          <span className={`text-xs font-semibold ${feature.direction === 'positive' ? 'text-[#DE350B]' : 'text-[#00875A]'} ml-2`}>
                            {feature.direction === 'positive' ? '↑' : '↓'} {Math.abs(feature.importance).toFixed(2)}
                          </span>
                        </div>
                        <div className="relative w-full h-8 bg-gray-100 rounded-lg overflow-hidden">
                          <div 
                            className={`absolute h-full ${feature.direction === 'positive' ? 'bg-[#DE350B]' : 'bg-[#00875A]'} transition-all`}
                            style={{
                              width: `${normalizedWidth}%`,
                              left: feature.direction === 'positive' ? '50%' : 'auto',
                              right: feature.direction === 'negative' ? '50%' : 'auto'
                            }}
                          />
                          <div className="absolute inset-0 flex items-center justify-center">
                            <div className="w-0.5 h-full bg-gray-300"></div>
                          </div>
                        </div>
                      </div>
                    );
                  });
                })()}
              </div>
            </div>
          </div>

          {/* Right Column - Recommended Offer */}
          <div className="space-y-6">
            {customer.recommended_offer && (
              <div className="bg-gradient-to-br from-[#00875A]/10 to-transparent rounded-lg border border-[#00875A]/30 p-8 shadow-sm">
                <div className="flex items-center gap-3 mb-6">
                  <div className="w-12 h-12 bg-[#00875A]/10 rounded-lg flex items-center justify-center">
                    <svg className="w-6 h-6 text-[#00875A]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7" />
                    </svg>
                  </div>
                  <h3 className="text-[#172B4D] text-lg font-semibold">Önerilen Kampanya</h3>
                  <Tooltip id="campaign-recommendation" side="right">
                    <Info className="w-4 h-4 text-gray-400" />
                  </Tooltip>
                </div>

                <div className="space-y-4">
                  <div>
                    <h4 className="text-[#172B4D] text-xl font-bold mb-2">{customer.recommended_offer.campaign_name}</h4>
                    <p className="text-[#5E6C84] text-sm leading-relaxed">{customer.recommended_offer.rationale}</p>
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
                    <div>
                      <p className="text-[#5E6C84] text-xs mb-1">İndirim</p>
                      <p className="text-[#172B4D] text-2xl font-bold">%{customer.recommended_offer.discount_percentage}</p>
                    </div>
                    <div>
                      <p className="text-[#5E6C84] text-xs mb-1">Süre</p>
                      <p className="text-[#172B4D] text-2xl font-bold">{customer.recommended_offer.duration_months} ay</p>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-gray-200">
                    <p className="text-[#5E6C84] text-xs mb-1">Tahmini Maliyet</p>
                    <p className="text-[#172B4D] text-2xl font-bold">{formatCurrency(customer.recommended_offer.estimated_cost)}</p>
                  </div>

                  <button className="w-full px-4 py-3 rounded-lg bg-[#00875A] hover:bg-[#006644] text-white text-sm font-medium transition-colors shadow-sm mt-4">
                    Kampanyayı Uygula
                  </button>
                </div>
              </div>
            )}

            {/* Quick Actions */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
              <h3 className="text-[#172B4D] text-sm font-semibold mb-4">Hızlı İşlemler</h3>
              <div className="space-y-2">
                <button className="w-full px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 text-[#172B4D] text-sm font-medium transition-colors text-left flex items-center gap-3">
                  <svg className="w-5 h-5 text-[#5E6C84]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span>Email Gönder</span>
                </button>
                <button className="w-full px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 text-[#172B4D] text-sm font-medium transition-colors text-left flex items-center gap-3">
                  <svg className="w-5 h-5 text-[#5E6C84]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  <span>Ara</span>
                </button>
                <button className="w-full px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 text-[#172B4D] text-sm font-medium transition-colors text-left flex items-center gap-3">
                  <svg className="w-5 h-5 text-[#5E6C84]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span>Not Ekle</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
    </TooltipProvider>
  );
}
