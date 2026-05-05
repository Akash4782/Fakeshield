import React, { useState } from 'react';
import Sidebar from './Sidebar';
import TopBar from './TopBar';

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
        {showTopBar && (
          <div className="px-4 md:px-8 pt-6 pb-4 shrink-0">
            <TopBar onMenuClick={() => setIsSidebarOpen(true)} />
          </div>
        )}
        <div className="flex-1 overflow-y-auto">
          {children}
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
