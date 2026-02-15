'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';

interface ShapFeature {
  feature_name: string;
  importance: number;
  direction: string;
  display_name_tr: string;
}

interface ShapChartProps {
  features: ShapFeature[];
}

export default function ShapChart({ features }: ShapChartProps) {
  // Sort by absolute importance and take top 5
  const chartData = features
    .sort((a, b) => Math.abs(b.importance) - Math.abs(a.importance))
    .slice(0, 5)
    .map(feature => ({
      name: feature.display_name_tr,
      value: feature.importance,
      absValue: Math.abs(feature.importance),
      direction: feature.direction,
    }))
    .reverse(); // Reverse for better visual order (highest at top)

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white border border-gray-200 rounded-lg shadow-lg p-3">
          <p className="text-[#172B4D] text-sm font-semibold">{data.name}</p>
          <p className={`text-xs mt-1 font-bold ${data.direction === 'positive' ? 'text-[#DE350B]' : 'text-[#00875A]'}`}>
            {data.direction === 'positive' ? 'Risk Artırıcı' : 'Risk Azaltıcı'}
          </p>
          <p className="text-[#5E6C84] text-xs mt-1">
            Etki: {Math.abs(data.value).toFixed(3)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart 
        data={chartData} 
        layout="vertical"
        margin={{ top: 10, right: 30, left: 120, bottom: 10 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" horizontal={false} />
        <XAxis 
          type="number"
          tick={{ fill: '#5E6C84', fontSize: 11 }}
          axisLine={{ stroke: '#E5E7EB' }}
        />
        <YAxis 
          type="category" 
          dataKey="name"
          tick={{ fill: '#172B4D', fontSize: 11 }}
          axisLine={{ stroke: '#E5E7EB' }}
          width={110}
        />
        <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0, 82, 204, 0.05)' }} />
        <ReferenceLine x={0} stroke="#172B4D" strokeWidth={1.5} />
        <Bar dataKey="value" radius={[0, 4, 4, 0]} maxBarSize={24}>
          {chartData.map((entry, index) => (
            <Cell 
              key={`cell-${index}`} 
              fill={entry.direction === 'positive' ? '#DE350B' : '#00875A'} 
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
