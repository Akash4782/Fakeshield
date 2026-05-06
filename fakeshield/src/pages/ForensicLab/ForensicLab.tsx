// @ts-nocheck
import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ShieldAlert, 
  Search, 
  Trash2, 
  Download, 
  Brain, 
  Fingerprint, 
  Zap, 
  BarChart3, 
  Info,
  CheckCircle2,
  FileSearch,
  Activity,
  ChevronRight
} from 'lucide-react';
import Sidebar from '../../components/layout/Sidebar';
import { scanTextSync } from '../../services/textService';
import type { TextResult } from '../../services/textService';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  Tooltip, 
  ResponsiveContainer, 
  Cell 
} from 'recharts';

const ForensicLab = () => {
  const [text, setText] = useState("");
  const [result, setResult] = useState<TextResult | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [mode, setMode] = useState<"quick" | "deep" | "forensic">("deep");

  const handleScan = async () => {
    if (!text || text.length < 20) {
      alert("Minimum 20 characters required for forensic analysis.");
      return;
    }

    setIsScanning(true);
    setResult(null);
    try {
      const data = await scanTextSync(text);
      setResult(data);
    } catch (error) {
      console.error("Forensic scan failed:", error);
      alert("Analysis engine failure. Check backend logs.");
    } finally {
      setIsScanning(false);
    }
  };

  const getLabelColor = (label: string, score: number | null) => {
    if (label === 'too_short') return 'transparent';
    const s = (score || 0) / 100;
    
    // Proper Heatmap Logic: Clearer, more distinct highlighting
    if (label === 'AI') {
      return `rgba(239, 68, 68, ${0.4 + s * 0.4})`; // Red
    }
    if (label === 'LIKELY_AI') {
      return `rgba(249, 115, 22, ${0.3 + s * 0.4})`; // Orange
    }
    if (label === 'UNCERTAIN') {
      return `rgba(234, 179, 8, ${0.3 + s * 0.3})`; // Yellow/Amber
    }
    if (label === 'HUMAN') {
      return `rgba(34, 197, 94, ${0.2 + (1 - s) * 0.2})`; // Green
    }
    return 'transparent';
  };

  const getBorderColor = (label: string) => {
    if (label === 'AI') return 'border-[var(--accent-red)]/40';
    if (label === 'LIKELY_AI') return 'border-orange-500/30';
    if (label === 'UNCERTAIN') return 'border-[var(--accent-purple)]/30';
    if (label === 'HUMAN') return 'border-[var(--accent-green)]/30';
    return 'border-transparent';
  };

  const signalData = useMemo(() => {
    if (!result) return [];
    return [
      { name: 'CLF1 (ChatGPT)', score: result.signals.clf1 * 100, color: '#00E5CC' },
      { name: 'CLF2 (OpenAI)', score: (result.signals.clf2 || 0) * 100, color: 'var(--accent-purple)' },
      { name: 'Embedding', score: result.signals.embedding * 100, color: '#6366f1' },
      { name: 'GPT2 Stats', score: result.signals.gpt2_entropy * 100, color: 'var(--accent-red)' },
      { name: 'Stylometric', score: result.signals.stylometric * 100, color: 'var(--text-active)' },
      { name: 'Consistency', score: (result.signals.consistency || 0) * 100, color: '#06b6d4' },
      { name: 'Repetition', score: (result.signals.repetition || 0) * 100, color: '#f97316' },
      { name: 'Entropy', score: (result.signals.entropy_var || 0) * 100, color: '#ec4899' },
    ];
  }, [result]);

  return (
    <div className="flex h-screen overflow-hidden text-[var(--text-primary)] font-sans" style={{ background: 'var(--bg-primary)' }}>
      <Sidebar activeTab="Text Lab" />

      <div className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="h-16 border-b bg-[var(--panel-bg)] backdrop-blur-xl flex items-center justify-between px-8 z-50" style={{ borderColor: 'var(--panel-border)' }}>
          <div className="flex items-center space-x-4">
            <div className="flex items-center text-xs font-mono text-[var(--text-muted)]">
              <span className="hover:text-[var(--accent-purple)] transition-colors cursor-pointer">FORENSICS</span>
              <ChevronRight className="w-3 h-3 mx-2" />
              <span className="text-[var(--accent-purple)]">TEXT INTELLIGENCE LAB</span>
            </div>
            <div className="h-4 w-px bg-[var(--panel-border)]" />
            <div className="flex bg-[var(--bg-secondary)] p-1 rounded-lg border border-[var(--panel-border)]">
              {(['quick', 'deep', 'forensic'] as const).map((m) => (
                <button
                  key={m}
                  onClick={() => setMode(m)}
                  className={`px-3 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md transition-all ${
                    mode === m ? 'bg-[var(--accent-purple)] text-white shadow-lg shadow-purple-500/20' : 'text-[var(--text-muted)] hover:text-[var(--text-secondary)]'
                  }`}
                >
                  {m}
                </button>
              ))}
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center px-3 py-1.5 bg-[var(--accent-green-transparent)] border border-[var(--accent-green-border)] rounded-full">
              <div className="w-1.5 h-1.5 rounded-full bg-[var(--accent-green)] animate-pulse mr-2" />
              <span className="text-[10px] font-mono text-[var(--accent-green)] tracking-tighter uppercase">V7.0-ALPHA-READY</span>
            </div>
            <button className="flex items-center px-4 py-2 bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] rounded-lg hover:bg-[var(--btn-secondary-hover)] transition-all font-mono text-[10px] uppercase tracking-widest text-[var(--text-primary)]">
              <Download className="w-3 h-3 mr-2" />
              REPORT.PDF
            </button>
          </div>
        </header>

        <main className="flex-1 flex overflow-hidden">
          {/* Main Input/Result Area */}
          <div className="flex-1 flex flex-col p-6 space-y-6 overflow-hidden">
            <div className="flex-1 flex flex-col min-h-0 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <FileSearch className="w-5 h-5 text-[var(--accent-purple)]" />
                  <h2 className="text-sm font-bold uppercase tracking-widest text-[var(--text-heading)]">Investigation Chamber</h2>
                </div>
                <div className="flex items-center text-[10px] font-mono text-[var(--text-muted)]">
                  <Activity className="w-3 h-3 mr-1 text-[var(--accent-green)] opacity-50" />
                  REAL-TIME PATTERN MATCHING ENABLED
                </div>
              </div>

              <div className="flex-1 rounded-2xl overflow-hidden relative shadow-2xl" style={{ background: 'var(--bg-secondary)', border: '1px solid var(--panel-border)' }}>
                {!result && !isScanning && (
                  <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Paste technical document, essay, or raw text for deep forensic analysis..."
                    className="w-full h-full bg-transparent p-8 text-lg font-light leading-relaxed outline-none resize-none placeholder:text-[var(--text-muted)] text-[var(--text-primary)]"
                  />
                )}

                <AnimatePresence>
                  {isScanning && (
                    <motion.div 
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="absolute inset-0 z-50 flex flex-col items-center justify-center bg-[var(--bg-primary)]/80 backdrop-blur-md"
                    >
                      <div className="relative">
                        <div className="w-24 h-24 border-2 border-[var(--accent-purple)]/20 rounded-full animate-ping absolute inset-0" />
                        <div className="w-24 h-24 border-t-2 border-[var(--accent-purple)] rounded-full animate-spin" />
                        <Brain className="w-8 h-8 text-[var(--accent-purple)] absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
                      </div>
                      <h3 className="mt-8 font-mono text-xs uppercase tracking-[0.4em] text-[var(--accent-purple)] animate-pulse">Running Neural Inference</h3>
                      <p className="mt-2 text-[10px] font-mono text-[var(--text-muted)]">ENGINE V7.0 • DEBERTA • MINI-LM • GPT2-E</p>
                    </motion.div>
                  )}
                </AnimatePresence>

                {result && (
                  <div className="w-full h-full p-8 overflow-y-auto custom-scrollbar">
                    <div className="prose prose-invert max-w-none">
                      <p className="text-lg leading-[1.8] font-light text-[var(--text-primary)]">
                        {result.sentence_highlights.map((h, i) => (
                          <motion.span
                            initial={{ backgroundColor: 'transparent', borderBottomColor: 'transparent' }}
                            animate={{ 
                                backgroundColor: getLabelColor(h.label, h.ai_score),
                                borderBottomColor: h.label === 'too_short' ? 'transparent' : 'inherit'
                            }}
                            key={i}
                            className={`inline px-1 py-1 mx-0.5 rounded-md border-b-2 ${getBorderColor(h.label)} transition-all duration-700 cursor-help group relative`}
                          >
                            {h.sentence}
                            {h.ai_score !== null && (
                              <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 invisible group-hover:visible w-56 p-4 bg-[var(--bg-secondary)] border border-[var(--panel-border)] rounded-2xl shadow-2xl z-[100] text-[10px] pointer-events-none backdrop-blur-xl">
                                <div className="flex items-center justify-between mb-2">
                                  <span className="font-bold text-[var(--text-muted)] uppercase tracking-tighter">FORENSIC SIGNAL</span>
                                  <span className={h.ai_score > 70 ? 'text-[var(--accent-red)] font-black' : h.ai_score > 40 ? 'text-[var(--accent-yellow)]' : 'text-[var(--accent-green)]'}>
                                    {h.ai_score}% AI
                                  </span>
                                </div>
                                <div className="h-1.5 bg-[var(--border-subtle)] rounded-full overflow-hidden">
                                  <div className={`h-full transition-all duration-1000 ${
                                    h.label === 'AI' ? 'bg-gradient-to-r from-red-500 to-red-600' : 
                                    h.label === 'LIKELY_AI' ? 'bg-gradient-to-r from-orange-400 to-orange-500' : 
                                    h.label === 'UNCERTAIN' ? 'bg-gradient-to-r from-yellow-400 to-amber-500' : 
                                    'bg-gradient-to-r from-emerald-400 to-green-500'
                                  }`} style={{ width: `${h.ai_score || 0}%` }} />
                                </div>
                                <div className="mt-3 flex items-center justify-between font-mono text-[9px] text-[var(--text-muted)] uppercase">
                                  <span>VERDICT: {h.label.replace('_', ' ')}</span>
                                  <div className="flex space-x-1">
                                    <div className={`w-1.5 h-1.5 rounded-full ${h.label === 'AI' ? 'bg-red-500 shadow-[0_0_5px_red]' : 'bg-transparent'}`} />
                                    <div className={`w-1.5 h-1.5 rounded-full ${h.label === 'LIKELY_AI' ? 'bg-orange-500' : 'bg-transparent'}`} />
                                    <div className={`w-1.5 h-1.5 rounded-full ${h.label === 'UNCERTAIN' ? 'bg-yellow-500' : 'bg-transparent'}`} />
                                    <div className={`w-1.5 h-1.5 rounded-full ${h.label === 'HUMAN' ? 'bg-green-500' : 'bg-transparent'}`} />
                                  </div>
                                </div>
                              </span>
                            )}
                          </motion.span>
                        ))}
                      </p>
                    </div>
                  </div>
                )}
              </div>

              <div className="flex items-center space-x-4">
                <button
                  disabled={isScanning}
                  onClick={handleScan}
                  className={`flex-1 group h-14 flex items-center justify-center space-x-3 rounded-2xl transition-all font-bold uppercase tracking-[0.2em] text-sm ${
                    isScanning 
                      ? 'bg-[var(--btn-secondary-bg)] text-[var(--text-muted)] cursor-not-allowed' 
                      : 'bg-gradient-to-r from-[var(--accent-purple)] to-indigo-600 hover:opacity-90 text-white shadow-xl shadow-purple-500/20 active:scale-[0.98]'
                  }`}
                >
                  {isScanning ? (
                    'PROCESSING ENGINE...'
                  ) : (
                    <>
                      <Zap className="w-4 h-4 group-hover:animate-pulse" />
                      <span>{result ? 'INITIATE NEW SCAN' : 'RUN FORENSIC ANALYSIS'}</span>
                    </>
                  )}
                </button>
                <button 
                  onClick={() => { setText(""); setResult(null); }}
                  className="w-14 h-14 bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] rounded-2xl flex items-center justify-center hover:bg-[var(--accent-red-transparent)] hover:border-[var(--accent-red-border)] hover:text-[var(--accent-red)] transition-all active:scale-95 text-[var(--text-muted)]"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          {/* Right Sidebar - Analytics */}
          <aside className="w-[400px] border-l overflow-y-auto custom-scrollbar flex flex-col" style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}>
            <div className="p-8 space-y-8">
              {/* Verdict Section */}
              <section className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-[var(--text-muted)]">Forensic Verdict</h3>
                  {result && (
                    <div className="flex items-center text-[10px] font-mono text-[var(--accent-purple)] bg-[var(--accent-purple-transparent)] px-2 py-0.5 rounded border border-[var(--accent-purple-border)]">
                      ID: {result.engine_version.split('-')[0]}
                    </div>
                  )}
                </div>

                <div className="rounded-3xl p-8 flex flex-col items-center relative overflow-hidden group" style={{ background: 'var(--bg-secondary)', border: '1px solid var(--panel-border)' }}>
                  <div className="absolute inset-0 bg-gradient-to-br from-[var(--accent-purple)]/5 to-transparent pointer-events-none" />
                  
                  <div className="relative w-40 h-40 flex items-center justify-center">
                    <svg className="w-full h-full -rotate-90 pointer-events-none">
                      <circle cx="80" cy="80" r="70" className="fill-none stroke-[var(--border-subtle)] stroke-[8]" />
                      <motion.circle 
                        cx="80" cy="80" r="70" 
                        initial={{ strokeDasharray: "0, 440" }}
                        animate={{ strokeDasharray: `${(result ? result.confidence : 0) * 4.4}, 440` }}
                        transition={{ duration: 1.5, ease: "easeOut" }}
                        className={`fill-none stroke-[8] stroke-linecap-round ${
                          !result ? 'stroke-[var(--text-muted)]' : 
                          result.threat_level === 'CRITICAL' ? 'stroke-[var(--accent-red)] shadow-[0_0_15px_rgba(239,68,68,0.5)]' : 
                          result.threat_level === 'HIGH' ? 'stroke-[var(--accent-yellow)]' : 'stroke-[var(--accent-purple)]'
                        }`}
                      />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <AnimatePresence mode="wait">
                        <motion.span 
                          key={result ? result.confidence : 'no'}
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className="text-4xl font-black text-[var(--text-heading)]"
                        >
                          {result ? Math.round(result.confidence) : '00'}<span className="text-xl text-[var(--text-muted)]">%</span>
                        </motion.span>
                      </AnimatePresence>
                      <span className="text-[10px] font-mono text-[var(--text-muted)] uppercase tracking-widest mt-1">AI PROBABILITY</span>
                    </div>
                  </div>

                  <div className="mt-8 text-center space-y-2">
                    <div className={`text-xl font-black uppercase tracking-tighter ${
                      !result ? 'text-[var(--text-muted)]' : 
                      result.threat_level === 'CRITICAL' ? 'text-[var(--accent-red)]' : 
                      result.verdict.includes('HUMAN') ? 'text-[var(--accent-green)]' : 'text-[var(--text-heading)]'
                    }`}>
                      {result ? result.verdict : 'PENDING INPUT'}
                    </div>
                    {result && (
                      <div className="flex flex-col items-center space-y-1">
                        <div className="flex items-center space-x-2 text-[10px] font-mono">
                          <span className="text-[var(--text-muted)] uppercase tracking-widest">CONFIDENCE:</span>
                          <span className={`font-bold ${
                            result.confidence_level === 'HIGH' ? 'text-[var(--accent-green)]' :
                            result.confidence_level === 'MEDIUM' ? 'text-[var(--accent-yellow)]' : 'text-[var(--accent-red)]'
                          }`}>{result.confidence_level}</span>
                        </div>
                        <div className="flex items-center space-x-2 text-[10px] font-mono">
                          <span className="text-[var(--text-muted)] uppercase tracking-widest">RISK LEVEL:</span>
                          <span className={result.threat_level === 'CRITICAL' ? 'text-[var(--accent-red)]' : 'text-[var(--text-secondary)]'}>{result.threat_level}</span>
                        </div>
                        <div className="flex items-center space-x-2 text-[10px] font-mono">
                          <span className="text-[var(--text-muted)] uppercase tracking-widest">AGREEMENT:</span>
                          <span className="text-[var(--text-secondary)]">{result.agreement_score}/4 SIGNALS</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </section>

              {/* Signal Breakdown Section */}
              <section className="space-y-4">
                <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-[var(--text-muted)]">Signal Breakdown</h3>
                <div className="rounded-3xl p-6" style={{ background: 'var(--bg-secondary)', border: '1px solid var(--panel-border)' }}>
                  <div className="h-56 w-full">
                    {result ? (
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={signalData} margin={{ top: 20, right: 0, left: -25, bottom: 0 }}>
                          <XAxis 
                            dataKey="name" 
                            axisLine={false} 
                            tickLine={false} 
                            tick={{ fill: 'var(--text-muted)', fontSize: 10, fontWeight: 700 }} 
                          />
                          <Tooltip 
                            cursor={{ fill: 'var(--border-subtle)' }}
                            content={({ active, payload }) => {
                              if (active && payload && payload.length) {
                                return (
                                  <div className="bg-[var(--bg-secondary)] border border-[var(--panel-border)] p-3 rounded-xl shadow-2xl">
                                    <p className="text-[10px] font-bold text-[var(--text-muted)] uppercase mb-1">{payload[0].payload.name}</p>
                                    <p className="text-lg font-black text-[var(--text-heading)]">{Math.round(payload[0].value as number)}%</p>
                                  </div>
                                );
                              }
                              return null;
                            }}
                          />
                          <Bar dataKey="score" radius={[6, 6, 6, 6]} barSize={32}>
                            {signalData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.color} fillOpacity={0.8} />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="h-full flex flex-col items-center justify-center text-[var(--text-muted)] opacity-20 space-y-4">
                        <BarChart3 className="w-12 h-12" />
                        <span className="text-[10px] font-mono uppercase tracking-[0.2em]">WAITING FOR SCAN DATA</span>
                      </div>
                    )}
                  </div>
                </div>
              </section>

              {/* Forensic Reasons */}
              <section className="space-y-4">
                <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-[var(--text-muted)]">Forensic Explanation</h3>
                <div className="space-y-2">
                  {result && result.reasons ? (
                    result.reasons.map((reason, i) => (
                      <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.1 }}
                        key={i}
                        className="flex items-start space-x-3 p-4 rounded-2xl group border hover:border-[#00E5CC]/30 transition-colors"
                        style={{ background: 'var(--bg-secondary)', border: '1px solid var(--panel-border)' }}
                      >
                        <div className="mt-0.5">
                          <CheckCircle2 className="w-4 h-4" style={{ color: '#00E5CC' }} />
                        </div>
                        <div>
                          <div className="text-[11px] font-bold text-[var(--text-primary)]">{reason}</div>
                        </div>
                      </motion.div>
                    ))
                  ) : (
                    <div className="p-8 border border-[var(--panel-border)] border-dashed rounded-3xl flex flex-col items-center justify-center text-[var(--text-muted)] opacity-20">
                      <Info className="w-8 h-8 mb-2" />
                      <span className="text-[10px] font-mono uppercase">NO ANOMALIES DETECTED</span>
                    </div>
                  )}
                </div>
              </section>

              {/* Indicators */}
              <section className="space-y-4">
                <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-[var(--text-muted)]">Key Indicators</h3>
                <div className="flex flex-wrap gap-2">
                  {result && result.indicators.map((indicator, i) => (
                    <span key={i} className="px-3 py-1 bg-[var(--bg-secondary)] border border-[var(--panel-border)] rounded-full text-[9px] font-bold text-[var(--text-secondary)] uppercase">
                      {indicator}
                    </span>
                  ))}
                </div>
              </section>

              {/* Stability Score */}
              {result && (
                <section className="space-y-4">
                  <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-[var(--text-muted)]">Engine Stability</h3>
                  <div className="rounded-3xl p-6" style={{ background: 'var(--bg-secondary)', border: '1px solid var(--panel-border)' }}>
                    <div className="flex justify-between items-center mb-4">
                      <div className="flex items-center space-x-2">
                        <Activity className="w-4 h-4 text-[var(--accent-green)]" />
                        <span className="text-[10px] font-bold text-[var(--text-secondary)] uppercase tracking-wider">Detection Stability</span>
                      </div>
                      <span className="text-sm font-black text-[var(--accent-green)]">{Math.round(result.stability_score * 100)}%</span>
                    </div>
                    <div className="h-1.5 bg-[var(--border-subtle)] rounded-full overflow-hidden">
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: `${result.stability_score * 100}%` }}
                        className="h-full bg-[var(--accent-green)]"
                      />
                    </div>
                  </div>
                </section>
              )}

              {/* Linguistic Fingerprint Section */}
              {result && result.stylometric_details && (
                <section className="space-y-4">
                  <h3 className="text-[10px] font-black uppercase tracking-[0.3em] text-[var(--text-muted)]">Linguistic Fingerprint</h3>
                  <div className="grid grid-cols-2 gap-3">
                    {[
                      { label: 'Burstiness', value: result.stylometric_details.burstiness_cv, icon: Activity, color: 'text-[#00E5CC]' },
                      { label: 'Vocab Diversity', value: result.stylometric_details.ttr, icon: Fingerprint, color: 'text-[var(--accent-purple)]' },
                      { label: 'AI Phrases', value: result.stylometric_details.ai_phrases, icon: Search, color: 'text-[var(--accent-yellow)]' },
                      { label: 'Passive Voice', value: result.stylometric_details.passives, icon: ShieldAlert, color: 'text-indigo-400' }
                    ].map((item, i) => (
                      <div key={i} className="rounded-2xl p-4 flex flex-col space-y-2" style={{ background: 'var(--bg-secondary)', border: '1px solid var(--panel-border)' }}>
                        <div className="flex items-center space-x-2">
                          <item.icon className={`w-3 h-3 ${item.color}`} />
                          <span className="text-[9px] font-bold text-[var(--text-muted)] uppercase">{item.label}</span>
                        </div>
                        <div className="text-lg font-black text-[var(--text-heading)]">
                          {typeof item.value === 'number' && item.value < 1 ? Math.round(item.value * 100) + '%' : item.value}
                        </div>
                      </div>
                    ))}
                  </div>
                </section>
              )}
            </div>
            
            <div className="mt-auto p-8 border-t" style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}>
              <div className="flex items-center space-x-3 text-[var(--text-muted)] mb-4">
                <Brain className="w-5 h-5 text-[var(--accent-purple)]" />
                <div>
                  <div className="text-[10px] font-black uppercase tracking-widest text-[var(--text-secondary)]">FAKESHIELD V7 FORENSIC JUDGE</div>
                  <div className="text-[8px] font-mono tracking-tighter uppercase">NEURAL LOGIC • STYLOGRAPHY • ENTROPY</div>
                </div>
              </div>
              <p className="text-[10px] leading-relaxed text-[var(--text-muted)] italic">
                {result 
                  ? `Forensic analysis complete. System identifies the text as ${result.verdict.toLowerCase()} with ${result.confidence_level.toLowerCase()} confidence markers based on ${result.agreement_score} cross-engine signals.`
                  : "Awaiting forensic target for comprehensive linguistic analysis. Neural models pre-loaded and stabilized."
                }
              </p>
            </div>
          </aside>
        </main>
      </div>
      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: var(--panel-border);
          border-radius: 10px;
        }
      `}</style>
    </div>
  );
};

export default ForensicLab;
