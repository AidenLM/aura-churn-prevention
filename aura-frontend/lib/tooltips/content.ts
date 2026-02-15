/**
 * Tooltip Content Store
 * 
 * Centralized storage for all tooltip content in the AURA system.
 * All content is in Turkish language with proper UTF-8 encoding.
 */

export interface TooltipContent {
  id: string;
  title: string;
  content: string;
  category: 'risk' | 'shap' | 'campaign' | 'metric' | 'field';
}

export const tooltipContent: Record<string, TooltipContent> = {
  // Risk Score Tooltips
  'risk-score': {
    id: 'risk-score',
    title: 'Risk Skoru',
    content: 'Risk skoru 0-100 arasında bir değerdir. Yüksek değerler müşterinin hizmeti bırakma olasılığının daha yüksek olduğunu gösterir. Skor, müşteri süresi, aylık ücret, sözleşme tipi gibi faktörler kullanılarak XGBoost makine öğrenmesi modeliyle hesaplanır. Model %91 doğruluk oranına sahiptir.',
    category: 'risk'
  },
  'risk-distribution': {
    id: 'risk-distribution',
    title: 'Risk Dağılımı',
    content: 'Müşterilerin risk seviyelerine göre dağılımını gösterir. Düşük risk (0-33): Sadık müşteriler, Orta risk (34-66): İzlenmesi gereken müşteriler, Yüksek risk (67-100): Acil müdahale gereken müşteriler. Bu dağılım, kaynak tahsisi ve kampanya planlaması için kritik öneme sahiptir.',
    category: 'risk'
  },
  'high-risk-count': {
    id: 'high-risk-count',
    title: 'Yüksek Riskli Müşteri Sayısı',
    content: 'Risk skoru 67 ve üzeri olan müşteri sayısını gösterir. Bu müşteriler öncelikli olarak elde tutma kampanyalarına dahil edilmelidir. Yüksek riskli müşterilere zamanında müdahale edilmesi, kayıp oranını önemli ölçüde azaltabilir.',
    category: 'risk'
  },

  // SHAP Value Tooltips
  'shap-values': {
    id: 'shap-values',
    title: 'SHAP Değerleri',
    content: 'SHAP (SHapley Additive exPlanations) değerleri, her faktörün risk skorunu ne kadar artırdığını veya azalttığını gösterir. Pozitif değerler (+) riski artıran faktörlerdir, negatif değerler (-) riski azaltan faktörlerdir. Örneğin: "Aylık sözleşme: +15" bu faktörün riski 15 puan artırdığı anlamına gelir. SHAP değerleri, hangi faktörlerin müşteri kaybına yol açtığını anlamak için kullanılır.',
    category: 'shap'
  },

  // Campaign Recommendation Tooltips
  'campaign-recommendation': {
    id: 'campaign-recommendation',
    title: 'Kampanya Önerisi',
    content: 'Kampanya önerileri, müşterinin risk faktörlerine göre yapay zeka tarafından otomatik olarak oluşturulur. Her öneri, müşterinin kayıp olasılığını azaltmak için özel olarak tasarlanmıştır ve beklenen etki yüzdesi ile birlikte sunulur. Öneriler, sözleşme yenileme, indirim, ek hizmet gibi stratejileri içerebilir.',
    category: 'campaign'
  },
  'ai-insights': {
    id: 'ai-insights',
    title: 'Yapay Zeka İçgörüleri',
    content: 'Yapay zeka modeli tarafından üretilen müşteri davranış analizi ve öngörüleri. Bu içgörüler, müşterinin geçmiş davranışlarını, hizmet kullanım paternlerini ve risk faktörlerini analiz ederek oluşturulur. Müşteri ile iletişim stratejisi geliştirmek için kullanılabilir.',
    category: 'campaign'
  },

  // Metric Tooltips - Dashboard
  'churn-rate': {
    id: 'churn-rate',
    title: 'Kayıp Oranı (Churn Rate)',
    content: 'Kayıp oranı, belirli bir dönemde hizmeti bırakan müşterilerin toplam müşteri sayısına oranıdır. Hesaplama: (Kaybedilen Müşteri Sayısı / Toplam Müşteri Sayısı) × 100. Örneğin %5 kayıp oranı, her 100 müşteriden 5\'inin hizmeti bıraktığı anlamına gelir. Düşük kayıp oranı, müşteri memnuniyetinin ve iş sağlığının göstergesidir.',
    category: 'metric'
  },
  'retention-rate': {
    id: 'retention-rate',
    title: 'Elde Tutma Oranı (Retention Rate)',
    content: 'Elde tutma oranı, belirli bir dönemde hizmete devam eden müşterilerin yüzdesidir. Hesaplama: (Devam Eden Müşteri / Toplam Müşteri) × 100. %95 elde tutma oranı, müşterilerin %95\'inin hizmete devam ettiği anlamına gelir. Yüksek elde tutma oranı, uzun vadeli gelir istikrarı sağlar.',
    category: 'metric'
  },
  'roi': {
    id: 'roi',
    title: 'Yatırım Getirisi (ROI)',
    content: 'ROI, kampanya maliyetlerine göre elde edilen finansal getiriyi gösterir. Hesaplama: (Kazanılan Gelir - Kampanya Maliyeti) / Kampanya Maliyeti × 100. Pozitif ROI kampanyanın karlı olduğunu, negatif ROI ise zarar ettiğini gösterir. Örneğin %150 ROI, her 1 TL harcama için 2.5 TL gelir elde edildiği anlamına gelir.',
    category: 'metric'
  },
  'total-customers': {
    id: 'total-customers',
    title: 'Toplam Müşteri Sayısı',
    content: 'Sistemde kayıtlı aktif müşterilerin toplam sayısı. Bu metrik, müşteri tabanının büyüklüğünü ve pazar payını gösterir. Müşteri sayısındaki değişimler, büyüme veya kayıp trendlerini anlamak için izlenir.',
    category: 'metric'
  },
  'monthly-revenue': {
    id: 'monthly-revenue',
    title: 'Aylık Gelir',
    content: 'Tüm aktif müşterilerden elde edilen toplam aylık gelir. Bu metrik, işletmenin finansal sağlığını ve gelir akışını gösterir. Aylık gelirdeki değişimler, müşteri kaybı veya fiyatlandırma stratejilerinin etkisini yansıtır.',
    category: 'metric'
  },

  // ROI Simulation Tooltips
  'projected-revenue': {
    id: 'projected-revenue',
    title: 'Öngörülen Gelir',
    content: 'Kampanya sonucunda elde tutulması beklenen müşterilerden gelecek tahmini gelir. Bu hesaplama, müşterilerin aylık ücretleri ve beklenen elde tutma süreleri dikkate alınarak yapılır. Kampanya etkinliğinin finansal değerini gösterir.',
    category: 'metric'
  },
  'campaign-cost': {
    id: 'campaign-cost',
    title: 'Kampanya Maliyeti',
    content: 'Elde tutma kampanyasının toplam maliyeti. İndirimler, promosyonlar, iletişim giderleri ve operasyonel maliyetleri içerir. ROI hesaplamasında kullanılan temel maliyet bileşenidir.',
    category: 'metric'
  },
  'customer-lifetime-value': {
    id: 'customer-lifetime-value',
    title: 'Müşteri Yaşam Boyu Değeri (CLV)',
    content: 'Bir müşterinin işletmeye sağlayacağı toplam tahmini gelir. Hesaplama: Aylık Gelir × Ortalama Müşteri Ömrü (ay). CLV, müşteri edinme ve elde tutma kampanyalarına ne kadar yatırım yapılabileceğini belirlemek için kullanılır.',
    category: 'metric'
  },

  // Calculator Input Field Tooltips
  'tenure': {
    id: 'tenure',
    title: 'Müşteri Süresi (Tenure)',
    content: 'Müşterinin hizmeti kullandığı toplam ay sayısı. Uzun süreli müşteriler (24+ ay) genellikle daha düşük kayıp riskine sahiptir çünkü hizmete alışmış ve bağlılık geliştirmişlerdir. Yeni müşteriler (0-12 ay) daha yüksek risk taşır.',
    category: 'field'
  },
  'contract-type': {
    id: 'contract-type',
    title: 'Sözleşme Tipi',
    content: 'Müşterinin sözleşme türü ve süresi. Aylık sözleşme: En yüksek risk (esneklik nedeniyle), 1 Yıllık: Orta risk, 2 Yıllık: En düşük risk (uzun vadeli taahhüt). Uzun süreli sözleşmeler müşteri bağlılığını artırır ve kayıp riskini azaltır.',
    category: 'field'
  },
  'monthly-charges': {
    id: 'monthly-charges',
    title: 'Aylık Ücret',
    content: 'Müşterinin aylık ödediği toplam tutar (TL). Yüksek ücretler kayıp riskini artırabilir, özellikle müşteri değer algısı düşükse veya alternatif daha ucuz seçenekler varsa. Fiyat-değer dengesi müşteri memnuniyeti için kritiktir.',
    category: 'field'
  },
  'total-charges': {
    id: 'total-charges',
    title: 'Toplam Ücret',
    content: 'Müşterinin hizmeti kullanmaya başladığından beri ödediği toplam tutar. Bu değer, müşterinin işletmeye sağladığı toplam geliri gösterir ve müşteri değerini anlamak için kullanılır.',
    category: 'field'
  },
  'payment-method': {
    id: 'payment-method',
    title: 'Ödeme Yöntemi',
    content: 'Müşterinin fatura ödeme şekli. Otomatik ödeme yöntemleri (banka transferi, kredi kartı) daha düşük kayıp riski ile ilişkilidir çünkü ödeme sürtünmesi azdır. Elektronik çek ve posta çeki gibi manuel yöntemler daha yüksek risk taşır.',
    category: 'field'
  },
  'paperless-billing': {
    id: 'paperless-billing',
    title: 'Kağıtsız Fatura',
    content: 'Müşterinin elektronik fatura kullanıp kullanmadığı. Kağıtsız fatura kullanan müşteriler genellikle daha teknoloji odaklı ve dijital hizmetlere daha bağlıdır, bu da düşük kayıp riski ile ilişkilendirilebilir.',
    category: 'field'
  },

  // Service-related Field Tooltips
  'phone-service': {
    id: 'phone-service',
    title: 'Telefon Hizmeti',
    content: 'Müşterinin telefon hizmeti kullanıp kullanmadığı. Telefon hizmeti, temel bir hizmet olup müşteri bağlılığını etkiler. Birden fazla hizmet kullanan müşteriler (paket hizmet) daha düşük kayıp riskine sahiptir.',
    category: 'field'
  },
  'multiple-lines': {
    id: 'multiple-lines',
    title: 'Çoklu Hat',
    content: 'Müşterinin birden fazla telefon hattı kullanıp kullanmadığı. Çoklu hat kullanımı, aile veya iş kullanımını gösterir ve müşteri bağlılığını artırır. Daha fazla hizmet, değiştirme maliyetini yükseltir.',
    category: 'field'
  },
  'internet-service': {
    id: 'internet-service',
    title: 'İnternet Hizmeti',
    content: 'Müşterinin kullandığı internet hizmet türü (DSL, Fiber optik, veya Yok). Fiber optik kullanıcıları genellikle daha yüksek ücret öder ancak daha iyi hizmet kalitesi alır. İnternet hizmeti olmayan müşteriler sadece telefon kullanıcısıdır.',
    category: 'field'
  },
  'online-security': {
    id: 'online-security',
    title: 'Çevrimiçi Güvenlik',
    content: 'Müşterinin çevrimiçi güvenlik hizmeti (antivirüs, firewall) kullanıp kullanmadığı. Ek hizmetler, müşteri bağlılığını artırır ve toplam değer algısını yükseltir. Daha fazla hizmet paketi, kayıp riskini azaltır.',
    category: 'field'
  },
  'online-backup': {
    id: 'online-backup',
    title: 'Çevrimiçi Yedekleme',
    content: 'Müşterinin çevrimiçi yedekleme hizmeti kullanıp kullanmadığı. Bu hizmet, müşterinin verilerini bulutta saklamasını sağlar. Ek hizmet kullanımı, müşteri bağlılığını ve değiştirme maliyetini artırır.',
    category: 'field'
  },
  'device-protection': {
    id: 'device-protection',
    title: 'Cihaz Koruma',
    content: 'Müşterinin cihaz koruma sigortası kullanıp kullanmadığı. Bu hizmet, telefon veya modem gibi cihazların hasar görmesi durumunda koruma sağlar. Ek hizmetler, müşteri memnuniyetini ve bağlılığını artırır.',
    category: 'field'
  },
  'tech-support': {
    id: 'tech-support',
    title: 'Teknik Destek',
    content: 'Müşterinin premium teknik destek hizmeti kullanıp kullanmadığı. Bu hizmet, 7/24 teknik yardım ve öncelikli destek sağlar. Teknik destek kullanan müşteriler, sorunlarını hızlı çözdükleri için daha memnun ve sadıktır.',
    category: 'field'
  },
  'streaming-tv': {
    id: 'streaming-tv',
    title: 'Streaming TV',
    content: 'Müşterinin internet üzerinden TV yayını hizmeti kullanıp kullanmadığı. Streaming hizmetleri, müşteri bağlılığını artıran ek değer sağlar. Birden fazla eğlence hizmeti, müşterinin platforma bağlılığını güçlendirir.',
    category: 'field'
  },
  'streaming-movies': {
    id: 'streaming-movies',
    title: 'Streaming Film',
    content: 'Müşterinin internet üzerinden film izleme hizmeti kullanıp kullanmadığı. Bu hizmet, eğlence içeriği sağlayarak müşteri memnuniyetini artırır. Daha fazla hizmet paketi, kayıp riskini azaltır.',
    category: 'field'
  },

  // Demographic Field Tooltips
  'gender': {
    id: 'gender',
    title: 'Cinsiyet',
    content: 'Müşterinin cinsiyeti. Bu demografik bilgi, kampanya segmentasyonu ve kişiselleştirme için kullanılabilir. Ancak cinsiyet tek başına kayıp riskinin güçlü bir göstergesi değildir.',
    category: 'field'
  },
  'senior-citizen': {
    id: 'senior-citizen',
    title: 'Yaşlı Vatandaş',
    content: 'Müşterinin 65 yaş ve üzeri olup olmadığı. Yaşlı müşteriler genellikle daha sadık ve değişime dirençlidir, ancak teknik destek ihtiyaçları daha fazla olabilir. Demografik segmentasyon için önemli bir faktördür.',
    category: 'field'
  },
  'partner': {
    id: 'partner',
    title: 'Eş/Partner',
    content: 'Müşterinin eşi veya partneri olup olmadığı. Aile bağları olan müşteriler genellikle daha istikrarlı ve uzun vadeli müşterilerdir. Aile paketleri ve çoklu hat kullanımı ile ilişkilidir.',
    category: 'field'
  },
  'dependents': {
    id: 'dependents',
    title: 'Bakmakla Yükümlü Olunan Kişiler',
    content: 'Müşterinin bakmakla yükümlü olduğu kişiler (çocuklar, yaşlı ebeveynler) olup olmadığı. Bakmakla yükümlü olunan kişileri olan müşteriler, aile ihtiyaçları nedeniyle daha fazla hizmet kullanır ve daha sadıktır.',
    category: 'field'
  },
};

/**
 * Get tooltip content by ID
 * Returns fallback content if ID not found
 */
export function getTooltipContent(id: string): TooltipContent {
  const content = tooltipContent[id];
  
  if (!content) {
    console.warn(`[Tooltip Warning] No content found for tooltip ID: ${id}`);
    return {
      id,
      title: 'Bilgi Eksik',
      content: 'Bu alan için açıklama henüz eklenmemiş.',
      category: 'field'
    };
  }
  
  return content;
}

/**
 * Get all tooltip IDs for a specific category
 */
export function getTooltipIdsByCategory(category: TooltipContent['category']): string[] {
  return Object.values(tooltipContent)
    .filter(tooltip => tooltip.category === category)
    .map(tooltip => tooltip.id);
}

/**
 * Validate that all required tooltip IDs exist
 */
export function validateTooltipIds(requiredIds: string[]): { valid: boolean; missing: string[] } {
  const missing = requiredIds.filter(id => !tooltipContent[id]);
  
  if (missing.length > 0) {
    console.warn(`[Tooltip Warning] Missing tooltip content for IDs: ${missing.join(', ')}`);
  }
  
  return {
    valid: missing.length === 0,
    missing
  };
}
