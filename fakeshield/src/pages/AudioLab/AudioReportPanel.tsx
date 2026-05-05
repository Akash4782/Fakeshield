import React, { useMemo } from 'react';
import type { AudioResult, AudioReason } from '../../services/audioService';
import { Shield, AlertTriangle, CheckCircle, Info, Download, Trash2 } from 'lucide-react';

interface AudioReportPanelProps {
  result: AudioResult;
  onReset: () => void;
}

function generateCaseId(result: AudioResult): string {
  // Deterministic case ID derived from result data — stable across re-renders
  const seed = `${result.ai_probability}-${result.verdict}-${result.audio_metadata.duration_sec}`;
  let hash = 0;
  for (let i = 0; i < seed.length; i++) {
    hash = ((hash << 5) - hash + seed.charCodeAt(i)) & 0xffffffff;
  }
  return Math.abs(hash).toString(36).toUpperCase().padStart(9, '0').slice(0, 9);
}

const AudioReportPanel: React.FC<AudioReportPanelProps> = ({ result, onReset }) => {
  // Stable case ID — won't change on re-renders
  const caseId = useMemo(() => generateCaseId(result), [result]);

  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'critical': return 'var(--accent-red)';
      case 'high':     return 'var(--accent-orange)';
      case 'medium':   return 'var(--accent-yellow)';
      default:         return '#00E5CC';
    }
  };

  const handleDownload = () => {
    const report = {
      case_id:       caseId,
      generated_at:  new Date().toISOString(),
      verdict:       result.verdict,
      ai_probability: result.ai_probability,
      threat_level:  result.threat_level,
      confidence:    result.confidence,
      agreement:     result.agreement,
      fusion_rule:   result.fusion_rule,
      forensic_summary: result.forensic_summary,
      recommended_action: result.recommended_action,
      audio_metadata: result.audio_metadata,
      signal_scores: result.signal_scores,
      stability_score: result.stability_score,
      primary_reasons: result.primary_reasons,
      supporting_reasons: result.supporting_reasons,
      exonerating_factors: result.exonerating_factors,
    };
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fakeshield-audio-report-${caseId}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="flex flex-col h-full animate-fade-in">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-2xl font-display font-bold text-[var(--text-heading)]">Forensic Report</h2>
          <p className="text-sm font-medium text-[var(--text-secondary)] mt-1">
            Case ID: {caseId}
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleDownload}
            title="Download JSON report"
            className="p-2 rounded-lg bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:border-[rgba(0,229,204,0.2)] transition-all"
          >
            <Download className="w-4 h-4" />
          </button>
          <button
            onClick={onReset}
            title="Reset — start new scan"
            className="p-2 rounded-lg bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] text-[var(--text-muted)] hover:text-[var(--accent-red)] hover:border-[var(--accent-red-border)] transition-all"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="space-y-6 overflow-y-auto pr-2 custom-scrollbar flex-1">

        {/* Summary Card */}
        <div className="p-5 rounded-xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] relative overflow-hidden">
          <div
            className="absolute top-0 left-0 w-1 h-full"
            style={{ background: getSeverityColor(result.threat_level) }}
          />
          <div className="flex items-start gap-4">
            <div
              className="p-3 rounded-lg flex-shrink-0"
              style={{ background: `${getSeverityColor(result.threat_level)}15` }}
            >
              {result.threat_level === 'CRITICAL' || result.threat_level === 'HIGH' ? (
                <AlertTriangle className="w-6 h-6" style={{ color: getSeverityColor(result.threat_level) }} />
              ) : (
                <CheckCircle className="w-6 h-6" style={{ color: getSeverityColor(result.threat_level) }} />
              )}
            </div>
            <div>
              <h4
                className="font-bold text-lg leading-tight"
                style={{ color: getSeverityColor(result.threat_level) }}
              >
                {result.verdict.replace(/_/g, ' ')}
              </h4>
              <p className="text-sm text-[var(--text-secondary)] mt-1 italic leading-relaxed">
                "{result.forensic_summary}"
              </p>
            </div>
          </div>
        </div>

        {/* Fusion rule badge */}
        {result.fusion_rule && (
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg border border-[var(--panel-border)] bg-[var(--bg-primary)]">
            <span className="text-xs font-medium text-[var(--text-secondary)]">
              Decision Rule:
            </span>
            <span className="text-xs font-semibold text-[var(--accent-blue)] capitalize">
              {result.fusion_rule.replace(/_/g, ' ').toLowerCase()}
            </span>
          </div>
        )}

        {/* Action Recommendation */}
        <div className="p-4 rounded-xl border border-[var(--accent-green-border)] bg-[var(--accent-green-transparent)]">
          <h5 className="text-xs font-semibold text-[var(--accent-green)] mb-2 flex items-center">
            <Shield className="w-3 h-3 mr-2" />
            Counter-Measures
          </h5>
          <p className="text-sm text-[var(--text-primary)] font-medium leading-relaxed">
            {result.recommended_action}
          </p>
        </div>

        {/* Audio metadata strip */}
        <div className="grid grid-cols-2 gap-2">
          {[
            { label: 'Duration', value: `${result.audio_metadata.duration_sec.toFixed(1)}s` },
            { label: 'Segments', value: `${result.audio_metadata.num_chunks}` },
            { label: 'Format', value: result.audio_metadata.format_hint.toUpperCase() },
            { label: 'Stability', value: `${((result.stability_score ?? 1) * 100).toFixed(0)}%` },
          ].map(({ label, value }) => (
            <div
              key={label}
              className="p-3 rounded-lg border border-[var(--panel-border)] bg-[var(--bg-primary)] flex flex-col"
            >
              <span className="text-xs font-medium text-[var(--text-secondary)] mb-1">{label}</span>
              <span className="text-sm font-semibold text-[var(--accent-blue)]">{value}</span>
            </div>
          ))}
        </div>

        {/* Primary Reasons */}
        {result.primary_reasons.length > 0 && (
          <div>
            <h5 className="text-sm font-semibold text-[var(--text-primary)] mb-4 flex items-center">
              <Shield className="w-4 h-4 mr-2 text-[var(--accent-blue)]" />
              Primary Evidence Indicators
            </h5>
            <div className="space-y-3">
              {result.primary_reasons.map((reason: AudioReason, i: number) => (
                <div
                  key={i}
                  className="p-4 rounded-lg bg-[var(--bg-primary)] border border-[var(--panel-border)] hover:border-[var(--accent-blue-border)] transition-all"
                >
                  <div className="flex justify-between items-start mb-2">
                    <span
                      className="text-xs font-bold uppercase tracking-tight"
                      style={{ color: getSeverityColor(reason.severity) }}
                    >
                      {reason.signal} Analysis
                    </span>
                    <span className="text-xs font-medium px-2 py-1 rounded bg-[var(--bg-secondary)] text-[var(--text-secondary)] border border-[var(--panel-border)]">
                      {Math.round(reason.score * 100)}% match
                    </span>
                  </div>
                  <p className="text-sm font-semibold text-[var(--text-primary)] mb-1">{reason.message}</p>
                  <p className="text-xs text-[var(--text-muted)] leading-relaxed">{reason.evidence}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {result.primary_reasons.length === 0 && (
          <p className="text-xs text-[var(--text-muted)] italic px-2">
            No primary synthesis indicators detected.
          </p>
        )}

        {/* Supporting Reasons */}
        {result.supporting_reasons.length > 0 && (
          <div>
            <h5 className="text-sm font-semibold text-[var(--text-primary)] mb-4 flex items-center">
              <Info className="w-4 h-4 mr-2 text-[var(--accent-green)]" />
              Supporting Forensic Signals
            </h5>
            <div className="space-y-2">
              {result.supporting_reasons.map((reason: AudioReason, i: number) => (
                <div
                  key={i}
                  className="p-3 rounded-lg bg-[var(--bg-primary)] border border-[var(--panel-border)]/50 opacity-80 hover:opacity-100 transition-all"
                >
                  <p className="text-xs font-semibold text-[var(--text-secondary)]">{reason.message}</p>
                  <p className="text-xs text-[var(--text-muted)] mt-1 italic">{reason.evidence}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Exonerating Factors */}
        {result.exonerating_factors.length > 0 && (
          <div className="pb-6">
            <h5 className="text-sm font-semibold text-[var(--text-primary)] mb-4 flex items-center">
              <CheckCircle className="w-4 h-4 mr-2 text-green-500" />
              Human Authenticity Markers
            </h5>
            <ul className="space-y-1">
              {result.exonerating_factors.map((factor: string, i: number) => (
                <li key={i} className="text-xs text-[var(--text-muted)] flex items-start gap-2">
                  <span className="text-green-500 mt-1 flex-shrink-0">✓</span>
                  {factor}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default AudioReportPanel;
