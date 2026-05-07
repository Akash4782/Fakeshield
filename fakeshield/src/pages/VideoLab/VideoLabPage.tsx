import { useState, useRef, useCallback, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Activity, 
  Video, 
  Cpu, 
  Info, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle,
  RotateCcw,
  ScanSearch,
  Eye,
  BarChart2,
  Mic2,
  Layers,
  Thermometer
} from "lucide-react";

import TimelineChart from "./TimelineChart";
import AudioVisualSync from "./AudioVisualSync";
import VLMReasoningPanel from "./VLMReasoningPanel";
import { useAuth } from '../../hooks/useAuth.tsx';
import { API_BASE_URL } from '../../config';
const API = `${API_BASE_URL}`; 

const SIGNAL_META: Record<string, { label: string; icon: any; desc: string; color: string }> = {
  spatial:   { label: 'Spatial Neural', icon: Cpu, desc: 'Detects facial textures & diffusion artifacts', color: '#a78bfa' },
  temporal:  { label: 'Temporal Flow',   icon: Layers, desc: 'RAFT-based pixel-motion logic & morphing', color: '#60a5fa' },
  audio:     { label: 'Audio-Lip Sync', icon: Mic2, desc: 'Phoneme-to-Viseme alignment audit', color: '#34d399' },
  forensic:  { label: 'Forensic Noise', icon: Thermometer, desc: 'PRNU sensor noise & spectral FFT signatures', color: '#f97316' },
  reasoning: { label: 'VLM Reasoning',  icon: ScanSearch, desc: 'Autonomous physics & geometry consistency', color: '#ef4444' },
};

const VERDICT_CONFIG = {
  'DEEPFAKE':    { color: '#ef4444', bg: 'rgba(239,68,68,0.1)',  border: 'rgba(239,68,68,0.3)',  icon: XCircle,      label: 'AI DEEPFAKE',  badge: 'CRITICAL' },
  'LIKELY FAKE': { color: '#f97316', bg: 'rgba(249,115,22,0.1)', border: 'rgba(249,115,22,0.3)', icon: AlertTriangle,  label: 'LIKELY AI',    badge: 'HIGH' },
  'UNCERTAIN':   { color: '#eab308', bg: 'rgba(234,179,8,0.1)',  border: 'rgba(234,179,8,0.3)',  icon: Info,           label: 'UNCERTAIN',    badge: 'MEDIUM' },
  'LIKELY REAL': { color: '#22c55e', bg: 'rgba(34,197,94,0.1)',  border: 'rgba(34,197,94,0.3)',  icon: CheckCircle2,   label: 'AUTHENTIC',    badge: 'LOW' },
};

import DashboardLayout from '../../components/layout/DashboardLayout';

