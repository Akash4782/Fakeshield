import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2 } from 'lucide-react';

interface ForensicLensProps {
  originalUrl: string | null;
  fftUrl?: string | null;
  heatmapUrl?: string | null;
  elaUrl?: string | null;
  isLoading: boolean;
}

const TABS = [
  { id: 'original', label: 'Original', color: '#00E5CC' },
  { id: 'fft', label: 'FFT Spectrum', color: '#00E5CC' },
  { id: 'heatmap', label: 'Noise Map', color: '#f97316' },
  { id: 'ela', label: 'ELA', color: '#eab308' },
];

const TAB_DESCRIPTIONS: Record<string, string> = {
  original: 'Raw input capture',
  fft: '1/f² power — deviations indicate AI generator upsampling artifacts',
  heatmap: 'Pixel-residual map — camera sensor fingerprint analysis',
  ela: 'Error Level Analysis — compression uniformity (flat = AI)',
};

export default function ForensicLens({ originalUrl, fftUrl, heatmapUrl, elaUrl, isLoading }: ForensicLensProps) {
  const [activeTab, setActiveTab] = useState('original');

  const imageFor = (tab: string) => {
    if (tab === 'original') return originalUrl;
    if (tab === 'fft') return fftUrl;
    if (tab === 'heatmap') return heatmapUrl;
    if (tab === 'ela') return elaUrl;
    return null;
  };

  const activeTabCfg = TABS.find(t => t.id === activeTab)!;
  const currentImage = imageFor(activeTab);

  return (
    <div
      className="rounded-2xl overflow-hidden border flex flex-col shadow-sm"
      style={{ borderColor: 'var(--panel-border)', background: '#ffffff', color: '#1e293b', minHeight: 420 }}
    >
      {/* Tab bar */}
      <div className="flex border-b shrink-0" style={{ borderColor: 'var(--panel-border)' }}>
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className="relative flex-1 py-3 text-xs font-bold tracking-tight uppercase transition-colors"
            style={{
              color: activeTab === tab.id ? tab.color : '#64748b',
              background: activeTab === tab.id ? `${tab.color}08` : 'transparent',
            }}
          >
            {tab.label}
            {activeTab === tab.id && (
              <motion.div
                layoutId="forensic-tab-underline"
                className="absolute bottom-0 left-0 right-0 h-0.5"
                style={{ background: tab.color }}
                transition={{ type: 'spring', stiffness: 500, damping: 30 }}
              />
            )}
          </button>
        ))}
      </div>

      {/* Description bar */}
      <div
        className="px-5 py-2 text-[11px] font-medium shrink-0 border-b bg-slate-50"
        style={{ borderColor: 'var(--panel-border)', color: '#64748b' }}
      >
        <span className="font-bold mr-1" style={{ color: activeTabCfg.color }}>ANALYSIS:</span>
        {TAB_DESCRIPTIONS[activeTab]}
      </div>

      {/* Image area */}
      <div className="flex-1 relative flex items-center justify-center p-2 min-h-[340px]">
        {isLoading ? (
          <div className="flex flex-col items-center gap-3 text-cyan-400">
            <Loader2 className="w-10 h-10 animate-spin" />
            <p className="font-mono text-xs tracking-widest animate-pulse">PROCESSING IMAGE SIGNAL...</p>
          </div>
        ) : (
          <AnimatePresence mode="wait">
            {currentImage ? (
              <motion.img
                key={activeTab}
                src={currentImage}
                className="max-w-full max-h-full object-contain rounded-lg"
                style={{ maxHeight: 340 }}
                initial={{ opacity: 0, scale: 0.97 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.97 }}
                transition={{ duration: 0.25 }}
              />
            ) : (
              <motion.div
                key={`no-${activeTab}`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center gap-2 text-center"
              >
                <div className="text-4xl opacity-20">📡</div>
                <p className="text-xs font-mono" style={{ color: 'var(--text-muted)' }}>
                  {activeTab === 'original' ? 'Upload an image to begin' : 'Signal data unavailable'}
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        )}
      </div>
    </div>
  );
}
