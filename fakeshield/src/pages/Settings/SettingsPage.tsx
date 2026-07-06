import React, { useState, useRef, useEffect } from 'react';
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
  Monitor,
  Loader2,
  Trash2
} from 'lucide-react';
import { useAuth } from '../../hooks/useAuth.tsx';
import { API_BASE_URL } from '../../config';

import TopBar from '../../components/layout/TopBar';

const SettingsPage: React.FC = () => {
  const { user, token, login, updateUser, logout } = useAuth();
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

  // Save status: 'idle' | 'saving' | 'success' | 'error'
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'success' | 'error'>('idle');
  const [saveError, setSaveError] = useState('');

  // Form State - Password
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showNew, setShowNew] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  // OTP step state
  const [pwdStep, setPwdStep] = useState<'form' | 'otp' | 'done'>('form');
  const [otpDigits, setOtpDigits] = useState(['', '', '', '', '', '']);
  const otpRefs = [useRef<HTMLInputElement>(null), useRef<HTMLInputElement>(null), useRef<HTMLInputElement>(null), useRef<HTMLInputElement>(null), useRef<HTMLInputElement>(null), useRef<HTMLInputElement>(null)];
  const otpValue = otpDigits.join('');
  const [pwdStatus, setPwdStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [pwdError, setPwdError] = useState('');
  const [pwdSuccess, setPwdSuccess] = useState('');

  // Tab state handled implicitly 

  const tabs = [
    { id: 'Personal information', label: 'Personal info', icon: User, color: '#00E5CC' },
    { id: 'Change password', label: 'Password', icon: Lock, color: '#FFB800' },
    { id: 'Billing information', label: 'Billing', icon: CreditCard, color: '#0092ff' },

    { id: 'Activity Log', label: 'Activity', icon: Activity, color: '#64748b' },
    { id: 'Data export', label: 'Export', icon: Download, color: '#FF00FF' },
    { id: 'Notifications', label: 'Notifications', icon: Bell, color: '#a855f7' },
    { id: 'Danger Zone', label: 'Danger Zone', icon: Trash2, color: '#ef4444' },
  ];

  // Mock Data

  // Activity Log State
  const [activityLog, setActivityLog] = useState<any[]>([]);
  const [loadingActivity, setLoadingActivity] = useState(false);

  useEffect(() => {
    if (activeTab === 'Activity Log') {
      const fetchActivity = async () => {
        setLoadingActivity(true);
        try {
          const res = await fetch(`${API_BASE_URL}/auth/activity`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          if (res.ok) {
            const data = await res.json();
            setActivityLog(data);
          }
        } catch (e) {
          console.error('Failed to fetch activity log', e);
        } finally {
          setLoadingActivity(false);
        }
      };
      fetchActivity();
    }
  }, [activeTab, token]);

  const [isExporting, setIsExporting] = useState(false);

  const handleExportData = async (format: 'json' | 'csv') => {
    setIsExporting(true);
    try {
      const res = await fetch(`${API_BASE_URL}/auth/export-data`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!res.ok) throw new Error('Failed to export data');
      const data = await res.json();
      
      let blob;
      let filename;
      
      if (format === 'json') {
        blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        filename = 'fakeshield_export.json';
      } else {
         const logs = data.activity_logs || [];
         let csvContent = "=== LOGIN & ACTIVITY LOGS ===\n";
         csvContent += "Event,IP,Device,Location,Time\n";
         csvContent += logs.map((l:any) => `"${l.event || ''}","${l.ip || ''}","${l.device || ''}","${l.location || ''}","${l.timestamp || l.time || ''}"`).join("\n");

         const detections = data.detections || {};
         const allDetections: any[] = [];
         
         ['video', 'audio', 'image', 'text'].forEach(type => {
            if (detections[type]) {
                detections[type].forEach((d: any) => {
                   allDetections.push({
                      type: type.toUpperCase(),
                      filename: (d.filename || d.source || d.text_excerpt || 'N/A').replace(/"/g, '""'),
                      status: d.status || d.conclusion || 'Completed',
                      risk: typeof d.ai_probability === 'number' ? (d.ai_probability * 100).toFixed(2) + '%' : (d.risk_level || 'N/A'),
                      date: d.created_at || d.timestamp || 'N/A'
                   });
                });
            }
         });

         if (allDetections.length > 0) {
            csvContent += "\n\n=== FORENSIC DETECTIONS ===\n";
            csvContent += "Scan Type,Filename/Source,Analysis Status,AI Risk / Probability,Date\n";
            csvContent += allDetections.map(d => `"${d.type}","${String(d.filename).substring(0, 50)}","${d.status}","${d.risk}","${d.date}"`).join("\n");
         }

         blob = new Blob([csvContent], { type: 'text/csv' });
         filename = 'fakeshield_export.csv';
      }
      
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (e: any) {
      console.error(e);
      alert('Error exporting data: ' + e.message);
    } finally {
      setIsExporting(false);
    }
  };

  // ── Preferences / Notifications ──
  const [prefs, setPrefs] = useState({
    email_scan_complete: true,
    email_suspicious_login: true,
    email_monthly_report: false
  });
  const [savingPrefs, setSavingPrefs] = useState(false);

  useEffect(() => {
    if (activeTab === 'Notifications') {
      fetch(`${API_BASE_URL}/auth/preferences`, { headers: { 'Authorization': `Bearer ${token}` } })
        .then(res => res.json())
        .then(data => { if (!data.detail) setPrefs(data); })
        .catch(console.error);
    }
  }, [activeTab, token]);

  const togglePref = async (key: keyof typeof prefs) => {
    const newPrefs = { ...prefs, [key]: !prefs[key] };
    setPrefs(newPrefs);
    setSavingPrefs(true);
    try {
      await fetch(`${API_BASE_URL}/auth/preferences`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(newPrefs)
      });
    } catch {}
    setSavingPrefs(false);
  };

  // ── Danger Zone (Account Deletion) ──
  const [deleteConfirm, setDeleteConfirm] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);

  const handleDeleteAccount = async () => {
    if (deleteConfirm !== 'DELETE') return;
    setIsDeleting(true);
    try {
      const res = await fetch(`${API_BASE_URL}/auth/account`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        alert("Account and all associated forensic data deleted successfully.");
        logout();
        window.location.href = '/'; 
      } else {
        const d = await res.json();
        alert(d.detail || "Error deleting account.");
      }
    } catch {
      alert("Error deleting account. Check your connection.");
    }
    setIsDeleting(false);
  };

  const handleRequestOtp = async () => {
    setPwdError('');
    setPwdSuccess('');
    if (newPassword.length < 8) { setPwdError('New password must be at least 8 characters.'); return; }
    if (newPassword !== confirmPassword) { setPwdError('New passwords do not match.'); return; }
    setPwdStatus('loading');
    try {
      const res = await fetch(`${API_BASE_URL}/auth/change-password/request-otp`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      });
      const data = await res.json();
      if (!res.ok) { setPwdStatus('error'); setPwdError(data.detail || 'Failed to send OTP.'); return; }
      setPwdStatus('idle');
      setPwdStep('otp');
      setPwdSuccess('A 6-digit OTP was sent to your email. Enter it below.');
    } catch { setPwdStatus('error'); setPwdError('Network error. Please check your connection.'); }
  };

  const handleConfirmPasswordChange = async () => {
    setPwdError('');
    setPwdSuccess('');
    if (otpValue.length !== 6) { setPwdError('Please enter the 6-digit OTP.'); return; }
    setPwdStatus('loading');
    try {
      const res = await fetch(`${API_BASE_URL}/auth/change-password/confirm`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({ new_password: newPassword, otp: otpValue }),
      });
      const data = await res.json();
      if (!res.ok) { setPwdStatus('error'); setPwdError(data.detail || 'Failed to update password.'); return; }
      setPwdStatus('success');
      setPwdStep('done');
      setPwdSuccess('Password changed successfully! Your account is now secured with the new password.');
      setNewPassword(''); setConfirmPassword(''); setOtpDigits(['', '', '', '', '', '']);
    } catch { setPwdStatus('error'); setPwdError('Network error. Please check your connection.'); }
  };

  const handleResetPwdForm = () => {
    setPwdStep('form'); setPwdStatus('idle'); setPwdError(''); setPwdSuccess('');
    setNewPassword(''); setConfirmPassword(''); setOtpDigits(['', '', '', '', '', '']);
  };


  const handleSaveProfile = async () => {
    setSaveStatus('saving');
    setSaveError('');
    try {
      const res = await fetch(`${API_BASE_URL}/auth/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          fullName: `${firstName.trim()} ${lastName.trim()}`.trim(),
          email: email.trim(),
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setSaveStatus('error');
        setSaveError(data.detail || 'Failed to save changes.');
        return;
      }

      // Persist fresh token + updated user into auth context
      if (data.access_token && data.user) {
        login(data.access_token, {
          name: data.user.name,
          email: data.user.email,
          subscription_tier: data.user.subscription_tier,
          profile_pic: data.user.profile_pic,
        });
      }

      setSaveStatus('success');
      setTimeout(() => setSaveStatus('idle'), 3000);
    } catch (err) {
      setSaveStatus('error');
      setSaveError('Network error. Please check your connection.');
    }
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
                    <div className="pt-8 border-t border-slate-200 flex flex-col items-end gap-3">
                      {saveStatus === 'error' && (
                        <p className="text-xs font-bold text-red-500 flex items-center gap-1.5">
                          <AlertCircle size={13} /> {saveError}
                        </p>
                      )}
                      {saveStatus === 'success' && (
                        <p className="text-xs font-bold text-[#00b8a5] flex items-center gap-1.5">
                          <CheckCircle size={13} /> Profile updated successfully!
                        </p>
                      )}
                      <button
                        onClick={handleSaveProfile}
                        disabled={saveStatus === 'saving'}
                        className="px-10 py-3 rounded-xl bg-[#00E5CC] text-[#000000] text-sm font-black hover:bg-[#00d1ba] shadow-lg shadow-[#00E5CC]/20 transition-all active:scale-95 disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2"
                      >
                        {saveStatus === 'saving' ? (
                          <><Loader2 size={15} className="animate-spin" /> Saving…</>
                        ) : 'Save Changes'}
                      </button>
                    </div>
                  </section>
                </div>
              )}

              {activeTab === 'Change password' && (
                <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                  <div className="p-5 md:p-8 bg-slate-50 rounded-[2rem] border border-slate-200 space-y-6">

                    {/* Step indicator */}
                    <div className="flex items-center gap-3 mb-2">
                      {['Enter Details', 'Verify via Email', 'Done'].map((label, i) => {
                        const stepNum = i + 1;
                        const currentStep = pwdStep === 'form' ? 1 : pwdStep === 'otp' ? 2 : 3;
                        const isActive = stepNum === currentStep;
                        const isDone = stepNum < currentStep;
                        return (
                          <React.Fragment key={label}>
                            <div className="flex items-center gap-2">
                              <div className={`w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-black transition-all ${
                                isDone ? 'bg-[#00E5CC] text-black' : isActive ? 'bg-[#FFB800] text-black' : 'bg-slate-200 text-slate-500'
                              }`}>
                                {isDone ? <CheckCircle size={12} /> : stepNum}
                              </div>
                              <span className={`text-[10px] font-bold uppercase tracking-widest hidden sm:block ${
                                isActive ? 'text-slate-800' : 'text-slate-400'
                              }`}>{label}</span>
                            </div>
                            {i < 2 && <div className="flex-1 h-[1px] bg-slate-200" />}
                          </React.Fragment>
                        );
                      })}
                    </div>

                    {/* STEP 1 — Password fields */}
                    {pwdStep === 'form' && (
                      <div className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div className="space-y-2">
                            <label className="text-[11px] font-black uppercase tracking-widest text-slate-500 ml-1">New Password</label>
                            <div className="relative">
                              <input
                                type={showNew ? 'text' : 'password'}
                                value={newPassword}
                                onChange={e => setNewPassword(e.target.value)}
                                placeholder="Min. 8 characters"
                                className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3.5 pr-12 outline-none focus:border-[#00E5CC] transition-all text-sm font-medium"
                              />
                              <button type="button" onClick={() => setShowNew(v => !v)} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700">
                                {showNew ? <EyeOff size={16} /> : <Eye size={16} />}
                              </button>
                            </div>
                          </div>
                          <div className="space-y-2">
                            <label className="text-[11px] font-black uppercase tracking-widest text-slate-500 ml-1">Confirm New Password</label>
                            <div className="relative">
                              <input
                                type={showConfirm ? 'text' : 'password'}
                                value={confirmPassword}
                                onChange={e => setConfirmPassword(e.target.value)}
                                placeholder="Repeat new password"
                                className="w-full bg-white border border-slate-200 rounded-xl px-4 py-3.5 pr-12 outline-none focus:border-[#00E5CC] transition-all text-sm font-medium"
                              />
                              <button type="button" onClick={() => setShowConfirm(v => !v)} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700">
                                {showConfirm ? <EyeOff size={16} /> : <Eye size={16} />}
                              </button>
                            </div>
                          </div>
                        </div>
                        {/* Password strength hint */}
                        {newPassword.length > 0 && (
                          <div className="flex items-center gap-2">
                            {[1,2,3,4].map(i => (
                              <div key={i} className={`h-1 flex-1 rounded-full transition-all ${
                                newPassword.length >= i * 4
                                  ? i <= 1 ? 'bg-red-400' : i <= 2 ? 'bg-yellow-400' : i <= 3 ? 'bg-blue-400' : 'bg-[#00E5CC]'
                                  : 'bg-slate-200'
                              }`} />
                            ))}
                            <span className="text-[10px] font-bold text-slate-400 whitespace-nowrap">
                              {newPassword.length < 8 ? 'Too short' : newPassword.length < 12 ? 'Fair' : newPassword.length < 16 ? 'Good' : 'Strong'}
                            </span>
                          </div>
                        )}
                      </div>
                    )}

                    {/* STEP 2 — OTP Entry */}
                    {pwdStep === 'otp' && (
                      <div className="space-y-6 text-center">
                        <div className="w-14 h-14 rounded-2xl bg-[#FFB800]/10 flex items-center justify-center mx-auto text-[#FFB800]">
                          <Lock size={28} />
                        </div>
                        <div>
                          <h3 className="text-lg font-black text-slate-800 mb-1">Check Your Email</h3>
                          <p className="text-sm text-slate-500">We sent a 6-digit code to <strong>{user?.email}</strong></p>
                        </div>
                        <div className="space-y-3">
                          <label className="text-[11px] font-black uppercase tracking-widest text-slate-500">Enter OTP Code</label>
                          <div className="flex justify-center gap-2">
                            {otpDigits.map((digit, idx) => (
                              <input
                                key={idx}
                                ref={otpRefs[idx]}
                                type="text"
                                inputMode="numeric"
                                maxLength={1}
                                value={digit}
                                onChange={e => {
                                  const val = e.target.value.replace(/\D/g, '').slice(-1);
                                  const next = [...otpDigits];
                                  next[idx] = val;
                                  setOtpDigits(next);
                                  if (val && idx < 5) otpRefs[idx + 1].current?.focus();
                                }}
                                onKeyDown={e => {
                                  if (e.key === 'Backspace' && !otpDigits[idx] && idx > 0) {
                                    otpRefs[idx - 1].current?.focus();
                                  }
                                }}
                                onPaste={e => {
                                  e.preventDefault();
                                  const pasted = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
                                  const next = ['', '', '', '', '', ''];
                                  pasted.split('').forEach((ch, i) => { next[i] = ch; });
                                  setOtpDigits(next);
                                  const focusIdx = Math.min(pasted.length, 5);
                                  otpRefs[focusIdx].current?.focus();
                                }}
                                className={`w-11 h-14 text-center text-2xl font-black rounded-xl border-2 outline-none transition-all ${
                                  digit
                                    ? 'border-[#FFB800] bg-[#FFB800]/5 text-slate-900'
                                    : 'border-slate-200 bg-white text-slate-400'
                                } focus:border-[#FFB800] focus:bg-[#FFB800]/5`}
                              />
                            ))}
                          </div>
                        </div>
                        <button onClick={handleResetPwdForm} className="text-xs font-bold text-slate-400 hover:text-slate-600 underline">
                          ← Go back and edit
                        </button>
                      </div>
                    )}

                    {/* STEP 3 — Done */}
                    {pwdStep === 'done' && (
                      <div className="text-center space-y-4 py-4">
                        <div className="w-16 h-16 rounded-full bg-[#00E5CC]/10 flex items-center justify-center mx-auto">
                          <CheckCircle size={32} className="text-[#00E5CC]" />
                        </div>
                        <h3 className="text-lg font-black text-slate-800">Password Updated!</h3>
                        <p className="text-sm text-slate-500">A confirmation email has been sent to <strong>{user?.email}</strong>.</p>
                        <button onClick={handleResetPwdForm} className="mt-2 text-xs font-black text-[#00b8a5] hover:underline">Change Again</button>
                      </div>
                    )}

                    {/* Feedback messages */}
                    {pwdError && (
                      <div className="flex items-center gap-2 p-3 rounded-xl bg-red-50 border border-red-100">
                        <AlertCircle size={14} className="text-red-500 flex-shrink-0" />
                        <p className="text-xs font-bold text-red-600">{pwdError}</p>
                      </div>
                    )}
                    {pwdSuccess && pwdStep !== 'done' && (
                      <div className="flex items-center gap-2 p-3 rounded-xl bg-[#00E5CC]/10 border border-[#00E5CC]/20">
                        <CheckCircle size={14} className="text-[#00b8a5] flex-shrink-0" />
                        <p className="text-xs font-bold text-[#00b8a5]">{pwdSuccess}</p>
                      </div>
                    )}

                    {/* Action buttons */}
                    {pwdStep !== 'done' && (
                      <div className="pt-4 border-t border-slate-200 flex justify-end">
                        {pwdStep === 'form' && (
                          <button
                            onClick={handleRequestOtp}
                            disabled={pwdStatus === 'loading'}
                            className="px-10 py-3 rounded-xl bg-[#FFB800] text-[#000000] text-sm font-black hover:bg-[#e6a700] shadow-lg shadow-[#FFB800]/20 transition-all active:scale-95 disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2"
                          >
                            {pwdStatus === 'loading' ? <><Loader2 size={15} className="animate-spin" /> Sending OTP…</> : '📧 Send OTP to Email'}
                          </button>
                        )}
                        {pwdStep === 'otp' && (
                          <button
                            onClick={handleConfirmPasswordChange}
                            disabled={pwdStatus === 'loading' || otpValue.length !== 6}
                            className="px-10 py-3 rounded-xl bg-[#00E5CC] text-[#000000] text-sm font-black hover:bg-[#00d1ba] shadow-lg shadow-[#00E5CC]/20 transition-all active:scale-95 disabled:opacity-60 disabled:cursor-not-allowed flex items-center gap-2"
                          >
                            {pwdStatus === 'loading' ? <><Loader2 size={15} className="animate-spin" /> Confirming…</> : '✅ Confirm Password Change'}
                          </button>
                        )}
                      </div>
                    )}
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
                               <th className="px-6 py-4 text-[10px] font-black uppercase text-[var(--text-muted)] tracking-widest">Device / OS</th>
                               <th className="px-6 py-4 text-[10px] font-black uppercase text-[var(--text-muted)] tracking-widest">Location</th>
                               <th className="px-6 py-4 text-[10px] font-black uppercase text-[var(--text-muted)] tracking-widest text-right">Time</th>
                            </tr>
                         </thead>
                         <tbody className="divide-y divide-[var(--panel-border)]">
                            {loadingActivity ? (
                              <tr><td colSpan={4} className="p-8 text-center text-sm font-bold text-[var(--text-muted)]"><Loader2 size={16} className="animate-spin inline mr-2" /> Loading records...</td></tr>
                            ) : activityLog.length === 0 ? (
                              <tr><td colSpan={4} className="p-8 text-center text-sm font-bold text-[var(--text-muted)]">No activity recorded yet.</td></tr>
                            ) : (
                              activityLog.map(log => (
                                <tr key={log.id} className="hover:bg-[var(--btn-secondary-bg)] transition-colors">
                                   <td className="px-6 py-4">
                                      <div className="flex items-center gap-2">
                                         <div className={`w-2 h-2 rounded-full ${log.event.includes('Failed') ? 'bg-red-500' : 'bg-[#00E5CC]'}`} />
                                         <span className="text-xs font-bold text-[var(--text-primary)]">{log.event}</span>
                                      </div>
                                   </td>
                                   <td className="px-6 py-4">
                                      <div className="flex items-center gap-2 text-xs font-medium text-[var(--text-secondary)]">
                                         <Monitor size={14} className="opacity-50" /> {log.device}
                                      </div>
                                   </td>
                                   <td className="px-6 py-4 text-xs font-medium text-[var(--text-secondary)]">{log.location}</td>
                                   <td className="px-6 py-4 text-xs font-bold text-[#00E5CC] text-right whitespace-nowrap">{log.time}</td>
                                </tr>
                              ))
                            )}
                         </tbody>
                      </table>
                   </div>
                </div>
              )}

              {activeTab === 'Data export' && (
                <div className="space-y-8 animate-in fade-in slide-in-from-left-4 duration-500">
                   <div className="p-6 md:p-10 bg-[var(--btn-secondary-bg)] rounded-[2rem] md:rounded-[2.5rem] border border-[var(--panel-border)] text-center"><div className="w-20 h-20 bg-[var(--bg-secondary)] rounded-3xl shadow-xl flex items-center justify-center mx-auto mb-6 text-[#FF00FF]"><Download size={32} /></div><h3 className="text-xl md:text-2xl font-black text-[var(--text-primary)] mb-2">Export Laboratory Data</h3><p className="text-sm text-[var(--text-secondary)] max-w-md mx-auto">Download a complete, accurate record of all your forensic scans and login history.</p></div>
                   <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                      <button onClick={() => handleExportData('json')} disabled={isExporting} className="p-6 md:p-8 bg-[var(--bg-secondary)] border border-[var(--panel-border)] rounded-[2rem] text-left hover:border-[#00E5CC] transition-all group disabled:opacity-50">
                          <div className="w-12 h-12 bg-[var(--btn-secondary-bg)] rounded-2xl flex items-center justify-center text-blue-500 mb-6">{isExporting ? <Loader2 className="animate-spin" /> : <FileJson size={24} />}</div>
                          <h4 className="text-lg font-bold text-[var(--text-primary)] mb-1">Raw JSON Format</h4>
                          <p className="text-xs text-[var(--text-secondary)]">Includes all deepfake detections across modules.</p>
                      </button>
                      <button onClick={() => handleExportData('csv')} disabled={isExporting} className="p-6 md:p-8 bg-[var(--bg-secondary)] border border-[var(--panel-border)] rounded-[2rem] text-left hover:border-[#00E5CC] transition-all group disabled:opacity-50">
                          <div className="w-12 h-12 bg-[var(--btn-secondary-bg)] rounded-2xl flex items-center justify-center text-green-500 mb-6">{isExporting ? <Loader2 className="animate-spin" /> : <FileSpreadsheet size={24} />}</div>
                          <h4 className="text-lg font-bold text-[var(--text-primary)] mb-1">CSV Spreadsheet</h4>
                          <p className="text-xs text-[var(--text-secondary)]">Flattened activity logs for Excel/Sheets analysis.</p>
                      </button>
                   </div>
                </div>
              )}

              {activeTab === 'Notifications' && (
                <div className="space-y-8 animate-in fade-in slide-in-from-left-4 duration-500">
                   <div className="p-6 md:p-8 bg-[var(--btn-secondary-bg)] rounded-[2rem] md:rounded-[2.5rem] border border-[var(--panel-border)]">
                      <div className="mb-6">
                         <h3 className="text-xl md:text-2xl font-black text-[var(--text-primary)]">Notification Preferences</h3>
                         <p className="text-sm text-[var(--text-secondary)] mt-1">Manage what alerts you receive in your inbox.</p>
                      </div>
                      
                      <div className="space-y-4">
                         {[
                           { key: 'email_scan_complete', label: 'Email me when an automated scan finishes', icon: CheckCircle, color: '#00E5CC' },
                           { key: 'email_suspicious_login', label: 'Alert me on suspicious logins', icon: Shield, color: '#FFB800' },
                           { key: 'email_monthly_report', label: 'Email me monthly forensic reports', icon: FileJson, color: '#0092ff' }
                         ].map(item => (
                           <div key={item.key} className="flex items-center justify-between p-4 rounded-xl border border-[var(--panel-border)] bg-[var(--bg-secondary)] hover:border-[#00E5CC]/30 transition-all">
                              <div className="flex items-center gap-4">
                                 <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ background: `${item.color}15`, color: item.color }}>
                                    <item.icon size={18} />
                                 </div>
                                 <span className="text-sm font-bold text-[var(--text-primary)]">{item.label}</span>
                              </div>
                              <button 
                                onClick={() => togglePref(item.key as keyof typeof prefs)}
                                disabled={savingPrefs}
                                className={`w-12 h-6 rounded-full relative transition-all duration-300 disabled:opacity-50 ${prefs[item.key as keyof typeof prefs] ? 'bg-[#00E5CC]' : 'bg-slate-300'}`}
                              >
                                 <div className={`absolute top-1 w-4 h-4 bg-white rounded-full shadow-sm transition-all duration-300 ${prefs[item.key as keyof typeof prefs] ? 'right-1' : 'left-1'}`} />
                              </button>
                           </div>
                         ))}
                      </div>
                   </div>
                </div>
              )}

              {activeTab === 'Danger Zone' && (
                <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                   <div className="p-6 md:p-8 bg-red-500/5 rounded-[2rem] md:rounded-[2.5rem] border border-red-500/20 text-left">
                      <div className="w-14 h-14 bg-red-500/10 rounded-2xl flex items-center justify-center text-red-500 mb-6">
                         <Trash2 size={24} />
                      </div>
                      <h3 className="text-xl md:text-2xl font-black text-red-500 mb-2">Delete Account</h3>
                      <p className="text-sm text-red-400 max-w-xl mb-6">
                        Once you delete your account, there is no going back. All of your forensic scans, payment history, and login data will be permanently wiped according to GDPR guidelines. Please be certain.
                      </p>
                      
                      <div className="max-w-md space-y-4">
                         <div>
                            <label className="text-xs font-bold text-red-500 uppercase tracking-widest mb-1 block">Type 'DELETE' to confirm</label>
                            <input 
                              type="text"
                              value={deleteConfirm}
                              onChange={(e) => setDeleteConfirm(e.target.value)}
                              placeholder="DELETE"
                              className="w-full bg-red-500/5 border border-red-500/20 focus:border-red-500 rounded-xl px-4 py-3 text-sm text-[var(--text-primary)] outline-none transition-all"
                            />
                         </div>
                         <button 
                           onClick={handleDeleteAccount}
                           disabled={deleteConfirm !== 'DELETE' || isDeleting}
                           className="w-full py-3 rounded-xl bg-red-500 text-white font-black hover:bg-red-600 active:scale-95 transition-all shadow-lg shadow-red-500/20 flex items-center justify-center gap-2 disabled:opacity-50 disabled:active:scale-100 disabled:cursor-not-allowed"
                         >
                           {isDeleting ? <><Loader2 size={16} className="animate-spin" /> Wiping Records...</> : <><Trash2 size={16} /> Permanently Delete Account</>}
                         </button>
                      </div>
                   </div>
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
