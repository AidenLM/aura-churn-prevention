/**
 * Tooltip System - Main Export
 * 
 * Exports all tooltip-related types, content, and utilities
 */

export { tooltipContent, getTooltipContent, getTooltipIdsByCategory, validateTooltipIds } from './content';
export type { TooltipContent } from './content';

// Page-specific tooltip ID mappings
export const dashboardTooltips = {
  riskDistribution: 'risk-distribution',
  churnRate: 'churn-rate',
  totalCustomers: 'total-customers',
  highRiskCount: 'high-risk-count',
  monthlyRevenue: 'monthly-revenue'
} as const;

export const customerDetailTooltips = {
  riskScore: 'risk-score',
  shapValues: 'shap-values',
  aiInsights: 'ai-insights',
  campaignRecommendations: 'campaign-recommendation'
} as const;

export const calculatorTooltips = {
  // Customer demographics
  gender: 'gender',
  seniorCitizen: 'senior-citizen',
  partner: 'partner',
  dependents: 'dependents',
  
  // Account information
  tenure: 'tenure',
  contractType: 'contract-type',
  monthlyCharges: 'monthly-charges',
  totalCharges: 'total-charges',
  paymentMethod: 'payment-method',
  paperlessBilling: 'paperless-billing',
  
  // Services
  phoneService: 'phone-service',
  multipleLines: 'multiple-lines',
  internetService: 'internet-service',
  onlineSecurity: 'online-security',
  onlineBackup: 'online-backup',
  deviceProtection: 'device-protection',
  techSupport: 'tech-support',
  streamingTV: 'streaming-tv',
  streamingMovies: 'streaming-movies',
  
  // Results
  resultRiskScore: 'risk-score',
  resultShapAnalysis: 'shap-values'
} as const;

export const simulationTooltips = {
  roi: 'roi',
  retentionRate: 'retention-rate',
  projectedRevenue: 'projected-revenue',
  campaignCost: 'campaign-cost',
  customerLifetimeValue: 'customer-lifetime-value'
} as const;
