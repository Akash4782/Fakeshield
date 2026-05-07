import { useState, useRef, useCallback, useEffect, type ChangeEvent } from 'react';
import { useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Sidebar from '../../components/layout/Sidebar';
import {
  RotateCcw,
  Loader2,
  ShieldAlert,
  ShieldCheck,
  CheckCircle2,
  XCircle,
  HelpCircle,
  ScanSearch,
  Upload,
  Zap,
  Brain,
  Eye,
  Waves,
  Fingerprint,
  GitFork,
  CheckCircle,
  X,
  AlertCircle
} from 'lucide-react';
import { analyzeImage, type ImageAnalysisResponse } from '../../services/imageService';
import ForensicLens from './ForensicLens';
import MetadataInspector from './MetadataInspector';
import ImageReportPanel from './ImageReportPanel';
import { useAuth } from '../../hooks/useAuth.tsx';

// ── VERDICT CONFIG: matches backend strings exactly ────────────────
const VERDICT_CONFIG = {
  'AI GENERATED': {
    color: '#ef4444',
    bg: 'rgba(239,68,68,0.08)',
    border: 'rgba(239,68,68,0.25)',
    icon: XCircle,
    label: 'AI GENERATED',
    badge: 'SYNTHETIC',
    glow: '0 0 40px rgba(239,68,68,0.2)',
  },
  'UNCERTAIN': {
    color: '#eab308',
    bg: 'rgba(234,179,8,0.08)',
    border: 'rgba(234,179,8,0.25)',
    icon: HelpCircle,
    label: 'UNCERTAIN',
    badge: 'REVIEW',
    glow: '0 0 40px rgba(234,179,8,0.15)',
  },
  'LIKELY HUMAN': {
    color: '#22c55e',
    bg: 'rgba(34,197,94,0.08)',
    border: 'rgba(34,197,94,0.25)',
    icon: ShieldCheck,
    label: 'REAL PHOTO',
    badge: 'VERIFIED',
    glow: '0 0 40px rgba(34,197,94,0.15)',
  },
} as const;

type VerdictKey = keyof typeof VERDICT_CONFIG;

// ── MODULE CONFIG: all 8 forensic signals ────────────────────────
const MODULE_CONFIG = [
  {
    key: 'rigid',
    label: 'RIGID / DINOv2',
    desc: 'Perturbation sensitivity',
    icon: Brain,
    color: '#00E5CC',
    weight: 'HIGH',
  },
  {
    key: 'classifier',
    label: 'SigLIP / ViT',
    desc: 'Neural classifier ensemble',
    icon: Eye,
    color: '#00E5CC',
    weight: 'HIGH',
  },
  {
    key: 'clip',
    label: 'CLIP Semantic',
    desc: 'Zero-shot domain gap',
    icon: Zap,
    color: '#f97316',
    weight: 'MED',
  },
  {
    key: 'exif',
    label: 'EXIF Guard',
    desc: 'Metadata provenance',
    icon: Fingerprint,
    color: '#22c55e',
    weight: 'HIGH',
  },
  {
    key: 'noise',
    label: 'PRNU Noise',
    desc: 'Sensor fingerprint',
    icon: Waves,
    color: '#e879f9',
    weight: 'MED',
  },
  {
    key: 'fft',
    label: 'FFT Spectral',
    desc: '1/f² power law deviation',
    icon: GitFork,
    color: '#38bdf8',
    weight: 'LOW',
  },
  {
    key: 'ela',
    label: 'ELA',
    desc: 'Compression uniformity',
    icon: ScanSearch,
    color: '#eab308',
    weight: 'LOW',
  },
  {
    key: 'aug',
    label: 'Aug Consistency',
    desc: 'Classifier stability test',
    icon: ShieldAlert,
    color: '#fb7185',
    weight: 'MED',
  },
  {
    key: 'c2pa',
    label: 'C2PA Provenance',
    desc: 'Content Credentials',
    icon: CheckCircle2,
    color: '#3b82f6',
    weight: 'ULTRA',
  },
] as const;

// ── HELPERS ────────────────────────────────────────────────────────
const scoreColor = (s: number): string => {
  if (s >= 0.72) return '#ef4444';
  if (s >= 0.55) return '#f97316';
  if (s >= 0.40) return '#eab308';
  return '#22c55e';
};

const scoreLabel = (s: number): string => {
  if (s >= 0.72) return 'HIGH PROBABILITY';
  if (s >= 0.55) return 'ELEVATED';
  if (s >= 0.40) return 'UNCERTAIN';
  return 'AUTHENTIC';
};

import DashboardLayout from '../../components/layout/DashboardLayout';

// ── MAIN COMPONENT ─────────────────────────────────────────────────
const ImageLabPage = () => {
  const { token } = useAuth();
  const location = useLocation();
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<{ status: string; data: ImageAnalysisResponse } | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const scanId = params.get('scan_id');
    if (scanId && token) {
      const fetchScan = async () => {
        setIsAnalyzing(true);
        try {
          const res = await fetch(`http://127.0.0.1:8001/api/v1/dashboard/scan/${scanId}`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          if (res.ok) {
            const json = await res.json();
            const scanData = json.data.full_result || json.data;
            setResult({ status: 'success', data: scanData });
            // For historical images, we might not have the original base64 if it wasn't saved.
            // But we can show the heatmap if available.
            if (scanData.heatmap_url) setPreviewUrl(scanData.heatmap_url);
          }
        } catch (err) {
          console.error("Failed to load historical scan:", err);
        } finally {
          setIsAnalyzing(false);
        }
      };
      fetchScan();
    }
  }, [location.search, token]);

  // Auto-dismiss errors after 6s
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(null), 6000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  const data = result?.data;

  // ── Map verdict → config (with fallback to UNCERTAIN) ──
  const verdictKey = (data?.verdict ?? 'UNCERTAIN') as VerdictKey;
  const vCfg = VERDICT_CONFIG[verdictKey] ?? VERDICT_CONFIG['UNCERTAIN'];

  const processFile = useCallback(async (file: File) => {
    if (!file.type.startsWith('image/')) return;
    setIsAnalyzing(true);
    setResult(null);

    // Show preview immediately
    const previewReader = new FileReader();
    previewReader.onloadend = () => setPreviewUrl(previewReader.result as string);
    previewReader.readAsDataURL(file);

    // Analyze
    const b64Reader = new FileReader();
    b64Reader.onloadend = async () => {
      try {
        const dataUrl = b64Reader.result as string;
        if (!dataUrl?.startsWith('data:image/')) {
          throw new Error('Invalid image data. Please upload a valid image file.');
        }
        const res = await analyzeImage(dataUrl, token);
        setResult(res);
      } catch (e: any) {
        let msg = e.message || 'An unknown anomaly occurred during signal extraction.';
        if (msg === 'Failed to fetch') {
          msg = 'Backend Connection Lost: Is the forensic server running offline?';
        }
        setError(msg);
        setResult(null);
        setPreviewUrl(null);
      } finally {
        setIsAnalyzing(false);
      }
    };
    b64Reader.readAsDataURL(file);
  }, []);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) processFile(f);
    e.target.value = '';
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) processFile(f);
  }, [processFile]);

  const reset = () => {
    setResult(null);
    setPreviewUrl(null);
    setIsAnalyzing(false);
  };

  const showWorkspace = previewUrl || isAnalyzing;

  return (
    <DashboardLayout activeTab="Image lab">
      <div className="flex flex-col flex-1 min-w-0">

        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 px-4 md:px-8 mt-12 mb-8">
          <div className="space-y-1">
            <h1 className="text-4xl md:text-5xl font-display font-black text-[#00E5CC] tracking-tighter uppercase">Image lab</h1>
            <div className="flex items-center gap-2">
              <span className="w-8 h-[1px] bg-[var(--panel-border)]"></span>
              <p className="text-[10px] font-bold text-[var(--text-muted)] tracking-[0.4em] uppercase">Neural visual authentication suite</p>
            </div>
          </div>
          {showWorkspace && (
            <button
              onClick={reset}
              className="px-4 md:px-6 py-2 md:py-2.5 rounded-xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] hover:bg-[var(--btn-secondary-bg)] font-bold uppercase text-[9px] md:text-[10px] tracking-widest transition-all flex items-center gap-2"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              New Analysis
            </button>
          )}
        </header>

        {/* ── Upload Zone ── */}
        {!showWorkspace ? (
          <div className="flex-1 flex items-center justify-center p-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="w-full max-w-xl"
            >
              {/* Drop zone */}
              <div
                className="relative rounded-2xl border-2 border-dashed flex flex-col items-center justify-center cursor-pointer transition-all p-12 gap-5"
                style={{
                  borderColor: isDragging ? '#00E5CC' : 'var(--panel-border)',
                  background: isDragging ? 'rgba(0,229,204,0.05)' : 'var(--panel-bg)',
                  boxShadow: isDragging ? '0 0 40px rgba(0,229,204,0.15)' : '0 10px 30px rgba(0,0,0,0.04)',
                  color: 'var(--text-primary)'
                }}
                onClick={() => fileInputRef.current?.click()}
                onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
              >
                <input type="file" ref={fileInputRef} onChange={handleFileChange} accept="image/*" className="hidden" />



                <div className="text-center">
                  <h2 className="text-xl font-bold mb-2">Upload Image for Analysis</h2>
                  <p className="text-sm" style={{ color: 'var(--text-muted)' }}>
                    Drag & drop or click to upload · JPG, PNG, WEBP · Max 20MB
                  </p>
                </div>

                <div
                  className="flex items-center gap-2 px-5 py-2.5 rounded-xl font-mono text-sm font-bold"
                  style={{ background: 'linear-gradient(135deg, #00E5CC, #00E5CC)', color: '#000' }}
                >
                  <Upload className="w-4 h-4" />
                  Select Image
                </div>

                </div>
              </motion.div>
            </div>
          ) : (
          /* ── Analysis Workspace ── */
          <div className="flex-1 p-5 flex flex-col gap-8 min-h-0 overflow-y-auto custom-scrollbar">

            {/* TOP ROW: FORENSIC LENS + MASTER GAUGE */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
              
              {/* LEFT: Image Viewer (8/12) */}
              <div className="lg:col-span-8 flex flex-col gap-4 min-w-0">
                <ForensicLens
                  originalUrl={previewUrl}
                  fftUrl={data?.fft_spectrum_url}
                  heatmapUrl={data?.heatmap_url}
                  elaUrl={data?.ela_image}
                  isLoading={isAnalyzing}
                />
              </div>

              {/* RIGHT: Master Verdict Gauge (4/12) */}
              <div className="lg:col-span-4 h-full">
                <div
                  className="rounded-2xl p-8 border flex flex-col items-center justify-center gap-6 h-full min-h-[420px]"
                  style={{
                    borderColor: data ? vCfg.border : 'var(--panel-border)',
                    background: data ? vCfg.bg : 'var(--panel-bg)',
                    boxShadow: data ? vCfg.glow : '0 10px 30px rgba(0,0,0,0.04)',
                    transition: 'all 0.5s ease',
                    color: 'var(--text-primary)'
                  }}
                >
                  {isAnalyzing ? (
                    <div className="flex flex-col items-center gap-3 py-6">
                    <Loader2 className="w-16 h-16 animate-spin text-cyan-500" />
                    <p className="text-sm font-semibold tracking-wide animate-pulse mt-4 text-[var(--text-secondary)]">
                      PROCESSING IMAGE PATTERNS...
                    </p>
                    </div>
                  ) : data ? (
                    <>
                      {/* Circular gauge */}
                      <div className="relative w-56 h-56">
                        <svg width="100%" height="100%" viewBox="0 0 100 100">
                          <path d="M 15 85 A 42 42 0 1 1 85 85" fill="none" stroke="rgba(0,0,0,0.05)" strokeWidth="6" strokeLinecap="round" />
                          <motion.path
                            d="M 15 85 A 42 42 0 1 1 85 85"
                            fill="none"
                            stroke={vCfg.color}
                            strokeWidth="8"
                            strokeLinecap="round"
                            strokeDasharray="198"
                            initial={{ strokeDashoffset: 198 }}
                            animate={{ strokeDashoffset: 198 - (198 * data.ai_probability) }}
                            transition={{ duration: 1.5, ease: 'easeOut' }}
                          />
                        </svg>
                        <div className="absolute inset-0 flex flex-col items-center justify-center mt-2">
                          <motion.span
                            className="font-black tracking-tighter text-5xl"
                            style={{ color: vCfg.color }}
                            initial={{ opacity: 0, scale: 0.7 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.4, delay: 0.5 }}
                          >
                            {Math.round(data.ai_probability * 100)}%
                          </motion.span>
                          <span className="text-xs font-bold mt-2 tracking-widest text-[var(--text-muted)] uppercase">AI PROBABILITY SCORE</span>
                        </div>
                      </div>

                      {/* Verdict label */}
                      <div className="text-center mt-4">
                        <div className="flex items-center gap-3 justify-center mb-2">
                          {(() => { const Icon = vCfg.icon; return <Icon className="w-6 h-6" style={{ color: vCfg.color }} />; })()}
                          <span className="text-2xl font-black tracking-wider" style={{ color: vCfg.color }}>
                            {vCfg.label}
                          </span>
                        </div>
                        <div className="flex items-center justify-center gap-3">
                          <span
                            className="text-xs font-bold px-3 py-1 rounded-full uppercase"
                            style={{ background: `${vCfg.color}15`, color: vCfg.color, border: `1px solid ${vCfg.color}30` }}
                          >
                            {vCfg.badge}
                          </span>
                          <span className="text-xs font-medium text-[var(--text-secondary)]">
                            Confidence: {data.confidence.toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    </>
                  ) : (
                    <div className="flex flex-col items-center gap-4 text-center opacity-30">
                       <ShieldAlert className="w-16 h-16" />
                       <p className="text-xs font-mono tracking-widest uppercase">Awaiting Image Content</p>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* BOTTOM ROW: MODULE SCORECARD + REPORT + METADATA */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              
              {/* LEFT: Forensic Scorecard (5/12) */}
              <div className="lg:col-span-5 flex flex-col gap-6">
                <div className="rounded-2xl border overflow-hidden shadow-sm" style={{ borderColor: 'var(--panel-border)', background: 'var(--panel-bg)', color: 'var(--text-primary)' }}>
                  <div className="px-5 py-4 border-b text-sm font-bold flex justify-between items-center bg-[var(--btn-secondary-bg)]"
                    style={{ borderColor: 'var(--panel-border)', color: 'var(--text-primary)' }}>
                    <span>Signal analysis breakdown</span>
                    <Fingerprint className="w-5 h-5 text-[var(--text-muted)]" />
                  </div>

                  <div className="p-4 space-y-3">
                    {isAnalyzing ? (
                      [...Array(8)].map((_, i) => (
                        <div key={i} className="animate-pulse h-12 rounded-xl bg-[var(--btn-secondary-bg)]" />
                      ))
                    ) : data?.signals ? (
                      MODULE_CONFIG.map((mod) => {
                        const rawScore = (data.signals as any)[mod.key] as number | undefined;
                        const score = rawScore ?? 0;
                        const pct = Math.round(score * 100);
                        const col = scoreColor(score);
                        const Icon = mod.icon;
                        return (
                          <motion.div
                            key={mod.key}
                            initial={{ opacity: 0, x: -8 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.3 }}
                            className="px-4 py-3 rounded-xl border border-[var(--panel-border)] bg-[var(--btn-secondary-bg)]"
                          >
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center gap-3">
                                <div className="w-8 h-8 rounded-lg flex items-center justify-center bg-[var(--bg-secondary)] shadow-sm border border-[var(--panel-border)]">
                                  <Icon className="w-5 h-5" style={{ color: mod.color }} />
                                </div>
                                <div>
                                  <div className="text-sm font-bold text-[var(--text-primary)]">{mod.label}</div>
                                  <div className="text-[11px] text-[var(--text-secondary)] font-medium">{mod.desc}</div>
                                </div>
                              </div>
                              <div className="text-right">
                                <div className="text-sm font-black tracking-tight" style={{ color: col }}>{rawScore !== undefined ? `${pct}%` : '—'}</div>
                                <div className="text-[10px] font-bold uppercase tracking-tight" style={{ color: `${col}cc` }}>{scoreLabel(score)}</div>
                              </div>
                            </div>
                            <div className="w-full h-1.5 rounded-full bg-[var(--bg-secondary)] border border-[var(--panel-border)] overflow-hidden">
                              <motion.div
                                className="h-full rounded-full"
                                style={{ background: col }}
                                initial={{ width: 0 }}
                                animate={{ width: rawScore !== undefined ? `${pct}%` : 0 }}
                                transition={{ duration: 0.8, ease: 'easeOut' }}
                              />
                            </div>
                          </motion.div>
                        );
                      })
                    ) : (
                      <div className="text-center py-12 text-xs font-mono opacity-40">
                        Upload an image to start signal extraction
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* RIGHT: Reasoning & Metadata (7/12) */}
              <div className="lg:col-span-7 flex flex-col gap-8">
                {/* Reasoning Panel */}
                <AnimatePresence>
                  {data && (
                    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
                      <ImageReportPanel
                        reasons={data.reasons}
                        perGeneratorAccuracy={data.per_generator_accuracy}
                        verdict={data.verdict}
                      />
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Metadata Inspector */}
                {(data || isAnalyzing) && (
                  <div className="mt-auto">
                    {isAnalyzing ? (
                      <div className="rounded-2xl border p-6 bg-[var(--panel-bg)] animate-pulse" style={{ borderColor: 'var(--panel-border)' }}>
                        <div className="h-4 bg-[var(--btn-secondary-bg)] rounded w-48 mb-4" />
                        <div className="grid grid-cols-2 gap-4">
                          {[...Array(4)].map((_, i) => <div key={i} className="h-12 bg-[var(--btn-secondary-bg)] rounded-xl" />)}
                        </div>
                      </div>
                    ) : data?.metadata ? (
                      <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}>
                        <MetadataInspector metadata={data.metadata} />
                      </motion.div>
                    ) : null}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ── Premium Error Toast Popup ── */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95, filter: 'blur(4px)' }}
            className="fixed bottom-8 right-8 z-50 flex items-start gap-4 p-5 rounded-2xl border"
            style={{
              background: 'rgba(15, 15, 20, 0.95)',
              backdropFilter: 'blur(24px)',
              borderColor: 'rgba(239, 68, 68, 0.3)',
              boxShadow: '0 20px 40px rgba(0,0,0,0.4), 0 0 0 1px rgba(239,68,68,0.1) inset, 0 0 60px rgba(239,68,68,0.15)',
              width: '420px',
              fontFamily: "'Inter', sans-serif"
            }}
          >
            <div className="shrink-0 p-2.5 rounded-full" style={{ background: 'linear-gradient(135deg, rgba(239,68,68,0.2), rgba(239,68,68,0.05))', border: '1px solid rgba(239,68,68,0.2)' }}>
              <AlertCircle className="w-6 h-6 text-red-500 shadow-[0_0_15px_rgba(239,68,68,0.4)] rounded-full" />
            </div>
            
            <div className="flex-1 pt-0.5 min-w-0">
              <h3 className="text-sm font-black text-red-400 mb-1 tracking-widest uppercase flex items-center gap-2">
                System Error
                <span className="h-[1px] flex-1 bg-gradient-to-r from-red-500/50 to-transparent"></span>
              </h3>
              <p className="text-xs leading-relaxed text-slate-300 break-words drop-shadow-md">
                {error}
              </p>
            </div>

            <button 
              onClick={() => setError(null)}
              className="shrink-0 p-1.5 rounded-lg transition-all hover:bg-white/10 hover:text-white text-slate-500"
            >
              <X className="w-5 h-5" />
            </button>
          </motion.div>
        )}
      </AnimatePresence>

    </DashboardLayout>
  );
};

export default ImageLabPage;
