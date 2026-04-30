import React from 'react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';

interface TimelineChartProps {
  data: number[];
  label: string;
  color: string;
}

const TimelineChart: React.FC<TimelineChartProps> = ({ data, label, color }) => {
  const chartData = data.map((val, i) => ({
    time: i,
    score: Math.round(val * 100),
  }));

  return (
    <div className="w-full h-48 mt-4">
      <h4 className="text-[10px] font-black uppercase tracking-widest opacity-40 mb-2">{label} Timeline</h4>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={color} stopOpacity={0.3}/>
              <stop offset="95%" stopColor={color} stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
          <XAxis 
            dataKey="time" 
            hide 
          />
          <YAxis 
            domain={[0, 100]} 
            tick={{ fontSize: 10, fill: 'rgba(255,255,255,0.3)' }} 
            axisLine={false}
            tickLine={false}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#111', 
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: '8px',
              fontSize: '10px'
            }}
            itemStyle={{ color: color }}
          />
          <ReferenceLine y={70} stroke="#ef4444" strokeDasharray="3 3" label={{ position: 'right', value: 'High Risk', fill: '#ef4444', fontSize: 8 }} />
          <Area 
            type="monotone" 
            dataKey="score" 
            stroke={color} 
            fillOpacity={1} 
            fill="url(#colorScore)" 
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TimelineChart;
