import Link from 'next/link';
import { getAllCustomers, formatCurrency } from '@/lib/api';

export default async function CustomersPage() {
  const data = await getAllCustomers(1, 50);
  
  const getRiskColor = (level: string) => {
    switch (level?.toLowerCase()) {
      case 'high': return { bg: 'bg-[#FFEBE6]', text: 'text-[#DE350B]', border: 'border-[#DE350B]' };
      case 'medium': return { bg: 'bg-[#FFF0B3]', text: 'text-[#FF991F]', border: 'border-[#FF991F]' };
      case 'low': return { bg: 'bg-[#E3FCEF]', text: 'text-[#00875A]', border: 'border-[#00875A]' };
      default: return { bg: 'bg-gray-100', text: 'text-gray-600', border: 'border-gray-300' };
    }
  };
  
  return (
    <div className="min-h-screen bg-[#F4F5F7]">
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 lg:px-8 py-4 lg:py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/dashboard" className="text-[#5E6C84] hover:text-[#172B4D] transition-colors">
                <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </Link>
              <div>
                <h1 className="text-[#172B4D] text-2xl font-bold">Müşteriler</h1>
                <p className="text-[#5E6C84] text-sm">{data.total} müşteri</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 lg:px-8 py-8">
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#5E6C84] uppercase tracking-wider">Müşteri</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#5E6C84] uppercase tracking-wider">Plan</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#5E6C84] uppercase tracking-wider">Aylık Ücret</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#5E6C84] uppercase tracking-wider">Süre</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#5E6C84] uppercase tracking-wider">Risk</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-[#5E6C84] uppercase tracking-wider"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {data.customers.map((customer) => {
                  const colors = getRiskColor(customer.risk_level);
                  return (
                    <tr key={customer.customer_id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4">
                        <div>
                          <div className="text-[#172B4D] text-sm font-medium">{customer.name}</div>
                          <div className="text-[#5E6C84] text-xs">{customer.email}</div>
                        </div>
                      </td>
                      <td className="px-6 py-4 text-[#172B4D] text-sm">{customer.plan_type}</td>
                      <td className="px-6 py-4 text-[#172B4D] text-sm font-medium">{formatCurrency(customer.monthly_charge)}</td>
                      <td className="px-6 py-4 text-[#5E6C84] text-sm">{customer.tenure} ay</td>
                      <td className="px-6 py-4">
                        <span className={`inline-flex px-3 py-1 rounded-full text-xs font-semibold ${colors.bg} ${colors.text} ${colors.border} border`}>
                          {customer.risk_level} ({(customer.risk_score * 100).toFixed(0)}%)
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <Link 
                          href={`/customers/${customer.customer_id}`}
                          className="text-[#0052CC] hover:text-[#0747A6] text-sm font-medium transition-colors"
                        >
                          Detay →
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  );
}
