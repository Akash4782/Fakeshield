import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Filter, 
  Download, 
  Trash2, 
  FileText, 
  Image as ImageIcon, 
  Mic2, 
  Video,
  ChevronLeft,
  ChevronRight,
  ExternalLink,
  MoreVertical,
  Calendar,
  AlertCircle
} from 'lucide-react';
import Sidebar from '../../components/layout/Sidebar';
import { useAuth } from '../../hooks/useAuth.tsx';
import { Link } from 'react-router-dom';

interface ScanRecord {
  _id: string;
  lab: string;
  filename: string;
  verdict: string;
  confidence: number;
  threat_level: string;
  scan_id: string;
  created_at: string;
}

const LAB_ICONS: Record<string, any> = {
  text: FileText,
  image: ImageIcon,
  audio: Mic2,
  video: Video,
};

const LAB_PATHS: Record<string, string> = {
  text: '/text-lab',
  image: '/image-lab',
  audio: '/audio-lab',
  video: '/video-lab',
};

const ArchivePage: React.FC = () => {
  const { token } = useAuth();
  const [history, setHistory] = useState<ScanRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    const fetchHistory = async () => {
      if (!token) return;
      try {
        const res = await fetch('http://127.0.0.1:8001/api/v1/dashboard/history?limit=100', {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setHistory(data.data);
        }
      } catch (err) {
        console.error("Archive fetch failed:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, [token]);

  const filtered = history.filter(s => {
    const matchSearch = s.filename.toLowerCase().includes(search.toLowerCase()) || s.scan_id.toLowerCase().includes(search.toLowerCase());
    const matchFilter = filter === 'all' || s.lab === filter;
    return matchSearch && matchFilter;
  });

  return (
    <div className="flex h-screen overflow-hidden" style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)' }}>
      <Sidebar activeTab="Archive" />
      
      <div className="flex-1 flex flex-col min-w-0">
        <header className="flex items-center justify-between px-8 py-6 border-b" style={{ borderColor: 'var(--panel-border)', background: 'var(--glass-bg)' }}>
          <div className="flex items-center gap-4">
            <div className="w-1.5 h-8 rounded-full" style={{ background: '#00E5CC' }} />
            <h1 className="text-3xl font-extrabold tracking-tight">Forensic Archive</h1>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--text-muted)]" />
              <input 
                type="text" 
                placeholder="Search scans..." 
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10 pr-4 py-2 rounded-xl text-sm border focus:outline-none transition-all"
                style={{ background: 'var(--bg-secondary)', borderColor: 'var(--panel-border)', width: '280px' }}
              />
            </div>
            
            <select 
              className="px-4 py-2 rounded-xl text-sm border focus:outline-none"
              style={{ background: 'var(--bg-secondary)', borderColor: 'var(--panel-border)' }}
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            >
              <option value="all">All Labs</option>
              <option value="text">Text Lab</option>
              <option value="image">Image Lab</option>
              <option value="audio">Audio Lab</option>
              <option value="video">Video Lab</option>
            </select>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <div className="glass-card rounded-2xl border overflow-hidden" style={{ borderColor: 'var(--panel-border)' }}>
            <table className="w-full text-left">
              <thead className="text-[11px] font-black uppercase tracking-[0.2em] bg-[var(--bg-secondary)]" style={{ color: 'var(--text-muted)' }}>
                <tr>
                  <th className="py-5 px-6">Source / ID</th>
                  <th className="py-5 px-6">Verdicts</th>
                  <th className="py-5 px-6">Confidence</th>
                  <th className="py-5 px-6">Timestamp</th>
                  <th className="py-5 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--panel-border)]">
                {loading ? (
                  <tr>
                    <td colSpan={5} className="py-20 text-center">
                      <div className="flex flex-col items-center gap-3">
                        <div className="w-10 h-10 border-2 border-[#00E5CC] border-t-transparent animate-spin rounded-full" />
                        <span className="text-xs font-mono uppercase tracking-widest opacity-50">Querying Cold Storage...</span>
                      </div>
                    </td>
                  </tr>
                ) : filtered.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="py-20 text-center">
                      <div className="flex flex-col items-center gap-4 opacity-40">
                        <AlertCircle className="w-12 h-12" />
                        <span className="text-sm font-medium">No archived records found matching your criteria.</span>
                      </div>
                    </td>
                  </tr>
                ) : filtered.map((s) => {
                  const Icon = LAB_ICONS[s.lab] || FileText;
                  const col = s.threat_level === 'critical' ? 'var(--accent-red)' : s.threat_level === 'high' ? 'var(--accent-orange)' : '#00E5CC';
                  
                  return (
                    <tr key={s._id} className="group hover:bg-white/[0.02] transition-colors">
                      <td className="py-4 px-6">
                        <div className="flex items-center gap-4">
                          <div className="w-10 h-10 rounded-xl flex items-center justify-center border transition-all group-hover:border-[#00E5CC]/30" style={{ background: 'var(--bg-secondary)', borderColor: 'var(--panel-border)' }}>
                            <Icon className="w-5 h-5" style={{ color: 'var(--text-muted)' }} />
                          </div>
                          <div>
                            <p className="text-sm font-bold truncate max-w-[200px]" style={{ color: 'var(--text-heading)' }}>{s.filename}</p>
                            <p className="text-[10px] font-mono opacity-50">{s.scan_id}</p>
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-6">
                        <span className="text-[10px] font-black uppercase tracking-wider px-2 py-1 rounded-md border" style={{ background: `${col}10`, color: col, borderColor: `${col}20` }}>
                          {s.verdict}
                        </span>
                      </td>
                      <td className="py-4 px-6">
                        <div className="flex items-center gap-2">
                          <div className="w-16 h-1 rounded-full bg-[var(--panel-border)] overflow-hidden">
                            <div className="h-full rounded-full" style={{ background: col, width: `${(s.confidence || 0) * 100}%` }} />
                          </div>
                          <span className="text-xs font-mono font-bold" style={{ color: 'var(--text-primary)' }}>{((s.confidence || 0) * 100).toFixed(0)}%</span>
                        </div>
                      </td>
                      <td className="py-4 px-6">
                        <div className="flex items-center gap-2 text-[var(--text-muted)]">
                          <Calendar className="w-3.5 h-3.5" />
                          <span className="text-xs font-medium">{new Date(s.created_at).toLocaleDateString()}</span>
                        </div>
                      </td>
                      <td className="py-4 px-6 text-right">
                        <div className="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                          <Link 
                            to={`${LAB_PATHS[s.lab]}?scan_id=${s.scan_id}`}
                            className="p-2 rounded-lg hover:bg-[#00E5CC]/10 text-[var(--text-muted)] hover:text-[#00E5CC] transition-all"
                            title="View Forensic Details"
                          >
                            <ExternalLink className="w-4 h-4" />
                          </Link>
                          <button className="p-2 rounded-lg hover:bg-red-500/10 text-[var(--text-muted)] hover:text-red-500 transition-all" title="Delete Permanent Record">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
          
          <div className="mt-8 flex items-center justify-between">
            <p className="text-xs font-medium text-[var(--text-muted)] uppercase tracking-wider">
              Showing {filtered.length} of {history.length} archived scans
            </p>
            
            <div className="flex items-center gap-2">
              <button className="p-2 rounded-xl border opacity-50 cursor-not-allowed" style={{ borderColor: 'var(--panel-border)', background: 'var(--bg-secondary)' }}>
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button className="p-2 rounded-xl border opacity-50 cursor-not-allowed" style={{ borderColor: 'var(--panel-border)', background: 'var(--bg-secondary)' }}>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default ArchivePage;
