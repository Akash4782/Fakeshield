import React from 'react';
import {
  LayoutDashboard,
  FileText,
  Image as ImageIcon,
  Mic2,
  Video,
  BarChart3 as Analysis,
  Settings,
  Sun,
  Moon
} from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../../hooks/useTheme';
import logo from '../../assets/logo.png';

interface SidebarProps {
  activeTab?: string;
}

const Sidebar: React.FC<SidebarProps> = ({ activeTab }) => {
  const location = useLocation();
  const { theme, toggleTheme } = useTheme();
  
  const menuItems = [
    { name: 'Dashboard', icon: LayoutDashboard, path: '/dashboard' },
    { name: 'Image Lab', icon: ImageIcon, path: '/image-lab' },
    { name: 'Text Lab', icon: FileText, path: '/text-lab' },
    { name: 'Audio Lab', icon: Mic2, path: '/audio-lab' },
    { name: 'Video Lab', icon: Video, path: '/video-lab' },
    { name: 'Analytics', icon: Analysis, path: '/analytics' },
  ];

  const currentTab = activeTab || menuItems.find(item => item.path === location.pathname)?.name || 'Image Lab';

  return (
    <aside className="w-64 flex-shrink-0 border-r flex flex-col z-[60]" style={{ background: 'var(--sidebar-bg)', borderColor: 'var(--panel-border)' }}>
      {/* Brand */}
      <div className="p-8 pb-4 flex items-center justify-start">
        <Link to="/dashboard" className="transition-transform hover:scale-105 active:scale-95">
          <img 
            src={logo} 
            alt="FakeShield Logo" 
            style={{ 
              height: '6.5rem', 
              width: 'auto',
              filter: theme === 'dark' ? 'brightness(1.1) contrast(1.1)' : 'none' 
            }}
          />
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-4 space-y-2 overflow-y-auto custom-scrollbar">
        {menuItems.slice(0, 5).map((item) => {
          const isActive = item.name === currentTab;
          const Icon = item.icon;

          return (
            <Link
              key={item.name}
              to={item.path}
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

        {/* Separator space or middle items if needed, but the image shows them as a list */}
        {menuItems.slice(5).map((item) => {
          const isActive = item.name === currentTab;
          const Icon = item.icon;

          return (
            <Link
              key={item.name}
              to={item.path}
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
      </div>
    </aside>
  );
};

export default Sidebar;
