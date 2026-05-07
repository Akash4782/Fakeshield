import React, { useState, useEffect, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Sidebar from '../../components/layout/Sidebar';
import TopBar from '../../components/layout/TopBar';
import { useAuth } from '../../hooks/useAuth.tsx';
import { API_BASE_URL } from '../../config';

interface ScanRecord {
  _id: string;
  lab: 'text' | 'image' | 'audio' | 'video';
  filename: string;
  verdict: string;
  confidence: number;
  threat_level: string;
  scan_id: string;
  created_at: string;
}

interface DashStats {
  total_scans: number;
  total_threats: number;
  total_authentic: number;
  ai_detected: number;
  lab_breakdown: {
    text:  { total: number; ai: number };
    image: { total: number; ai: number };
    audio: { total: number; ai: number };
    video: { total: number; ai: number };
  };
}

const LAB_COLORS: Record<string, string> = {
  text: '#6366f1', image: '#00E5CC', audio: '#f59e0b', video: '#ef4444',
};

const LAB_PATHS: Record<string, string> = {
  text: '/text-lab', image: '/image-lab', audio: '/audio-lab', video: '/video-lab',
};

function timeAgo(iso: string) {
  const diff = Date.now() - new Date(iso).getTime();
  const m = Math.floor(diff / 60000);
  if (m < 1) return 'just now';
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  return `${Math.floor(h / 24)}d ago`;
}

function pct(c: number) { return Math.round(c > 1 ? c : c * 100); }

const VERDICT_DOT: Record<string, string> = {
  'AI-Generated': '#ef4444',
  'AI GENERATED': '#ef4444',
  'DEEPFAKE':     '#ef4444',
  'LIKELY_AI':    '#ef4444',
  'AI':           '#ef4444',
  'Suspicious':   '#f59e0b',
  'UNCERTAIN':    '#f59e0b',
  'Authentic':    '#22c55e',
  'AUTHENTIC':    '#22c55e',
  'LIKELY HUMAN': '#22c55e',
  'LIKELY REAL':  '#22c55e',
};

import DashboardLayout from '../../components/layout/DashboardLayout';

const DashboardPage: React.FC = () => {
  const { token, user } = useAuth();
  const navigate = useNavigate();
  const [scans,   setScans]   = useState<ScanRecord[]>([]);
  const [stats,   setStats]   = useState<DashStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter,  setFilter]  = useState<'all'|'text'|'image'|'audio'|'video'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [error,   setError]   = useState('');

  const load = useCallback(async () => {
    if (!token) return;
    setLoading(true); setError('');
    try {
      const h = { Authorization: `Bearer ${token}` };
      const [rh, rs] = await Promise.all([
        fetch(`${API_BASE_URL}/dashboard/history?limit=30`, { headers: h }),
        fetch(`${API_BASE_URL}/dashboard/stats`, { headers: h }),
      ]);
      if (rh.ok) setScans((await rh.json()).scans ?? []);
      if (rs.ok) setStats(await rs.json());
    } catch { setError('Backend unreachable.'); }
    finally { setLoading(false); }
  }, [token]);

  useEffect(() => { load(); }, [load]);

  const visible = scans.filter(s => {
    const matchesFilter = filter === 'all' || s.lab === filter;
    const matchesSearch = 
      s.filename.toLowerCase().includes(searchQuery.toLowerCase()) || 
      s.scan_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.verdict.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const maxLab  = stats ? Math.max(...Object.values(stats.lab_breakdown).map(l => l.total), 1) : 1;

  return (
    <DashboardLayout activeTab="Dashboard">
        {/* upgrade strip */}
        {user?.subscription_tier !== 'paid' && (
          <div className="mx-4 md:mx-8 mb-6 flex flex-col sm:flex-row items-start sm:items-center justify-between px-5 py-3 rounded-xl border gap-4" style={{ background: 'rgba(0,229,204,0.04)', borderColor: 'rgba(0,229,204,0.15)' }}>
            <div className="flex items-center gap-3">
              <div className="w-1.5 h-1.5 rounded-full bg-[#00E5CC] animate-pulse" />
              <span className="text-xs font-semibold" style={{ color: '#00E5CC' }}>Basic Access</span>
              <span className="text-xs" style={{ color: 'var(--text-secondary)' }}>— Pro Shield required for advanced labs</span>
            </div>
            <button onClick={() => navigate('/subscription')}
              className="text-xs font-bold px-4 py-1.5 rounded-lg transition-all hover:opacity-90 whitespace-nowrap"
              style={{ background: '#00E5CC', color: '#000' }}>
              Upgrade →
            </button>
          </div>
        )}

        <div className="px-4 md:px-8 space-y-6 pb-16">
          <header className="mt-8 mb-10">
            <h1 className="text-4xl font-bold text-slate-900 tracking-tight mb-2">Dashboard</h1>
            <p className="text-sm text-slate-500 font-medium">Real-time deepfake & synthetic media intelligence</p>
          </header>

          {/* ── 4-stat row ──────────────────────────────────────────── */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { label: 'Total scans',  value: stats?.total_scans ?? 0,     sub: 'All labs',            color: '#00E5CC', icon: (
                <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/><path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd"/></svg>
              )},
              { label: 'Synthetic detected',  value: stats?.ai_detected ?? 0,     sub: 'Flagged as AI-generated',  color: '#ef4444', icon: (
                <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4"><path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/></svg>
              )},
              { label: 'Verified human',    value: stats?.total_authentic ?? 0, sub: 'Confirmed authentic',       color: '#22c55e', icon: (
                <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/></svg>
              )},
              { label: 'Uncertain',   value: (stats?.total_threats ?? 0) - (stats?.ai_detected ?? 0), sub: 'Manual review needed', color: '#f59e0b', icon: (
                <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4"><path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd"/></svg>
              )},
            ].map(({ label, value, sub, color, icon }) => (
              <div key={label} className="rounded-2xl border p-5 flex flex-col gap-4" style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold" style={{ color: 'var(--text-secondary)' }}>{label}</span>
                  <div className="w-7 h-7 rounded-lg flex items-center justify-center" style={{ background: `${color}18`, color }}>
                    {icon}
                  </div>
                </div>
                <div>
                  <p className="text-4xl font-black font-mono leading-none" style={{ color: loading ? 'var(--text-secondary)' : color }}>
                    {loading ? '—' : value}
                  </p>
                  <p className="text-[11px] mt-2" style={{ color: 'var(--text-secondary)' }}>{sub}</p>
                </div>
              </div>
            ))}
          </div>

          {/* ── middle row ──────────────────────────────────────────── */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">

            {/* Lab breakdown */}
            <div className="col-span-1 lg:col-span-4 rounded-2xl border p-6 flex flex-col gap-5" style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}>
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-bold" style={{ color: 'var(--text-secondary)' }}>Analysis activity</h3>
                <button onClick={load} className="text-[10px] font-mono transition-colors hover:text-[#00E5CC]" style={{ color: 'var(--text-secondary)' }}>↻ refresh</button>
              </div>
              {loading ? (
                <div className="flex flex-col gap-4">{[0,1,2,3].map(i => <div key={i} className="h-10 rounded-lg animate-pulse" style={{ background: 'var(--panel-border)' }} />)}</div>
              ) : stats ? (
                <div className="flex flex-col gap-5">
                  {(['text','image','audio','video'] as const).map(lab => {
                    const d = stats.lab_breakdown[lab];
                    const barW = maxLab > 0 ? Math.round((d.total / maxLab) * 100) : 0;
                    return (
                      <div key={lab}>
                        <div className="flex items-center justify-between mb-1.5">
                          <span className="text-[12px] font-semibold capitalize" style={{ color: 'var(--text-heading)' }}>{lab} Analysis</span>
                          <span className="text-[11px] font-mono" style={{ color: 'var(--text-secondary)' }}>{d.total} records</span>
                        </div>
                        <div className="h-1.5 rounded-full" style={{ background: 'var(--panel-border)' }}>
                          <div className="h-full rounded-full transition-all duration-700" style={{ width: `${barW}%`, background: LAB_COLORS[lab] }} />
                        </div>
                        {d.ai > 0 && (
                          <p className="text-[10px] mt-1 font-mono" style={{ color: '#ef4444' }}>
                            {d.ai} synthetic records
                          </p>
                        )}
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>No data yet.</p>
              )}
            </div>

            {/* Quick access */}
            <div className="col-span-1 lg:col-span-8 rounded-2xl border p-6" style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}>
              <h3 className="text-sm font-bold mb-5" style={{ color: 'var(--text-secondary)' }}>Analysis laboratories</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 h-[calc(100%-2rem)]">
                {([
                  { key: 'text',  name: 'Text lab',  desc: 'Linguistic pattern & stylistic analysis' },
                  { key: 'image', name: 'Image lab', desc: 'Neural signal & spectral extraction' },
                  { key: 'audio', name: 'Audio lab', desc: 'Voice biometric & pitch analysis' },
                  { key: 'video', name: 'Video lab', desc: 'VLM-based physics & temporal audit' },
                ] as const).map(({ key, name, desc }) => {
                  const isPaid = user?.subscription_tier === 'paid';
                  const locked = key !== 'text' && !isPaid;
                  const count  = stats?.lab_breakdown[key]?.total ?? 0;
                  const color  = LAB_COLORS[key];
                  return (
                    <Link key={key} to={locked ? '/subscription' : LAB_PATHS[key]}
                      className="flex flex-col gap-3 p-5 rounded-xl border transition-all hover:border-opacity-50 group"
                      style={{ borderColor: locked ? 'var(--panel-border)' : `${color}25`, background: `${color}06` }}
                    >
                      <div className="flex items-center justify-between">
                        <div className="w-2 h-2 rounded-full" style={{ background: color }} />
                        {locked && (
                          <span className="text-[9px] font-black uppercase tracking-widest px-1.5 py-0.5 rounded" style={{ background: 'rgba(245,158,11,0.12)', color: '#f59e0b' }}>PRO</span>
                        )}
                      </div>
                      <div>
                        <p className="text-sm font-bold" style={{ color: locked ? 'var(--text-secondary)' : 'var(--text-heading)' }}>{name}</p>
                        <p className="text-[11px] mt-0.5 leading-relaxed" style={{ color: 'var(--text-secondary)' }}>{desc}</p>
                      </div>
                      <p className="text-[11px] font-mono" style={{ color: count > 0 ? color : 'var(--text-secondary)' }}>
                        {count} record{count !== 1 ? 's' : ''}
                      </p>
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>

          {/* ── scan history table ───────────────────────────────────── */}
          <div className="rounded-2xl border overflow-hidden" style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}>
            {/* table header */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between px-6 py-4 border-b gap-4" style={{ borderColor: 'var(--panel-border)' }}>
              <div>
                <h3 className="text-sm font-bold" style={{ color: 'var(--text-secondary)' }}>Scan history</h3>
                <p className="text-[12px] mt-0.5" style={{ color: 'var(--text-secondary)' }}>{visible.length} record{visible.length !== 1 ? 's' : ''}</p>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                {(['all','text','image','audio','video'] as const).map(f => {
                  const active = filter === f;
                  const col = f === 'all' ? '#00E5CC' : LAB_COLORS[f];
                  return (
                    <button key={f} onClick={() => setFilter(f)}
                      className="px-3 py-1 rounded-lg text-[10px] font-bold uppercase tracking-widest border transition-all"
                      style={{
                        background:  active ? col : 'transparent',
                        color:       active ? '#000' : 'var(--text-secondary)',
                        borderColor: active ? col : 'var(--panel-border)',
                      }}>
                      {f}
                    </button>
                  );
                })}
                <button onClick={load} className="ml-1 px-3 py-1 rounded-lg text-[10px] font-mono border transition-all hover:border-[#00E5CC] hover:text-[#00E5CC]" style={{ borderColor: 'var(--panel-border)', color: 'var(--text-secondary)' }}>↻</button>
              </div>
            </div>

            {error && (
              <div className="mx-6 my-4 px-4 py-3 rounded-xl border text-xs font-mono" style={{ background: 'rgba(239,68,68,0.07)', borderColor: 'rgba(239,68,68,0.2)', color: '#ef4444' }}>
                ⚠ {error}
              </div>
            )}

            {loading ? (
              <div className="p-6 space-y-3">
                {[...Array(4)].map((_, i) => <div key={i} className="h-10 rounded-lg animate-pulse" style={{ background: 'var(--panel-border)' }} />)}
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full min-w-[700px]">
                  <thead>
                    <tr style={{ background: 'rgba(255,255,255,0.02)', borderBottom: '1px solid var(--panel-border)' }}>
                      {['File', 'Lab', 'Verdict', 'Confidence', 'Time'].map(h => (
                        <th key={h} className="text-left py-3 px-5 text-xs font-bold" style={{ color: 'var(--text-secondary)' }}>{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {visible.map((s, i) => {
                      const col   = LAB_COLORS[s.lab];
                      const dot   = VERDICT_DOT[s.verdict] ?? '#94a3b8';
                      const p     = pct(s.confidence);
                      const barCol = p >= 70 ? '#ef4444' : p >= 45 ? '#f59e0b' : '#22c55e';
                      return (
                        <tr key={s._id} style={{ borderBottom: i < visible.length - 1 ? '1px solid var(--panel-border)' : 'none' }}
                          className="transition-colors hover:bg-white/[0.02]">
                          <td className="py-3 px-5">
                            <Link 
                              to={`${LAB_PATHS[s.lab]}?scan_id=${s.scan_id}`}
                              className="group/link"
                            >
                              <p className="text-[13px] font-semibold truncate max-w-[200px] transition-colors group-hover/link:text-[#00E5CC]" style={{ color: 'var(--text-heading)' }}>{s.filename}</p>
                              <p className="text-[10px] font-mono mt-0.5" style={{ color: 'var(--text-secondary)' }}>{s.scan_id}</p>
                            </Link>
                          </td>
                          <td className="py-3 px-5">
                            <span className="text-[10px] font-black uppercase tracking-wider px-2 py-1 rounded-md" style={{ background: `${col}15`, color: col }}>
                              {s.lab}
                            </span>
                          </td>
                          <td className="py-3 px-5">
                            <div className="flex items-center gap-2">
                              <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: dot }} />
                              <span className="text-[12px] font-semibold" style={{ color: dot }}>{s.verdict}</span>
                            </div>
                          </td>
                          <td className="py-3 px-5">
                            <div className="flex items-center gap-3">
                              <div className="w-20 h-1.5 rounded-full" style={{ background: 'var(--panel-border)' }}>
                                <div className="h-full rounded-full" style={{ width: `${p}%`, background: barCol }} />
                              </div>
                              <span className="text-[11px] font-mono font-bold" style={{ color: barCol }}>{p}%</span>
                            </div>
                          </td>
                          <td className="py-3 px-5">
                            <span className="text-[11px]" style={{ color: 'var(--text-secondary)' }}>{timeAgo(s.created_at)}</span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
    </DashboardLayout>
  );
};

export default DashboardPage;
