import React, { useState, useRef, useCallback, useMemo } from 'react';
import type { ChangeEvent, DragEvent } from 'react';
import Sidebar from '../../components/layout/Sidebar';
import {
  FileAudio,
  Search,
  ChevronRight,
  Shield,
  Activity,
  Mic2,
  AlertCircle,
  Clock,
  HardDrive,
  Upload,
  BarChart2,
  Layers,
} from 'lucide-react';
import { analyzeAudioAsync, isValidAudioFile } from '../../services/audioService';
import type { AudioResult } from '../../services/audioService';
import WaveformHeatmap from './WaveformVisualizer';
import AudioReportPanel from './AudioReportPanel';
import PitchStability from './PitchStability';
import SpectrogramView from './SpectrogramView';
import AnomalyMarkers from './AnomalyMarkers';

/* ─── Inline styles injected once ────────────────────────────────── */
const PAGE_STYLES = `
  .audio-glass-panel {
    background: var(--panel-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--panel-border);
    border-radius: 14px;
  }
  .audio-glow {
    box-shadow: 0 0 24px rgba(0, 229, 204, 0.25);
  }
  .gauge-container {
    position: relative;
    width: 180px;
    height: 180px;
  }
  .gauge-svg {
    transform: rotate(-90deg);
  }
  .gauge-bg {
    fill: none;
    stroke: var(--panel-border);
    stroke-width: 10;
  }
  .gauge-fill {
    fill: none;
    stroke-width: 10;
    stroke-linecap: round;
    stroke-dasharray: 440;
    transition: stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1),
                stroke 0.5s ease;
  }
  .audio-fade-in {
    animation: audioFadeIn 0.45s ease-out both;
  }
  @keyframes audioFadeIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .drop-zone-active {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 32px rgba(0, 229, 204, 0.20);
    background: rgba(0, 229, 204, 0.04) !important;
  }
  @keyframes audioLoader {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(400%); }
  }
  .audio-loader-bar {
    animation: audioLoader 1.6s ease-in-out infinite;
    width: 30%;
  }
`;

/* ─── Helpers ──────────────────────────────────────────────────────── */
function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
}

function threatColor(prob: number): string {
  if (prob > 65) return 'var(--accent-red)';
  if (prob > 40) return 'var(--accent-orange)';
  return '#00E5CC';
}

