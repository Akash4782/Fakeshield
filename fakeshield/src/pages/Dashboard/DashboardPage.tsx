import React, { useState, useEffect } from 'react';
import Sidebar from '../../components/layout/Sidebar';
import ThreatRadar from './ThreatRadar';
import { useTheme } from '../../hooks/useTheme';

const DashboardPage: React.FC = () => {
  const { theme } = useTheme();
  const [displayText, setDisplayText] = useState('');
  const fullText = "Today’s activity shows a 15% rise in high-quality voice clones. We recommend extra caution with audio-only verification.";

  useEffect(() => {
    let i = 0;
    const timer = setInterval(() => {
      setDisplayText(fullText.substring(0, i));
      i++;
      if (i > fullText.length) clearInterval(timer);
    }, 50);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex h-screen overflow-hidden font-sans" style={{ background: 'var(--page-bg)', color: 'var(--text-primary)' }}>
      <Sidebar activeTab="Dashboard" />
      
      <main className="flex-1 overflow-y-auto relative p-6 custom-scrollbar">
        {/* Top Header Row */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="font-display text-3xl font-bold tracking-tight" style={{ color: 'var(--text-heading)' }}>Dashboard</h1>
            <p className="text-sm mt-1" style={{ color: 'var(--text-secondary)' }}>Real-time deepfake & synthetic media intelligence</p>
          </div>
        </div>

        {/* Bento Grid Container */}
        <div className="grid grid-cols-12 gap-6 pb-24">
          
          {/* Global Veracity Score */}
          <div className="col-span-12 lg:col-span-4 p-6 flex flex-col justify-between relative overflow-hidden h-[300px]" style={{ background: 'var(--panel-bg)', border: '1px solid var(--panel-border)', borderRadius: '1.5rem' }}>
            <div className="absolute top-0 right-0 p-4 opacity-10">
              <svg className="w-24 h-24" fill="currentColor" viewBox="0 0 24 24" style={{ color: '#00E5CC' }}>
                <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"></path>
              </svg>
            </div>
            <h3 className="font-display text-xs font-bold uppercase tracking-widest mb-4" style={{ color: 'var(--text-secondary)' }}>Global Veracity Score</h3>
            <div className="flex flex-col items-center justify-center relative">
              <div className="relative w-48 h-24 overflow-hidden">
                <div className="absolute top-0 left-0 w-48 h-48 border-[12px] opacity-20 rounded-full" style={{ borderColor: 'var(--text-secondary)' }}></div>
                <div 
                  className="absolute top-0 left-0 w-48 h-48 border-[12px] rounded-full" 
                  style={{ borderColor: '#00E5CC', clipPath: 'polygon(0 0, 100% 0, 100% 50%, 0 50%)', transform: 'rotate(151deg)' }}
                ></div>
                <div className="absolute inset-0 flex items-end justify-center">
                  <span className="font-display text-5xl font-bold mb-[-8px]" style={{ color: 'var(--text-heading)' }}>84%</span>
                </div>
              </div>
                <p className="text-xs font-bold uppercase tracking-widest mt-4" style={{ color: '#00E5CC' }}>Trust Level: Stable</p>
            </div>
            <div className="mt-4 pt-4 border-t border-[var(--panel-border)]">
              <div className="flex items-center justify-between">
                <div className="flex flex-col">
                  <span className="text-[10px] uppercase font-bold tracking-widest" style={{ color: 'var(--text-secondary)' }}>Risk Trend</span>
                  <span className="text-[var(--accent-red)] text-sm font-medium">+5.2% synthetic activity</span>
                </div>
                <div className="w-20 h-6">
                  <svg className="w-full h-full text-[var(--accent-red)]" viewBox="0 0 100 30">
                    <path d="M0 25 L10 20 L20 22 L30 15 L40 18 L50 10 L60 12 L70 5 L80 8 L90 2 L100 5" fill="none" stroke="currentColor" strokeWidth="2"></path>
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* Shield Efficiency KPIs */}
          <div className="col-span-12 lg:col-span-4 grid grid-rows-3 gap-4">
            <div className="glass-card p-4 flex items-center gap-4 group hover:bg-[var(--btn-secondary-bg)] transition-colors cursor-default">
              <div className="w-12 h-12 rounded-xl bg-[rgba(0,229,204,0.1)] flex items-center justify-center text-[#00E5CC]">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
                </svg>
              </div>
              <div>
                <p className="text-[10px] uppercase font-bold tracking-widest" style={{ color: 'var(--text-secondary)' }}>Total Scans</p>
                <h4 className="text-2xl font-display font-bold" style={{ color: 'var(--text-heading)' }}>1,284</h4>
              </div>
            </div>
            <div className="glass-card p-4 flex items-center gap-4 group hover:bg-[var(--btn-secondary-bg)] transition-colors cursor-default">
              <div className="w-12 h-12 rounded-xl bg-[var(--accent-red-transparent)] flex items-center justify-center text-[var(--accent-red)]">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
                </svg>
              </div>
              <div>
                <p className="text-[10px] uppercase font-bold tracking-widest" style={{ color: 'var(--text-secondary)' }}>Threats Blocked</p>
                <h4 className="text-2xl font-display font-bold" style={{ color: 'var(--text-heading)' }}>92</h4>
              </div>
            </div>
            <div className="glass-card p-4 flex items-center gap-4 group hover:bg-[var(--btn-secondary-bg)] transition-colors cursor-default">
              <div className="w-12 h-12 rounded-xl bg-[var(--accent-purple-transparent)] flex items-center justify-center text-[var(--accent-purple)]">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
                </svg>
              </div>
              <div>
                <p className="text-[10px] uppercase font-bold tracking-widest" style={{ color: 'var(--text-secondary)' }}>Avg. Detection Time</p>
                <h4 className="text-2xl font-display font-bold" style={{ color: 'var(--text-heading)' }}>1.14s</h4>
              </div>
            </div>
          </div>

          {/* Multi-Modal Threat Map */}
          <div className="col-span-12 lg:col-span-4 p-6 h-[300px] flex flex-col" style={{ background: 'var(--panel-bg)', border: '1px solid var(--panel-border)', borderRadius: '1.5rem' }}>
            <h3 className="font-display text-xs font-bold uppercase tracking-widest mb-2" style={{ color: 'var(--text-secondary)' }}>Multi-Modal Threat Map</h3>
            <ThreatRadar />
          </div>

          {/* Live Activity Feed */}
          <div className="col-span-12 lg:col-span-8 flex flex-col h-[500px]" style={{ background: 'var(--panel-bg)', border: '1px solid var(--panel-border)', borderRadius: '1.5rem' }}>
            <div className="p-6 border-b flex justify-between items-center" style={{ borderColor: 'var(--panel-border)' }}>
              <h3 className="font-display text-xs font-bold uppercase tracking-widest" style={{ color: 'var(--text-secondary)' }}>Live Activity Feed</h3>
              <span className="text-[10px] px-2 py-1 rounded border" style={{ 
                color: '#00E5CC', 
                backgroundColor: 'rgba(0, 229, 204, 0.1)',
                borderColor: 'rgba(0, 229, 204, 0.2)' 
              }}>AUTO-REFRESH: ON</span>
            </div>
            <div className="flex-1 overflow-y-auto p-2">
              <table className="w-full text-left border-separate border-spacing-y-2">
                <tbody>
                  {/* Feed Item 1 */}
                  <tr className="bg-[var(--bg-secondary)] hover:bg-[var(--btn-secondary-bg)] transition-colors rounded-lg overflow-hidden">
                    <td className="p-3 rounded-l-lg">
                      <img 
                        alt="Scan Thumbnail" 
                        className="w-10 h-10 rounded object-cover border border-[var(--panel-border)]" 
                        src="https://lh3.googleusercontent.com/aida-public/AB6AXuCMU9UdG1ZRpB1hnIC-WHp4uslHvERkeE6vTv57E0Nnh0-7Charq3L5lgNgYFIyr0BlGjjYvwqM2S94FANBugmg8TFuda7FcMppVAe01rFyJxBHoA7jyWFhg636r1wrV8rKUyiny36QLZFDdc0dMyDVVtgEnjUFA-xr4HXN5GFAzVRDWttS7Azy_zkGrJ3K7g3dDMBN8s5nnTCRPrrqfSONhY88lO3bckhhy51zDMCf-_ZKH2fY4oNfL0Cbuq85WIbg7UQUmm4A27H5" 
                      />
                    </td>
                    <td className="p-3">
                      <div className="flex flex-col">
                        <span className="text-sm font-medium" style={{ color: 'var(--text-heading)' }}>Portrait_Scan_092.png</span>
                        <span className="text-[10px]" style={{ color: 'var(--text-secondary)' }}>2 mins ago • ID: FS-9281</span>
                      </div>
                    </td>
                    <td className="p-3">
                      <span className="px-2 py-1 rounded text-[10px] font-mono" style={{ background: 'var(--bg-primary)', border: '1px solid var(--panel-border)', color: 'var(--text-primary)' }}>rPPG Pulse Failure</span>
                    </td>
                    <td className="p-3 text-right rounded-r-lg">
                      <span className="px-3 py-1 bg-[var(--accent-red-transparent)] text-[var(--accent-red)] border border-[var(--accent-red-border)] rounded-full text-[10px] font-bold uppercase tracking-tighter">CRITICAL</span>
                    </td>
                  </tr>
                  {/* Feed Item 2 */}
                  <tr className="bg-[var(--bg-secondary)] hover:bg-[var(--btn-secondary-bg)] transition-colors rounded-lg overflow-hidden">
                    <td className="p-3 rounded-l-lg">
                      <div className="w-10 h-10 rounded flex items-center justify-center border" style={{ background: 'var(--bg-primary)', borderColor: 'var(--panel-border)', color: 'var(--text-secondary)' }}>
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"></path>
                        </svg>
                      </div>
                    </td>
                    <td className="p-3">
                      <div className="flex flex-col">
                        <span className="text-sm font-medium" style={{ color: 'var(--text-heading)' }}>Newsletter_Editorial.txt</span>
                        <span className="text-[10px]" style={{ color: 'var(--text-secondary)' }}>8 mins ago • ID: FS-9280</span>
                      </div>
                    </td>
                    <td className="p-3">
                      <span className="px-2 py-1 rounded text-[10px] font-mono" style={{ background: 'var(--bg-primary)', border: '1px solid var(--panel-border)', color: 'var(--text-primary)' }}>Low Perplexity</span>
                    </td>
                    <td className="p-3 text-right rounded-r-lg">
                      <span className="px-3 py-1 bg-[var(--accent-green-transparent)] text-[var(--accent-green)] border border-[var(--accent-green-border)] rounded-full text-[10px] font-bold uppercase tracking-tighter">AUTHENTIC</span>
                    </td>
                  </tr>
                  {/* Feed Item 3 */}
                  <tr className="bg-[var(--bg-secondary)] hover:bg-[var(--btn-secondary-bg)] transition-colors rounded-lg overflow-hidden">
                    <td className="p-3 rounded-l-lg">
                      <img 
                        alt="Scan Thumbnail" 
                        className="w-10 h-10 rounded object-cover border border-[var(--panel-border)]" 
                        src="https://lh3.googleusercontent.com/aida-public/AB6AXuDKTyISzo9-fFrLHjBlnTkv5-eNjL6XZvfBoMXu8oUlBFASYTa3qGYsLKVgv0UNUQxvcjVVHi0G33-tA0M2660ql-yfr7XuR2VC4jcpEi684I166n3miKFOc4AfruQkAd7m-P877hHqzg98HwMTj7CQJ03SGf9mLSvEA6eg1a-F2sj4MqTbzT_37Nesz7zVm4vF-Ozjra0kswEg-7U52GyYtNgTbqJEyzH0AcjFEyNBoruwg1-V5V5ZVggkj3Vp7iE8H0MWDdkFCJlO" 
                      />
                    </td>
                    <td className="p-3">
                      <div className="flex flex-col">
                        <span className="text-sm font-medium" style={{ color: 'var(--text-heading)' }}>Executive_Briefing.mp4</span>
                        <span className="text-[10px]" style={{ color: 'var(--text-secondary)' }}>14 mins ago • ID: FS-9279</span>
                      </div>
                    </td>
                    <td className="p-3">
                      <span className="px-2 py-1 rounded text-[10px] font-mono" style={{ background: 'var(--bg-primary)', border: '1px solid var(--panel-border)', color: 'var(--text-primary)' }}>Facial Mesh Anomaly</span>
                    </td>
                    <td className="p-3 text-right rounded-r-lg">
                      <span className="px-3 py-1 bg-[var(--accent-red-transparent)] text-[var(--accent-red)] border border-[var(--accent-red-border)] rounded-full text-[10px] font-bold uppercase tracking-tighter">CRITICAL</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Right Column Utility */}
          <div className="col-span-12 lg:col-span-4 flex flex-col gap-6">
            {/* AI Insights Briefing */}
            <div className="p-6 flex-1 flex flex-col" style={{ background: 'var(--panel-bg)', border: '1px solid var(--panel-border)', borderRadius: '1.5rem' }}>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-2 h-2 rounded-full bg-[var(--accent-purple)] animate-pulse"></div>
                <h3 className="font-display text-xs font-bold uppercase tracking-widest text-[var(--accent-purple)]">AI Insights Briefing</h3>
              </div>
              <div className="flex-1 rounded-lg p-4 font-mono text-sm leading-relaxed border border-[var(--accent-purple)]/20" style={{ background: 'var(--bg-secondary)', color: 'var(--accent-purple)' }}>
                <p className="typewriter min-h-[4rem]">
                  {displayText}
                  <span className="animate-pulse">|</span>
                </p>
              </div>
            </div>

            {/* API Health Monitor */}
            <div className="p-6" style={{ background: 'var(--panel-bg)', border: '1px solid var(--panel-border)', borderRadius: '1.5rem' }}>
            <h3 className="font-display text-xs font-bold uppercase tracking-widest mb-6" style={{ color: 'var(--text-secondary)' }}>API Health Monitor</h3>
              <div className="grid grid-cols-2 gap-4">
                {[
                  { name: 'Text Lab', status: 'Online', color: 'bg-[var(--accent-green)]', textColor: 'text-[var(--accent-green)]' },
                  { name: 'Image Lab', status: 'Online', color: 'bg-[var(--accent-green)]', textColor: 'text-[var(--accent-green)]' },
                  { name: 'Audio Lab', status: 'Maintenance', color: 'bg-[var(--accent-yellow)]', textColor: 'text-[var(--accent-yellow)]' },
                  { name: 'Video Lab', status: 'Online', color: 'bg-[var(--accent-green)]', textColor: 'text-[var(--accent-green)]' },
                ].map((lab) => (
                  <div key={lab.name} className="flex flex-col gap-1">
                    <span className="text-[10px] font-bold uppercase" style={{ color: 'var(--text-muted)' }}>{lab.name}</span>
                    <div className="flex items-center gap-2">
                      <div className={`w-1.5 h-1.5 rounded-full ${lab.color}`}></div>
                      <span className={`text-[10px] font-mono ${lab.textColor} uppercase font-bold tracking-widest`}>{lab.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

        </div>
      </main>

      <style>{`
        .glass-card {
          background: var(--panel-bg);
          backdrop-filter: blur(12px);
          border: 1px solid var(--panel-border);
          border-radius: 1rem;
        }
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: var(--panel-border);
          border-radius: 10px;
        }
      `}</style>
    </div>
  );
};

export default DashboardPage;
