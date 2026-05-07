import { CheckCircle2, XCircle, MapPin, Camera, Cpu, Scan, AlertCircle, Info } from 'lucide-react';

interface MetadataInspectorProps {
  metadata?: {
    camera: string;
    gps: string;
    lens: string;
    software: string;
    dimensions: string;
  };
}

type BadgeState = 'present' | 'missing' | 'ai' | 'info';

function getBadgeState(key: string, value: string): BadgeState {
  if (!value || value === 'NONE' || value === '') return 'missing';
  const v = value.toLowerCase();
  const aiKeywords = ['stable diffusion', 'midjourney', 'dall', 'firefly', 'comfy', 'automatic1111', 'flux', 'ai'];
  if (key === 'software' && aiKeywords.some(k => v.includes(k))) return 'ai';
  if (key === 'gps' && v === 'present') return 'present';
  return 'present';
}

const BADGE_CONFIG: Record<BadgeState, { color: string; bgColor: string; icon: React.ComponentType<any> }> = {
  present: { color: '#22c55e', bgColor: 'rgba(34,197,94,0.1)', icon: CheckCircle2 },
  missing: { color: '#94a3b8', bgColor: 'rgba(148,163,184,0.1)', icon: XCircle },
  ai:      { color: '#ef4444', bgColor: 'rgba(239,68,68,0.12)', icon: AlertCircle },
  info:    { color: '#0ea5e9', bgColor: 'rgba(14,165,233,0.1)',  icon: Info },
};

const FIELD_ICONS: Record<string, React.ComponentType<any>> = {
  camera: Camera,
  gps: MapPin,
  lens: Scan,
  software: Cpu,
};

const FIELD_LABELS: Record<string, string> = {
  camera: 'Camera Hardware',
  gps: 'GPS Location Data',
  lens: 'Lens Model',
  software: 'Processing Software',
};

const FIELD_NOTES: Record<string, string> = {
  camera: 'AI images have no camera make/model',
  gps: 'Real photos often embed GPS coordinates',
  lens: 'Real cameras embed lens EXIF data',
  software: 'AI tools embed their name in EXIF',
};

export default function MetadataInspector({ metadata }: MetadataInspectorProps) {
  if (!metadata) return null;

  const fields = ['camera', 'gps', 'lens', 'software'] as const;

  return (
    <div className="rounded-2xl border overflow-hidden shadow-sm" style={{ borderColor: 'var(--panel-border)', background: 'var(--panel-bg)', color: 'var(--text-primary)' }}>
      {/* Header */}
      <div
        className="px-4 py-3 border-b flex items-center justify-between"
        style={{ borderColor: 'var(--panel-border)' }}
      >
        <span className="text-xs font-bold tracking-tight text-[var(--text-primary)] uppercase">
          EXIF Metadata Guard
        </span>
        {metadata.dimensions && (
          <span className="text-[11px] font-semibold text-[var(--text-muted)]">
            {metadata.dimensions}
          </span>
        )}
      </div>

      <div className="p-3 space-y-2">
        {fields.map(key => {
          const value = metadata[key];
          const state = getBadgeState(key, value);
          const cfg = BADGE_CONFIG[state];
          const Icon = FIELD_ICONS[key] || Camera;
          const StatusIcon = cfg.icon;

          return (
            <div
              key={key}
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl"
              style={{ background: cfg.bgColor, border: `1px solid ${cfg.color}20` }}
            >
              {/* Icon */}
              <div style={{ color: cfg.color }} className="shrink-0">
                <Icon className="w-3.5 h-3.5" />
              </div>

              {/* Label + note */}
              <div className="flex-1 min-w-0">
                <div className="text-[10px] font-bold uppercase tracking-wide text-[var(--text-secondary)]">
                  {FIELD_LABELS[key]}
                </div>
                <div
                  className="text-xs mt-0.5 truncate font-bold"
                  style={{ color: state === 'missing' ? '#94a3b8' : cfg.color }}
                  title={value}
                >
                  {state === 'missing' ? 'SIGNAL MISSING' : value}
                </div>
              </div>

              {/* Badge */}
              <div
                className="shrink-0 w-6 h-6 rounded-full flex items-center justify-center"
                style={{ background: cfg.color }}
              >
                <StatusIcon className="w-3.5 h-3.5 text-white" strokeWidth={3} />
              </div>
            </div>
          );
        })}
      </div>

      {/* Forensic note */}
      <div
        className="px-4 py-3 border-t text-[10px] font-medium leading-relaxed bg-[var(--btn-secondary-bg)]"
        style={{ borderColor: 'var(--panel-border)', color: 'var(--text-secondary)' }}
      >
        <span className="font-bold text-cyan-500">FORENSIC NOTE:</span>
        {" "}Camera make/model is a primary indicator. Missing GPS or shutter speed data is common in web-optimized images but remains a diagnostic factor.
      </div>
    </div>
  );
}
