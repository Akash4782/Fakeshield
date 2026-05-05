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
      <h4 className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-400 mb-2">{label} Timeline</h4>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={color} stopOpacity={0.2}/>
              <stop offset="95%" stopColor={color} stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" vertical={false} />
          <XAxis 
            dataKey="time" 
            hide 
          />
          <YAxis 
            domain={[0, 100]} 
            tick={{ fontSize: 9, fill: '#94a3b8', fontWeight: 600 }} 
            axisLine={false}
            tickLine={false}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#fff', 
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              fontSize: '11px',
              boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'
            }}
            itemStyle={{ color: color, fontWeight: 700 }}
          />
          <ReferenceLine y={75} stroke="#ef4444" strokeDasharray="4 4" label={{ position: 'right', value: 'THREAT THRESHOLD', fill: '#ef4444', fontSize: 8, fontWeight: 800 }} />
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