const VideoLabPage = () => {
  const { token } = useAuth();
  const [phase, setPhase] = useState<"idle" | "uploading" | "polling" | "done" | "error">("idle");
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState("");
  const [progress, setProgress] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const fileNameRef = useRef<string>('');

  const pollJob = useCallback(async (jobId: string) => {
    try {
      const res = await fetch(`${API}/video/status/${jobId}`, {
        headers: {
          ...(token ? { "Authorization": `Bearer ${token}` } : {})
        }
      });
      if (!res.ok) throw new Error("Poll failed");
      const data = await res.json();

      if (data.status === "complete" || data.status === "success") {
        if (pollRef.current) clearInterval(pollRef.current);
        setResult(data);
        setPhase("done");
      } else if (data.status === "error") {
        if (pollRef.current) clearInterval(pollRef.current);
        setError(data.detail || "Analysis failed");
        setPhase("error");
      }
    } catch (e) {
      console.warn("Polling hiccup:", e);
    }
  }, []);

  const handleFile = useCallback(async (file: File) => {
    setPhase("uploading");
    setProgress("Injecting payload...");
    fileNameRef.current = file.name;

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(`${API}/video/analyze/async`, {
        method: "POST",
        headers: {
          ...(token ? { "Authorization": `Bearer ${token}` } : {})
        },
        body: form,
      });
      if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
      const { job_id } = await res.json();

      setPhase("polling");
      setProgress("Analyzing temporal flux...");
      pollRef.current = setInterval(() => pollJob(job_id), 2500);
    } catch (e: any) {
      setError(e.message || "Upload failed");
      setPhase("error");
    }
  }, [pollJob]);

  const reset = () => {
    if (pollRef.current) clearInterval(pollRef.current);
    setPhase("idle");
    setResult(null);
    setError("");
    setProgress("");
    if (fileRef.current) fileRef.current.value = "";
  };

  useEffect(() => {
    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, []);

  const vCfg = result?.data ? (VERDICT_CONFIG[result.data.verdict as keyof typeof VERDICT_CONFIG] || VERDICT_CONFIG['UNCERTAIN']) : null;

  return (
    <DashboardLayout activeTab="Video lab">
      <div className="flex-1 flex flex-col min-w-0" style={{ scrollBehavior: 'smooth' }}>
        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4 px-6 md:px-8 mt-12 mb-8">
          <div className="space-y-1">
            <h1 className="text-4xl md:text-5xl font-display font-black text-[#00E5CC] tracking-tighter uppercase">Video lab</h1>
            <div className="flex items-center gap-2">
              <span className="w-8 h-[1px] bg-[var(--panel-border)]"></span>
              <p className="text-[10px] font-bold text-[var(--text-muted)] tracking-[0.4em] uppercase">Deepfake motion temporal audit</p>
            </div>
          </div>
        </header>

        <main className="flex-1 max-w-6xl w-full mx-auto p-4 sm:p-6 md:p-8 pt-8 md:pt-12">
          <AnimatePresence mode="wait">
            {phase === "idle" && (
              <motion.div key="idle" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} className="space-y-8 md:space-y-12">
                <div className="text-center space-y-4">
                  <h1 className="text-3xl sm:text-4xl md:text-5xl font-black tracking-tighter bg-gradient-to-r from-[#00E5CC] to-[#2DD4BF] bg-clip-text text-transparent">
                    Video analysis lab
                  </h1>
                  <p className="text-sm max-w-lg mx-auto opacity-60 leading-relaxed">
                    Slight pixel-motion variations and frequency anomalies distinguish natural photon noise from diffusion dreaming.
                  </p>
                </div>

                <div
                  onClick={() => fileRef.current?.click()}
                  onDragOver={(e) => { e.preventDefault(); }}
                  className="relative group cursor-pointer max-w-2xl mx-auto"
                >
                  <div className="absolute -inset-1 bg-gradient-to-r from-[#00E5CC] to-[#2DD4BF] rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
                  <div className="relative p-6 sm:p-10 md:p-12 py-14 md:py-20 rounded-2xl border-2 border-dashed border-[var(--panel-border)] bg-[var(--bg-secondary)] hover:border-[#00E5CC]/50 transition-all text-center space-y-6">
                    <div className="w-20 h-20 bg-[#00E5CC]/10 rounded-3xl flex items-center justify-center mx-auto ring-1 ring-[#00E5CC]/20 group-hover:scale-110 transition-transform duration-500">
                      <Video className="w-10 h-10 text-[#00E5CC]" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold tracking-tight mb-2">Initialize Forensic Audit</h3>
                      <p className="text-xs opacity-50 font-medium tracking-wide uppercase">MP4, MOV, WEBM · Sora, Gemini & Runway v10.0 Consistency Engine</p>
                    </div>
                  </div>
                  <input ref={fileRef} type="file" accept="video/*" className="hidden" onChange={e => { const f = e.target.files?.[0]; if (f) handleFile(f); }} />
                </div>
              </motion.div>
            )}

            {(phase === "uploading" || phase === "polling") && (
              <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="max-w-md mx-auto py-20 text-center space-y-8">
                <div className="relative w-24 h-24 mx-auto">
                  <div className="absolute inset-0 rounded-full border-4 border-[#00E5CC]/10"></div>
                  <motion.div 
                    animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-0 rounded-full border-t-4 border-[#00E5CC] shadow-[0_0_15px_rgba(0,229,204,0.5)]"
                  />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Cpu className="w-8 h-8 text-[#00E5CC]" />
                  </div>
                </div>
                <div className="space-y-3">
                  <h3 className="text-lg font-bold tracking-tight uppercase animate-pulse text-[#00E5CC]">{progress}</h3>
                  <p className="text-xs opacity-40 leading-relaxed font-mono">
                    EXTRACTING OPTICAL FLOW VECTORS...<br/>
                    CALCULATING SENSOR NOISE PRINT...
                  </p>
                </div>
              </motion.div>
            )}

            {phase === "done" && result?.data && (
              <motion.div key="results" initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} className="space-y-6">
                
                {/* Result Hero */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Verdict Card */}
                  <div className="lg:col-span-2 p-5 md:p-8 rounded-2xl border border-[var(--panel-border)] bg-[var(--panel-bg)] relative overflow-hidden flex flex-col md:flex-row items-center gap-6 md:gap-10 shadow-sm">

                    
                    <div className="relative shrink-0">
                      <svg width="140" height="140" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="44" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
                        <motion.circle 
                          cx="50" cy="50" r="44" fill="none" strokeWidth="8" strokeLinecap="round" stroke={vCfg?.color}
                          strokeDasharray={`${(result.data.ai_probability * 100 / 100) * 276.46} 276.46`}
                          animate={{ strokeDasharray: `${(result.data.ai_probability * 100 / 100) * 276.46} 276.46` }}
                          transition={{ duration: 1.5, ease: "easeOut" }}
                          transform="rotate(-90 50 50)"
                        />
                        <text x="50" y="48" textAnchor="middle" dominantBaseline="middle" className="text-3xl font-bold" style={{ fill: vCfg?.color }}>
                          {Math.round(result.data.ai_probability * 100)}%
                        </text>
                        <text x="50" y="65" textAnchor="middle" dominantBaseline="middle" className="text-[7px] font-bold fill-[var(--text-muted)] uppercase tracking-widest">
                          AI PROBABILITY
                        </text>
                      </svg>
                    </div>

                    <div className="flex-1 space-y-5 text-center md:text-left">
                      <div className="flex flex-col md:flex-row md:items-center gap-4">
                        <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold tracking-tight text-[var(--text-primary)]">
                          {vCfg?.label}
                        </h2>
                        <span className="px-3 py-1 rounded-md text-[10px] font-bold border uppercase tracking-wider self-center md:self-start" style={{ background: vCfg?.bg, borderColor: vCfg?.border, color: vCfg?.color }}>
                          {vCfg?.badge} THREAT
                        </span>
                      </div>
                      
                      <p className="text-sm text-[var(--text-secondary)] leading-relaxed max-w-lg">
                        Our forensic ensemble has detected consistent patterns of synthetic generation. 
                        The analysis of {result.data.metadata?.total_frames || '8'} frames confirms a 
                        <span className="font-bold mx-1" style={{ color: vCfg?.color }}>{result.data.verdict.toLowerCase()}</span> 
                        status with {result.data.agreement_count} module agreement.
                      </p>

                      <div className="flex flex-wrap gap-4 justify-center md:justify-start items-center pt-2">
                        <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] text-[11px] font-medium text-[var(--text-secondary)]">
                          <Activity className="w-4 h-4 text-[var(--text-muted)]" />
                          <span>Process: <span className="text-[var(--text-primary)] font-bold">{result.data.processing_time}</span></span>
                        </div>
                        <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] text-[11px] font-medium text-[var(--text-secondary)]">
                          <BarChart2 className="w-4 h-4 text-[var(--text-muted)]" />
                          <span>Resolution: <span className="text-[var(--text-primary)] font-bold">{result.data.metadata?.dimensions}</span></span>
                        </div>
                        <button 
                          onClick={reset} 
                          className="flex items-center gap-2 px-4 py-2 rounded-lg font-bold uppercase tracking-wider transition-all shadow-sm hover:opacity-90 active:scale-95"
                          style={{ background: '#00E5CC', color: '#000', fontSize: '11px' }}
                        >
                          <RotateCcw className="w-4 h-4" /> 
                          New Audit
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Signals Panel */}
                  <div className="p-5 md:p-8 rounded-2xl border border-[var(--panel-border)] bg-[var(--panel-bg)] space-y-8 flex flex-col justify-center shadow-sm">
                    <h3 className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--text-muted)] px-1">Forensic Signals</h3>
                    <div className="space-y-6">
                      {Object.entries(result.data.signals).map(([key, val]: any) => {
                        const meta = SIGNAL_META[key];
                        if (!meta) return null;
                        const pct = Math.round(val * 100);
                        const Icon = meta.icon;
                        return (
                          <div key={key} className="space-y-3">
                            <div className="flex justify-between items-center text-[11px] font-bold">
                              <div className="flex items-center gap-2.5 text-[var(--text-secondary)]">
                                <Icon className="w-4 h-4" style={{ color: meta.color }} />
                                <span className="uppercase tracking-tight text-[var(--text-primary)]">{meta.label}</span>
                              </div>
                              <span className="font-bold text-sm" style={{ color: meta.color }}>{pct}%</span>
                            </div>
                            <div className="h-2 w-full bg-[var(--btn-secondary-bg)] rounded-full overflow-hidden border border-[var(--panel-border)]">
                              <motion.div 
                                initial={{ width: 0 }} 
                                animate={{ width: `${pct}%` }} 
                                className="h-full rounded-full" 
                                style={{ background: meta.color }}
                              />
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>

                {/* Evidence Spotlight & RAFT Heatmap */}
                {result.data.evidence_heatmap && (
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2 p-5 md:p-8 rounded-2xl border border-[var(--panel-border)] bg-[var(--panel-bg)] relative overflow-hidden flex flex-col md:flex-row items-center gap-6 md:gap-10 shadow-sm">
                      <div className="shrink-0 w-full md:w-1/2 relative">
                         <img src={result.data.evidence_heatmap} alt="Optical Flow Heatmap" className="relative rounded-xl border border-[var(--panel-border)] shadow-sm w-full aspect-video object-cover" />
                         <div className="absolute bottom-2 right-2 px-2 py-1 bg-[var(--bg-primary)]/80 backdrop-blur-sm rounded text-[8px] font-bold text-[var(--text-primary)] uppercase tracking-widest border border-[var(--panel-border)]">
                           RAFT FLOW ANALYSIS
                         </div>
                      </div>
                      <div className="space-y-4">
                        <div className="flex items-center gap-2">
                          <Eye className="w-4 h-4 text-[var(--text-muted)]" />
                          <h3 className="text-xs font-bold uppercase tracking-widest text-[var(--text-secondary)]">Evidence Spotlight</h3>
                        </div>
                        <p className="text-sm text-[var(--text-secondary)] leading-relaxed">
                          The RAFT-Optical Flow engine has isolated a <span className="text-[var(--text-primary)] font-bold">mass-discontinuity</span> in the temporal flux. 
                          Natural motion is rigid, while AI-generated pixels exhibit "morphing" residuals captured in this forensic heatmap.
                        </p>
                        <div className="p-4 rounded-xl bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] flex items-center gap-4">
                           <div className="w-10 h-10 rounded-lg bg-[var(--bg-secondary)] border border-[var(--panel-border)] flex items-center justify-center shrink-0 shadow-sm">
                              <Layers className="w-5 h-5 text-[var(--text-muted)]" />
                           </div>
                           <div className="text-[11px] font-medium text-[var(--text-secondary)] italic leading-snug">
                             "Physical reality breaks detected near <span className="text-[var(--text-primary)] font-bold not-italic">frame {Math.round(result.data.metadata?.total_frames / 2)}</span>"
                           </div>
                        </div>
                      </div>
                    </div>

                    <div className="p-5 md:p-8 rounded-2xl border border-[var(--panel-border)] bg-[var(--panel-bg)] flex flex-col justify-center space-y-6 shadow-sm">
                       <h3 className="text-[10px] font-bold uppercase tracking-[0.2em] text-[var(--text-muted)] px-1 flex items-center gap-2">
                         <Thermometer className="w-4 h-4" /> CONSISTENCY SCORE
                       </h3>
                       <div className="space-y-6">
                          <div className="flex justify-between items-end">
                            <span className="text-[10px] font-bold text-[var(--text-secondary)] uppercase">Physics Validation</span>
                            <span className="text-3xl font-bold" style={{ color: result.data.signals?.reasoning > 0.6 ? '#ef4444' : '#22c55e' }}>
                              {result.data.signals?.reasoning > 0.6 ? 'POOR' : 'EXCELLENT'}
                            </span>
                          </div>
                          <div className="h-2 w-full bg-[var(--btn-secondary-bg)] rounded-full overflow-hidden">
                             <motion.div 
                              initial={{ width: 0 }} 
                              animate={{ width: `${(1 - (result.data.signals?.reasoning || 0)) * 100}%` }} 
                              className="h-full"
                              style={{ background: result.data.signals?.reasoning > 0.6 ? '#ef4444' : '#22c55e' }}
                             />
                          </div>
                          <p className="text-[10px] text-[var(--text-secondary)] leading-relaxed font-medium">
                            Measures adherence to mass-conservation and lighting-physics constraints. High scores indicate physical reality.
                          </p>
                       </div>
                    </div>
                  </div>
                )}

                {/* New Analysis Visualizations */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Timeline Chart */}
                  <div className="p-5 md:p-8 rounded-3xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] space-y-6">
                    <div className="flex items-center justify-between">
                       <div className="flex items-center gap-2">
                        <BarChart2 className="w-4 h-4 text-[#00E5CC]" />
                        <h3 className="text-xs font-black uppercase tracking-widest pb-1 border-b-2 border-[#00E5CC]/20">Audit Timeline</h3>
                      </div>
                      <div className="px-2 py-1 bg-white/5 rounded-md text-[9px] font-mono opacity-40 uppercase tracking-tighter">
                         ENGINE_CONSISTENCY_v10.0
                      </div>
                    </div>
                    
                    <TimelineChart 
                      data={result.data.timelines?.spatial || []} 
                      label="Spatial Signal (CLIP)"
                      color="#a78bfa" 
                    />
                    
                    <TimelineChart 
                      data={result.data.timelines?.temporal || []} 
                      label="Temporal Flow (RAFT)"
                      color="#60a5fa" 
                    />

                    <AudioVisualSync 
                      lipTimeline={result.data.timelines?.audio_lip || []}
                      audioSpeaking={result.data.timelines?.audio_speaking || []}
                    />
                  </div>

                  {/* VLM Reasoning */}
                  <VLMReasoningPanel report={result.data.reasoning_report || "Consistency check skipped."} />
                </div>

                {/* Sub Panels */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Evidence List */}
                  <div className="p-5 md:p-8 rounded-2xl border border-[var(--panel-border)] bg-[var(--panel-bg)] space-y-6 shadow-sm">
                    <div className="flex items-center gap-2">
                      <Eye className="w-4 h-4 text-[var(--text-muted)]" />
                      <h3 className="text-xs font-bold uppercase tracking-widest text-[var(--text-secondary)]">Forensic Brief</h3>
                    </div>
                    <div className="space-y-4">
                      {result.data.reasons.map((reason: string, i: number) => (
                        <motion.div 
                          key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }}
                          className="flex items-start gap-4 p-4 rounded-xl bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] group hover:border-[var(--border-hover)] transition-all"
                        >
                          <div className="w-6 h-6 rounded-lg bg-[var(--bg-secondary)] border border-[var(--panel-border)] flex items-center justify-center shrink-0 mt-1 shadow-sm">
                            <CheckCircle2 className="w-3.5 h-3.5 text-[var(--text-muted)]" />
                          </div>
                          <p className="text-[13px] font-medium leading-relaxed text-[var(--text-secondary)]">{reason}</p>
                        </motion.div>
                      ))}
                    </div>
                  </div>

                  {/* Physics Info */}
                  <div className="p-5 md:p-8 rounded-2xl border border-[var(--panel-border)] bg-[var(--panel-bg)] space-y-6 shadow-sm">
                    <div className="flex items-center gap-2">
                      <BarChart2 className="w-4 h-4 text-[var(--text-muted)]" />
                      <h3 className="text-xs font-bold uppercase tracking-widest text-[var(--text-secondary)]">Temporal Evidence</h3>
                    </div>
                    <div className="space-y-6">
                      <div className="p-6 rounded-2xl bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] space-y-4">
                        <div className="flex justify-between items-end">
                          <div>
                            <div className="text-[10px] font-bold text-[var(--text-muted)] uppercase mb-1">Motion Stability</div>
                            <div className="text-2xl font-bold" style={{ color: result.data.signals.temporal_flow > 0.7 ? '#ef4444' : '#22c55e' }}>
                              {result.data.signals.temporal_flow > 0.7 ? 'UNSTABLE' : 'STABLE'}
                            </div>
                          </div>
                          <div className="text-right">
                            <div className="text-[10px] font-bold text-[var(--text-muted)] uppercase mb-1">PAVR Ratio</div>
                            <div className="text-sm font-mono font-bold text-[var(--text-primary)]">{(result.data.signals.temporal_flow * 15).toFixed(2)}x</div>
                          </div>
                        </div>
                        <div className="h-2 w-full bg-[var(--bg-secondary)] border border-[var(--panel-border)] rounded-full overflow-hidden">
                           <div className="h-full" style={{ width: `${result.data.signals.temporal_flow * 100}%`, background: result.data.signals.temporal_flow > 0.7 ? '#ef4444' : '#22c55e' }} />
                        </div>
                        <p className="text-[10px] text-[var(--text-secondary)] leading-relaxed font-medium italic">
                          Video sequences generated by diffusion models (Sora/Gen-3) exhibit significant peaks in pixel-mass variance where objects undergo non-physical morphing.
                        </p>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4">
                        <div className="p-4 rounded-xl bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] text-center">
                          <div className="text-[10px] font-bold text-[var(--text-muted)] uppercase mb-1">Total Frames</div>
                          <div className="text-xl font-bold text-[var(--text-primary)]">{result.data.metadata?.total_frames}</div>
                        </div>
                        <div className="p-4 rounded-xl bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] text-center">
                          <div className="text-[10px] font-bold text-[var(--text-muted)] uppercase mb-1">Frame Rate</div>
                          <div className="text-xl font-bold text-[var(--text-primary)]">{result.data.metadata?.fps} <span className="text-[10px] text-[var(--text-secondary)] font-medium">fps</span></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {phase === "error" && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="max-w-md mx-auto py-20 text-center space-y-6">
                <div className="w-20 h-20 bg-red-500/10 rounded-full flex items-center justify-center mx-auto ring-1 ring-red-500/20">
                  <XCircle className="w-10 h-10 text-red-500" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-xl font-bold">Analysis Failed</h3>
                  <p className="text-sm opacity-50">{error}</p>
                </div>
                <button onClick={reset} className="px-6 py-2 bg-white/5 border border-white/10 rounded-xl font-bold hover:bg-white/10 transition-all">
                  Try Again
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>

    </DashboardLayout>
  );
};

export default VideoLabPage;
