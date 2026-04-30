import React, { useState } from 'react';
import Sidebar from '../../components/layout/Sidebar';
import { scanTextAsync, downloadForensicReport, type TextResult } from '../../services/textService';

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
            strokeWidth={size === "sm" ? "2" : "4"}
            className="text-[var(--panel-border)]"
          />
          <circle
            cx={viewSize/2}
            cy={viewSize/2}
            r={radius}
            fill="transparent"
            stroke={color}
            strokeWidth={size === "sm" ? "5" : "12"}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
            style={{ filter: `drop-shadow(0 0 ${size === "sm" ? '4px' : '12px'} ${color})` }}
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

const TextLabPage: React.FC = () => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');
  const [result, setResult] = useState<TextResult | null>(null);
  const [downloading, setDownloading] = useState(false);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await scanTextAsync(text, (msg) => setStatusMsg(msg));
      setResult(res);
    } catch (err) {
      console.error(err);
      alert("Forensic Engine offline. Please check infrastructure status.");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!result?.scan_id) return;
    setDownloading(true);
    try {
      await downloadForensicReport(result.scan_id);
    } catch (err) {
      alert("Error generating PDF. Please try again.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden font-sans bg-[var(--page-bg)] text-[var(--text-primary)]">
      <Sidebar activeTab="Text Lab" />
      
      <main className="flex-1 overflow-y-auto p-8 custom-scrollbar relative">
        <div className="max-w-7xl mx-auto space-y-8">
          
          <header className="flex justify-between items-end">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="px-2 py-0.5 rounded bg-[var(--accent-blue-transparent)] text-[var(--accent-blue)] text-[10px] font-bold uppercase tracking-widest border border-[var(--accent-blue-border)]">
                  v16.5.0-RESEARCH-ELITE
                </div>
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase tracking-tighter">Forensic Console Level: Elite</span>
              </div>
              <h1 className="text-4xl font-display font-black text-[var(--text-heading)] tracking-tight">Text Forensic Lab</h1>
            </div>
            
            <div className="flex gap-4">
               <button 
                onClick={() => { setResult(null); setText(""); }}
                className="px-6 py-2.5 rounded-xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] hover:bg-[var(--btn-secondary-bg)] font-bold uppercase text-[10px] tracking-widest transition-all"
               >
                 NEW SCAN
               </button>
               {result && (
                 <button 
                  onClick={handleDownload}
                  disabled={downloading}
                  className="px-6 py-2.5 rounded-xl bg-[rgba(0,229,204,0.1)] text-[#00E5CC] border border-[rgba(0,229,204,0.2)] font-bold uppercase text-[10px] tracking-widest hover:bg-[#00E5CC] hover:text-[#020617] transition-all shadow-[0_0_15px_rgba(0,229,204,0.1)] flex items-center gap-2"
                 >
                   {downloading ? "PRINTING..." : "GENERATE PDF REPORT"}
                 </button>
               )}
            </div>
          </header>

          {/* TOP ROW: EVIDENCE & MASTER VERDICT */}
          <div className="grid grid-cols-12 gap-8">
            
            {/* EVIDENCE AREA (Col 1-8) */}
            <div className="col-span-12 lg:col-span-8 space-y-6">
               <div className="relative group p-1.5 rounded-3xl bg-gradient-to-br from-[var(--panel-border)] to-transparent shadow-2xl">
                 <div className="p-8 rounded-[1.2rem] border border-[var(--panel-border)] bg-[var(--panel-bg)] relative overflow-hidden backdrop-blur-3xl min-h-[520px] flex flex-col">
                   <div className="absolute inset-0 opacity-[0.03] pointer-events-none" style={{ backgroundImage: 'radial-gradient(var(--text-secondary) 1px, transparent 1px)', backgroundSize: '32px 32px' }} />
                   
                   {!result ? (
                     <>
                        <div className="flex justify-between items-center mb-6 relative z-10">
                          <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-[var(--text-secondary)]">Input Evidence</span>
                          <span className="text-[10px] font-mono text-[var(--accent-blue)]">CHARS: {text.length}</span>
                        </div>
                        <textarea
                          className="flex-1 bg-transparent text-xl leading-relaxed resize-none outline-none placeholder-[var(--text-muted)] relative z-10 font-medium custom-scrollbar"
                          placeholder="Paste or type text for professional forensic analysis..."
                          value={text}
                          onChange={(e) => setText(e.target.value)}
                          disabled={loading}
                        />
                        <div className="flex justify-between items-center mt-6 pt-6 border-t border-[var(--panel-border)] relative z-10">
                           <div className="flex items-center gap-4">
                              <div className="flex flex-col">
                                <span className="text-[8px] text-[var(--text-secondary)] font-bold uppercase tracking-wider">Word Count</span>
                                <span className="text-sm font-mono">{text.trim() ? text.trim().split(/\s+/).length : 0}</span>
                              </div>
                              <div className="flex flex-col border-l border-[var(--panel-border)] pl-4">
                                <span className="text-[8px] text-[var(--text-secondary)] font-bold uppercase tracking-wider">Engine Mode</span>
                                <span className="text-sm font-mono text-[#00E5CC]">ELITE-16.0</span>
                              </div>
                           </div>
                           <button
                             onClick={handleAnalyze}
                             disabled={loading || text.trim().length < 20}
                             className={`px-12 py-4 rounded-2xl font-black uppercase tracking-[0.2em] text-sm transition-all relative overflow-hidden ${
                               loading || text.trim().length < 20
                               ? 'bg-[var(--btn-secondary-bg)] text-[var(--text-muted)] cursor-not-allowed opacity-50' 
                               : 'bg-gradient-to-r from-[#00E5CC] to-[#0092ff] text-[#020617] hover:scale-[1.02] hover:shadow-[0_0_30px_rgba(0,229,204,0.3)] active:scale-95'
                             }`}
                           >
                             {loading ? "ANALYZING DNA..." : "RUN FORENSIC SCAN"}
                           </button>
                        </div>
                     </>
                   ) : (
                     <div className="flex flex-col h-full">
                         <div className="flex justify-between items-center mb-6 relative z-10">
                          <span className="text-[10px] font-bold uppercase tracking-[0.3em] text-[#00E5CC]">Linguistic Heatmap (2026 Audit)</span>
                          <div className="flex gap-4">
                            <span className="text-[8px] text-red-500 font-bold uppercase tracking-widest flex items-center gap-1">
                               <div className="w-1.5 h-1.5 rounded-full bg-red-500" /> AI-LIKE
                            </span>
                            <span className="text-[8px] text-yellow-500 font-bold uppercase tracking-widest flex items-center gap-1">
                               <div className="w-1.5 h-1.5 rounded-full bg-yellow-500" /> UNCERTAIN
                            </span>
                             <span className="text-[8px] text-green-500 font-bold uppercase tracking-widest flex items-center gap-1">
                               <div className="w-1.5 h-1.5 rounded-full bg-green-500" /> HUMAN-LIKE
                            </span>
                          </div>
                        </div>
                        <div className="flex-1 overflow-y-auto custom-scrollbar relative z-10 pr-4">
                           <div className="prose prose-invert max-w-none leading-[1.8] text-xl font-medium">
                              {result.sentence_highlights.map((h, i) => {
                                const s = (h.ai_score ?? 0) / 100;
                                const bgColor = h.label === "AI" ? `rgba(239, 68, 68, 0.4)` 
                                  : h.label === "UNCERTAIN" ? `rgba(234, 179, 8, 0.4)`
                                  : h.label === "HUMAN" ? `rgba(34, 197, 94, 0.4)` : "transparent";

                                return (
                                  <span 
                                    key={i} 
                                    className="px-0.5 py-0.5 rounded-md transition-all group relative cursor-crosshair hover:ring-1 hover:ring-white/20"
                                    style={{ backgroundColor: bgColor }}
                                  >
                                    {h.sentence}{" "}
                                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-3 px-4 py-3 bg-[var(--panel-bg)] border border-[var(--panel-border)] text-[var(--text-primary)] text-xs font-bold rounded-2xl opacity-0 scale-90 group-hover:opacity-100 group-hover:scale-100 transition-all duration-200 pointer-events-none whitespace-nowrap z-50 shadow-2xl backdrop-blur-xl border-t-4 border-t-[#00E5CC]">
                                       <div className="flex flex-col items-center gap-2">
                                          <span className="text-[8px] text-[var(--text-secondary)] uppercase tracking-[0.2em] font-black border-b border-[var(--panel-border)] pb-1 w-full text-center">Linguistic DNA</span>
                                          <div className="flex flex-col items-center">
                                            <span className={(h.ai_score ?? 0) > 50 ? 'text-red-400' : 'text-green-400'}>{h.ai_score ?? 0}% AI SCORE</span>
                                            <span className="text-[7px] font-bold text-[var(--text-muted)] uppercase tracking-widest mt-0.5">{h.label}</span>
                                            <span className="text-[9px] font-mono text-[var(--text-muted)] mt-1">PPL: {h.perplexity?.toFixed(1) || '0.0'}</span>
                                          </div>
                                       </div>
                                       <div className="absolute top-full left-1/2 -translate-x-1/2 border-[8px] border-transparent border-t-[var(--panel-border)]" />
                                    </div>
                                  </span>
                                );
                              })}
                           </div>
                        </div>
                     </div>
                   )}

                   {loading && (
                      <div className="absolute inset-0 z-50 backdrop-blur-md flex flex-col items-center justify-center p-12 bg-[rgba(2,6,23,0.8)] animate-in fade-in duration-500">
                        <div className="relative w-24 h-24 mb-8">
                          <div className="absolute inset-0 border-[6px] border-[rgba(0,229,204,0.1)] rounded-full"></div>
                          <div className="absolute inset-0 border-[6px] border-t-[#00E5CC] rounded-full animate-spin"></div>
                          <div className="absolute inset-4 border-2 border-[rgba(255,0,146,0.2)] rounded-full"></div>
                          <div className="absolute inset-4 border-2 border-b-[#ff0092] rounded-full animate-[spin_1.5s_linear_infinite_reverse]"></div>
                        </div>
                        <p className="font-mono text-lg text-[#00E5CC] animate-pulse uppercase tracking-[0.4em] font-black text-center max-w-md">{statusMsg}</p>
                      </div>
                   )}
                 </div>
               </div>
            </div>

            {/* MASTER VERDICT (Col 9-12) */}
            <div className="col-span-12 lg:col-span-4">
               <div className={`h-[520px] sticky top-8 p-8 rounded-[2rem] border-2 flex flex-col items-center justify-center text-center relative overflow-hidden transition-all duration-700 shadow-2xl ${
                  !result ? 'bg-[var(--panel-bg)] border-[var(--panel-border)] opacity-60 grayscale' :
                  result.threat_level === 'CRITICAL' || result.threat_level === 'HIGH' ? 'bg-[rgba(239,68,68,0.05)] border-[rgba(239,68,68,0.3)] shadow-[0_0_50px_rgba(239,68,68,0.1)]' :
                  result.threat_level === 'MEDIUM' ? 'bg-[rgba(234,179,8,0.05)] border-[rgba(234,179,8,0.3)] shadow-[0_0_50px_rgba(234,179,8,0.1)]' :
                  'bg-[rgba(16,185,129,0.05)] border-[rgba(16,185,129,0.3)] shadow-[0_0_50px_rgba(16,185,129,0.1)]'
                }`}>
                  <div className="absolute top-0 inset-x-0 h-1 px-8">
                    <div className={`h-full w-full rounded-full ${
                      !result ? 'bg-[var(--panel-border)]' :
                      result.threat_level === 'CRITICAL' || result.threat_level === 'HIGH' ? 'bg-red-500' :
                      result.threat_level === 'MEDIUM' ? 'bg-yellow-500' : 'bg-green-500'
                    }`} />
                  </div>

                  <span className="text-[10px] font-bold uppercase tracking-[0.4em] mb-6 text-[var(--text-secondary)]">Master Forensic Verdict</span>
                  
                  <ForensicGauge 
                    size="xl"
                    score={result ? Math.round(result.score * 100) : 0}
                    label={result?.verdict || "AWAITING EVIDENCE"}
                    sublabel={result ? `AI PROBABILITY (±${result.confidence === 'HIGH' ? '5' : '10'}%)` : "AI PROBABILITY"}
                    color={
                      !result ? 'var(--text-muted)' :
                      result.threat_level === 'CRITICAL' || result.threat_level === 'HIGH' ? '#EF4444' :
                      result.threat_level === 'MEDIUM' ? '#F59E0B' : '#10B981'
                    }
                  />

                  {result && (
                    <div className="mt-8 w-full grid grid-cols-2 gap-4">
                       <div className="p-4 rounded-2xl bg-[var(--bg-secondary)] border border-[var(--panel-border)]">
                          <span className="block text-[8px] uppercase tracking-widest text-[var(--text-secondary)] font-bold mb-1">Stability</span>
                          <span className="text-lg font-black text-white">{result.confidence}</span>
                       </div>
                       <div className="p-4 rounded-2xl bg-[var(--bg-secondary)] border border-[var(--panel-border)]">
                          <span className="block text-[8px] uppercase tracking-widest text-[var(--text-secondary)] font-bold mb-1">Threat</span>
                          <span className={`text-lg font-black ${result.threat_level === 'CRITICAL' || result.threat_level === 'HIGH' ? 'text-red-500' : 'text-orange-500'}`}>{result.threat_level}</span>
                       </div>
                    </div>
                  )}
                  
                  {!result && (
                    <p className="mt-8 text-[10px] text-[var(--text-muted)] italic font-medium uppercase tracking-widest">
                       Pipeline Status: Standby
                    </p>
                  )}
                </div>
            </div>
          </div>

          {/* BELOW ROW: MULTI-VECTOR AUDIT STRIP */}
          <div className={`p-8 rounded-[2rem] border border-[var(--panel-border)] bg-[var(--panel-bg)] transition-all duration-700 ${!result && 'opacity-30'}`}>
             <h3 className="text-[10px] font-bold uppercase tracking-[0.3em] mb-8 text-[var(--text-secondary)] text-center">Multi-Vector Synthetic Profile</h3>
             <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 items-center">
                <ForensicGauge size="sm" score={result ? (result.signals.binoculars || 0) * 100 : 0} label="Binoculars" color="#3b82f6" sublabel="" />
                <ForensicGauge size="sm" score={result ? (result.signals.classifier || 0) * 100 : 0} label="Neural DNA" color="#8b5cf6" sublabel="" />
                <ForensicGauge size="sm" score={result ? (result.signals.stylometry || 0) * 100 : 0} label="Stylometry" color="#00E5CC" sublabel="" />
                <ForensicGauge size="sm" score={result ? (result.signals.retrieval || 0) * 100 : 0} label="Retrieval" color="#F59E0B" sublabel="" />
                <ForensicGauge size="sm" score={result ? (result.signals.statistical || 0) * 100 : 0} label="Entropy" color="#ff0092" sublabel="" />
                <ForensicGauge size="sm" score={result ? (result.signals.lexical || 0) * 100 : 0} label="Lexical" color="#0092ff" sublabel="" />
             </div>
          </div>

          {/* BOTTOM SECTION: DIAGNOSTICS & REASONING */}
          {result && (
            <div className="grid grid-cols-12 gap-8 animate-in slide-in-from-bottom-8 duration-1000">
               
               {/* LINGUISTIC DNA DIAGNOSTICS */}
               <div className="col-span-12 lg:col-span-5 flex flex-col gap-6">
                 <div className="p-8 rounded-[2rem] border border-[var(--panel-border)] bg-[var(--panel-bg)] h-full">
                    <h3 className="text-[10px] font-bold uppercase tracking-[0.2em] mb-8 text-[var(--text-secondary)] border-b border-[var(--panel-border)] pb-4">Internal Signal Audit</h3>
                    <div className="space-y-6">
                       <div className="flex justify-between items-center">
                          <div className="flex flex-col">
                             <span className="text-xs font-bold text-white">Tree Depth Variance</span>
                             <span className="text-[10px] text-[var(--text-muted)]">Syntactic Complexity Metric</span>
                          </div>
                          <span className="text-sm font-mono font-bold text-[#00E5CC]">{result.structural_details.depth_variance}</span>
                       </div>
                       <div className="flex justify-between items-center">
                          <div className="flex flex-col">
                             <span className="text-xs font-bold text-white">Semantic Consistency</span>
                             <span className="text-[10px] text-[var(--text-muted)]">Contextual Drift Coefficient</span>
                          </div>
                          <span className="text-sm font-mono font-bold text-[#ffcd00]">{Math.round(result.semantic_details.semantic_consistency * 100)}%</span>
                       </div>
                       <div className="flex justify-between items-center">
                          <div className="flex flex-col">
                             <span className="text-xs font-bold text-white">Syntactic Complexity</span>
                             <span className="text-[10px] text-[var(--text-muted)]">Mechanical Balance Guard</span>
                          </div>
                          <span className="text-sm font-mono font-bold text-[#ff0092]">{result.linguistic_profile?.syntactic_complexity || "MODERATE"}</span>
                       </div>
                       <div className="flex justify-between items-center">
                          <div className="flex flex-col">
                             <span className="text-xs font-bold text-white">Entropy Efficiency</span>
                             <span className="text-[10px] text-[var(--text-muted)]">Bits per character ratio</span>
                          </div>
                          <span className="text-sm font-mono font-bold text-[#3b82f6] text-right">{result.linguistic_profile?.entropy_bits_per_char || "0.0"}</span>
                       </div>
                    </div>
                 </div>
               </div>

               {/* EXPERT AUDIT persona */}
               <div className="col-span-12 lg:col-span-7 space-y-6">
                  <div className="p-10 rounded-[2rem] border border-[var(--accent-blue-border)] bg-[var(--panel-bg)] shadow-[0_0_50px_rgba(0,229,204,0.05)] relative overflow-hidden group h-full flex flex-col justify-center">
                    <div className="absolute top-0 left-0 w-2 h-full bg-gradient-to-b from-[#00E5CC] via-[#ff0092] to-transparent" />
                    
                    <div className="flex items-center gap-4 mb-8">
                       <div className="w-12 h-12 rounded-2xl bg-[var(--accent-blue-transparent)] flex items-center justify-center text-[#00E5CC] border border-[var(--accent-blue-border)]">
                          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                             <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
                          </svg>
                       </div>
                       <div className="flex flex-col">
                          <h3 className="text-sm font-black uppercase tracking-[0.3em] text-[#00E5CC]">Forensic Audit Note</h3>
                          <span className="text-[8px] text-[var(--text-secondary)] font-bold uppercase tracking-widest">Generated by v11.0 Reasoning Judge</span>
                       </div>
                    </div>
                    
                    <div className="relative">
                      <span className="absolute -top-6 -left-2 text-6xl text-[var(--accent-blue)] opacity-10 font-serif">"</span>
                      <p className="text-lg font-medium leading-relaxed italic text-[var(--text-primary)] relative z-10 pl-6 border-l-2 border-[var(--panel-border)]">
                        {result.forensic_reasoning || "No anomalous linguistic patterns detected during structural and semantic trajectory audit."}
                      </p>
                    </div>

                    <div className="mt-10 flex flex-wrap gap-2">
                       {result.indicators && result.indicators.map((ind, i) => (
                         <span key={i} className="px-3 py-1.5 rounded-lg bg-[rgba(255,255,255,0.03)] border border-[var(--panel-border)] text-[9px] font-bold text-[var(--text-secondary)] uppercase tracking-wider">
                           DETECTED: {ind}
                         </span>
                       ))}
                    </div>
                  </div>
               </div>

            </div>
          )}

          <div className="h-20" /> {/* Bottom Spacing */}
        </div>
      </main>

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
    </div>
  );
};

export default TextLabPage;
