import { useEffect, useRef, useMemo } from 'react';
import {
  Download,
  Calendar,
  FolderCheck,
  AlertTriangle,
  ShieldCheck,
  Zap,
  Plus,
  Minus,
  Activity
} from 'lucide-react';
import Sidebar from '../../components/layout/Sidebar';
import { useTheme } from '../../hooks/useTheme';

const AnalyticsPage = () => {
  return (
    <div className="flex h-screen overflow-hidden" style={{ background: 'var(--page-bg)', color: 'var(--text-primary)' }}>
      <style>
        {`
          .glass-card {
            background: var(--panel-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--panel-border);
          }
          .neon-glow {
            box-shadow: 0 0 15px var(--accent-blue-transparent);
          }
          .heatmap-cell {
            width: 12px;
            height: 12px;
            border-radius: 2px;
          }
          .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
          }
          .custom-scrollbar::-webkit-scrollbar-track {
            background: transparent;
          }
          .custom-scrollbar::-webkit-scrollbar-thumb {
            background: var(--panel-border);
            border-radius: 3px;
          }
          .cesium-viewer-bottom {
            display: none !important;
          }
          .cesium-viewer {
            background: transparent !important;
          }
          .cesium-canvas {
            filter: var(--map-filter);
            opacity: 0.4;
            transition: opacity 1s ease, filter 0.5s ease;
          }
          .group-hover-map .cesium-canvas {
            opacity: 0.6;
          }
        `}
      </style>

      <Sidebar activeTab="Analytics" />

      <main className="flex-1 flex flex-col h-screen overflow-y-auto custom-scrollbar" style={{ background: 'var(--page-bg)' }}>
        <AnalyticsContent />
      </main>
    </div>
  );
};

