import React, { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, 
  FileText, 
  Image as ImageIcon, 
  Mic2, 
  Video, 
  Settings, 
  Sun, 
  Moon,
  LogOut,
  Crown,
  ShieldCheck,
  ArrowRight
} from 'lucide-react';
import { useTheme } from '../../hooks/useTheme';
import { useAuth } from '../../hooks/useAuth.tsx';
import logo from '../../assets/logo.png';

interface SidebarProps {
  activeTab?: string;
  isOpen?: boolean;
  onClose?: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeTab, isOpen, onClose }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const { user, logout, isAuthenticated } = useAuth();

  const [showConfirm, setShowConfirm] = useState(false);

  // Close on Esc
  useEffect(() => {
    if (!showConfirm) return;
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') setShowConfirm(false); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [showConfirm]);

  const handleLogout = () => {
    logout();
    navigate('/', { replace: true });
  };
  
  const menuItems = [
    { name: 'Dashboard', icon: LayoutDashboard, path: '/dashboard' },
    { name: 'Image lab', icon: ImageIcon, path: '/image-lab' },
    { name: 'Text lab', icon: FileText, path: '/text-lab' },
    { name: 'Audio lab', icon: Mic2, path: '/audio-lab' },
    { name: 'Video lab', icon: Video, path: '/video-lab' },
  ];

  const currentTab = activeTab || menuItems.find(item => item.path === location.pathname)?.name || 'Image lab';

  const isPaid = user?.subscription_tier === 'paid';

  return (
    <>
    {/* ── Logout Confirmation Modal ── */}
    {showConfirm && (
      <div
        className="fixed inset-0 z-[999] flex items-end sm:items-center justify-center"
        style={{ background: 'rgba(0,0,0,0.55)', backdropFilter: 'blur(6px)' }}
        onClick={() => setShowConfirm(false)}
      >
        <div
          className="w-full sm:w-[400px] rounded-t-2xl sm:rounded-2xl border flex flex-col overflow-hidden"
          style={{
            background: 'var(--bg-primary)',
            borderColor: 'var(--panel-border)',
            boxShadow: '0 32px 80px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.04) inset',
          }}
          onClick={e => e.stopPropagation()}
        >
          {/* top red accent line */}
          <div className="h-[2px] w-full" style={{ background: 'linear-gradient(90deg, #ef4444 0%, rgba(239,68,68,0) 60%)' }} />

          {/* header */}
          <div className="px-6 pt-6 pb-5 flex items-start gap-4">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 mt-0.5"
              style={{ background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.15)' }}>
              <LogOut size={17} style={{ color: '#ef4444' }} />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-[14px] font-bold leading-snug" style={{ color: 'var(--text-heading)' }}>
                Sign out of FakeShield
              </p>
              <p className="text-[12px] mt-1 leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
                Your session will be terminated and you will be redirected to the landing page.
              </p>
            </div>
          </div>

          {/* session info row */}
          <div className="mx-6 mb-5 px-4 py-3 rounded-xl border flex items-center gap-3"
            style={{ background: 'rgba(255,255,255,0.02)', borderColor: 'var(--panel-border)' }}>
            <div className="w-7 h-7 rounded-lg flex items-center justify-center text-[11px] font-black text-black flex-shrink-0"
              style={{ background: '#00E5CC' }}>
              {(user?.name || user?.fullName || 'U').charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-[12px] font-semibold truncate" style={{ color: 'var(--text-heading)' }}>
                {user?.name || user?.fullName || 'User Account'}
              </p>
              <p className="text-[10px] font-mono truncate" style={{ color: 'var(--text-secondary)' }}>
                {user?.email ?? 'session active'}
              </p>
            </div>
            <span className="text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded-md flex-shrink-0"
              style={{ background: 'rgba(0,229,204,0.08)', color: '#00E5CC', border: '1px solid rgba(0,229,204,0.15)' }}>
              {user?.subscription_tier === 'paid' ? 'PRO' : 'FREE'}
            </span>
          </div>

          {/* divider */}
          <div className="mx-6" style={{ height: '1px', background: 'var(--panel-border)' }} />

          {/* actions */}
          <div className="px-6 py-5 flex items-center gap-3">
            <button
              onClick={() => setShowConfirm(false)}
              className="flex-1 py-2.5 rounded-xl text-[13px] font-semibold border transition-all hover:bg-white/5 active:scale-95"
              style={{ borderColor: 'var(--panel-border)', color: 'var(--text-secondary)' }}
            >
              Cancel
            </button>
            <button
              onClick={handleLogout}
              className="flex-1 py-2.5 rounded-xl text-[13px] font-bold transition-all hover:opacity-90 active:scale-95 flex items-center justify-center gap-2"
              style={{ background: '#ef4444', color: '#fff' }}
            >
              <LogOut size={14} />
              Sign out
            </button>
          </div>

          {/* keyboard hint */}
          <div className="px-6 pb-5 flex items-center gap-1.5">
            <span className="text-[9px] px-1.5 py-0.5 rounded border font-mono" style={{ borderColor: 'var(--panel-border)', color: 'var(--text-secondary)' }}>Esc</span>
            <span className="text-[10px]" style={{ color: 'var(--text-secondary)' }}>to cancel</span>
          </div>
        </div>
      </div>
    )}

    {/* Mobile Overlay */}
    {isOpen && (
      <div 
        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[70] lg:hidden transition-opacity duration-300"
        onClick={onClose}
      />
    )}

    <aside 
      className={`
        fixed lg:static inset-y-0 left-0 w-64 flex-shrink-0 border-r flex flex-col z-[80] 
        transition-transform duration-300 transform 
        ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `} 
      style={{ background: 'var(--sidebar-bg)', borderColor: 'var(--panel-border)' }}
    >
      {/* Brand */}
      <div className="p-8 pb-4 flex items-center justify-between">
        <Link to="/dashboard" className="transition-transform hover:scale-105 active:scale-95">
          <img 
            src={logo} 
            alt="FakeShield Logo" 
            style={{ 
              height: '5.5rem', 
              width: 'auto',
              filter: theme === 'dark' ? 'brightness(1.1) contrast(1.1)' : 'none' 
            }}
          />
        </Link>
        {isPaid && (
          <div className="bg-gradient-to-r from-[#FFD700] to-[#FFA500] p-1.5 rounded-lg shadow-lg">
            <Crown size={16} className="text-black" />
          </div>
        )}
      </div>

      {/* Subscription Status Card - Clean Light Theme */}
      <div className="px-6 py-6 mt-2">
        <div className="group relative p-4 rounded-2xl bg-white border border-slate-200 hover:border-[#00E5CC]/50 transition-all duration-300 shadow-sm overflow-hidden">
          {/* Subtle Background Accent */}
          <div className="absolute -top-12 -right-12 w-24 h-24 bg-[#00E5CC]/5 rounded-full blur-2xl group-hover:bg-[#00E5CC]/10 transition-all duration-500"></div>
          
          <div className="relative z-10">
            <div className="flex items-center justify-between mb-4">
              <div className="flex flex-col">
                <span className="text-[9px] font-bold text-slate-400 uppercase tracking-[0.2em] mb-0.5">Account Status</span>
                <span className={`text-xs font-black tracking-wide ${isPaid ? 'text-[#00E5CC]' : 'text-slate-800'}`}>
                  {isPaid ? 'PREMIUM SHIELD' : 'STANDARD ACCESS'}
                </span>
              </div>
              <div className={`p-1.5 rounded-lg ${isPaid ? 'bg-[#00E5CC]/10' : 'bg-slate-100'}`}>
                {isPaid ? <Crown size={14} className="text-[#00E5CC]" /> : <ShieldCheck size={14} className="text-slate-400" />}
              </div>
            </div>

            {!isPaid ? (
              <Link 
                to="/subscription" 
                className="flex items-center justify-center gap-2 w-full py-2.5 rounded-xl bg-[#00E5CC] hover:bg-[#00d1ba] text-black text-[11px] font-black transition-all duration-200 active:scale-95 shadow-lg shadow-[#00E5CC]/20"
              >
                <span>Unlock Full Access</span>
                <ArrowRight size={12} className="opacity-70 group-hover:translate-x-1 transition-transform" />
              </Link>
            ) : (
              <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden mt-2">
                <div className="h-full w-full bg-gradient-to-r from-[#00E5CC] to-indigo-500"></div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-4 space-y-2 overflow-y-auto custom-scrollbar">
        {menuItems.map((item) => {
          const isActive = item.name === currentTab;
          const Icon = item.icon;

          return (
            <Link
              key={item.name}
              to={item.path}
              onClick={onClose}
              className={`
                flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 cursor-pointer group
                ${isActive
                  ? 'bg-[#00E5CC]/10 border border-[#00E5CC]/30 text-[#00E5CC] shadow-[0_0_15px_rgba(0,229,204,0.15)]'
                  : 'text-[var(--text-inactive)] hover:text-[var(--text-active)] hover:bg-[var(--sidebar-hover-bg)]'
                }
              `}
            >
              <Icon className={`w-5 h-5 ${isActive ? 'text-[#00E5CC]' : 'group-hover:text-[var(--text-active)] transition-colors'}`} />
              <span className="font-medium text-[15px]">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer / Settings at bottom */}
      <div className="p-6 border-t flex flex-col gap-2" style={{ borderColor: 'var(--panel-border)' }}>
        <Link 
          to="/settings"
          onClick={onClose}
          className={`
            flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 cursor-pointer group
            ${currentTab === 'Settings'
              ? 'bg-[#00E5CC]/10 border border-[#00E5CC]/30 text-[#00E5CC] shadow-[0_0_15px_rgba(0,229,204,0.15)]'
              : 'text-[var(--text-inactive)] hover:text-[var(--text-active)] hover:bg-[var(--sidebar-hover-bg)]'
            }
          `}
        >
          <Settings className={`w-5 h-5 ${currentTab === 'Settings' ? 'text-[#00E5CC]' : 'group-hover:text-[var(--text-active)] transition-colors'}`} />
          <span className="font-medium text-[15px]">Settings</span>
        </Link>
        
        <button
          onClick={(e) => toggleTheme(e)}
          className="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 cursor-pointer group text-[var(--text-inactive)] hover:text-[var(--text-active)] hover:bg-[var(--sidebar-hover-bg)]"
        >
          {theme === 'dark' ? (
            <>
              <Sun className="w-5 h-5 group-hover:text-[var(--text-active)] transition-colors" />
              <span className="font-medium text-[15px]">Light Mode</span>
            </>
          ) : (
            <>
              <Moon className="w-5 h-5 group-hover:text-[var(--text-active)] transition-colors" />
              <span className="font-medium text-[15px]">Dark Mode</span>
            </>
          )}
        </button>
        
        <button
          onClick={() => setShowConfirm(true)}
          className="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 cursor-pointer group text-red-400 hover:text-red-500 hover:bg-red-500/10"
        >
          <LogOut className="w-5 h-5 group-hover:text-red-500 transition-colors" />
          <span className="font-medium text-[15px]">Logout</span>
        </button>
      </div>
    </aside>
    </>
  );
};

export default Sidebar;Sidebar;
