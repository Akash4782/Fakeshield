import React from 'react';
import { Cpu, Terminal, ShieldAlert } from 'lucide-react';
import { motion } from 'framer-motion';

interface VLMReasoningPanelProps {
  report: string;
}

const VLMReasoningPanel: React.FC<VLMReasoningPanelProps> = ({ report }) => {
  if (!report) return null;
  
  // Format the report for better display
  const lines = report.split(' | ');
  
  return (
    <div className="p-8 rounded-2xl border border-[var(--panel-border)] bg-white space-y-6 shadow-sm">
      <div className="flex items-center gap-2">
        <Cpu className="w-4 h-4 text-slate-400" />
        <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Visual Physics Analysis</h3>
      </div>
      
      <div className="space-y-4">
        {lines.map((line, i) => {
          const [q, a] = line.split(' | A: ');
          const questionText = q?.replace('Q: ', '') || 'System Query';
          const answerText = a || 'N/A';
          const isSuspicious = answerText.toLowerCase().includes('inconsistent') || 
                               answerText.toLowerCase().includes('yes') || 
                               answerText.toLowerCase().includes('unnatural');
                               
          return (
            <motion.div 
              key={i} 
              initial={{ opacity: 0, y: 10 }} 
              animate={{ opacity: 1, y: 0 }} 
              transition={{ delay: i * 0.15 }}
              className="p-4 rounded-xl bg-slate-50 border border-slate-100 space-y-2"
            >
              <div className="flex items-center gap-2 text-slate-400">
                <Terminal className="w-3 h-3" />
                <span className="text-[9px] font-bold uppercase tracking-tight">{questionText}</span>
              </div>
              <div className="flex gap-3">
                {isSuspicious && <ShieldAlert className="w-4 h-4 text-red-500 shrink-0 mt-1" />}
                <p className="text-sm text-slate-600 leading-relaxed font-medium">
                  {answerText}
                </p>
              </div>
            </motion.div>
          );
        })}
      </div>
      
      <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-1.5 h-1.5 rounded-full bg-green-500"></div>
          <span className="text-[10px] font-bold text-slate-400 uppercase">Engine Status: Active</span>
        </div>
        <span className="text-[8px] font-mono text-slate-300 uppercase tracking-tighter">Version 1.4.2</span>
      </div>
    </div>
  );
};

export default VLMReasoningPanel;
