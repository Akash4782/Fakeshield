import { motion } from 'framer-motion';
import { ChevronRight, TrendingUp, Info } from 'lucide-react';

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
        <div className="rounded-2xl border overflow-hidden shadow-sm" style={{ borderColor: 'var(--panel-border)', background: '#ffffff', color: '#1e293b' }}>
          <div
            className="px-4 py-3 border-b text-[10px] font-mono tracking-widest uppercase"
            style={{ borderColor: 'var(--panel-border)', color: '#00E5CC' }}
          >
            Logical Arbiter — Forensic Reasoning
          </div>
          <div className="p-3 space-y-2">
            {reasons.map((reason, i) => {
              const isPositive = reason.startsWith('✓') || reason.startsWith('○');
              const isNegative = reason.startsWith('✗');
              const color = isPositive ? '#22c55e' : isNegative ? '#ef4444' : '#eab308';
              return (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.08 }}
                  className="flex items-start gap-2 px-3 py-2 rounded-xl text-[10px] font-mono leading-relaxed"
                  style={{ background: `${color}08`, border: `1px solid ${color}20`, color: 'var(--text-secondary)' }}
                >
                  <ChevronRight className="w-3 h-3 mt-0.5 shrink-0" style={{ color }} />
                  <span>{reason}</span>
                </motion.div>
              );
            })}
          </div>
        </div>
      )}

      {/* Per-generator accuracy table */}
      {perGeneratorAccuracy && Object.keys(perGeneratorAccuracy).length > 0 && (
        <div className="rounded-2xl border overflow-hidden shadow-sm" style={{ borderColor: 'var(--panel-border)', background: '#ffffff', color: '#1e293b' }}>
          <div
            className="px-4 py-3 border-b flex items-center gap-2"
            style={{ borderColor: 'var(--panel-border)' }}
          >
            <TrendingUp className="w-3 h-3" style={{ color: '#00E5CC' }} />
            <span className="text-[10px] font-mono tracking-widest uppercase" style={{ color: '#00E5CC' }}>
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
                    <span className="text-[9px] font-mono" style={{ color: 'var(--text-secondary)' }}>{gen}</span>
                    <span className="text-[9px] font-mono font-bold" style={{ color: col }}>{data.accuracy}</span>
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
                  <div className="text-[8px] font-mono" style={{ color: 'var(--text-muted)' }}>{data.notes}</div>
                </div>
              );
            })}
          </div>
          <div
            className="px-4 py-2 border-t flex items-start gap-1.5 text-[8px] font-mono leading-relaxed"
            style={{ borderColor: 'var(--panel-border)', color: 'var(--text-muted)' }}
          >
            <Info className="w-3 h-3 shrink-0 mt-0.5 text-yellow-500" />
            Accuracy varies by compression, platform re-encoding, and steganographic post-processing.
          </div>
        </div>
      )}
    </div>
  );
}
