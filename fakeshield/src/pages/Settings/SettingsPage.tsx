import React, { useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { 
  User, 
  Shield, 
  CreditCard, 
  MessageSquare, 
  Download, 
  Palette,
  ChevronRight,
  Globe,
  Phone,
  Info,
  Lock,
  Eye,
  EyeOff,
  CheckCircle,
  Plus,
  ExternalLink,
  Receipt,
  FileJson,
  FileSpreadsheet,
  History,
  AlertCircle,
  Bell,
  Zap,
  Activity,
  ShieldCheck,
  Monitor
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth.tsx';

import TopBar from '../../components/layout/TopBar';

const SettingsPage: React.FC = () => {
  const { user, updateUser } = useAuth();
  const [activeTab, setActiveTab] = useState('Personal information');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  
  // Form State - Personal Info
  const [firstName, setFirstName] = useState(user?.name?.split(' ')[0] || '');
  const [lastName, setLastName] = useState(user?.name?.split(' ')[1] || '');
  const [email, setEmail] = useState(user?.email || '');
  const [phone, setPhone] = useState('');
  const [about, setAbout] = useState('');
  const [country, setCountry] = useState('United States');
  const [language, setLanguage] = useState('English');
  const [reportTone, setReportTone] = useState('Detailed Technical');

  // Form State - Password
  const [currentPassword, setCurrentPassword] = useState('');

  // Privacy State
  const [ephemeralMode, setEphemeralMode] = useState(false);

  const tabs = [
    { id: 'Personal information', label: 'Personal info', icon: User, color: '#00E5CC' },
    { id: 'Change password', label: 'Password', icon: Lock, color: '#FFB800' },
    { id: 'Billing information', label: 'Billing', icon: CreditCard, color: '#0092ff' },
    { id: 'Privacy & Logic', label: 'Privacy', icon: ShieldCheck, color: '#7c5cfc' },
    { id: 'Activity Log', label: 'Activity', icon: Activity, color: '#64748b' },
    { id: 'Messages', label: 'Messages', icon: Bell, color: '#ef4444' },
    { id: 'Data export', label: 'Export', icon: Download, color: '#FF00FF' },
  ];

  // Mock Data

  const activityLog = [
    { id: 1, event: 'Success Login', ip: '192.168.1.1', device: 'Chrome on Windows 11', location: 'Mumbai, IN', time: '2 mins ago' },
    { id: 2, event: 'Password Changed', ip: '192.168.1.1', device: 'Chrome on Windows 11', location: 'Mumbai, IN', time: '3 hours ago' },
    { id: 3, event: 'Success Login', ip: '10.0.0.42', device: 'Safari on MacOS', location: 'London, UK', time: '1 day ago' },
    { id: 4, event: 'Failed Login', ip: '45.123.5.67', device: 'Firefox on Linux', location: 'Moscow, RU', time: '2 days ago' },
  ];

  const notifications = [
    { id: 1, type: 'Critical', title: 'Deepfake Detected', text: 'Critical AI signature found in video scan #8234', time: '2h ago', icon: AlertCircle, color: '#ef4444' },
    { id: 2, type: 'Success', title: 'Scan Complete', text: 'Text Forensic Analysis finished.', time: '5h ago', icon: CheckCircle, color: '#00E5CC' },
  ];

  const handleSaveProfile = () => {
    updateUser({ name: `${firstName} ${lastName}`, email });
    alert("Profile updated successfully.");
  };

  return (
    <DashboardLayout activeTab="Settings">
      <div className="max-w-6xl mx-auto px-4 md:px-8 space-y-8 md:space-y-0 md:flex gap-12 pb-16">
          
          {/* LEFT SIDEBAR TABS */}
          <div className="w-full md:w-64 flex-shrink-0 mt-12 mb-8">
            <div className="space-y-1 mb-8">
              <h1 className="text-4xl font-display font-black text-[#00E5CC] tracking-tighter uppercase">Settings</h1>
              <div className="flex items-center gap-2">
                <span className="w-8 h-[1px] bg-[var(--panel-border)]"></span>
                <p className="text-[10px] font-bold text-[var(--text-muted)] tracking-[0.4em] uppercase">Control Panel</p>
              </div>
            </div>
            <nav className="flex md:flex-col overflow-x-auto md:overflow-x-visible pb-4 md:pb-0 gap-1 md:gap-1 no-scrollbar">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex-shrink-0 md:w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group ${
                      isActive 
                        ? 'bg-[rgba(0,229,204,0.1)] text-[#00b8a5] border border-[rgba(0,229,204,0.2)]' 
                        : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'
                    }`}
                  >
                    <div className={`w-6 h-6 rounded-full flex items-center justify-center transition-transform group-hover:scale-110 ${isActive ? 'scale-110 shadow-[0_0_10px_rgba(0,229,204,0.3)]' : ''}`} style={{ background: tab.color }}>
                      <Icon size={12} className="text-white" />
                    </div>
                    <span className="text-[13px] font-bold capitalize whitespace-nowrap">{tab.label}</span>
                  </button>
                );
              })}
            </nav>
          </div>

          {/* MAIN CONTENT AREA */}
          <div className="flex-1">
            <div className="max-w-3xl">
              <h2 className="text-2xl md:text-3xl font-black text-[var(--text-heading)] mb-8 md:mb-10">{activeTab}</h2>
              
              {activeTab === 'Personal information' && (
                <div className="space-y-12 animate-in fade-in duration-500">
                  <section>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                      <div className="space-y-2"><label className="text-[11px] font-black uppercase tracking-widest text-slate-500 ml-1">First name</label><input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3.5 outline-none focus:border-[#00E5CC] transition-all text-sm font-medium" /></div>
                      <div className="space-y-2"><label className="text-[11px] font-black uppercase tracking-widest text-slate-500 ml-1">Last name</label><input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3.5 outline-none focus:border-[#00E5CC] transition-all text-sm font-medium" /></div>
                    </div>
                    <div className="space-y-2 mb-6"><label className="text-[11px] font-black uppercase tracking-widest text-slate-500 ml-1">Email</label><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3.5 outline-none focus:border-[#00E5CC] transition-all text-sm font-medium" /></div>
                    <div className="pt-8 border-t border-slate-200 flex justify-end"><button onClick={handleSaveProfile} className="px-10 py-3 rounded-xl bg-[#00E5CC] text-[#000000] text-sm font-black hover:bg-[#00d1ba] shadow-lg shadow-[#00E5CC]/20 transition-all active:scale-95">Save Changes</button></div>
                  </section>
                </div>
              )}

              {activeTab === 'Change password' && (
                <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                  <div className="p-5 md:p-8 bg-slate-50 rounded-[2rem] border border-slate-200">
                    <form className="space-y-6">
                      <div className="space-y-2"><label className="text-[11px] font-black uppercase tracking-widest text-slate-500 ml-1">Current Password</label><input type="password" placeholder="••••••••" className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3.5 outline-none focus:border-[#00E5CC] transition-all text-sm font-medium" /></div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6"><div className="space-y-2"><label className="text-[11px] font-black uppercase tracking-widest text-slate-500 ml-1">New Password</label><input type="password" placeholder="New password" className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3.5 outline-none focus:border-[#00E5CC] transition-all text-sm font-medium" /></div><div className="space-y-2"><label className="text-[11px] font-black uppercase tracking-widest text-slate-500 ml-1">Confirm New Password</label><input type="password" placeholder="Repeat new password" className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3.5 outline-none focus:border-[#00E5CC] transition-all text-sm font-medium" /></div></div>
                      <div className="pt-6 flex justify-end"><button type="submit" className="px-10 py-3 rounded-xl bg-[#00E5CC] text-[#000000] text-sm font-black hover:bg-[#00d1ba] shadow-lg shadow-[#00E5CC]/20 transition-all active:scale-95">Update Password</button></div>
                    </form>
                  </div>
                </div>
              )}

              {activeTab === 'Billing information' && (
                <div className="space-y-10 animate-in fade-in slide-in-from-right-4 duration-500">
                   <div className="p-5 md:p-8 rounded-[2rem] md:rounded-[2.5rem] bg-gradient-to-br from-[#00E5CC] to-[#00b8a5] text-[#000000] overflow-hidden shadow-2xl shadow-[#00E5CC]/20">
                      <div className="relative z-10 flex flex-col sm:flex-row sm:justify-between sm:items-center gap-6"><div><span className="px-3 py-1 bg-[#000000]/10 rounded-full text-[10px] font-black uppercase tracking-widest border border-[#000000]/10">Current Plan</span><h3 className="text-3xl md:text-4xl font-black mt-3">Pro Forensic</h3></div><div className="sm:text-right"><p className="text-2xl md:text-3xl font-black">$29.00</p><p className="text-[10px] font-bold opacity-60 uppercase tracking-widest">per month</p></div></div>
                   </div>
                </div>
              )}

              {activeTab === 'Privacy & Logic' && (
                <div className="space-y-10 animate-in fade-in slide-in-from-top-4 duration-500">
                   {/* Ephemeral Mode */}
                   <section className="p-5 md:p-8 rounded-[2rem] md:rounded-[2.5rem] border border-[var(--panel-border)] bg-[var(--panel-bg)] group hover:border-[#00E5CC]/30 transition-all">
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-5">
                         <div className="flex items-center gap-5 min-w-0">
                            <div className={`p-4 rounded-2xl transition-colors ${ephemeralMode ? 'bg-[#00E5CC] text-[#000000]' : 'bg-[var(--btn-secondary-bg)] text-[var(--text-muted)]'}`}>
                               <Zap size={24} />
                            </div>
                            <div>
                               <h3 className="text-lg font-bold text-[var(--text-primary)]">Ephemeral Privacy Mode</h3>
                               <p className="text-xs text-[var(--text-secondary)] mt-1 max-w-[400px]">When active, nothing is saved to the cloud after a scan is finished. This is critical for high-security forensic workflows.</p>
                            </div>
                         </div>
                         <div onClick={() => setEphemeralMode(!ephemeralMode)} className={`w-14 h-7 rounded-full relative cursor-pointer transition-all duration-300 ${ephemeralMode ? 'bg-[#00E5CC]' : 'bg-slate-300'}`}>
                            <div className={`absolute top-1 w-5 h-5 bg-white rounded-full shadow-sm transition-all duration-300 ${ephemeralMode ? 'right-1' : 'left-1'}`} />
                         </div>
                      </div>
                      {ephemeralMode && (
                        <div className="mt-6 p-4 bg-[#00E5CC]/10 border border-[#00E5CC]/20 rounded-2xl flex items-center gap-3 text-[#00b8a5] text-[10px] font-black uppercase tracking-widest">
                           <ShieldCheck size={14} /> Stealth Protocol Active • Cloud Records Disabled
                        </div>
                      )}
                   </section>

                   {/* AI Report Tone */}
                   <section className="p-5 md:p-8 rounded-[2rem] md:rounded-[2.5rem] border border-[var(--panel-border)] bg-[var(--panel-bg)]">
                      <div className="mb-8">
                         <h3 className="text-lg font-bold text-[var(--text-primary)]">AI Report Tone</h3>
                         <p className="text-xs text-[var(--text-secondary)] mt-1">Calibrate how the AI Reasoner explains forensic findings in your reports.</p>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                         {['Detailed Technical', 'Executive Summary', 'Legal Standard'].map(tone => (
                           <button 
                            key={tone} 
                            onClick={() => setReportTone(tone)}
                            className={`p-5 rounded-2xl border transition-all text-left ${reportTone === tone ? 'bg-[var(--accent-blue-transparent)] border-[var(--accent-blue-border)] shadow-lg shadow-[#00E5CC]/10' : 'bg-[var(--btn-secondary-bg)] border-[var(--panel-border)] hover:border-[var(--border-hover)]'}`}
                           >
                              <div className={`w-8 h-8 rounded-lg flex items-center justify-center mb-4 ${reportTone === tone ? 'bg-[#00E5CC]/10 text-[#00E5CC]' : 'bg-[var(--btn-secondary-bg)] text-[var(--text-muted)]'}`}>
                                 <Info size={16} />
                              </div>
                              <p className={`text-xs font-bold ${reportTone === tone ? 'text-[var(--text-primary)]' : 'text-[var(--text-secondary)]'}`}>{tone}</p>
                           </button>
                         ))}
                      </div>
                   </section>
                </div>
              )}

              {activeTab === 'Activity Log' && (
                <div className="space-y-6 animate-in fade-in duration-500">
                   <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4 mb-2">
                      <div>
                         <h3 className="text-xl font-bold text-[var(--text-primary)]">Login Activity Log</h3>
                         <p className="text-xs text-[var(--text-secondary)] mt-1">Monitor recent access to your forensic laboratory.</p>
                      </div>
                      <button className="text-[10px] font-black text-[#00b8a5] uppercase tracking-widest hover:underline">Download full log</button>
                   </div>

                   <div className="overflow-x-auto border border-[var(--panel-border)] rounded-[2rem] md:rounded-[2.5rem]">
                      <table className="w-full text-left min-w-[600px]">
                         <thead className="bg-[var(--btn-secondary-bg)] border-b border-[var(--panel-border)]">
                            <tr>
                               <th className="px-6 py-4 text-[10px] font-black uppercase text-[var(--text-muted)] tracking-widest">Event</th>
                               <th className="px-6 py-4 text-[10px] font-black uppercase text-[var(--text-muted)] tracking-widest">IP Address</th>
                               <th className="px-6 py-4 text-[10px] font-black uppercase text-[var(--text-muted)] tracking-widest">Device / OS</th>
                               <th className="px-6 py-4 text-[10px] font-black uppercase text-[var(--text-muted)] tracking-widest">Location</th>
                               <th className="px-6 py-4 text-[10px] font-black uppercase text-[var(--text-muted)] tracking-widest text-right">Time</th>
                            </tr>
                         </thead>
                         <tbody className="divide-y divide-[var(--panel-border)]">
                            {activityLog.map(log => (
                              <tr key={log.id} className="hover:bg-[var(--btn-secondary-bg)] transition-colors">
                                 <td className="px-6 py-4">
                                    <div className="flex items-center gap-2">
                                       <div className={`w-2 h-2 rounded-full ${log.event.includes('Failed') ? 'bg-red-500' : 'bg-[#00E5CC]'}`} />
                                       <span className="text-xs font-bold text-[var(--text-primary)]">{log.event}</span>
                                    </div>
                                 </td>
                                 <td className="px-6 py-4 text-[11px] font-mono text-[var(--text-secondary)]">{log.ip}</td>
                                 <td className="px-6 py-4">
                                    <div className="flex items-center gap-2 text-[var(--text-secondary)]">
                                       <Monitor size={12} />
                                       <span className="text-[11px] font-medium">{log.device}</span>
                                    </div>
                                 </td>
                                 <td className="px-6 py-4 text-[11px] font-medium text-[var(--text-secondary)]">{log.location}</td>
                                 <td className="px-6 py-4 text-right text-[10px] font-bold text-[var(--text-muted)]">{log.time}</td>
                              </tr>
                            ))}
                         </tbody>
                      </table>
                   </div>
                </div>
              )}

              {activeTab === 'Messages' && (
                <div className="space-y-6 animate-in fade-in duration-500">{notifications.map(notif => (<div key={notif.id} className="p-5 md:p-6 bg-[var(--btn-secondary-bg)] rounded-3xl border border-[var(--panel-border)] flex items-start gap-4 hover:bg-[var(--border-hover)] transition-all cursor-pointer"><div className="w-12 h-12 rounded-2xl flex items-center justify-center flex-shrink-0" style={{ background: `${notif.color}15`, color: notif.color }}><notif.icon size={24} /></div><div className="flex-1 min-w-0"><div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-1 mb-1"><h4 className="text-sm font-black text-[var(--text-primary)]">{notif.title}</h4><span className="text-[10px] font-bold text-[var(--text-muted)]">{notif.time}</span></div><p className="text-xs text-[var(--text-secondary)]">{notif.text}</p></div></div>))}</div>
              )}

              {activeTab === 'Data export' && (
                <div className="space-y-8 animate-in fade-in slide-in-from-left-4 duration-500">
                   <div className="p-6 md:p-10 bg-[var(--btn-secondary-bg)] rounded-[2rem] md:rounded-[2.5rem] border border-[var(--panel-border)] text-center"><div className="w-20 h-20 bg-[var(--bg-secondary)] rounded-3xl shadow-xl flex items-center justify-center mx-auto mb-6 text-[#FF00FF]"><Download size={32} /></div><h3 className="text-xl md:text-2xl font-black text-[var(--text-primary)] mb-2">Export Laboratory Data</h3><p className="text-sm text-[var(--text-secondary)] max-w-md mx-auto">Download a complete, accurate record of all your forensic scans.</p></div>
                   <div className="grid grid-cols-1 sm:grid-cols-2 gap-6"><button className="p-6 md:p-8 bg-[var(--bg-secondary)] border border-[var(--panel-border)] rounded-[2rem] text-left hover:border-[#00E5CC] transition-all group"><div className="w-12 h-12 bg-[var(--btn-secondary-bg)] rounded-2xl flex items-center justify-center text-blue-500 mb-6"><FileJson size={24} /></div><h4 className="text-lg font-bold text-[var(--text-primary)] mb-1">Raw JSON Format</h4></button><button className="p-6 md:p-8 bg-[var(--bg-secondary)] border border-[var(--panel-border)] rounded-[2rem] text-left hover:border-[#00E5CC] transition-all group"><div className="w-12 h-12 bg-[var(--btn-secondary-bg)] rounded-2xl flex items-center justify-center text-green-500 mb-6"><FileSpreadsheet size={24} /></div><h4 className="text-lg font-bold text-[var(--text-primary)] mb-1">CSV Spreadsheet</h4></button></div>
                </div>
              )}
            </div>
          </div>
        </div>
        <div className="h-24" />
    </DashboardLayout>
  );
};

export default SettingsPage;
