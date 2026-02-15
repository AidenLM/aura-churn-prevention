'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface RiskDistributionChartProps {
  data: {
    low: number;
    medium: number;
    high: number;
  };
}

export default function RiskDistributionChart({ data }: RiskDistributionChartProps) {
  const chartData = [
    { name: 'Düşük Risk', value: data.low, color: '#00875A' },
    { name: 'Orta Risk', value: data.medium, color: '#FF991F' },
    { name: 'Yüksek Risk', value: data.high, color: '#DE350B' },
  ];

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border border-gray-200 rounded-lg shadow-lg p-3">
          <p className="text-[#172B4D] text-sm font-semibold">{payload[0].payload.name}</p>
          <p className="text-[#5E6C84] text-xs mt-1">
            {payload[0].value} müşteri
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" vertical={false} />
        <XAxis 
          dataKey="name" 
          tick={{ fill: '#5E6C84', fontSize: 12 }}
          axisLine={{ stroke: '#E5E7EB' }}
        />
        <YAxis 
          tick={{ fill: '#5E6C84', fontSize: 12 }}
          axisLine={{ stroke: '#E5E7EB' }}
        />
        <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0, 82, 204, 0.05)' }} />
        <Bar dataKey="value" radius={[8, 8, 0, 0]} maxBarSize={80}>
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