const AnalyticsContent = () => {
  const cesiumContainerRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<any>(null);
  const { theme: _theme } = useTheme();

  useEffect(() => {
    const initCesium = () => {
      const Cesium = (window as any).Cesium;
      if (Cesium && cesiumContainerRef.current && !viewerRef.current) {
        viewerRef.current = new Cesium.Viewer(cesiumContainerRef.current, {
          imageryProvider: new Cesium.OpenStreetMapImageryProvider({
            url: 'https://a.tile.openstreetmap.org/'
          }),
          baseLayerPicker: false,
          geocoder: false,
          homeButton: false,
          infoBox: false,
          sceneModePicker: false,
          selectionIndicator: false,
          timeline: false,
          navigationHelpButton: false,
          animation: false,
          fullscreenButton: false,
          scene3DOnly: true,
        });

        viewerRef.current.camera.setView({
          destination: Cesium.Cartesian3.fromDegrees(0, 20, 20000000)
        });
      }
    };

    const timer = setTimeout(initCesium, 100);

    return () => {
      clearTimeout(timer);
      if (viewerRef.current) {
        (viewerRef.current as any).destroy();
        viewerRef.current = null;
      }
    };
  }, []);

  return (
    <>
      <div className="p-8 space-y-8 max-w-[1600px] mx-auto w-full">
        <div className="flex items-end justify-between">
          <div>
            <h2 className="text-3xl font-display font-bold tracking-tight uppercase" style={{ color: 'var(--text-heading)' }}>Command Center</h2>
            <p className="mt-1" style={{ color: 'var(--text-secondary)' }}>Real-time forensic integrity monitoring and threat analysis.</p>
          </div>
          <div className="flex gap-3">
            <button className="flex items-center gap-2 px-4 py-2 rounded text-sm font-medium transition-all" style={{ background: 'var(--btn-secondary-bg)', border: '1px solid var(--panel-border)', color: 'var(--text-primary)' }}>
              <Calendar className="w-4 h-4" />
              Last 24 Hours
            </button>
            <button className="flex items-center gap-2 px-4 py-2 rounded text-sm font-bold shadow-lg transition-all" style={{ background: '#00E5CC', color: '#020617' }}>
              <Download className="w-4 h-4" />
              Export Report
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KPIStoreCard title="Total Scans" value="1,284,592" change="+12.5%" icon={FolderCheck} color="#00E5CC" />
          <KPIStoreCard title="Threats Detected" value="42,301" change="+5.2%" icon={AlertTriangle} color="var(--accent-red)" />
          <KPIStoreCard title="System Accuracy" value="99.7%" change="+0.1%" icon={ShieldCheck} color="#00E5CC" />
          <KPIStoreCard title="Avg. Analysis Time" value="1.2s" change="-0.4%" icon={Zap} color="#00E5CC" />
        </div>

        <div className="glass-card rounded-xl p-8 overflow-hidden">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
            <div>
              <h3 className="text-xl font-display font-bold uppercase tracking-wider" style={{ color: 'var(--text-heading)' }}>Threat Detection Trends</h3>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Aggregated forensic telemetry across all media vectors.</p>
            </div>
            <div className="flex flex-wrap gap-4">
              <ChartLegend color="#00E5CC" label="Video" />
              <ChartLegend color="var(--accent-green)" label="Audio" />
              <ChartLegend color="var(--accent-yellow)" label="Image" />
              <ChartLegend color="var(--text-muted)" label="Text" />
            </div>
          </div>
          <div className="h-64 w-full relative">
            <svg className="w-full h-full" viewBox="0 0 1000 250" preserveAspectRatio="none">
              <line stroke="var(--panel-border)" x1="0" x2="1000" y1="50" y2="50"></line>
              <line stroke="var(--panel-border)" x1="0" x2="1000" y1="100" y2="100"></line>
              <line stroke="var(--panel-border)" x1="0" x2="1000" y1="150" y2="150"></line>
              <line stroke="var(--panel-border)" x1="0" x2="1000" y1="200" y2="200"></line>
              
              <path d="M0,200 Q100,180 200,190 T400,150 T600,100 T800,130 T1000,80 L1000,250 L0,250 Z" fill="var(--accent-blue-transparent)" stroke="var(--accent-blue)" strokeWidth="2"></path>
              <path d="M0,210 Q150,200 300,180 T500,195 T750,150 T1000,160 L1000,250 L0,250 Z" fill="var(--accent-green-transparent)" stroke="var(--accent-green)" strokeWidth="2"></path>
              
              <circle className="animate-pulse" cx="600" cy="100" fill="var(--accent-blue)" r="4"></circle>
              <line stroke="var(--accent-blue-border)" strokeDasharray="4" x1="600" x2="600" y1="0" y2="250"></line>
            </svg>
          </div>
          <div className="flex justify-between mt-4 px-2">
            {['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '23:59'].map(time => (
              <span key={time} className="text-[10px] font-bold font-mono" style={{ color: 'var(--text-muted)' }}>{time}</span>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="glass-card rounded-xl p-6 lg:col-span-1">
            <h3 className="text-lg font-display font-bold mb-6 uppercase tracking-wider" style={{ color: 'var(--text-heading)' }}>Media Distribution</h3>
            <div className="relative w-48 h-48 mx-auto flex items-center justify-center">
              <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" fill="transparent" r="16" stroke="var(--panel-border)" strokeWidth="3"></circle>
                <circle cx="18" cy="18" fill="transparent" r="16" stroke="var(--accent-blue)" strokeDasharray="45 100" strokeLinecap="round" strokeWidth="3"></circle>
                <circle cx="18" cy="18" fill="transparent" r="16" stroke="var(--accent-green)" strokeDasharray="25 100" strokeDashoffset="-45" strokeLinecap="round" strokeWidth="3"></circle>
                <circle cx="18" cy="18" fill="transparent" r="16" stroke="var(--accent-yellow)" strokeDasharray="15 100" strokeDashoffset="-70" strokeLinecap="round" strokeWidth="3"></circle>
                <circle cx="18" cy="18" fill="transparent" r="16" stroke="var(--text-muted)" strokeDasharray="15 100" strokeDashoffset="-85" strokeLinecap="round" strokeWidth="3"></circle>
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <p className="text-2xl font-bold font-display" style={{ color: 'var(--text-heading)' }}>1.2M</p>
                <p className="text-[10px] uppercase font-mono" style={{ color: 'var(--text-muted)' }}>Total Items</p>
              </div>
            </div>
            <div className="mt-8 space-y-3">
              <DistributionItem color="#00E5CC" label="Video" percent="45%" />
              <DistributionItem color="var(--accent-green)" label="Audio" percent="25%" />
              <DistributionItem color="var(--accent-yellow)" label="Image" percent="15%" />
              <DistributionItem color="var(--text-muted)" label="Text" percent="15%" />
            </div>
          </div>

          <div className="glass-card rounded-xl p-6 lg:col-span-2">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-display font-bold uppercase tracking-wider" style={{ color: 'var(--text-heading)' }}>Forensic Activity Calendar</h3>
              <div className="flex items-center gap-2 text-[10px] font-mono" style={{ color: 'var(--text-muted)' }}>
                Less <div className="w-3 h-3 rounded" style={{ background: 'var(--bg-primary)' }}></div><div className="w-3 h-3 rounded" style={{ background: 'rgba(0, 229, 204, 0.1)' }}></div><div className="w-3 h-3 rounded" style={{ background: 'rgba(0, 229, 204, 0.2)' }}></div><div className="w-3 h-3 rounded" style={{ background: '#00E5CC' }}></div> More
              </div>
            </div>
            <div className="overflow-x-auto custom-scrollbar">
              <div className="flex gap-1 py-4">
                {[...Array(26)].map((_, i) => (
                  <div key={i} className="grid grid-flow-col grid-rows-7 gap-1">
                    {[...Array(7)].map((_, j) => {
                      const opacity = Math.random();
                      const color = opacity > 0.8 ? '#00E5CC' : 
                                    opacity > 0.6 ? '#00E5CC' :
                                    opacity > 0.4 ? 'rgba(0, 229, 204, 0.2)' :
                                    opacity > 0.2 ? 'rgba(0, 229, 204, 0.1)' : 'var(--bg-primary)';
                      const style = { background: color, opacity: opacity > 0.2 ? opacity : 1 };
                      return <div key={j} className="heatmap-cell" style={style}></div>;
                    })}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl p-8 overflow-hidden relative">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8 relative z-20">
            <div>
              <h3 className="text-xl font-display font-bold uppercase tracking-wider" style={{ color: 'var(--text-heading)' }}>Global Threat Origin</h3>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Live 3D monitoring of suspect generation clusters.</p>
            </div>
            <div className="text-right">
              <p className="font-bold text-lg animate-pulse uppercase tracking-widest" style={{ color: '#00E5CC' }}>Live Uplink Active</p>
              <p className="text-[10px] font-mono uppercase" style={{ color: 'var(--text-muted)' }}>Last synchronized: 2 seconds ago</p>
            </div>
          </div>
          
          <div className="h-[500px] w-full rounded-xl relative flex items-center justify-center overflow-hidden group/map border" style={{ background: 'var(--bg-primary)', borderColor: 'var(--panel-border)' }}>
            <div 
              id="cesiumContainer" 
              ref={cesiumContainerRef} 
              className="absolute inset-0 z-0 w-full h-full"
            ></div>
            
            <div className="absolute inset-0 z-10 pointer-events-none opacity-80" style={{ background: 'linear-gradient(to top, var(--bg-primary), transparent)' }}></div>
            <div className="absolute inset-0 z-10 pointer-events-none backdrop-blur-[0.5px]"></div>

            <div className="absolute inset-0 z-20 pointer-events-none">
              <svg className="absolute inset-0 w-full h-full opacity-50" viewBox="0 0 800 400">
                <path 
                  d="M500,180 Q600,150 700,220" 
                  fill="none" 
                  stroke="#00E5CC" 
                  strokeWidth="1.5"
                  strokeDasharray="4 4"
                  className="animate-[dash_10s_linear_infinite]"
                />
              </svg>

              <div className="absolute top-[30%] left-[25%]">
                <div className="absolute inset-0 w-6 h-6 -translate-x-1/2 -translate-y-1/2 rounded-full animate-ping" style={{ background: '#00E5CC', opacity: 0.4 }}></div>
                <div className="relative w-3.5 h-3.5 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-[var(--bg-primary)]" style={{ background: '#00E5CC', boxShadow: '0 0 15px #00E5CC' }}></div>
              </div>
              
              <div className="absolute top-[40%] left-[52%]">
                <div className="absolute inset-0 w-10 h-10 -translate-x-1/2 -translate-y-1/2 rounded-full animate-ping" style={{ background: 'var(--accent-red)', opacity: 0.4 }}></div>
                <div className="relative w-5 h-5 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-[var(--bg-primary)]" style={{ background: 'var(--accent-red)', boxShadow: '0 0 20px var(--accent-red)' }}></div>
              </div>

              <div className="absolute top-[45%] left-[65%]">
                <div className="absolute inset-0 w-4 h-4 -translate-x-1/2 -translate-y-1/2 rounded-full animate-pulse" style={{ background: 'var(--accent-green)', opacity: 0.3 }}></div>
                <div className="relative w-2.5 h-2.5 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-[var(--bg-primary)]" style={{ background: 'var(--accent-green)' }}></div>
              </div>
            </div>

            <div className="absolute bottom-6 left-6 z-30 glass-card p-4 rounded-lg w-64 animate-in fade-in slide-in-from-left-4 duration-700" style={{ borderColor: 'var(--accent-red-border)' }}>
              <div className="flex items-center gap-3 mb-2">
                <div className="w-2 h-2 rounded-full bg-[var(--accent-red)] animate-pulse"></div>
                <p className="text-[10px] font-bold uppercase tracking-widest font-mono" style={{ color: 'var(--accent-red)' }}>Anomaly Detected</p>
              </div>
              <p className="font-display font-medium text-xs mb-3" style={{ color: 'var(--text-primary)' }}>Unusual ingress pattern detected from cluster EU_WEST.</p>
              <div className="space-y-1.5 border-t pt-3" style={{ borderColor: 'var(--panel-border)' }}>
                <ModelDetail label="Source ID" value="TR-742-X" />
                <ModelDetail label="Threat Type" value="Deepfake Injection" />
                <ModelDetail label="Confidence" value="94.2%" color="var(--accent-red)" />
              </div>
            </div>

            <div className="absolute bottom-6 right-6 z-30 flex flex-col gap-2">
              <button className="w-10 h-10 glass-card rounded-lg flex items-center justify-center text-[var(--text-primary)] hover:bg-[var(--btn-secondary-bg)] transition-colors">
                <Plus className="w-4 h-4" />
              </button>
              <button className="w-10 h-10 glass-card rounded-lg flex items-center justify-center text-[var(--text-primary)] hover:bg-[var(--btn-secondary-bg)] transition-colors">
                <Minus className="w-4 h-4" />
              </button>
            </div>

            <div className="absolute top-6 right-6 z-30 flex items-center gap-4 backdrop-blur-md px-3 py-1.5 rounded-full border" style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}>
              <div className="flex items-center gap-2">
                <Activity className="w-3 h-3" style={{ color: '#00E5CC' }} />
                <span className="text-[8px] font-mono uppercase tracking-tighter" style={{ color: 'var(--text-secondary)' }}>Attempted bypass: <span className="text-[var(--accent-red)]">0</span></span>
              </div>
              <div className="w-px h-3" style={{ background: 'var(--panel-border)' }}></div>
              <span className="text-[8px] font-mono text-[var(--accent-green)] uppercase animate-pulse">Syncing database...</span>
            </div>
          </div>
        </div>

        <div className="glass-card rounded-xl overflow-hidden">
          <div className="p-8 border-b flex items-center justify-between" style={{ borderColor: 'var(--panel-border)', background: 'linear-gradient(to right, rgba(0,229,204,0.05), transparent)' }}>
            <div>
              <h3 className="text-xl font-display font-bold uppercase tracking-wider" style={{ color: 'var(--text-heading)' }}>AI Model Performance Fleet</h3>
              <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Validation benchmarks for detection modules.</p>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b text-[10px] font-mono uppercase tracking-widest" style={{ borderColor: 'var(--panel-border)', background: 'var(--bg-secondary)' }}>
                  <th className="px-6 py-4" style={{ color: 'var(--text-muted)' }}>Node ID</th>
                  <th className="px-6 py-4" style={{ color: 'var(--text-muted)' }}>Vector</th>
                  <th className="px-6 py-4" style={{ color: 'var(--text-muted)' }}>Accuracy</th>
                  <th className="px-6 py-4" style={{ color: 'var(--text-muted)' }}>Latency</th>
                  <th className="px-6 py-4" style={{ color: 'var(--text-muted)' }}>Throughput</th>
                  <th className="px-6 py-4" style={{ color: 'var(--text-muted)' }}>Status</th>
                </tr>
              </thead>
              <tbody className="divide-y text-sm" style={{ borderColor: 'var(--panel-border)' }}>
                <ModelRow id="ViT-Forensics-v4" vector="IMAGE" accuracy="99.82%" latency="124ms" throughput="1,200 req/m" status="Operational" statusColor="var(--accent-green)" />
                <ModelRow id="GPT-4o Detector-S" vector="TEXT" accuracy="99.41%" latency="450ms" throughput="850 req/m" status="Operational" statusColor="var(--accent-green)" />
                <ModelRow id="DeepVoice-Diff-Alpha" vector="AUDIO" accuracy="98.15%" latency="312ms" throughput="400 req/m" status="Synchronizing" statusColor="var(--accent-yellow)" pulse />
                <ModelRow id="Temporal-Flow-Video" vector="VIDEO" accuracy="99.12%" latency="890ms" throughput="120 req/m" status="Operational" statusColor="var(--accent-green)" />
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <footer className="p-8 text-center text-[10px] mt-auto border-t font-mono uppercase tracking-widest relative z-20" style={{ borderColor: 'var(--panel-border)', color: 'var(--text-muted)' }}>
        <p>© 2024 FakeShield Forensics. All systems nominal.</p>
      </footer>
    </>
  );
};

const KPIStoreCard = ({ title, value, change, icon: Icon, color }: { title: string, value: string | number, change: string, icon: React.ElementType, color: string }) => {
  const heights = useMemo(() => Array(6).fill(0).map(() => 20 + Math.random() * 80), []);
  return (
    <div className="glass-card p-6 rounded-xl relative overflow-hidden group">
      <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
        <Icon className="w-10 h-10" style={{ color: 'var(--text-primary)' }} />
      </div>
      <p className="text-sm font-medium uppercase tracking-wider" style={{ color: 'var(--text-secondary)' }}>{title}</p>
      <div className="flex items-end gap-3 mt-2">
        <h3 className="text-3xl font-display font-bold" style={{ color: 'var(--text-heading)' }}>{value}</h3>
        <span className={`${change.startsWith('+') ? 'text-[var(--accent-green)]' : 'text-[var(--accent-red)]'} text-xs font-bold mb-1 flex items-center`}>{change}</span>
      </div>
      <div className="mt-4 h-8 flex items-end gap-1">
        {[...Array(6)].map((_, i) => (
          <div 
            key={i} 
            className="flex-1 rounded-t opacity-20"
            style={{ 
              height: `${heights[i]}%`,
              backgroundColor: color
            }}
          ></div>
        ))}
      </div>
    </div>
  );
};

const ChartLegend = ({ color, label }: { color: string, label: string }) => (
  <div className="flex items-center gap-2">
    <span className="w-2 h-2 rounded-full" style={{ background: color }}></span>
    <span className="text-xs font-mono uppercase" style={{ color: 'var(--text-muted)' }}>{label}</span>
  </div>
);

const DistributionItem = ({ color, label, percent }: { color: string, label: string, percent: string | number }) => (
  <div className="flex items-center justify-between text-sm" style={{ color: 'var(--text-secondary)' }}>
    <span className="flex items-center gap-2"><span className="w-2 h-2 rounded-full" style={{ background: color }}></span> {label}</span>
    <span className="font-bold font-mono" style={{ color: 'var(--text-primary)' }}>{percent}</span>
  </div>
);

const ModelRow = ({ id, vector, accuracy, latency, throughput, status, statusColor, pulse }: { id: string, vector: string, accuracy: string, latency: string, throughput: string, status: string, statusColor: string, pulse?: boolean }) => (
  <tr className="transition-colors group hover:bg-[var(--btn-secondary-bg)]">
    <td className="px-6 py-4 font-bold font-display" style={{ color: 'var(--text-heading)' }}>{id}</td>
    <td className="px-6 py-4">
      <span className="px-2 py-1 rounded text-[10px] font-bold font-mono tracking-widest border border-[var(--panel-border)] bg-[var(--bg-secondary)]" style={{ color: 'var(--text-secondary)' }}>
        {vector}
      </span>
    </td>
    <td className="px-6 py-4 font-bold font-mono text-[var(--accent-green)]">{accuracy}</td>
    <td className="px-6 py-4 font-mono" style={{ color: 'var(--text-muted)' }}>{latency}</td>
    <td className="px-6 py-4 font-mono" style={{ color: 'var(--text-muted)' }}>{throughput}</td>
    <td className="px-6 py-4">
      <span className="flex items-center gap-2 font-medium" style={{ color: 'var(--text-secondary)' }}>
        <span className={`w-2 h-2 rounded-full ${pulse ? 'animate-pulse' : ''}`} style={{ background: statusColor }}></span>
        {status}
      </span>
    </td>
  </tr>
);

const ModelDetail = ({ label, value, color = "var(--text-primary)" }: { label: string, value: string | number, color?: string }) => (
  <div className="flex justify-between items-center text-[10px]">
    <span className="font-mono uppercase" style={{ color: 'var(--text-muted)' }}>{label}</span>
    <span className="font-bold font-mono" style={{ color: color }}>{value}</span>
  </div>
);

export default AnalyticsPage;
