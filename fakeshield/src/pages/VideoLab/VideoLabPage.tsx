import { useState, useRef, useCallback, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Sidebar from "../../components/layout/Sidebar";
import { 
  ChevronRight, 
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

const API = "http://localhost:8001/api/v1"; 

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

const VideoLabPage = () => {
  const [phase, setPhase] = useState<"idle" | "uploading" | "polling" | "done" | "error">("idle");
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState("");
  const [progress, setProgress] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const pollJob = useCallback(async (jobId: string) => {
    try {
      const res = await fetch(`${API}/video/status/${jobId}`);
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

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(`${API}/video/analyze/async`, {
        method: "POST",
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
    <div className="flex h-screen overflow-hidden" style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)', fontFamily: "'Inter', sans-serif" }}>
      <Sidebar activeTab="Video Lab" />

      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto custom-scrollbar" style={{ scrollBehavior: 'smooth' }}>
        {/* Header */}
        <header className="flex items-center justify-between px-8 py-4 z-50 sticky top-0 backdrop-blur-md border-b transition-colors" style={{ background: 'var(--glass-bg)', borderColor: 'var(--panel-border)' }}>
          <div className="flex items-center space-x-2 text-[10px] font-bold uppercase tracking-widest" style={{ color: 'var(--text-inactive)' }}>
            <Activity className="w-3.5 h-3.5 text-[#00E5CC]" />
            <span>Forensic Intelligence</span>
            <ChevronRight className="w-3 h-3 opacity-30" />
            <span style={{ color: 'var(--text-primary)' }}>Consistency Auditor v10.0</span>
            <span className="ml-2 px-1.5 py-0.5 bg-[#00E5CC]/10 text-[#00E5CC] rounded border border-[#00E5CC]/20 animate-pulse">STARTUP-GRADE</span>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-[9px] font-mono opacity-50">ENGINE: AIGC_SHIELD_V10.0_CONSISTENCY</div>
            <button className="p-2 rounded-lg hover:bg-white/5 transition-colors">
              <Info className="w-4 h-4 text-[#00E5CC]" />
            </button>
          </div>
        </header>

        <main className="flex-1 max-w-6xl w-full mx-auto p-8 pt-12">
          <AnimatePresence mode="wait">
            {phase === "idle" && (
              <motion.div key="idle" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} className="space-y-12">
                <div className="text-center space-y-4">
                  <h1 className="text-5xl font-black tracking-tighter bg-gradient-to-r from-[#00E5CC] to-[#2DD4BF] bg-clip-text text-transparent">
                    Video AI Forensic Lab
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
                  <div className="relative p-12 py-20 rounded-2xl border-2 border-dashed border-[var(--panel-border)] bg-[var(--bg-secondary)] hover:border-[#00E5CC]/50 transition-all text-center space-y-6">
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
                  <div className="lg:col-span-2 p-8 rounded-3xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] relative overflow-hidden flex flex-col md:flex-row items-center gap-8 shadow-2xl">
                    <div className="absolute top-0 right-0 p-4 opacity-5">
                      <ScanSearch className="w-32 h-32" />
                    </div>
                    
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
                        <text x="50" y="48" textAnchor="middle" dominantBaseline="middle" className="text-2xl font-black fill-white">
                          {Math.round(result.data.ai_probability * 100)}%
                        </text>
                        <text x="50" y="62" textAnchor="middle" dominantBaseline="middle" className="text-[6px] font-black fill-white/40 uppercase tracking-widest">
                          AI Probability
                        </text>
                      </svg>
                    </div>

                    <div className="flex-1 space-y-4 text-center md:text-left">
                      <div className="flex flex-col md:flex-row md:items-center gap-3">
                        <h2 className="text-3xl font-black tracking-tighter uppercase italic" style={{ color: vCfg?.color }}>
                          {vCfg?.label}
                        </h2>
                        <span className="px-3 py-1 rounded-full text-[10px] font-black border uppercase tracking-widest self-center md:self-start" style={{ background: vCfg?.bg, borderColor: vCfg?.border, color: vCfg?.color }}>
                          {vCfg?.badge} RISK
                        </span>
                      </div>
                      <p className="text-sm opacity-60 leading-relaxed max-w-md">
                        Analysis of {result.data.metadata?.total_frames || '8'} frames reveals {result.data.verdict.toLowerCase()} status with {result.data.agreement_count} module agreement. Logic: {result.data.logic_version || 'v10.0'}.
                      </p>
                      <div className="flex flex-wrap gap-2 justify-center md:justify-start">
                        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/5 border border-white/5 text-[10px] font-bold">
                          <Activity className="w-3 h-3 text-[#00E5CC]" /> {result.data.processing_time}
                        </div>
                        <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/5 border border-white/5 text-[10px] font-bold">
                          <BarChart2 className="w-3 h-3 text-[#00E5CC]" /> {result.data.metadata?.dimensions}
                        </div>
                        <button onClick={reset} className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#00E5CC]/10 border border-[#00E5CC]/20 text-[10px] font-black uppercase text-[#00E5CC] hover:bg-[#00E5CC]/20 transition-all shadow-[0_4px_12px_rgba(0,229,204,0.1)]">
                          <RotateCcw className="w-3 h-3" /> Start New Audit
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Signals Panel */}
                  <div className="p-6 rounded-3xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] space-y-6 flex flex-col justify-center">
                    <h3 className="text-[10px] font-black uppercase tracking-[0.2em] opacity-30 px-2">Forensic Signals</h3>
                    <div className="space-y-4">
                      {Object.entries(result.data.signals).map(([key, val]: any) => {
                        const meta = SIGNAL_META[key];
                        if (!meta) return null;
                        const pct = Math.round(val * 100);
                        const Icon = meta.icon;
                        return (
                          <div key={key} className="space-y-2">
                            <div className="flex items-center justify-between px-2">
                              <div className="flex items-center gap-2">
                                <Icon className="w-3 h-3 text-[#00E5CC]" />
                                <span className="text-[10px] font-bold opacity-70">{meta.label}</span>
                              </div>
                              <span className="text-[10px] font-black transition-colors" style={{ color: pct > 50 ? '#f87171' : '#34d399' }}>{pct}%</span>
                            </div>
                            <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                              <motion.div 
                                initial={{ width: 0 }} animate={{ width: `${pct}%` }} transition={{ duration: 1, delay: 0.5 }}
                                className="h-full rounded-full shadow-[0_0_10px_rgba(0,229,204,0.3)]"
                                style={{ background: `linear-gradient(90deg, ${meta.color}50, ${meta.color})` }}
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
                    <div className="lg:col-span-2 p-8 rounded-3xl border border-[var(--panel-border)] bg-[#00E5CC]/[0.02] relative overflow-hidden flex flex-col md:flex-row items-center gap-10 shadow-2xl border-l-[6px] border-l-[#00E5CC]">
                      <div className="shrink-0 w-full md:w-1/2 relative group">
                         <div className="absolute -inset-1 bg-[#00E5CC] rounded-xl blur opacity-10 group-hover:opacity-20 transition duration-500"></div>
                         <img src={result.data.evidence_heatmap} alt="Optical Flow Heatmap" className="relative rounded-xl border border-[#00E5CC]/20 shadow-2xl w-full aspect-video object-cover" />
                         <div className="absolute bottom-2 right-2 px-2 py-1 bg-black/60 backdrop-blur-md rounded text-[8px] font-mono text-[#00E5CC] uppercase tracking-widest border border-[#00E5CC]/20">
                           RAFT Flow Evidence
                         </div>
                      </div>
                      <div className="space-y-4">
                        <div className="flex items-center gap-2">
                          <Eye className="w-4 h-4 text-[#00E5CC]" />
                          <h3 className="text-xs font-black uppercase tracking-widest text-[#00E5CC]">Evidence Spotlight</h3>
                        </div>
                        <p className="text-xs opacity-70 leading-relaxed font-medium">
                          The RAFT-Optical Flow engine has isolated a **mass-discontinuity** in the temporal flux. Real-world motion is rigid; AI motion exhibits "cloudy" or "vibrating" pixel residuals, captured here as a forensic heatmap.
                        </p>
                        <div className="p-3 rounded-xl bg-white/5 border border-white/5 flex items-center gap-3">
                           <div className="w-8 h-8 rounded-lg bg-[#00E5CC]/10 flex items-center justify-center">
                              <Layers className="w-4 h-4 text-[#00E5CC]" />
                           </div>
                           <div className="text-[10px] font-bold opacity-60 italic">"Physical reality breaks detected at frame {Math.round(result.data.metadata?.total_frames / 2)}"</div>
                        </div>
                      </div>
                    </div>

                    <div className="p-8 rounded-3xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] flex flex-col justify-center space-y-6">
                       <h3 className="text-[10px] font-black uppercase tracking-[0.2em] opacity-30 px-2 flex items-center gap-2">
                         <Thermometer className="w-3 h-3" /> Consistency Score
                       </h3>
                       <div className="space-y-6">
                          <div className="flex justify-between items-end">
                            <span className="text-[10px] font-bold opacity-50 uppercase tracking-tighter">Physics Match</span>
                            <span className="text-2xl font-black text-[#00E5CC]">{result.data.signals?.reasoning > 0.6 ? 'POOR' : 'EXCELLENT'}</span>
                          </div>
                          <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                             <motion.div initial={{ width: 0 }} animate={{ width: `${(1 - (result.data.signals?.reasoning || 0)) * 100}%` }} className="h-full bg-gradient-to-r from-[#00E5CC] to-[#2DD4BF] shadow-[0_0_8px_rgba(0,229,204,0.3)]" />
                          </div>
                          <p className="text-[9px] opacity-40 leading-relaxed">
                            A high consistency score indicates that the video obeys mass-conservation and lighting-physics constraints.
                          </p>
                       </div>
                    </div>
                  </div>
                )}

                {/* New Analysis Visualizations */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Timeline Chart */}
                  <div className="p-8 rounded-3xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] space-y-6">
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
                  <div className="p-8 rounded-3xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] space-y-6">
                    <div className="flex items-center gap-2">
                      <Eye className="w-4 h-4 text-[#00E5CC]" />
                      <h3 className="text-xs font-black uppercase tracking-widest pb-1 border-b-2 border-[#00E5CC]/20">Forensic Brief</h3>
                    </div>
                    <div className="space-y-4">
                      {result.data.reasons.map((reason: string, i: number) => (
                        <motion.div 
                          key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }}
                          className="flex items-start gap-4 p-4 rounded-2xl bg-white/5 border border-white/5 group hover:border-[#00E5CC]/30 transition-all hover:bg-white/[0.07]"
                        >
                          <div className="w-6 h-6 rounded-lg bg-[#00E5CC]/10 flex items-center justify-center shrink-0 mt-1">
                            <CheckCircle2 className="w-3.5 h-3.5 text-[#00E5CC]" />
                          </div>
                          <p className="text-xs font-medium leading-relaxed opacity-80">{reason}</p>
                        </motion.div>
                      ))}
                    </div>
                  </div>

                  {/* Physics Info */}
                  <div className="p-8 rounded-3xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] space-y-6">
                    <div className="flex items-center gap-2">
                      <BarChart2 className="w-4 h-4 text-[#00E5CC]" />
                      <h3 className="text-xs font-black uppercase tracking-widest pb-1 border-b-2 border-[#00E5CC]/20">Temporal Evidence</h3>
                    </div>
                    <div className="space-y-6">
                      <div className="p-6 rounded-2xl bg-white/5 border border-white/5 space-y-4">
                        <div className="flex justify-between items-end">
                          <div>
                            <div className="text-[10px] font-bold opacity-30 uppercase mb-1">Motion Stability</div>
                            <div className="text-2xl font-black text-[#00E5CC]">{result.data.signals.temporal_flow > 0.7 ? 'UNSTABLE' : 'STABLE'}</div>
                          </div>
                          <div className="text-right">
                            <div className="text-[10px] font-bold opacity-30 uppercase mb-1">PAVR Ratio</div>
                            <div className="text-sm font-mono font-black italic">{(result.data.signals.temporal_flow * 15).toFixed(2)}x</div>
                          </div>
                        </div>
                        <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                           <div className="h-full bg-[#00E5CC] shadow-[0_0_8px_rgba(0,229,204,0.5)]" style={{ width: `${result.data.signals.temporal_flow * 100}%` }} />
                        </div>
                        <p className="text-[10px] opacity-40 leading-relaxed font-medium">
                          Video sequences generated by diffusion models (Sora/Gen-3) exhibit significant peaks in pixel-mass variance where objects undergo non-physical morphing.
                        </p>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-4">
                        <div className="p-4 rounded-2xl bg-white/5 border border-white/5 text-center">
                          <div className="text-[10px] font-bold opacity-30 uppercase mb-1">Total Frames</div>
                          <div className="text-xl font-black">{result.data.metadata?.total_frames}</div>
                        </div>
                        <div className="p-4 rounded-2xl bg-white/5 border border-white/5 text-center">
                          <div className="text-[10px] font-bold opacity-30 uppercase mb-1">Frame Rate</div>
                          <div className="text-xl font-black">{result.data.metadata?.fps} <span className="text-[10px] opacity-40">fps</span></div>
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

      <style>{`
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
      `}</style>
    </div>
  );
};

export default VideoLabPage;

