import React, { useState } from 'react';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import { Menu } from 'lucide-react';

interface DashboardLayoutProps {
  children: React.ReactNode;
  activeTab: string;
  showTopBar?: boolean;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children, activeTab, showTopBar = true }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden" style={{ background: 'var(--page-bg)', color: 'var(--text-primary)', fontFamily: "'Inter', sans-serif" }}>
      <Sidebar activeTab={activeTab} isOpen={isSidebarOpen} onClose={() => setIsSidebarOpen(false)} />

      <main className="flex-1 overflow-y-auto flex flex-col" style={{ scrollbarWidth: 'thin', scrollbarColor: 'rgba(255,255,255,0.08) transparent' }}>
        {(showTopBar && window.location.pathname === '/dashboard') && (
          <div className="px-4 md:px-8 pt-10 pb-4 shrink-0">
            <TopBar onMenuClick={() => setIsSidebarOpen(true)} />
          </div>
        )}
        {window.location.pathname !== '/dashboard' && (
          <button
            onClick={() => setIsSidebarOpen(true)}
            className="fixed left-4 top-4 z-[60] lg:hidden p-2.5 rounded-xl border border-[var(--panel-border)] bg-[var(--glass-bg)] backdrop-blur-xl shadow-lg active:scale-95 transition-all"
            aria-label="Open navigation"
          >
            <Menu size={20} style={{ color: 'var(--text-heading)' }} />
          </button>
        )}
        <div className="flex-1 overflow-y-auto">
          {children}
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
