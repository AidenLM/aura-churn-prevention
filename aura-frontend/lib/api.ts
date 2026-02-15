/**
 * API client for AURA backend - TrustedModel
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface DashboardSummary {
  total_customers: number;
  high_risk_count: number;
  average_risk: number;
  monthly_churn_rate: number;
  risk_distribution: {
    low: number;
    medium: number;
    high: number;
  };
  top_risky_customers: Array<{
    customer_id: string;
    name: string;
    risk_score: number;
    risk_level: string;
  }>;
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/dashboard/summary`, {
      cache: 'no-store', // Always fetch fresh data
    });
    
    if (!response.ok) {
      throw new Error('Dashboard verisi alınamadı');
    }
    
    return response.json();
  } catch (error) {
    // Fallback to mock data if API is not available
    console.warn('API not available, using mock data:', error);
    return {
      total_customers: 7043,
      high_risk_count: 0,
      average_risk: 0.18,
      monthly_churn_rate: 7.9,
      risk_distribution: {
        low: 1,
        medium: 0,
        high: 0
      },
      top_risky_customers: []
    };
  }
}

export function formatNumber(num: number): string {
  return new Intl.NumberFormat('tr-TR').format(num);
}

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('tr-TR', {
    style: 'currency',
    currency: 'TRY',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatPercentage(value: number): string {
  return `%${value.toFixed(1)}`;
}

// Customer Detail Types - TrustedModel
export interface CustomerDetail {
  customer_id: string;
  name: string;
  email: string | null;
  phone: string | null;
  plan_type: string;  // internet_service
  monthly_charge: number;
  tenure: number;
  risk_score: number;
  risk_level: string;
  ai_insights: string;
  shap_values: Array<{
    feature_name: string;
    importance: number;
    direction: string;
    display_name_tr: string;
  }>;
  recommended_offer?: {
    campaign_name: string;
    discount_percentage: number;
    duration_months: number;
    estimated_cost: number;
    rationale: string;
  };
  // TrustedModel metrics (not available in dataset)
  complaint_count: number;
  support_calls_count: number;
  payment_delays: number;
  data_usage_gb: number;
  voice_minutes: number;
  contract_type: string;
}

export async function getCustomerById(customerId: string): Promise<CustomerDetail> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/customers/${customerId}`, {
      cache: 'no-store',
    });
    
    if (!response.ok) {
      throw new Error('Müşteri verisi alınamadı');
    }
    
    return response.json();
  } catch (error) {
    console.error('Error fetching customer:', error);
    throw error;
  }
}

export async function getRandomCustomer(): Promise<CustomerDetail> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/customers/random/get`, {
      cache: 'no-store',
    });
    
    if (!response.ok) {
      throw new Error('Rastgele müşteri alınamadı');
    }
    
    return response.json();
  } catch (error) {
    console.error('Error fetching random customer:', error);
    throw error;
  }
}

// Risk Calculation Types - TrustedModel (19 features)
export interface RiskCalculationInput {
  // Demographic (4)
  gender: string;  // Male, Female
  senior_citizen: number;  // 0 or 1
  partner: string;  // Yes, No
  dependents: string;  // Yes, No
  
  // Account (5)
  tenure: number;  // months
  contract: string;  // Month-to-month, One year, Two year
  paperless_billing: string;  // Yes, No
  payment_method: string;  // Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic)
  monthly_charges: number;
  total_charges: number;
  
  // Phone Services (2)
  phone_service: string;  // Yes, No
  multiple_lines: string;  // Yes, No, No phone service
  
  // Internet Services (7)
  internet_service: string;  // DSL, Fiber optic, No
  online_security: string;  // Yes, No, No internet service
  online_backup: string;  // Yes, No, No internet service
  device_protection: string;  // Yes, No, No internet service
  tech_support: string;  // Yes, No, No internet service
  streaming_tv: string;  // Yes, No, No internet service
  streaming_movies: string;  // Yes, No, No internet service
}

export interface RiskCalculationResult {
  risk_score: number;
  risk_level: string;
  shap_values: Array<{
    feature_name: string;
    importance: number;
    direction: string;
    display_name_tr: string;
  }>;
  ai_analysis: string;
  recommended_offer?: {
    campaign_name: string;
    discount_percentage: number;
    duration_months: number;
    estimated_cost: number;
    rationale: string;
  };
}

export async function calculateRisk(input: RiskCalculationInput): Promise<RiskCalculationResult> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/predict/calculate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(input),
      cache: 'no-store',
    });
    
    if (!response.ok) {
      throw new Error('Risk hesaplanamadı');
    }
    
    return response.json();
  } catch (error) {
    console.error('Error calculating risk:', error);
    throw error;
  }
}

// ROI Simulation Types
export interface SimulationInput {
  risk_threshold: number;
  campaign_budget: number;
}

export interface SimulationResult {
  targeted_customers: number;
  cost_per_customer: number;
  total_cost: number;
  expected_retention_rate: number;
  projected_revenue: number;
  roi: number;
  net_gain: number;
  coverage_percentage: number;
}

export async function simulateROI(input: SimulationInput): Promise<SimulationResult> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/simulation/roi`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(input),
      cache: 'no-store',
    });
    
    if (!response.ok) {
      throw new Error('ROI simülasyonu çalıştırılamadı');
    }
    
    return response.json();
  } catch (error) {
    console.error('Error simulating ROI:', error);
    throw error;
  }
}


// All Customers Types
export interface AllCustomersResponse {
  customers: Array<{
    customer_id: string;
    name: string;
    email: string | null;
    plan_type: string;
    monthly_charge: number;
    tenure: number;
    risk_score: number;
    risk_level: string;
  }>;
  total: number;
  page: number;
  page_size: number;
}

export async function getAllCustomers(page: number = 1, pageSize: number = 50): Promise<AllCustomersResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/customers/all/list?page=${page}&page_size=${pageSize}`, {
      cache: 'no-store',
    });
    
    if (!response.ok) {
      throw new Error('Müşteri listesi alınamadı');
    }
    
    return response.json();
  } catch (error) {
    console.error('Error fetching all customers:', error);
    throw error;
  }
}
