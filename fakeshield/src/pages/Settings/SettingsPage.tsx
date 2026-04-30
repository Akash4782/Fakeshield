import React, { useState } from 'react';
import Sidebar from '../../components/layout/Sidebar';
import { 
  Settings, 
  Cpu, 
  Key, 
  Database, 
  ShieldCheck, 
  Fingerprint, 
  Activity, 
  Copy, 
  RefreshCw, 
  Cloud, 
  Trash2, 
  ChevronRight,
  Monitor,
  Globe,
  Zap
} from 'lucide-react';

const SettingsPage: React.FC = () => {
  const [sensitivity, setSensitivity] = useState(75);
  const [ephemeralMode, setEphemeralMode] = useState(false);
  const [biometrics, setBiometrics] = useState(true);
  const [apiKey] = useState('fs_live_xxxxxxxxxxxxxxxxxxxxxxxxxx4d2e');
  const [showKey, setShowKey] = useState(false);

  // Stats for Audit Logs
  const auditLogs = [
    { id: 1, event: 'Login Successful', ip: '192.168.1.1', device: 'Windows 11 / Chrome', time: '2 mins ago' },
    { id: 2, event: 'API Key Generated', ip: '192.168.1.1', device: 'Windows 11 / Chrome', time: '1 hour ago' },
    { id: 3, event: 'MFA Verified', ip: '192.168.1.1', device: 'mobile_app', time: '1 hour ago' },
    { id: 4, event: 'Login Successful', ip: '10.0.0.42', device: 'MacOS / Safari', time: '5 hours ago' },
  ];

  return (
    <div className="flex h-screen bg-[var(--bg-primary)] overflow-hidden font-sans">
      <Sidebar activeTab="Settings" />
      
      <main className="flex-1 overflow-y-auto custom-scrollbar relative">
        {/* Background Glows */}
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-[var(--accent-blue-transparent)] rounded-full blur-[120px] pointer-events-none -z-10" />
        <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-[var(--accent-purple-transparent)] rounded-full blur-[120px] pointer-events-none -z-10" />

        <div className="p-8 max-w-6xl mx-auto">
          {/* Header */}
          <header className="mb-10 animate-fade-in text-[var(--text-primary)]">
            <div className="flex items-center gap-3 mb-2 text-[#00E5CC]">
              <Settings className="w-5 h-5" />
              <span className="text-sm font-bold uppercase tracking-widest">Configuration Suite</span>
            </div>
            <h1 className="text-4xl font-bold text-[var(--text-heading)] mb-2">Systems & Logic</h1>
            <p className="text-[var(--text-secondary)]">Program your Forensic AI workflows and manage enterprise-grade security protocols.</p>
          </header>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* 1. Forensic Model Calibration */}
            <section className="p-6 rounded-[2rem] border-[var(--panel-border)] border animate-fade-in-up" style={{ background: 'var(--panel-bg)' }}>
              <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-[rgba(0,229,204,0.1)] rounded-2xl text-[#00E5CC]">
                  <Cpu className="w-6 h-6" />
                </div>
                <h2 className="text-xl font-bold text-[var(--text-heading)]">Forensic Model Calibration</h2>
              </div>

              <div className="space-y-6">
                <div>
                  <div className="flex justify-between items-center mb-4">
                    <label className="text-sm font-semibold text-[var(--text-secondary)]">Sensitivity Threshold</label>
                    <span className="text-xs font-bold px-2 py-1 bg-[rgba(0,229,204,0.1)] text-[#00E5CC] rounded-lg">{sensitivity}%</span>
                  </div>
                  <input 
                    type="range" 
                    min="0" 
                    max="100" 
                    value={sensitivity} 
                    onChange={(e) => setSensitivity(parseInt(e.target.value))}
                    className="w-full h-1.5 bg-[var(--panel-border)] rounded-lg appearance-none cursor-pointer accent-[#00E5CC]"
                  />
                  <div className="flex justify-between mt-2 text-[10px] text-[var(--text-muted)] uppercase font-bold tracking-tighter">
                    <span>Fast Scan</span>
                    <span>Deep Forensic</span>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-[var(--bg-primary)] rounded-2xl border border-[var(--panel-border)]">
                    <div className="flex items-center gap-3">
                      <Zap className="w-4 h-4 text-[var(--text-active)]" />
                      <div>
                        <p className="text-sm font-bold text-[var(--text-heading)]">rPPG Heartbeat Monitor</p>
                        <p className="text-[10px] text-[var(--text-muted)]">Analyze subtle skin tone variations for video liveness.</p>
                      </div>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" className="sr-only peer" defaultChecked />
                      <div className="w-11 h-6 bg-[var(--btn-secondary-bg)] rounded-full peer peer-checked:after:translate-x-full peer-checked:bg-[#00E5CC] after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
                    </label>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-[var(--bg-primary)] rounded-2xl border border-[var(--panel-border)]">
                    <div className="flex items-center gap-3">
                      <Activity className="w-4 h-4 text-[var(--accent-purple)]" />
                      <div>
                        <p className="text-sm font-bold text-[var(--text-heading)]">Spectrogram Neural-Sync</p>
                        <p className="text-[10px] text-[var(--text-muted)]">Cross-reference audio peaks with facial phoneme data.</p>
                      </div>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input type="checkbox" className="sr-only peer" defaultChecked />
                      <div className="w-11 h-6 bg-[var(--btn-secondary-bg)] rounded-full peer peer-checked:after:translate-x-full peer-checked:bg-[#00E5CC] after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all"></div>
                    </label>
                  </div>
                </div>

                <div>
                  <label className="text-sm font-semibold text-[var(--text-secondary)] block mb-3">LLM Reasoner Report Tone</label>
                  <select className="w-full bg-[var(--bg-primary)] border border-[var(--panel-border)] text-[var(--text-primary)] text-sm rounded-2xl p-4 outline-none focus:border-[#00E5CC]/50 transition-colors">
                    <option>Detailed Technical Analyst</option>
                    <option>Executive Summary (Non-Technical)</option>
                    <option>Legal Compliance Standard</option>
                  </select>
                </div>
              </div>
            </section>

            {/* 2. API & Webhook Management */}
            <section className="p-6 rounded-[2rem] border-[var(--panel-border)] border animate-fade-in-up delay-100" style={{ background: 'var(--panel-bg)' }}>
              <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-[rgba(0,229,204,0.1)] rounded-2xl text-[#00E5CC]">
                  <Key className="w-6 h-6" />
                </div>
                <h2 className="text-xl font-bold text-[var(--text-heading)]">n8n Gateway & APIs</h2>
              </div>

              <div className="space-y-6">
                <div className="p-5 bg-[var(--bg-primary)] rounded-3xl border border-[var(--panel-border)] relative overflow-hidden group">
                  <div className="flex justify-between items-center mb-3">
                    <span className="text-[10px] font-black uppercase text-[#00E5CC] tracking-widest">Active Shield-Key</span>
                    <button onClick={() => setShowKey(!showKey)} className="text-[10px] font-bold text-[var(--text-muted)] hover:text-[#00E5CC] transition-colors">
                      {showKey ? 'HIDE' : 'SHOW'}
                    </button>
                  </div>
                  <div className="flex items-center gap-3">
                    <code className="flex-1 text-sm text-[var(--text-primary)] font-mono tracking-tight overflow-hidden">
                      {showKey ? apiKey : apiKey.replace(/./g, '•')}
                    </code>
                    <button className="p-2 hover:bg-white/10 rounded-lg text-[var(--text-muted)] hover:text-[#00E5CC] transition-colors">
                      <Copy className="w-4 h-4" />
                    </button>
                    <button className="p-2 hover:bg-white/10 rounded-lg text-[var(--text-muted)] hover:text-[var(--accent-red)] transition-colors">
                      <RefreshCw className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="mt-4 flex gap-2">
                    <button className="flex-1 bg-gradient-to-r from-[#00E5CC] to-[#00b8a5] text-[#020617] text-[10px] font-bold py-2 rounded-xl hover:shadow-lg transition-all">
                      GENERATE NEW KEY
                    </button>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Globe className="w-3.5 h-3.5 text-[var(--text-muted)]" />
                      <span className="text-xs font-bold text-[var(--text-secondary)]">Inbound n8n Webhook</span>
                    </div>
                    <div className="flex gap-2">
                      <input 
                        readOnly 
                        value="https://n8n.fakeshield.ai/webhook/v1/trigger-scan" 
                        className="flex-1 bg-[var(--bg-primary)] border border-[var(--panel-border)] text-[var(--text-muted)] text-[10px] rounded-xl px-4 py-3 outline-none"
                      />
                      <button className="p-3 bg-[var(--bg-primary)] border border-[var(--panel-border)] rounded-xl text-[var(--text-muted)] hover:text-[#00E5CC] transition-colors">
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Monitor className="w-3.5 h-3.5 text-[var(--text-muted)]" />
                      <span className="text-xs font-bold text-[var(--text-secondary)]">Outbound Push Endpoint</span>
                    </div>
                    <div className="flex gap-2">
                      <input 
                        placeholder="https://your-server.com/alerts"
                        className="flex-1 bg-[var(--bg-primary)] border border-[var(--panel-border)] text-[var(--text-primary)] text-[11px] rounded-xl px-4 py-3 outline-none focus:border-[#00E5CC]/50 transition-colors"
                      />
                      <button className="px-4 bg-[var(--btn-secondary-bg)] border border-[var(--panel-border)] text-[var(--text-heading)] text-[10px] font-bold rounded-xl hover:bg-[var(--btn-secondary-hover)] transition-all">
                        SAVE
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* 3. Storage & Compliance */}
            <section className="p-6 rounded-[2rem] border-[var(--panel-border)] border animate-fade-in-up delay-200" style={{ background: 'var(--panel-bg)' }}>
              <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-[var(--accent-purple-transparent)] rounded-2xl text-[var(--accent-purple)]">
                  <Database className="w-6 h-6" />
                </div>
                <h2 className="text-xl font-bold text-[var(--text-heading)]">Storage & Compliance</h2>
              </div>

              <div className="space-y-6">
                <div className="space-y-3">
                  <p className="text-[10px] font-black uppercase text-[var(--text-muted)] tracking-widest pl-1">Auto-Archive Destinations</p>
                  <div className="grid grid-cols-2 gap-3">
                    {['Google Drive', 'AWS S3', 'Dropbox', 'Custom SFTP'].map(dest => (
                      <button key={dest} className="flex items-center justify-between p-3 bg-[var(--bg-primary)] rounded-xl border border-[var(--panel-border)] hover:border-[var(--accent-purple)]/30 transition-all text-left group">
                        <div className="flex items-center gap-2">
                          <Cloud className="w-4 h-4 text-[var(--text-muted)] group-hover:text-[var(--accent-purple)] transition-colors" />
                          <span className="text-[11px] font-bold text-[var(--text-secondary)]">{dest}</span>
                        </div>
                        <div className="w-2 h-2 rounded-full bg-[var(--accent-red)]"></div>
                      </button>
                    ))}
                  </div>
                </div>

                <div className={`p-5 rounded-3xl border transition-all duration-500 cursor-pointer ${ephemeralMode ? 'bg-[var(--accent-red-transparent)] border-[var(--accent-red-border)]' : 'bg-[var(--bg-primary)] border-[var(--panel-border)]'}`} onClick={() => setEphemeralMode(!ephemeralMode)}>
                  <div className="flex items-center gap-4 mb-3">
                    <div className={`p-2 rounded-xl ${ephemeralMode ? 'bg-[var(--accent-red)] text-white' : 'bg-[var(--btn-secondary-bg)] text-[var(--text-muted)]'}`}>
                      <Trash2 className="w-5 h-5" />
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-bold text-[var(--text-heading)]">Ephemeral Privacy Mode</p>
                      <p className="text-[10px] text-[var(--text-muted)]">Instantly wipe all file traces & reports after scan completion.</p>
                    </div>
                    <div className={`w-12 h-6 rounded-full relative ${ephemeralMode ? 'bg-[var(--accent-red)]' : 'bg-[var(--btn-secondary-bg)]'} transition-colors`}>
                      <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${ephemeralMode ? 'right-1' : 'left-1'}`} />
                    </div>
                  </div>
                  {ephemeralMode && (
                    <div className="animate-pulse flex items-center gap-2 text-[9px] font-bold text-[var(--accent-red)] uppercase tracking-widest mt-2">
                      <ShieldCheck className="w-3 h-3" /> Zero-Footprint Protocol Active
                    </div>
                  )}
                </div>
              </div>
            </section>

            {/* 4. Access & Identity */}
            <section className="p-6 rounded-[2rem] border-[var(--panel-border)] border animate-fade-in-up delay-300" style={{ background: 'var(--panel-bg)' }}>
              <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-[rgba(0,229,204,0.1)] rounded-2xl text-[#00E5CC]">
                  <ShieldCheck className="w-6 h-6" />
                </div>
                <h2 className="text-xl font-bold text-[var(--text-heading)]">Access & Identity</h2>
              </div>

              <div className="space-y-6">
                <div className="flex items-center justify-between p-4 bg-[var(--bg-primary)] rounded-3xl border border-[var(--panel-border)]">
                   <div className="flex items-center gap-4">
                     <div className="p-3 bg-[rgba(0,229,204,0.1)] rounded-2xl text-[#00E5CC]">
                       <Fingerprint className="w-6 h-6" />
                     </div>
                     <div>
                       <p className="text-sm font-bold text-[var(--text-heading)]">WebAuthn Biometrics</p>
                       <p className="text-[10px] text-[var(--text-muted)]">Enable TouchID / FaceID for instant forensic access.</p>
                     </div>
                   </div>
                   <button 
                    onClick={() => setBiometrics(!biometrics)}
                    className={`px-4 py-2 rounded-xl text-[10px] font-bold transition-all ${biometrics ? 'bg-[#00E5CC] text-[#020617]' : 'bg-[var(--btn-secondary-bg)] text-[var(--text-muted)]'}`}
                   >
                     {biometrics ? 'ENABLED' : 'DISABLED'}
                   </button>
                </div>

                <div className="space-y-3">
                   <div className="flex justify-between items-center mb-2">
                     <p className="text-[10px] font-black uppercase text-[var(--text-muted)] tracking-widest">Recent Security Events</p>
                     <p className="text-[10px] font-bold text-[#00E5CC] cursor-pointer flex items-center gap-1">FULL LOGS <ChevronRight className="w-3 h-3" /></p>
                   </div>
                   <div className="overflow-hidden rounded-2xl border border-[var(--panel-border)]">
                     <table className="w-full text-left text-[11px]">
                        <thead className="bg-[var(--bg-primary)] text-[var(--text-muted)] uppercase tracking-tighter font-black">
                          <tr>
                            <th className="px-4 py-3">Event</th>
                            <th className="px-4 py-3">IP Address</th>
                            <th className="px-4 py-3">Time</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-[var(--panel-border)]">
                          {auditLogs.map(log => (
                            <tr key={log.id} className="hover:bg-[var(--btn-secondary-bg)] transition-colors">
                              <td className="px-4 py-3 font-bold text-[var(--text-primary)]">{log.event}</td>
                              <td className="px-4 py-3 text-[var(--text-muted)] font-mono">{log.ip}</td>
                              <td className="px-4 py-3 text-[var(--text-muted)]">{log.time}</td>
                            </tr>
                          ))}
                        </tbody>
                     </table>
                   </div>
                </div>

                <div className="p-4 bg-gradient-to-br from-[rgba(0,229,204,0.15)] to-[rgba(124,92,252,0.1)] rounded-3xl border border-[var(--accent-blue-border)] flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-[var(--text-active)] animate-ping" />
                    <span className="text-[10px] font-black text-white tracking-widest">Multi-Factor Auth Active</span>
                  </div>
                  <ShieldCheck className="w-5 h-5 text-[var(--text-active)]" />
                </div>
              </div>
            </section>

          </div>
        </div>
      </main>

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
        .animate-fade-in {
          animation: fadeIn 0.8s ease-out forwards;
        }
        .animate-fade-in-up {
          animation: fadeInUp 0.8s ease-out forwards;
        }
        .delay-100 { animation-delay: 0.1s; }
        .delay-200 { animation-delay: 0.2s; }
        .delay-300 { animation-delay: 0.3s; }
        
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes fadeInUp {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
};

export default SettingsPage;
