interface ELAViewerProps {
  elaUrl?: string | null;
}

export default function ELAViewer({ elaUrl }: ELAViewerProps) {
  if (!elaUrl) return null;

  return (
    <div className="rounded-2xl border overflow-hidden" style={{ borderColor: 'var(--panel-border)', background: 'rgba(0,0,0,0.25)' }}>
      {/* Header */}
      <div className="px-4 py-2.5 border-b flex items-center justify-between"
        style={{ borderColor: 'var(--panel-border)' }}>
        <span className="text-[10px] font-mono tracking-widest uppercase" style={{ color: '#eab308' }}>
          ELA — Error Level Analysis
        </span>
        <span className="text-[9px] font-mono px-2 py-0.5 rounded-full" style={{ background: 'rgba(234,179,8,0.1)', color: '#eab308' }}>
          JPEG Forensics
        </span>
      </div>

      {/* Image */}
      <div className="relative">
        <img src={elaUrl} className="w-full object-contain" style={{ maxHeight: 220 }} />
      </div>

      {/* Legend */}
      <div className="px-4 py-2.5 border-t space-y-1.5" style={{ borderColor: 'var(--panel-border)' }}>
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-sm shrink-0" style={{ background: 'rgba(234,179,8,0.8)' }} />
          <span className="text-[9px] font-mono" style={{ color: 'var(--text-muted)' }}>
            Bright areas = high compression error = natural textures / real content
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-2.5 h-2.5 rounded-sm shrink-0" style={{ background: 'rgba(40,40,50,0.9)' }} />
          <span className="text-[9px] font-mono" style={{ color: 'var(--text-muted)' }}>
            Flat/dark areas = low compression error = suspiciously uniform (AI signal)
          </span>
        </div>
        <div className="pt-1 text-[8px] font-mono leading-relaxed" style={{ color: 'var(--text-muted)' }}>
          ⚠ ELA is most reliable on original, unmodified JPEG images. Social media re-encoding reduces reliability.
        </div>
      </div>
    </div>
  );
}
