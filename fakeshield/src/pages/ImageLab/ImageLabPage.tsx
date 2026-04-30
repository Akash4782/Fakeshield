import { useState, useRef, useCallback, useEffect, type ChangeEvent } from 'react';
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
  if (s >= 0.72) return 'HIGH AI';
  if (s >= 0.55) return 'ELEVATED';
  if (s >= 0.40) return 'UNCERTAIN';
  return 'REAL';
};

// ── MAIN COMPONENT ─────────────────────────────────────────────────
const ImageLabPage = () => {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<{ status: string; data: ImageAnalysisResponse } | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

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
        const res = await analyzeImage(dataUrl);
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
    <div
      className="flex h-screen overflow-hidden"
      style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)', fontFamily: "'Inter', sans-serif" }}
    >
      <Sidebar activeTab="Image Lab" />

      <div className="flex flex-col flex-1 min-w-0 overflow-y-auto">

        {/* ── Header ── */}
        <header
          className="flex items-center justify-between px-6 py-3.5 shrink-0 border-b shadow-sm"
          style={{ borderColor: 'var(--panel-border)', background: '#ffffff', color: '#1e293b' }}
        >
          <div className="flex items-center gap-3">
            <div className="w-1.5 h-6 rounded-full" style={{ background: 'linear-gradient(to bottom, #00E5CC, #00E5CC)' }} />
            <div>
              <div className="text-xs font-mono text-emerald-400 tracking-widest">FAKESHIELD IMAGE FORENSICS</div>
              <div className="text-[9px] font-mono mt-0.5" style={{ color: 'var(--text-muted)' }}>
                v8.0 · 8-Signal Multi-Modal Engine · RIGID + DINOv2 + SigLIP + CLIP
              </div>
            </div>
          </div>
          {showWorkspace && (
            <button
              onClick={reset}
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-mono uppercase tracking-wider border transition-all hover:bg-white/5"
              style={{ borderColor: 'var(--panel-border)', color: 'var(--text-muted)' }}
            >
              <RotateCcw className="w-3.5 h-3.5" />
              New Scan
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
                  background: isDragging ? 'rgba(0,229,204,0.05)' : '#ffffff',
                  boxShadow: isDragging ? '0 0 40px rgba(0,229,204,0.15)' : '0 10px 30px rgba(0,0,0,0.04)',
                  color: '#1e293b'
                }}
                onClick={() => fileInputRef.current?.click()}
                onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                onDragLeave={() => setIsDragging(false)}
                onDrop={handleDrop}
              >
                <input type="file" ref={fileInputRef} onChange={handleFileChange} accept="image/*" className="hidden" />

                <div
                  className="w-20 h-20 rounded-2xl flex items-center justify-center"
                  style={{ background: 'linear-gradient(135deg, rgba(0,229,204,0.2), rgba(0,229,204,0.1))', border: '1px solid rgba(0,229,204,0.3)' }}
                >
                  <ScanSearch className="w-10 h-10 text-cyan-400" />
                </div>

                <div className="text-center">
                  <h2 className="text-xl font-bold mb-2">Upload Image for Forensic Scan</h2>
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

                {/* Feature pills */}
                <div className="flex flex-wrap justify-center gap-2">
                  {['DINOv2 Perturbation', 'SigLIP+ViT Ensemble', 'CLIP Semantic', 'PRNU Noise', 'ELA + FFT', 'EXIF Guard'].map(f => (
                    <span key={f} className="text-[9px] font-mono px-2.5 py-1 rounded-full border"
                      style={{ borderColor: 'var(--panel-border)', color: 'var(--text-muted)' }}>
                      {f}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>

        ) : (
          /* ── Analysis Workspace ── */
          <div className="flex-1 p-5 flex flex-col xl:flex-row gap-5 min-h-0">

            {/* LEFT: Forensic Viewer */}
            <div className="flex-1 flex flex-col gap-4 min-w-0">

              {/* 4-Tab Forensic Lens */}
              <ForensicLens
                originalUrl={previewUrl}
                fftUrl={data?.fft_spectrum_url}
                heatmapUrl={data?.heatmap_url}
                elaUrl={data?.ela_image}
                isLoading={isAnalyzing}
              />

              {/* Report Panel */}
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
            </div>

            {/* RIGHT: Scoring Column */}
            <div className="xl:w-[400px] shrink-0 flex flex-col gap-4">

              {/* ── Gauge + Verdict Card ── */}
              <div
                className="rounded-2xl p-5 border flex flex-col items-center gap-4"
                style={{
                  borderColor: data ? vCfg.border : 'var(--panel-border)',
                  background: data ? vCfg.bg : '#ffffff',
                  boxShadow: data ? vCfg.glow : '0 10px 30px rgba(0,0,0,0.04)',
                  transition: 'all 0.5s ease',
                  color: '#1e293b'
                }}
              >
                {isAnalyzing ? (
                  <div className="flex flex-col items-center gap-3 py-6">
                    <Loader2 className="w-14 h-14 animate-spin text-cyan-500" />
                    <p className="text-xs font-mono tracking-widest animate-pulse" style={{ color: 'var(--text-muted)' }}>
                      RUNNING 8-SIGNAL FORENSIC ANALYSIS...
                    </p>
                  </div>
                ) : data ? (
                  <>
                    {/* Circular gauge */}
                    <div className="relative w-44 h-44">
                      <svg width="100%" height="100%" viewBox="0 0 100 100">
                        {/* Background arc */}
                        <path d="M 15 85 A 42 42 0 1 1 85 85" fill="none" stroke="var(--bg-secondary)" strokeWidth="8" strokeLinecap="round" />
                        {/* Score arc */}
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
                          className={`font-black tracking-tighter ${data.ai_probability === 1 ? 'text-3xl' : 'text-4xl'}`}
                          style={{ color: vCfg.color }}
                          initial={{ opacity: 0, scale: 0.7 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ duration: 0.4, delay: 0.5 }}
                        >
                          {Math.round(data.ai_probability * 100)}%
                        </motion.span>
                        <span className="text-[9px] font-mono mt-1 tracking-widest font-medium opacity-60" style={{ color: 'var(--text-muted)' }}>AI SCORE</span>
                      </div>
                    </div>

                    {/* Verdict label */}
                    <div className="text-center">
                      <div className="flex items-center gap-2 justify-center">
                        {(() => { const Icon = vCfg.icon; return <Icon className="w-5 h-5" style={{ color: vCfg.color }} />; })()}
                        <span className="text-lg font-black tracking-wider" style={{ color: vCfg.color }}>
                          {vCfg.label}
                        </span>
                      </div>
                      <div className="mt-1.5 flex items-center justify-center gap-2">
                        <span
                          className="text-[9px] font-mono font-bold px-2 py-0.5 rounded-full"
                          style={{ background: `${vCfg.color}20`, color: vCfg.color }}
                        >
                          {vCfg.badge}
                        </span>
                        <span className="text-[9px] font-mono" style={{ color: 'var(--text-muted)' }}>
                          Confidence: {data.confidence.toFixed(1)}%
                        </span>
                      </div>
                    </div>

                    {/* Processing meta */}
                    <div className="text-[9px] font-mono" style={{ color: 'var(--text-muted)' }}>
                      {data.engine_version} · {data.processing_time} · {data.metadata?.dimensions}
                    </div>
                  </>
                ) : null}
              </div>

              {/* ── 8-Signal Module Scorecard ── */}
              <div className="rounded-2xl border overflow-hidden shadow-sm" style={{ borderColor: 'var(--panel-border)', background: '#ffffff', color: '#1e293b' }}>
                <div className="px-4 py-3 border-b text-[10px] font-mono tracking-widest uppercase"
                  style={{ borderColor: 'var(--panel-border)', color: '#00E5CC' }}>
                  8-Signal Forensic Scorecard
                </div>

                <div className="p-3 space-y-2">
                  {isAnalyzing ? (
                    [...Array(8)].map((_, i) => (
                      <div key={i} className="animate-pulse h-10 rounded-lg" style={{ background: 'rgba(255,255,255,0.04)' }} />
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
                          className="px-3 py-2 rounded-xl"
                          style={{ background: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)' }}
                        >
                          <div className="flex items-center justify-between mb-1.5">
                            <div className="flex items-center gap-2">
                              <Icon className="w-3 h-3 shrink-0" style={{ color: mod.color }} />
                              <div>
                                <span className="text-[9px] font-mono font-bold" style={{ color: 'var(--text-secondary)' }}>
                                  {mod.label}
                                </span>
                                <span className="text-[8px] font-mono ml-1.5" style={{ color: 'var(--text-muted)' }}>
                                  {mod.desc}
                                </span>
                              </div>
                            </div>
                            <div className="flex items-center gap-1.5 shrink-0">
                              <span
                                className="text-[8px] font-mono px-1.5 py-0.5 rounded"
                                style={{ background: `${col}18`, color: col }}
                              >
                                {scoreLabel(score)}
                              </span>
                              <span className="text-[10px] font-mono font-black" style={{ color: col }}>
                                {rawScore !== undefined ? `${pct}%` : '—'}
                              </span>
                            </div>
                          </div>
                          {/* Progress bar */}
                          <div className="w-full rounded-full overflow-hidden" style={{ height: 3, background: 'rgba(255,255,255,0.06)' }}>
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
                    <div className="text-center py-4 text-xs font-mono" style={{ color: 'var(--text-muted)' }}>
                      Upload an image to run forensic analysis
                    </div>
                  )}
                </div>
              </div>

              {/* ── EXIF Metadata Inspector ── */}
              {(data || isAnalyzing) && (
                <AnimatePresence>
                  {isAnalyzing ? (
                    <div className="rounded-2xl border p-4 animate-pulse" style={{ borderColor: 'var(--panel-border)', background: 'rgba(0,0,0,0.2)' }}>
                      <div className="h-4 bg-white/5 rounded w-40 mb-3" />
                      {[...Array(4)].map((_, i) => <div key={i} className="h-10 bg-white/5 rounded-xl mb-2" />)}
                    </div>
                  ) : data?.metadata ? (
                    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}>
                      <MetadataInspector metadata={data.metadata} />
                    </motion.div>
                  ) : null}
                </AnimatePresence>
              )}

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
                System Overload
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

    </div>
  );
};

export default ImageLabPage;
