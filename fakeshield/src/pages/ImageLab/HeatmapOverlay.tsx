import { useState } from 'react';
import { motion } from 'framer-motion';

interface HeatmapOverlayProps {
  originalUrl: string | null;
  heatmapUrl?: string | null;
}

export default function HeatmapOverlay({ originalUrl, heatmapUrl }: HeatmapOverlayProps) {
  const [showHeatmap, setShowHeatmap] = useState(true);
  const currentUrl = showHeatmap && heatmapUrl ? heatmapUrl : originalUrl;

  return (
    <div className="relative rounded-2xl overflow-hidden border" style={{ borderColor: 'var(--panel-border)', background: 'rgba(0,0,0,0.3)', minHeight: 280 }}>
      {/* Header bar */}
      <div className="absolute top-0 left-0 right-0 z-10 flex items-center justify-between px-3 py-2 backdrop-blur-sm"
        style={{ background: 'rgba(0,0,0,0.6)' }}>
        <span className="text-[9px] font-mono tracking-widest uppercase text-orange-400">
          TruFor / PRNU Noise Analysis
        </span>
        {heatmapUrl && (
          <button
            onClick={() => setShowHeatmap(v => !v)}
            className="text-[9px] font-mono px-2 py-0.5 rounded transition-all border"
            style={{
              color: showHeatmap ? '#f97316' : 'var(--text-muted)',
              borderColor: showHeatmap ? '#f97316' : 'var(--panel-border)',
              background: showHeatmap ? 'rgba(249,115,22,0.1)' : 'transparent',
            }}
          >
            {showHeatmap ? 'HEATMAP' : 'ORIGINAL'}
          </button>
        )}
      </div>

      {/* Image */}
      <motion.img
        key={currentUrl}
        src={currentUrl || ''}
        className="w-full h-full object-contain"
        style={{ minHeight: 280, maxHeight: 340 }}
        initial={{ opacity: 0.5 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      />

      {/* Legend */}
      {showHeatmap && heatmapUrl && (
        <div className="absolute bottom-0 left-0 right-0 flex items-center justify-center gap-4 px-3 py-2 backdrop-blur-sm"
          style={{ background: 'rgba(0,0,0,0.6)' }}>
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#ef4444' }} />
            <span className="text-[9px] font-mono" style={{ color: 'var(--text-muted)' }}>AI-synthesized (uniform)</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#3b82f6' }} />
            <span className="text-[9px] font-mono" style={{ color: 'var(--text-muted)' }}>Authentic noise residual</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full" style={{ background: '#22c55e' }} />
            <span className="text-[9px] font-mono" style={{ color: 'var(--text-muted)' }}>Camera PRNU fingerprint</span>
          </div>
        </div>
      )}
    </div>
  );
}
