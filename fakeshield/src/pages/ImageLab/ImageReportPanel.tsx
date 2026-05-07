import { motion } from 'framer-motion';
import { CheckCircle2, XCircle, TrendingUp, Info } from 'lucide-react';

interface ImageReportPanelProps {
  reasons?: string[];
  perGeneratorAccuracy?: Record<string, { accuracy: string; notes: string }>;
  verdict: string;
}

const GENERATOR_COLORS: Record<string, string> = {
  'ChatGPT': '#22c55e',
  'Adobe': '#22c55e',
  'ProGAN': '#f97316',
  'Stable': '#eab308',
  'SDXL': '#f97316',
  'Midjourney': '#ef4444',
  'FLUX': '#ef4444',
};

function getGeneratorColor(name: string): string {
  const key = Object.keys(GENERATOR_COLORS).find(k => name.includes(k));
  return key ? GENERATOR_COLORS[key] : '#94a3b8';
}

function parseAccuracyValue(accuracy: string): number {
  const match = accuracy.match(/(\d+)/);
  return match ? parseInt(match[1], 10) : 50;
}

export default function ImageReportPanel({ reasons, perGeneratorAccuracy, verdict }: ImageReportPanelProps) {
  return (
    <div className="flex flex-col gap-4">
      {/* Forensic reasons */}
      {reasons && reasons.length > 0 && (
        <div className="rounded-2xl border overflow-hidden shadow-sm" style={{ borderColor: 'var(--panel-border)', background: 'var(--panel-bg)', color: 'var(--text-primary)' }}>
          <div
            className="px-5 py-4 border-b text-xs font-bold tracking-tight uppercase bg-[var(--btn-secondary-bg)]"
            style={{ borderColor: 'var(--panel-border)', color: 'var(--text-primary)' }}
          >
            Logical Arbiter — Forensic Reasoning
          </div>
          <div className="p-3 space-y-2">
            {reasons.map((reason, i) => {
              const isPositive = reason.includes('✓') || reason.includes('○');
              const isNegative = reason.includes('✗');
              const Icon = isPositive ? CheckCircle2 : isNegative ? XCircle : Info;
              const color = isPositive ? '#10b981' : isNegative ? '#ef4444' : '#64748b';
              
              // Clean the text by removing the markers
              const cleanText = reason.replace(/[✓✗○]/g, '').trim();

              return (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.08 }}
                  className="flex items-start gap-4 px-5 py-3.5 rounded-xl text-[11px] font-medium leading-relaxed border"
                  style={{ 
                    background: isPositive ? 'rgba(16,185,129,0.06)' : isNegative ? 'rgba(239,68,68,0.06)' : 'var(--btn-secondary-bg)', 
                    borderColor: isPositive ? 'rgba(16,185,129,0.16)' : isNegative ? 'rgba(239,68,68,0.16)' : 'var(--panel-border)',
                    color: 'var(--text-primary)' 
                  }}
                >
                  <Icon className="w-4 h-4 mt-0.5 shrink-0" style={{ color }} strokeWidth={2.5} />
                  <span className="flex-1">{cleanText}</span>
                </motion.div>
              );
            })}
          </div>
        </div>
      )}

      {/* Per-generator accuracy table */}
      {perGeneratorAccuracy && Object.keys(perGeneratorAccuracy).length > 0 && (
        <div className="rounded-2xl border overflow-hidden shadow-sm" style={{ borderColor: 'var(--panel-border)', background: 'var(--panel-bg)', color: 'var(--text-primary)' }}>
          <div
            className="px-5 py-4 border-b flex items-center gap-2 bg-[var(--btn-secondary-bg)]"
            style={{ borderColor: 'var(--panel-border)' }}
          >
            <TrendingUp className="w-4 h-4 text-cyan-500" />
            <span className="text-xs font-bold tracking-tight uppercase" style={{ color: 'var(--text-primary)' }}>
              Per-Generator Detection Accuracy
            </span>
          </div>
          <div className="p-3 space-y-2">
            {Object.entries(perGeneratorAccuracy).map(([gen, data]) => {
              const pct = parseAccuracyValue(data.accuracy);
              const col = getGeneratorColor(gen);
              return (
                <div key={gen} className="space-y-1">
                  <div className="flex justify-between items-center">
                    <span className="text-[10px] font-bold text-[var(--text-primary)]">{gen}</span>
                    <span className="text-[10px] font-black" style={{ color: col }}>{data.accuracy}</span>
                  </div>
                  <div className="w-full rounded-full overflow-hidden" style={{ height: 4, background: 'rgba(255,255,255,0.06)' }}>
                    <motion.div
                      className="h-full rounded-full"
                      style={{ background: col }}
                      initial={{ width: 0 }}
                      animate={{ width: `${pct}%` }}
                      transition={{ duration: 0.8, ease: 'easeOut' }}
                    />
                  </div>
                  <div className="text-[9px] font-medium text-[var(--text-muted)] mt-1 uppercase tracking-tighter">{data.notes}</div>
                </div>
              );
            })}
          </div>
          <div
            className="px-5 py-3 border-t flex items-start gap-2 text-[10px] font-medium leading-relaxed bg-[var(--btn-secondary-bg)]"
            style={{ borderColor: 'var(--panel-border)', color: 'var(--text-secondary)' }}
          >
            <Info className="w-3.5 h-3.5 shrink-0 mt-0.5 text-amber-500" />
            Accuracy varies by compression, platform re-encoding, and steganographic post-processing artifacts.
          </div>
        </div>
      )}
    </div>
  );
}
