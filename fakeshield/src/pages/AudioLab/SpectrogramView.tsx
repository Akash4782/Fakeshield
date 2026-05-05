import React from 'react';
import type { SpectralDetail } from '../../services/audioService';

interface SpectrogramViewProps {
  spectralDetail: SpectralDetail;
  aiScore: number;
}

interface Band {
  label: string;
  key: keyof SpectralDetail;
  range: string;
  invert?: boolean;  // true = lower value = more AI
  maxVal: number;
}

const BANDS: Band[] = [
  { label: 'HF Energy',     key: 'hf_energy_ratio',    range: '6–8 kHz',  invert: false, maxVal: 0.25 },
  { label: 'Mel Smoothness', key: 'mel_frame_diff',     range: 'Full Band', invert: false, maxVal: 5.0  },
  { label: 'MFCC Δ Std',    key: 'mfcc_delta_std',     range: 'Cepstral',  invert: false, maxVal: 10.0 },
  { label: 'Flatness Var',  key: 'flatness_variance',  range: 'Full Band', invert: false, maxVal: 0.015},
  { label: 'Centroid Var',  key: 'centroid_variance',  range: 'Spectral',  invert: false, maxVal: 0.005},
];

const SpectrogramView: React.FC<SpectrogramViewProps> = ({ spectralDetail, aiScore }) => {
  const isAI = aiScore > 60;

  return (
    <div className="p-4 rounded-xl border border-[var(--panel-border)] bg-[var(--bg-secondary)]">
      <div className="flex items-center justify-between mb-4">
        <h5 className="text-sm font-semibold text-[var(--text-primary)]">
          Spectral Fingerprint
        </h5>
        <span
          className="text-xs px-2 py-1 rounded-md font-semibold"
          style={{
            background: isAI ? 'var(--accent-red-transparent)' : 'var(--accent-green-transparent)',
            color: isAI ? 'var(--accent-red)' : 'var(--accent-green)',
            border: `1px solid ${isAI ? 'var(--accent-red-border)' : 'var(--accent-green-border)'}`,
          }}
        >
          {isAI ? 'Vocoder Signature' : 'Natural Spectrum'}
        </span>
      </div>

      {/* Pseudo-spectrogram frequency bands */}
      <div className="space-y-2">
        {BANDS.map(({ label, key, range, maxVal }) => {
          const rawVal = spectralDetail[key] as number | undefined;
          const val = rawVal ?? 0;
          const pct = Math.min(100, Math.max(0, (val / maxVal) * 100));

          // Low values on invert=false metrics = suspicious
          const suspicion = 100 - pct;
          const isSuspicious = suspicion > 65;

          const barColor = isSuspicious
            ? 'var(--accent-orange)'
            : pct > 60
            ? '#00E5CC'
            : 'var(--accent-yellow)';

          return (
            <div key={String(key)}>
              <div className="flex justify-between text-xs font-medium mb-1 text-[var(--text-secondary)]">
                <span>{label}</span>
                <span style={{ color: isSuspicious ? 'var(--accent-orange)' : 'var(--text-muted)' }}>
                  {typeof rawVal === 'number' ? rawVal.toFixed(4) : '—'} <span className="opacity-50">/ {range}</span>
                </span>
              </div>
              <div className="h-2 bg-[var(--panel-border)] rounded-full overflow-hidden relative">
                {/* Background gradient showing expected human range */}
                <div
                  className="absolute top-0 left-[40%] w-[40%] h-full bg-white/5 border-x border-white/10"
                />
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{
                    width: `${pct}%`,
                    background: `linear-gradient(90deg, ${barColor}88, ${barColor})`,
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>

      <p className="text-xs text-[var(--text-secondary)] mt-4 leading-relaxed">
        {isAI
          ? 'Frequency distribution shows neural vocoder characteristics — reduced high-frequency content and over-smoothed transitions.'
          : 'Frequency distribution shows natural acoustic properties — normal high-frequency energy and realistic spectral variation.'}
      </p>
    </div>
  );
};

export default SpectrogramView;
