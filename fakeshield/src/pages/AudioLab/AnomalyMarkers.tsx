import React from 'react';
import type { CodecDetail, RobustnessReport } from '../../services/audioService';
import { Zap, Radio, TrendingDown, Activity } from 'lucide-react';

interface AnomalyMarkersProps {
  codecDetail: CodecDetail;
  stabilityReport: RobustnessReport;
  aiProbability: number;
}

interface Anomaly {
  label: string;
  value: string;
  description: string;
  severity: 'ok' | 'warn' | 'alert';
  icon: React.ElementType;
}

const AnomalyMarkers: React.FC<AnomalyMarkersProps> = ({
  codecDetail,
  stabilityReport,
  aiProbability,
}) => {
  const snr    = codecDetail?.snr_proxy_db ?? 0;
  const enf    = codecDetail?.enf_strength ?? 0;
  const ripple = codecDetail?.spectral_ripple_peaks ?? 0;
  const dc     = codecDetail?.dc_offset ?? 0;
  const stability = stabilityReport?.stability_score ?? 1;

  const anomalies: Anomaly[] = [
    {
      label: 'SNR Floor',
      value: `${snr.toFixed(1)} dB`,
      description: snr > 60
        ? 'Suspiciously clean — real recordings have ambient noise'
        : snr > 40
        ? 'Elevated SNR — may indicate studio-grade TTS'
        : 'Normal noise floor — consistent with real recording',
      severity: snr > 60 ? 'alert' : snr > 40 ? 'warn' : 'ok',
      icon: Activity,
    },
    {
      label: 'ENF Signature',
      value: enf > 1.2 ? `${enf.toFixed(2)}× peak` : 'Absent',
      description: enf > 1.2
        ? 'Electrical network frequency detected — supports real recording origin'
        : 'No mains hum — common in TTS/synthetic audio',
      severity: enf > 1.2 ? 'ok' : 'warn',
      icon: Radio,
    },
    {
      label: 'Spectral Ripple',
      value: `${ripple} peak${ripple !== 1 ? 's' : ''}`,
      description: ripple > 3
        ? 'Periodic spectral ripple — consistent with resampling artifacts'
        : ripple > 1
        ? 'Mild spectral irregularity detected'
        : 'No significant resampling artifacts',
      severity: ripple > 3 ? 'alert' : ripple > 1 ? 'warn' : 'ok',
      icon: TrendingDown,
    },
    {
      label: 'Stress Stability',
      value: `${(stability * 100).toFixed(0)}%`,
      description: stability >= 0.80
        ? 'Detection is stable under compression & telephony simulation'
        : stability >= 0.60
        ? 'Moderate instability — result may shift with different formats'
        : 'Unstable detection — AI artifacts are compression-sensitive',
      severity: stability >= 0.80 ? 'ok' : stability >= 0.60 ? 'warn' : 'alert',
      icon: Zap,
    },
  ];

  const SEV_STYLES = {
    ok:    { bg: 'rgba(0, 229, 204, 0.1)',   border: 'rgba(0, 229, 204, 0.2)',   color: '#00E5CC',   dot: '#00E5CC' },
    warn:  { bg: 'var(--accent-yellow-transparent)', border: 'var(--accent-yellow-border)', color: 'var(--accent-yellow)', dot: '#eab308' },
    alert: { bg: 'var(--accent-red-transparent)',    border: 'var(--accent-red-border)',    color: 'var(--accent-red)',    dot: '#ef4444' },
  };

  return (
    <div className="p-4 rounded-xl border border-[var(--panel-border)] bg-[var(--bg-secondary)]">
      <div className="flex items-center justify-between mb-4">
        <h5 className="text-[10px] font-mono uppercase tracking-[0.2em] text-[var(--text-muted)]">
          Codec &amp; Physical Anomalies
        </h5>
        <span
          className="text-[9px] font-mono px-2 py-0.5 rounded"
          style={{
            background: aiProbability > 65 ? 'var(--accent-red-transparent)' : 'rgba(0, 229, 204, 0.1)',
            color: aiProbability > 65 ? 'var(--accent-red)' : '#00E5CC',
          }}
        >
          {anomalies.filter(a => a.severity === 'alert').length} anomalies
        </span>
      </div>

      <div className="space-y-2">
        {anomalies.map((a) => {
          const s = SEV_STYLES[a.severity];
          return (
            <div
              key={a.label}
              className="flex items-start gap-3 p-3 rounded-lg transition-all duration-200 hover:opacity-90"
              style={{
                background: s.bg,
                border: `1px solid ${s.border}`,
              }}
            >
              <div
                className="p-1.5 rounded-md flex-shrink-0 mt-0.5"
                style={{ background: s.bg }}
              >
                <a.icon className="w-3.5 h-3.5" style={{ color: s.color }} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-[10px] font-bold font-mono uppercase tracking-tight" style={{ color: s.color }}>
                    {a.label}
                  </span>
                  <span className="text-[10px] font-mono font-bold flex-shrink-0" style={{ color: s.color }}>
                    {a.value}
                  </span>
                </div>
                <p className="text-[9px] text-[var(--text-muted)] mt-0.5 leading-tight font-mono">
                  {a.description}
                </p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Stability scores bar */}
      {stabilityReport?.scores && (
        <div className="mt-4 pt-3 border-t border-[var(--panel-border)]">
          <p className="text-[9px] font-mono uppercase tracking-[0.15em] text-[var(--text-muted)] mb-2">
            Robustness Passes
          </p>
          <div className="flex gap-2">
            {Object.entries(stabilityReport.scores).map(([key, val]) => {
              const pct = Math.round(val * 100);
              return (
                <div key={key} className="flex-1 text-center">
                  <div className="text-[9px] font-mono text-[var(--text-muted)] mb-1 capitalize">{key}</div>
                  <div
                    className="text-xs font-bold font-mono"
                    style={{ color: pct > 70 ? 'var(--accent-red)' : '#00E5CC' }}
                  >
                    {pct}%
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default AnomalyMarkers;
