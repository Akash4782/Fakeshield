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
    <div className="p-8 rounded-3xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] space-y-6">
      <div className="flex items-center gap-2">
        <Cpu className="w-4 h-4 text-[#00E5CC]" />
        <h3 className="text-xs font-black uppercase tracking-widest pb-1 border-b-2 border-[#00E5CC]/20">VLM Physics Reasoning</h3>
      </div>
      
      <div className="space-y-4">
        {lines.map((line, i) => {
          const [q, a] = line.split(' | A: ');
          const questionText = q?.replace('Q: ', '') || 'Forensic Inquiry';
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
              className="p-4 rounded-xl bg-white/5 border border-white/5 space-y-2 group"
            >
              <div className="flex items-center gap-2 opacity-40 group-hover:opacity-100 transition-opacity">
                <Terminal className="w-3 h-3 text-[#00E5CC]" />
                <span className="text-[9px] font-black uppercase tracking-tighter">{questionText}</span>
              </div>
              <div className="flex gap-3">
                {isSuspicious && <ShieldAlert className="w-4 h-4 text-red-500 shrink-0 mt-1" />}
                <p className="text-xs font-medium leading-relaxed opacity-80">
                  {answerText}
                </p>
              </div>
            </motion.div>
          );
        })}
      </div>
      
      <div className="pt-4 border-t border-white/5 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-[10px] font-bold opacity-30">Moondream2 Reasoning Online</span>
        </div>
        <span className="text-[8px] font-mono opacity-20 uppercase">Phys-Inconsistency-Audit_v1</span>
      </div>
    </div>
  );
};

export default VLMReasoningPanel;
