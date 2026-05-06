import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Sidebar from '../../components/layout/Sidebar';
import { scanTextAsync, downloadForensicReport, type TextResult } from '../../services/textService';
import { useAuth } from '../../hooks/useAuth.tsx';

const ForensicGauge: React.FC<{ 
  score: number; 
  label: string; 
  color: string; 
  sublabel: string; 
  size?: "sm" | "lg" | "xl";
}> = ({ score, label, color, sublabel, size = "lg" }) => {
  const radius = size === "xl" ? 90 : size === "lg" ? 75 : 35;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;
  const viewSize = size === "xl" ? 220 : size === "lg" ? 200 : 100;

  return (
    <div className="relative flex flex-col items-center justify-center">
      <div className={`relative ${size === "xl" ? 'w-64 h-64' : size === "lg" ? 'w-56 h-56' : 'w-24 h-24'} flex items-center justify-center`}>
        <svg className="w-full h-full transform -rotate-90" viewBox={`0 0 ${viewSize} ${viewSize}`}>
          <circle
            cx={viewSize/2}
            cy={viewSize/2}
            r={radius}
            fill="transparent"
            stroke="currentColor"
            strokeWidth={size === "sm" ? "4" : "8"}
            className="text-[var(--panel-border)]"
          />
          <circle
            cx={viewSize/2}
            cy={viewSize/2}
            r={radius}
            fill="transparent"
            stroke={color}
            strokeWidth={size === "sm" ? "4" : "8"}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          <span className={`${size === "xl" ? 'text-6xl' : size === "lg" ? 'text-5xl' : 'text-xl'} font-display font-black tracking-tighter`} style={{ color }}>
            {Math.round(score)}%
          </span>
          {(size === "lg" || size === "xl") && <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-[var(--text-secondary)] mt-2">{sublabel}</span>}
        </div>
      </div>
      {label && (
        <h2 className={`${size === "xl" ? 'mt-8 text-4xl' : size === "lg" ? 'mt-8 text-3xl' : 'mt-2 text-[10px]'} font-display font-black tracking-[0.05em] uppercase text-center`} style={{ color }}>
          {label}
        </h2>
      )}
    </div>
  );
};

import DashboardLayout from '../../components/layout/DashboardLayout';

const TextLabPage: React.FC = () => {
  const { token } = useAuth();
  const location = useLocation();
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');
  const [result, setResult] = useState<TextResult | null>(null);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const scanId = params.get('scan_id');
    if (scanId && token) {
      const fetchScan = async () => {
        setLoading(true);
        setStatusMsg("RECOVERING FORENSIC DATA...");
        try {
          const res = await fetch(`http://127.0.0.1:8001/api/v1/dashboard/scan/${scanId}`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          if (res.ok) {
            const json = await res.json();
            // Use full_result if available, otherwise fallback to data
            const scanData = json.data.full_result || json.data;
            setResult(scanData);
            if (scanData.text_preview) setText(scanData.text_preview);
          }
        } catch (err) {
          console.error("Failed to load historical scan:", err);
        } finally {
          setLoading(false);
        }
      };
      fetchScan();
    }
  }, [location.search, token]);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await scanTextAsync(text, token, (msg) => setStatusMsg(msg));
      setResult(res);
    } catch (err: any) {
      console.error("Forensic analysis failed:", err);
      alert(`Forensic Engine Error: ${err.message || "Unknown Failure"}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!result?.scan_id) return;
    setDownloading(true);
    try {
      await downloadForensicReport(result.scan_id, token);
    } catch (err) {
      alert("Error generating PDF. Please try again.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <DashboardLayout activeTab="Text lab">
        <div className="max-w-7xl mx-auto px-4 md:px-8 space-y-6 md:space-y-8 pb-16">
          
          <header className="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-4">
            <div>
              <h1 className="text-3xl md:text-4xl font-display font-black text-[var(--text-heading)] tracking-tight">Text lab</h1>
            </div>
            
            <div className="flex flex-wrap gap-3">
               <button 
                onClick={() => { setResult(null); setText(""); }}
                className="px-4 md:px-6 py-2 md:py-2.5 rounded-xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] hover:bg-[var(--btn-secondary-bg)] font-bold uppercase text-[9px] md:text-[10px] tracking-widest transition-all"
               >
                 NEW ANALYSIS
               </button>
               {result && (
                 <button 
                  onClick={handleDownload}
                  disabled={downloading}
                  className="px-4 md:px-6 py-2 md:py-2.5 rounded-xl bg-[rgba(0,229,204,0.05)] text-[#00E5CC] border border-[var(--accent-blue-border)] font-bold uppercase text-[9px] md:text-[10px] tracking-widest hover:bg-[#00E5CC] hover:text-[#020617] transition-all flex items-center gap-2"
                 >
                   {downloading ? "EXPORTING..." : "EXPORT TECHNICAL REPORT"}
                 </button>
               )}
            </div>
          </header>

          {/* TOP ROW: EVIDENCE & MASTER VERDICT */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 md:gap-8">
            
            {/* EVIDENCE AREA (Col 1-8) */}
            <div className="col-span-1 lg:col-span-8 space-y-6">
               <div className="card-border p-1.5 rounded-2xl bg-[var(--panel-border)]">
                 <div className="p-8 rounded-[0.9rem] border border-[var(--panel-border)] bg-[var(--panel-bg)] relative overflow-hidden min-h-[520px] flex flex-col">
                   <div className="absolute inset-0 opacity-[0.03] pointer-events-none" style={{ backgroundImage: 'radial-gradient(var(--text-secondary) 1px, transparent 1px)', backgroundSize: '32px 32px' }} />
                   
                   {!result ? (
                     <>
                        <div className="flex justify-between items-center mb-6 relative z-10">
                          <span className="text-sm font-bold text-[var(--text-secondary)]">Input content</span>
                          <span className="text-[10px] font-mono text-[var(--accent-blue)]">CHARACTER COUNT: {text.length}</span>
                        </div>
                        <textarea
                          className="flex-1 bg-transparent text-xl leading-relaxed resize-none outline-none placeholder-[var(--text-muted)] relative z-10 font-medium custom-scrollbar"
                          placeholder="Paste or type text for professional forensic analysis..."
                          value={text}
                          onChange={(e) => setText(e.target.value)}
                          disabled={loading}
                        />
                        <div className="flex justify-between items-center mt-6 pt-6 border-t border-[var(--panel-border)] relative z-10">
                           <button
                             onClick={handleAnalyze}
                             disabled={loading || text.trim().length < 20}
                             className={`px-12 py-4 rounded-2xl font-black uppercase tracking-[0.2em] text-sm transition-all relative overflow-hidden ${
                               loading || text.trim().length < 20
                               ? 'bg-[var(--btn-secondary-bg)] text-[var(--text-muted)] cursor-not-allowed opacity-50' 
                               : 'bg-gradient-to-r from-[#00E5CC] to-[#0092ff] text-[#020617] hover:scale-[1.02] hover:shadow-[0_0_30px_rgba(0,229,204,0.3)] active:scale-95'
                             }`}
                           >
                             {loading ? "PROCESSING PATTERNS..." : "ANALYZE CONTENT"}
                           </button>
                        </div>
                     </>
                   ) : (
                     <div className="flex flex-col h-full">
                         <div className="flex justify-between items-center mb-6 relative z-10">
                          <span className="text-sm font-bold text-[#00E5CC]">AI probability heatmap</span>
                          <div className="flex gap-4">
                            <span className="text-[8px] text-red-500 font-bold uppercase tracking-widest flex items-center gap-1">
                                SYNTHETIC
                            </span>
                             <span className="text-[8px] text-green-500 font-bold uppercase tracking-widest flex items-center gap-1">
                                HUMAN
                            </span>
                          </div>
                        </div>
                        <div className="flex-1 overflow-y-auto custom-scrollbar relative z-10 pr-4">
                           <div className="prose prose-invert max-w-none leading-[1.8] text-xl font-medium">
                              {result.sentence_highlights.map((h, i) => {
                                const s = (h.ai_score ?? 0) / 100;
                                const bgColor = h.label === "AI" ? `rgba(239, 68, 68, 0.2)` 
                                  : h.label === "UNCERTAIN" ? `rgba(234, 179, 8, 0.2)`
                                  : h.label === "HUMAN" ? `rgba(34, 197, 94, 0.2)` : "transparent";

                                return (
                                  <span 
                                    key={i} 
                                    className="px-0.5 py-0.5 rounded transition-all group relative cursor-crosshair hover:ring-1 hover:ring-white/20"
                                    style={{ backgroundColor: bgColor }}
                                  >
                                    {h.sentence}{" "}
                                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-3 px-4 py-3 bg-[var(--bg-secondary)] border border-[var(--panel-border)] text-white text-xs font-mono font-bold rounded-xl opacity-0 scale-90 group-hover:opacity-100 group-hover:scale-100 transition-all duration-200 pointer-events-none whitespace-nowrap z-50 shadow-2xl">
                                       <div className="flex flex-col items-center gap-1">
                                          <span className="text-[8px] text-[var(--text-muted)] uppercase tracking-[0.2em] font-black border-b border-[var(--panel-border)] pb-1 w-full text-center mb-1">Signal Meta</span>
                                          <span className={(h.ai_score ?? 0) > 50 ? 'text-red-400' : 'text-green-400'}>{h.ai_score ?? 0}% AI</span>
                                          <span className="text-[7px] font-bold text-[var(--text-muted)] uppercase tracking-widest mt-0.5">PPL: {h.perplexity?.toFixed(1) || '0.0'}</span>
                                       </div>
                                    </div>
                                  </span>
                                );
                              })}
                           </div>
                        </div>
                     </div>
                   )}

                   {loading && (
                      <div className="absolute inset-0 z-50 backdrop-blur-sm flex flex-col items-center justify-center p-12 bg-[rgba(2,6,23,0.9)] animate-in fade-in duration-300">
                        <div className="w-48 h-1 bg-[var(--panel-border)] rounded-full overflow-hidden mb-6">
                           <div className="h-full bg-[var(--accent-blue)] animate-[loading-bar_2s_infinite]" style={{ width: '30%' }} />
                        </div>
                        <p className="font-mono text-sm text-[var(--text-muted)] uppercase tracking-[0.4em] text-center">{statusMsg}</p>
                      </div>
                   )}
                 </div>
               </div>
            </div>

            {/* MASTER VERDICT (Col 9-12) */}
            <div className="col-span-1 lg:col-span-4">
               <div className={`min-h-[520px] sticky top-8 p-8 pb-12 rounded-2xl border border-[var(--panel-border)] flex flex-col items-center justify-center text-center relative overflow-hidden transition-all duration-700 ${
                  !result ? 'bg-[var(--panel-bg)] opacity-60' :
                  result.threat_level === 'CRITICAL' || result.threat_level === 'HIGH' ? 'bg-[rgba(239,68,68,0.02)]' :
                  'bg-[rgba(16,185,129,0.02)]'
                }`}>
                  
                  <span className="text-sm font-bold mb-10 text-[var(--text-secondary)]">Consolidated verdict</span>
                  
                  <ForensicGauge 
                    size="xl"
                    score={result ? Math.round(result.score * 100) : 0}
                    label={result?.verdict || "STANDBY"}
                    sublabel={result ? `AI PROBABILITY SCORE` : "AWAITING INPUT"}
                    color={
                      !result ? 'var(--text-muted)' :
                      result.threat_level === 'CRITICAL' || result.threat_level === 'HIGH' ? '#EF4444' :
                      result.threat_level === 'MEDIUM' ? '#F59E0B' : '#10B981'
                    }
                  />

                  {result && (
                    <div className="mt-8 w-full grid grid-cols-2 gap-4">
                       <div className="p-4 rounded-2xl bg-[var(--bg-secondary)] border border-[var(--panel-border)] flex flex-col items-center justify-center text-center">
                          <span className="block text-[10px] uppercase tracking-widest text-[var(--text-secondary)] font-bold mb-2">Stability</span>
                          <div className="flex flex-col items-center">
                             <span className="text-lg font-black text-white leading-none">{result.confidence}</span>
                             <span className="text-[8px] font-bold text-[#00E5CC] uppercase tracking-[0.2em] mt-1">{result.confidence_level}</span>
                          </div>
                       </div>
                       <div className="p-4 rounded-2xl bg-[var(--bg-secondary)] border border-[var(--panel-border)] flex flex-col items-center justify-center text-center">
                          <span className="block text-[10px] uppercase tracking-widest text-[var(--text-secondary)] font-bold mb-2">Risk level</span>
                          <span className={`text-lg font-black leading-none ${result.threat_level === 'CRITICAL' || result.threat_level === 'HIGH' ? 'text-red-500' : 'text-orange-500'}`}>{result.threat_level}</span>
                       </div>
                    </div>
                  )}
                  
                  {/* Pipeline Status indicator removed */}
                </div>
            </div>
          </div>

          {/* BELOW ROW: MULTI-VECTOR AUDIT STRIP */}
          <div className={`mt-8 p-8 rounded-2xl border border-[var(--panel-border)] bg-[var(--panel-bg)] transition-all duration-700 ${!result && 'opacity-30'}`}>
             <h3 className="text-sm font-bold mb-10 text-[var(--text-secondary)] text-center">Diagnostic signal analytics</h3>
             <div className="grid grid-cols-2 md:grid-cols-4 gap-8 items-center">
                <ForensicGauge size="sm" score={result ? (result.signals.neural || 0) * 100 : 0} label="Neural Pulse" color="#8b5cf6" sublabel="" />
                <ForensicGauge size="sm" score={result ? (result.signals.statistical || 0) * 100 : 0} label="Binoculars" color="#0ea5e9" sublabel="" />
                <ForensicGauge size="sm" score={result ? (result.signals.rhythm || 0) * 100 : 0} label="Rhythm" color="#00E5CC" sublabel="" />
                <ForensicGauge size="sm" score={result ? (result.signals.flow || 0) * 100 : 0} label="Semantic Flow" color="#f59e0b" sublabel="" />
             </div>
          </div>

          {/* BOTTOM SECTION: DIAGNOSTICS & REASONING */}
          {result && (
            <div className="grid grid-cols-1 md:grid-cols-12 gap-8 animate-in slide-in-from-bottom-8 duration-1000">
               
               {/* LINGUISTIC DNA DIAGNOSTICS */}
               <div className="col-span-1 md:col-span-12 lg:col-span-5 flex flex-col gap-6">
                 <div className="p-8 rounded-2xl border border-[var(--panel-border)] bg-[var(--panel-bg)] h-full">
                    <h3 className="text-sm font-bold mb-8 text-[var(--text-secondary)] border-b border-[var(--panel-border)] pb-4">Internal metric breakdown</h3>
                    <div className="space-y-4">
                       <div className="flex justify-between items-center py-2 border-b border-[var(--panel-border)] last:border-0 border-dashed">
                          <span className="text-[10px] text-[var(--text-muted)] font-mono uppercase">Syntactic Complexity</span>
                          <span className="text-sm font-mono font-bold text-cyan-400">{result.structural_details?.depth_variance || 0}</span>
                       </div>
                       <div className="flex justify-between items-center py-2 border-b border-[var(--panel-border)] last:border-0 border-dashed">
                          <span className="text-[10px] text-[var(--text-muted)] font-mono uppercase">Semantic Consistency</span>
                          <span className="text-sm font-mono font-bold text-amber-400">{Math.round((result.semantic_details?.semantic_consistency || 0) * 100)}%</span>
                       </div>
                       <div className="flex justify-between items-center py-2 border-b border-[var(--panel-border)] last:border-0 border-dashed">
                          <span className="text-[10px] text-[var(--text-muted)] font-mono uppercase">Structural Balance</span>
                          <span className="text-sm font-mono font-bold text-pink-400 uppercase">{result.linguistic_profile?.syntactic_complexity || "MODERATE"}</span>
                       </div>
                       <div className="flex justify-between items-center py-2 border-b border-[var(--panel-border)] last:border-0 border-dashed">
                          <span className="text-[10px] text-[var(--text-muted)] font-mono uppercase">Entropy Efficiency</span>
                          <span className="text-sm font-mono font-bold text-blue-400">{result.linguistic_profile?.entropy_bits_per_char || "0.0"}</span>
                       </div>
                    </div>
                 </div>
               </div>

               {/* EXPERT AUDIT persona */}
               <div className="col-span-1 md:col-span-12 lg:col-span-7 space-y-6">
                  <div className="p-10 rounded-2xl border border-[var(--panel-border)] bg-[var(--panel-bg)] h-full flex flex-col justify-center">
                    <div className="flex items-center gap-4 mb-8">
                       <div className="w-10 h-10 rounded-xl bg-[var(--bg-secondary)] flex items-center justify-center text-[var(--text-muted)] border border-[var(--panel-border)]">
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                             <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" />
                          </svg>
                       </div>
                       <div className="flex flex-col">
                          <h3 className="text-sm font-bold uppercase tracking-[0.2em] text-white">System assessment note</h3>
                          <span className="text-[8px] text-[var(--text-muted)] font-mono uppercase">Report Ref / ID: {result.scan_id?.split('_')[1] || "0x0"}</span>
                       </div>
                    </div>
                    
                    <div className="relative">
                      <p className="text-lg font-medium leading-relaxed text-[var(--text-primary)] relative z-10 pl-6 border-l border-[var(--panel-border)]">
                        {result.forensic_reasoning || "No anomalous linguistic patterns detected during structural and semantic trajectory audit."}
                      </p>
                    </div>

                    <div className="mt-10 flex flex-wrap gap-2">
                       {result.indicators && result.indicators.map((ind, i) => (
                         <span key={i} className="px-3 py-1 rounded bg-[var(--bg-secondary)] border border-[var(--panel-border)] text-[9px] font-mono text-[var(--text-muted)] uppercase">
                           METRIC: {ind}
                         </span>
                       ))}
                    </div>
                  </div>
               </div>

            </div>
          )}
        </div>
        <style>{`
          .custom-scrollbar::-webkit-scrollbar { width: 4px; }
          .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
          .custom-scrollbar::-webkit-scrollbar-thumb { background: var(--panel-border); border-radius: 10px; }
          
          .font-display { font-family: 'Outfit', sans-serif; }
          .font-mono { font-family: 'JetBrains Mono', monospace; }

          @keyframes scan-line {
            0% { transform: translateY(-100%); }
            100% { transform: translateY(100%); }
          }
        `}</style>
    </DashboardLayout>
  );
};

export default TextLabPage;

