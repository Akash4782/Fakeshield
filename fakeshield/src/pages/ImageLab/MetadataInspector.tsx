import { CheckCircle2, XCircle, MapPin, Camera, Cpu, Aperture } from 'lucide-react';

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

const BADGE_CONFIG: Record<BadgeState, { color: string; bgColor: string; icon: string }> = {
  present: { color: '#22c55e', bgColor: 'rgba(34,197,94,0.1)', icon: '✓' },
  missing: { color: '#71717a', bgColor: 'rgba(113,113,122,0.1)', icon: '—' },
  ai:      { color: '#ef4444', bgColor: 'rgba(239,68,68,0.12)', icon: '⚠' },
  info:    { color: '#00E5CC', bgColor: 'rgba(0,229,204,0.1)',  icon: 'i' },
};

const FIELD_ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  camera: Camera,
  gps: MapPin,
  lens: Aperture as any,
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
    <div className="rounded-2xl border overflow-hidden shadow-sm" style={{ borderColor: 'var(--panel-border)', background: '#ffffff', color: '#1e293b' }}>
      {/* Header */}
      <div
        className="px-4 py-3 border-b flex items-center justify-between"
        style={{ borderColor: 'var(--panel-border)' }}
      >
        <span className="text-[10px] font-mono tracking-widest text-emerald-400 uppercase">
          EXIF Metadata Guard
        </span>
        {metadata.dimensions && (
          <span className="text-[9px] font-mono" style={{ color: 'var(--text-muted)' }}>
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
                <div className="text-[10px] font-mono uppercase tracking-wider" style={{ color: 'var(--text-muted)' }}>
                  {FIELD_LABELS[key]}
                </div>
                <div
                  className="text-[10px] font-mono mt-0.5 truncate font-bold"
                  style={{ color: state === 'missing' ? 'var(--text-muted)' : cfg.color }}
                  title={value}
                >
                  {state === 'missing' ? 'NOT FOUND' : value}
                </div>
              </div>

              {/* Badge */}
              <div
                className="shrink-0 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold"
                style={{ background: cfg.color, color: '#000' }}
              >
                {cfg.icon}
              </div>
            </div>
          );
        })}
      </div>

      {/* Forensic note */}
      <div
        className="px-4 py-2.5 border-t text-[9px] font-mono leading-relaxed"
        style={{ borderColor: 'var(--panel-border)', color: 'var(--text-muted)' }}
      >
        <span style={{ color: '#00E5CC' }}>★ </span>
        Camera make/model is a HARD VETO signal. GPS + shutter speed = strong real-photo indicator.
      </div>
    </div>
  );
}
