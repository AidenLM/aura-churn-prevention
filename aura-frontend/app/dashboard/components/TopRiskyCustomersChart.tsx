'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import Link from 'next/link';

interface Customer {
  customer_id: string;
  name: string;
  risk_score: number;
  risk_level: string;
}

interface TopRiskyCustomersChartProps {
  customers: Customer[];
}

export default function TopRiskyCustomersChart({ customers }: TopRiskyCustomersChartProps) {
  const chartData = customers.slice(0, 5).map(customer => ({
    name: customer.name.split(' ')[0], // First name only for chart
    fullName: customer.name,
    score: customer.risk_score * 100,
    customerId: customer.customer_id,
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border border-gray-200 rounded-lg shadow-lg p-3">
          <p className="text-[#172B4D] text-sm font-semibold">{payload[0].payload.fullName}</p>
          <p className="text-[#DE350B] text-xs mt-1 font-bold">
            Risk: {payload[0].value.toFixed(1)}%
          </p>
        </div>
      );
    }
    return null;
  };

  const getBarColor = (score: number) => {
    if (score >= 70) return '#DE350B'; // High risk - red
    if (score >= 30) return '#FF991F'; // Medium risk - orange
    return '#00875A'; // Low risk - green
  };

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart 
        data={chartData} 
        layout="vertical"
        margin={{ top: 10, right: 30, left: 80, bottom: 10 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" horizontal={false} />
        <XAxis 
          type="number" 
          domain={[0, 100]}
          tick={{ fill: '#5E6C84', fontSize: 12 }}
          axisLine={{ stroke: '#E5E7EB' }}
        />
        <YAxis 
          type="category" 
          dataKey="name"
          tick={{ fill: '#172B4D', fontSize: 12, fontWeight: 500 }}
          axisLine={{ stroke: '#E5E7EB' }}
        />
        <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0, 82, 204, 0.05)' }} />
        <Bar dataKey="score" radius={[0, 8, 8, 0]} maxBarSize={30}>
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={getBarColor(entry.score)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