/* ─── Component ────────────────────────────────────────────────────── */
const AudioLabPage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progressMsg, setProgressMsg] = useState('');
  const [progressStep, setProgressStep] = useState(0);
  const [result, setResult] = useState<AudioResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  /* ─── File selection ─────────────────────────────────────────── */
  const acceptFile = useCallback((file: File) => {
    const { valid, error: err } = isValidAudioFile(file);
    if (!valid) {
      setError(err ?? 'Invalid file');
      return;
    }
    setSelectedFile(file);
    setResult(null);
    setError(null);
  }, []);

  const handleBrowseClick = () => fileInputRef.current?.click();

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) acceptFile(file);
  };

  /* ─── Drag-and-drop ──────────────────────────────────────────── */
  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) acceptFile(file);
  };

  /* ─── Analysis ───────────────────────────────────────────────── */
  const handleStartAnalysis = async () => {
    if (!selectedFile) return;
    setIsAnalyzing(true);
    setProgressStep(0);
    setError(null);

    try {
      const res = await analyzeAudioAsync(selectedFile, (msg) => {
        setProgressMsg(msg);
        setProgressStep(prev => prev + 1);
      });
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Analysis failed. Check that the backend is running.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setResult(null);
    setError(null);
    setProgressStep(0);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  /* ─── Derived gauge values ───────────────────────────────────── */
  const gaugeOffset = useMemo(() => {
    if (!result) return 440;
    return 440 - (440 * result.ai_probability / 100);
  }, [result]);

  const gaugeColor = useMemo(() => {
    if (!result) return 'var(--accent-blue)';
    return threatColor(result.ai_probability);
  }, [result]);

  /* ─── Render ─────────────────────────────────────────────────── */
  return (
    <div className="flex h-screen overflow-hidden" style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)' }}>
      <style>{PAGE_STYLES}</style>

      <Sidebar activeTab="Audio Lab" />

      <div className="flex-1 flex flex-col min-w-0" style={{ background: 'var(--bg-primary)' }}>

        {/* ── Header ── */}
        <header
          className="flex items-center justify-between px-8 py-4 backdrop-blur-md z-50 shrink-0"
          style={{ borderBottom: '1px solid var(--panel-border)', background: 'var(--glass-bg)' }}
        >
          <nav className="hidden md:flex items-center space-x-2 text-sm font-medium" style={{ color: 'var(--text-inactive)' }}>
            <span>Forensic Labs</span>
            <ChevronRight className="w-4 h-4" />
            <span style={{ color: 'var(--text-active)' }}>Audio Forensic Lab</span>
          </nav>

          <div className="flex items-center space-x-3">
            <div
              className="flex items-center space-x-2 px-3 py-1.5 rounded-full"
              style={{ background: 'var(--accent-blue-transparent)', border: '1px solid var(--accent-blue-border)' }}
            >
              <div className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: 'var(--accent-blue)' }} />
              <span className="text-[10px] font-mono uppercase tracking-widest" style={{ color: 'var(--text-muted)' }}>
                Engine: <span className="text-[var(--text-active)]">Ready</span>
              </span>
            </div>
            {result && (
              <button
                onClick={handleReset}
                className="px-4 py-2 font-semibold text-sm rounded-lg transition-all hover:opacity-90"
                style={{
                  background: 'var(--btn-secondary-bg)',
                  border: '1px solid var(--panel-border)',
                  color: 'var(--text-muted)',
                }}
              >
                New Scan
              </button>
            )}
          </div>
        </header>

        <main className="flex-1 flex overflow-hidden relative">

          {/* ═══ Left: Input / Results ═══════════════════════════════════ */}
          <section className="flex-1 p-8 pt-7 flex flex-col items-center justify-start overflow-y-auto custom-scrollbar">

            {/* Page title */}
            <div className="max-w-3xl w-full text-center mb-8">
              <h1
                className="font-display text-4xl font-extrabold mb-3 leading-tight"
                style={{ color: 'var(--text-heading)' }}
              >
                AI Voice <span className="text-gradient">Forensics</span>
              </h1>
              <p className="text-[10px] font-mono uppercase tracking-widest opacity-60">
                WavLM · Wav2Vec2 · Prosody · Speaker Drift · Codec Analysis
              </p>
            </div>

            {/* ── Upload Zone ── */}
            {!result && !isAnalyzing && (
              <div className="max-w-xl w-full audio-fade-in">
                <div
                  className={`p-10 flex flex-col items-center text-center border-2 border-dashed transition-all duration-300 audio-glass-panel audio-glow ${isDragging ? 'drop-zone-active' : ''}`}
                  style={{ borderColor: isDragging ? 'var(--accent-blue)' : 'var(--panel-border)' }}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  {/* Icon */}
                  <div
                    className="w-20 h-20 rounded-3xl flex items-center justify-center mb-6 transition-all duration-500 shadow-xl"
                    style={{
                      background: isDragging
                        ? 'rgba(0, 229, 204, 0.2)'
                        : 'var(--accent-blue-transparent)',
                      transform: isDragging ? 'scale(1.1) rotate(3deg)' : 'none',
                    }}
                  >
                    {isDragging
                      ? <Upload className="w-10 h-10" style={{ color: 'var(--accent-blue)' }} />
                      : <FileAudio className="w-10 h-10" style={{ color: 'var(--accent-blue)' }} />
                    }
                  </div>

                  {isDragging ? (
                    <p className="text-base font-bold mb-6" style={{ color: 'var(--accent-blue)' }}>
                      Drop to analyze
                    </p>
                  ) : (
                    <p className="text-sm text-[var(--text-secondary)] mb-6">
                      Drag &amp; drop an audio file, or click <strong>Select</strong>
                    </p>
                  )}

                  {/* Hidden file input */}
                  <input
                    type="file"
                    id="audio-file-input"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    accept=".mp3,.wav,.flac,.ogg,.m4a"
                    style={{ display: 'none' }}
                  />

                  {/* File path input + Select button */}
                  <div className="flex w-full max-w-md gap-2 mb-6">
                    <div
                      className="flex-1 rounded-xl px-4 py-3 text-left text-sm font-mono overflow-hidden whitespace-nowrap text-ellipsis"
                      style={{
                        background: 'var(--bg-secondary)',
                        border: '1px solid var(--panel-border)',
                        color: selectedFile ? 'var(--text-primary)' : 'var(--text-muted)',
                      }}
                    >
                      {selectedFile ? selectedFile.name : 'No file selected...'}
                    </div>
                    <button
                      id="audio-select-btn"
                      className="px-6 py-3 font-bold text-sm rounded-xl transition-all hover:translate-y-[-1px] active:translate-y-0"
                      style={{
                        background: 'var(--btn-secondary-bg)',
                        border: '1px solid var(--panel-border)',
                        color: 'var(--text-primary)',
                      }}
                      onClick={handleBrowseClick}
                    >
                      Select
                    </button>
                  </div>

                  {/* Selected file info */}
                  {selectedFile && (
                    <div
                      className="flex items-center gap-3 mb-5 px-4 py-2 rounded-xl w-full max-w-md"
                      style={{ background: 'var(--accent-blue-transparent)', border: '1px solid var(--accent-blue-border)' }}
                    >
                      <FileAudio className="w-4 h-4 flex-shrink-0" style={{ color: 'var(--accent-blue)' }} />
                      <div className="flex-1 min-w-0">
                        <p className="text-xs font-bold truncate text-[var(--text-primary)]">{selectedFile.name}</p>
                        <p className="text-[10px] font-mono text-[var(--text-muted)]">
                          {formatFileSize(selectedFile.size)} · {selectedFile.type || selectedFile.name.split('.').pop()?.toUpperCase()}
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Format note */}
                  <p className="text-[10px] text-[var(--text-muted)] font-mono mb-6 opacity-60">
                    Supported: WAV, MP3, FLAC, OGG, M4A · Max 50 MB
                  </p>

                  {/* Scan button */}
                  <button
                    id="audio-scan-btn"
                    disabled={!selectedFile}
                    onClick={handleStartAnalysis}
                    className="w-full py-4 font-bold text-base rounded-2xl shadow-xl transition-all flex items-center justify-center gap-3 disabled:opacity-30 disabled:cursor-not-allowed disabled:translate-y-0 hover:translate-y-[-2px] hover:opacity-95"
                    style={{
                      background: 'var(--accent-blue)',
                      color: '#fff',
                      boxShadow: '0 8px 24px rgba(0, 229, 204, 0.3)',
                    }}
                  >
                    <Search className="w-5 h-5" />
                    INITIATE FORENSIC SCAN
                  </button>

                  {/* Error */}
                  {error && (
                    <div
                      className="mt-5 p-4 rounded-xl flex items-start gap-3 w-full text-left"
                      style={{
                        background: 'var(--accent-red-transparent)',
                        border: '1px solid var(--accent-red-border)',
                        color: 'var(--accent-red)',
                      }}
                    >
                      <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                      <p className="text-xs font-mono leading-relaxed">{error}</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* ── Loading State ── */}
            {isAnalyzing && (
              <div className="max-w-xl w-full p-16 flex flex-col items-center text-center audio-glass-panel audio-fade-in">
                {/* Spinner */}
                <div className="relative mb-8">
                  <div
                    className="h-20 w-20 rounded-full border-t-2 border-r-2 animate-spin"
                    style={{ borderColor: 'var(--accent-blue)' }}
                  />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Mic2 className="w-7 h-7 animate-pulse" style={{ color: 'var(--accent-blue)' }} />
                  </div>
                </div>

                <h3 className="text-lg font-bold mb-2" style={{ color: 'var(--text-heading)' }}>
                  Analyzing Forensic Signals
                </h3>
                <p
                  className="text-sm font-mono tracking-wider animate-pulse mb-1"
                  style={{ color: 'var(--accent-blue)' }}
                >
                  {progressMsg || 'Initializing...'}
                </p>
                <p className="text-[10px] font-mono text-[var(--text-muted)] mb-8">
                  Step {progressStep} of 10
                </p>

                {/* Progress bar */}
                <div
                  className="w-full h-1 rounded-full overflow-hidden"
                  style={{ background: 'var(--panel-border)' }}
                >
                  <div
                    className="h-full rounded-full audio-loader-bar"
                    style={{ background: 'var(--accent-blue)' }}
                  />
                </div>

                <p className="text-[10px] font-mono text-[var(--text-muted)] mt-4 opacity-60">
                  {selectedFile?.name}
                </p>
              </div>
            )}

            {/* ── Results ── */}
            {result && !isAnalyzing && (
              <div className="w-full max-w-4xl space-y-8 audio-fade-in pb-20">

                {/* Temporal Forensic Map */}
                <div className="audio-glass-panel p-7">
                  <div className="flex justify-between items-center mb-5">
                    <h3
                      className="text-xs font-mono uppercase tracking-[0.2em] font-bold flex items-center"
                      style={{ color: 'var(--accent-blue)' }}
                    >
                      <Activity className="w-4 h-4 mr-2" />
                      Temporal Forensic Map
                    </h3>
                    <span className="text-[10px] font-mono text-[var(--text-muted)]">
                      {result.audio_metadata.num_chunks} segments · {result.audio_metadata.duration_sec.toFixed(1)}s
                    </span>
                  </div>

                  <WaveformHeatmap
                    timeline={result.timeline}
                    duration={result.audio_metadata.duration_sec}
                  />

                  {result.timeline.length > 0 && (
                    <p
                      className="text-xs text-[var(--text-muted)] mt-5 leading-relaxed p-4 rounded-xl font-mono"
                      style={{ background: 'var(--bg-secondary)', border: '1px solid var(--panel-border)' }}
                    >
                      <span className="font-bold mr-2" style={{ color: 'var(--accent-blue)' }}>LOG:</span>
                      Signal agreement across {result.agreement}.
                      Temporal scan reveals{' '}
                      <span style={{ color: result.timeline.filter(t => t.level === 'critical').length > 0 ? 'var(--accent-red)' : '#00E5CC' }}>
                        {result.timeline.filter(t => t.level === 'critical').length}
                      </span>{' '}
                      critical and{' '}
                      <span style={{ color: result.timeline.filter(t => t.level === 'high').length > 0 ? 'var(--accent-orange)' : '#00E5CC' }}>
                        {result.timeline.filter(t => t.level === 'high').length}
                      </span>{' '}
                      high-risk synthesized markers.
                    </p>
                  )}

                  {result.timeline.length === 0 && (
                    <p className="text-xs text-[var(--text-muted)] mt-4 font-mono italic">
                      Timeline data unavailable — audio may be too short or mono signal was silent.
                    </p>
                  )}
                </div>

                {/* Signal Integrity + Prosody */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <PitchStability f0_std={result.signal_details.prosody?.f0_std_semitones ?? 2.5} />

                  {/* Signal Integrity bar chart */}
                  <div
                    className="p-5 rounded-xl flex flex-col"
                    style={{ border: '1px solid var(--panel-border)', background: 'var(--bg-secondary)' }}
                  >
                    <div className="flex items-center gap-2 mb-5">
                      <BarChart2 className="w-4 h-4" style={{ color: 'var(--accent-blue)' }} />
                      <h5 className="text-[10px] font-mono uppercase tracking-[0.2em] text-[var(--text-muted)]">
                        Signal Integrity Engine
                      </h5>
                    </div>
                    <div className="space-y-4 flex-1">
                      {([
                        { name: 'WavLM ITW',            value: result.signal_scores.wavlm    },
                        { name: 'Wav2Vec2 ASVspoof',     value: result.signal_scores.wav2vec  },
                        { name: 'Spectral Heuristics',   value: result.signal_scores.spectral },
                        { name: 'Speaker Consistency',   value: result.signal_scores.speaker  },
                        { name: 'Prosody Analysis',      value: result.signal_scores.prosody  },
                        { name: 'Codec Forensics',       value: result.signal_scores.codec    },
                      ] as { name: string; value: number }[]).map((s) => {
                        const color = s.value > 65 ? 'var(--accent-red)' : s.value > 40 ? 'var(--accent-orange)' : '#00E5CC';
                        return (
                          <div key={s.name}>
                            <div className="flex justify-between text-[10px] font-mono mb-1.5 uppercase opacity-70">
                              <span>{s.name}</span>
                              <span style={{ color }}>{s.value.toFixed(1)}%</span>
                            </div>
                            <div
                              className="h-1.5 rounded-full overflow-hidden"
                              style={{ background: 'var(--panel-border)' }}
                            >
                              <div
                                className="h-full rounded-full transition-all duration-1000 delay-200"
                                style={{ width: `${s.value}%`, background: color, opacity: 0.85 }}
                              />
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>

                {/* Spectrogram + Anomaly Markers */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <SpectrogramView
                    spectralDetail={result.signal_details.spectral}
                    aiScore={result.signal_scores.spectral}
                  />
                  <AnomalyMarkers
                    codecDetail={result.signal_details.codec}
                    stabilityReport={result.stability_report}
                    aiProbability={result.ai_probability}
                  />
                </div>

                {/* Speaker identity detail */}
                {result.signal_details.speaker && (
                  <div
                    className="p-6 rounded-xl"
                    style={{ border: '1px solid var(--panel-border)', background: 'var(--bg-secondary)' }}
                  >
                    <div className="flex items-center gap-2 mb-4">
                      <Layers className="w-4 h-4" style={{ color: 'var(--accent-blue)' }} />
                      <h5 className="text-[10px] font-mono uppercase tracking-[0.2em] text-[var(--text-muted)]">
                        Speaker Identity Analysis
                      </h5>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      {[
                        {
                          label: 'Mean Similarity',
                          val: result.signal_details.speaker.mean_sim,
                          fmt: (v: number) => v.toFixed(3),
                          warn: (v: number) => v < 0.82,
                        },
                        {
                          label: 'Similarity Std',
                          val: result.signal_details.speaker.std_sim,
                          fmt: (v: number) => v.toFixed(4),
                          warn: (v: number) => v < 0.012,
                        },
                        {
                          label: 'Identity Jumps',
                          val: result.signal_details.speaker.identity_jumps,
                          fmt: (v: number) => `${v}`,
                          warn: (v: number) => v > 2,
                        },
                        {
                          label: 'Voice Score',
                          val: result.signal_scores.speaker,
                          fmt: (v: number) => `${v.toFixed(1)}%`,
                          warn: (v: number) => v > 65,
                        },
                      ].map(({ label, val, fmt, warn }) => {
                        if (val === undefined || val === null) return null;
                        const isWarn = warn(val as number);
                        return (
                          <div
                            key={label}
                            className="p-3 rounded-lg text-center"
                            style={{
                              background: isWarn ? 'var(--accent-orange-transparent)' : 'var(--bg-primary)',
                              border: `1px solid ${isWarn ? 'var(--accent-orange-border)' : 'var(--panel-border)'}`,
                            }}
                          >
                            <div
                              className="text-sm font-bold font-mono"
                              style={{ color: isWarn ? 'var(--accent-orange)' : 'var(--text-primary)' }}
                            >
                              {fmt(val as number)}
                            </div>
                            <div className="text-[9px] font-mono uppercase tracking-wide text-[var(--text-muted)] mt-1">
                              {label}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                    {result.signal_details.speaker.is_unnatural_constancy && (
                      <p className="text-[10px] font-mono mt-3 px-3 py-2 rounded-lg" style={{ background: 'var(--accent-orange-transparent)', color: 'var(--accent-orange)' }}>
                        ⚠ Unnatural identity constancy detected — voice shows mathematically perfect consistency characteristic of TTS clones.
                      </p>
                    )}
                    {result.signal_details.speaker.is_identity_drift && (
                      <p className="text-[10px] font-mono mt-2 px-3 py-2 rounded-lg" style={{ background: 'var(--accent-red-transparent)', color: 'var(--accent-red)' }}>
                        ⚠ Identity drift detected — speaker embedding shifts suggest voice conversion (RVC/SVC) artifacts.
                      </p>
                    )}
                  </div>
                )}
              </div>
            )}
          </section>

          {/* ═══ Right: Forensic Dashboard Sidebar ═══════════════════════ */}
          <aside
            className="w-[420px] flex flex-col h-full z-40 shrink-0"
            style={{ borderLeft: '1px solid var(--panel-border)', background: 'var(--panel-bg)' }}
          >
            {!result ? (
              /* ── Standby Panel ── */
              <div className="flex-1 p-7 flex flex-col overflow-y-auto custom-scrollbar">
                {/* Gauge - empty */}
                <div
                  className="p-7 flex flex-col items-center mb-7 rounded-xl"
                  style={{ background: 'var(--bg-secondary)', border: '1px solid var(--panel-border)' }}
                >
                  <h3 className="text-[10px] font-mono uppercase tracking-[0.2em] text-[var(--text-muted)] mb-7">
                    System Calibration
                  </h3>
                  <div className="gauge-container opacity-25">
                    <svg className="gauge-svg" viewBox="0 0 160 160">
                      <circle className="gauge-bg" cx="80" cy="80" r="70" />
                      <circle className="gauge-fill" cx="80" cy="80" r="70" style={{ strokeDashoffset: 440, stroke: 'var(--accent-blue)' }} />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center font-mono">
                      <span className="text-3xl font-bold">0.0</span>
                      <span className="text-[9px] uppercase tracking-tighter">Standby</span>
                    </div>
                  </div>
                </div>

                {/* System parameters */}
                <h4 className="text-[10px] font-mono uppercase tracking-[0.2em] text-[var(--text-muted)] mb-4">
                  Forensic Parameters
                </h4>
                <div className="space-y-2 mb-7">
                  {[
                    { l: 'Sampling Rate', v: '16.0 kHz',      icon: Activity },
                    { l: 'Bit Depth',     v: '32-bit Float',  icon: HardDrive },
                    { l: 'Channel Mode',  v: 'Mono (Forensic)', icon: Mic2 },
                    { l: 'VAD Window',    v: '25ms / 10ms',   icon: Clock },
                  ].map(({ l, v, icon: Icon }) => (
                    <div
                      key={l}
                      className="flex items-center justify-between p-3 rounded-xl"
                      style={{ border: '1px solid var(--panel-border)', background: 'rgba(255,255,255,0.02)' }}
                    >
                      <div className="flex items-center gap-3">
                        <Icon className="w-4 h-4 opacity-40" style={{ color: 'var(--accent-blue)' }} />
                        <span className="text-xs font-medium opacity-60">{l}</span>
                      </div>
                      <span className="text-xs font-mono font-bold" style={{ color: 'var(--accent-blue)' }}>{v}</span>
                    </div>
                  ))}
                </div>

                {/* Models list */}
                <div
                  className="p-4 rounded-xl"
                  style={{ background: 'rgba(0,229,204,0.08)', border: '1px solid rgba(0,229,204,0.2)' }}
                >
                  <h5 className="text-[10px] font-mono font-bold uppercase tracking-tight mb-3" style={{ color: '#00E5CC' }}>
                    Active Models
                  </h5>
                  {[
                    'WavLM ITW Deepfake Classifier',
                    'Wav2Vec2 ASVspoof 2019',
                    'Prosody / Rhythm Engine',
                    'Speaker Embedding Drift',
                    'Spectral Vocoder Heuristics',
                    'Codec Artifact Scanner',
                  ].map(m => (
                    <div key={m} className="flex items-center gap-2 mb-1.5">
                      <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: '#00E5CC' }} />
                      <span className="text-[10px] font-mono opacity-70">{m}</span>
                    </div>
                  ))}
                </div>

                <div
                  className="mt-5 p-4 rounded-xl relative overflow-hidden"
                  style={{ border: '1px solid var(--panel-border)', background: 'rgba(255,255,255,0.02)' }}
                >
                  <Shield className="absolute top-3 right-3 w-4 h-4 opacity-20" />
                  <h5 className="text-[10px] font-mono font-bold uppercase tracking-tight text-[var(--text-muted)] mb-2">
                    Privacy Notice
                  </h5>
                  <p className="text-[10px] text-[var(--text-muted)] leading-relaxed font-mono opacity-70">
                    Audio is analyzed locally on the server. No data is stored permanently or transmitted to third parties.
                  </p>
                </div>
              </div>
            ) : (
              /* ── Result Panel ── */
              <div className="flex-1 p-7 overflow-y-auto custom-scrollbar">
                {/* Verdict Gauge */}
                <div
                  className="p-7 flex flex-col items-center mb-7 rounded-xl audio-fade-in"
                  style={{
                    background: 'var(--bg-secondary)',
                    border: `1px solid ${gaugeColor}30`,
                  }}
                >
                  <h3 className="text-[10px] font-mono uppercase tracking-[0.2em] text-[var(--text-muted)] mb-7">
                    Forensic Verdict
                  </h3>

                  <div className="gauge-container">
                    <svg className="gauge-svg" viewBox="0 0 160 160">
                      <circle className="gauge-bg" cx="80" cy="80" r="70" />
                      <circle
                        className="gauge-fill"
                        cx="80"
                        cy="80"
                        r="70"
                        style={{ strokeDashoffset: gaugeOffset, stroke: gaugeColor }}
                      />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <span className="text-4xl font-display font-bold" style={{ color: 'var(--text-heading)' }}>
                        {result.ai_probability.toFixed(1)}<span className="text-sm">%</span>
                      </span>
                      <span
                        className="text-[10px] font-mono font-bold uppercase tracking-tight mt-1"
                        style={{ color: gaugeColor }}
                      >
                        AI LIKELIHOOD
                      </span>
                    </div>
                  </div>

                  <div className="mt-5 flex flex-wrap gap-2 justify-center">
                    <span
                      className="text-[10px] font-mono uppercase px-2 py-1 rounded-lg font-bold"
                      style={{
                        background: `${gaugeColor}18`,
                        color: gaugeColor,
                        border: `1px solid ${gaugeColor}40`,
                      }}
                    >
                      {result.threat_level}
                    </span>
                    <span
                      className="text-[10px] font-mono uppercase px-2 py-1 rounded-lg"
                      style={{ background: 'var(--panel-border)', color: 'var(--text-muted)' }}
                    >
                      {result.confidence} CONF
                    </span>
                    <span
                      className="text-[10px] font-mono uppercase px-2 py-1 rounded-lg"
                      style={{ background: 'var(--panel-border)', color: 'var(--text-muted)' }}
                    >
                      {result.agreement}
                    </span>
                  </div>
                </div>

                <AudioReportPanel result={result} onReset={handleReset} />
              </div>
            )}
          </aside>
        </main>

        {/* ── Footer Telemetry Bar ── */}
        <footer
          className="h-9 flex items-center px-6 justify-between text-[10px] font-mono uppercase tracking-widest z-50 shrink-0"
          style={{ borderTop: '1px solid var(--panel-border)', background: 'var(--page-bg)', color: 'var(--text-muted)' }}
        >
          <div className="flex space-x-6">
            <span>
              Fmt: <span className="text-[var(--text-primary)]">
                {selectedFile ? selectedFile.name.split('.').pop()?.toUpperCase() : '—'}
              </span>
            </span>
            <span>
              SR: <span style={{ color: '#00E5CC' }}>16.0 kHz</span>
            </span>
            <span>
              Status:{' '}
              <span
                style={{ color: isAnalyzing ? 'var(--accent-blue)' : result ? 'var(--accent-green)' : '#00E5CC' }}
                className={isAnalyzing ? 'animate-pulse' : ''}
              >
                {isAnalyzing ? 'PROCESSING' : result ? 'COMPLETE' : 'IDLE'}
              </span>
            </span>
          </div>
          <span style={{ color: '#00E5CC' }}>● FakeShield Audio Engine v3.2.0-PRO</span>
        </footer>

      </div>
    </div>
  );
};

export default AudioLabPage;
