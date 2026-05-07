import React from 'react';
import { Settings, Menu } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

interface TopBarProps {
  searchValue?: string;
  onSearchChange?: (value: string) => void;
  onMenuClick?: () => void;
}

const TopBar: React.FC<TopBarProps> = ({ searchValue, onSearchChange, onMenuClick }) => {
  const { user } = useAuth();

  return (
    <div className="flex justify-between items-center mb-8 w-full gap-4">
      <div className="flex items-center gap-4">
        {onMenuClick && (
          <button 
            onClick={onMenuClick}
            className="lg:hidden p-2 rounded-xl border border-[var(--panel-border)] bg-[var(--panel-bg)] hover:bg-[var(--sidebar-hover-bg)] transition-colors"
          >
            <Menu size={20} style={{ color: 'var(--text-heading)' }} />
          </button>
        )}
        <div className="min-w-0">
          <h1 className="font-display text-2xl md:text-3xl font-bold tracking-tight truncate" style={{ color: 'var(--text-heading)' }}>
            {window.location.pathname === '/dashboard' ? 'Dashboard' : 
             window.location.pathname.split('/').pop()?.replace('Lab', ' Lab')}
          </h1>
          <p className="text-[10px] md:text-sm mt-0.5 md:mt-1 truncate" style={{ color: 'var(--text-secondary)' }}>
            Real-time deepfake & synthetic media intelligence
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3 md:gap-6">
        {/* Global Labs Search */}
        <div className="hidden md:flex items-center gap-3 bg-[var(--bg-secondary)] px-4 py-2.5 rounded-2xl border border-[var(--panel-border)] group focus-within:border-[#00E5CC] transition-all w-64 lg:w-80 shadow-inner">
          <svg className="w-4 h-4 text-[var(--text-muted)] group-focus-within:text-[#00E5CC] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5"></path>
          </svg>
          <input 
            type="text" 
            placeholder="Search all labs & forensic data..." 
            className="bg-transparent border-none outline-none text-xs w-full font-medium"
            style={{ color: 'var(--text-primary)' }}
            value={searchValue}
            onChange={onSearchChange ? (e) => onSearchChange(e.target.value) : undefined}
          />
          <div className="flex items-center gap-1 opacity-40 group-focus-within:opacity-100 transition-opacity">
            <span className="text-[9px] px-1.5 py-0.5 rounded bg-[var(--panel-bg)] border border-[var(--panel-border)] text-[var(--text-muted)]">⌘</span>
            <span className="text-[9px] px-1.5 py-0.5 rounded bg-[var(--panel-bg)] border border-[var(--panel-border)] text-[var(--text-muted)]">K</span>
          </div>
        </div>

      </div>
    </div>
  );
};

export default TopBar;
