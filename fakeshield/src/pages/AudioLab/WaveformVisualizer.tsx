import React, { useMemo } from 'react';
import type { AudioTimelineSegment } from '../../services/audioService';

interface WaveformHeatmapProps {
  timeline: AudioTimelineSegment[];
  duration: number;
  onSegmentClick?: (segment: AudioTimelineSegment) => void;
}

/** Deterministic pseudo-random heights seeded by segment index + bar index.
 *  This prevents flicker on every React re-render caused by Math.random(). */
function deterministicBarHeight(segIdx: number, barIdx: number, aiScore: number): number {
  // Simple seeded sequence: use combination of indices to produce variation
  const seed = (segIdx * 7 + barIdx * 13 + Math.floor(aiScore)) % 100;
  const base = 15 + (seed % 55); // 15–70%
  // Scale by ai_score so high-risk segments look taller
  const scaled = base * (0.4 + (aiScore / 100) * 0.6);
  return Math.min(95, Math.max(10, scaled));
}

const LEVEL_COLORS: Record<string, string> = {
  critical: 'var(--accent-red)',
  high:     'var(--accent-orange)',
  medium:   'var(--accent-yellow)',
  low:      '#00E5CC',
};

const WaveformHeatmap: React.FC<WaveformHeatmapProps> = ({ timeline, duration, onSegmentClick }) => {
  if (!timeline || timeline.length === 0) return null;

  // Memoize bar heights so they don't change on re-renders
  const barHeights = useMemo(() => {
    return timeline.map((seg, sIdx) =>
      Array.from({ length: 8 }, (_, bIdx) =>
        deterministicBarHeight(sIdx, bIdx, seg.ai_score)
      )
    );
  }, [timeline]);

  const [hoveredSeg, setHoveredSeg] = React.useState<number | null>(null);

  return (
    <div className="w-full mt-4">
      {/* Time ruler */}
      <div className="flex justify-between text-[10px] font-mono text-[var(--text-muted)] mb-2 px-1">
        <span>0.0s</span>
        {duration > 0 && <span className="absolute left-1/2 -translate-x-1/2">{(duration / 2).toFixed(1)}s</span>}
        <span>{duration.toFixed(1)}s</span>
      </div>

      {/* Heatmap bars */}
      <div className="h-28 w-full flex items-end gap-[2px] bg-[var(--bg-secondary)] rounded-xl p-3 border border-[var(--panel-border)] overflow-hidden relative">
        {timeline.map((seg, idx) => {
          const color = LEVEL_COLORS[seg.level] ?? '#00E5CC';
          const isHovered = hoveredSeg === idx;

          return (
            <div
              key={idx}
              onClick={() => onSegmentClick?.(seg)}
              onMouseEnter={() => setHoveredSeg(idx)}
              onMouseLeave={() => setHoveredSeg(null)}
              className="flex-1 h-full flex flex-col-reverse justify-start items-center cursor-pointer relative group"
              title={`Seg ${seg.segment}: ${seg.ai_score}% AI (${seg.start_sec.toFixed(1)}s – ${seg.end_sec.toFixed(1)}s)`}
            >
              <div className="w-full flex flex-col-reverse gap-[1px]">
                {barHeights[idx].map((h, bIdx) => (
                  <div
                    key={bIdx}
                    className="w-full rounded-sm transition-all duration-300"
                    style={{
                      height: `${h}%`,
                      minHeight: '2px',
                      background: color,
                      opacity: isHovered ? 1.0 : (0.45 + (seg.ai_score / 200)),
                      transform: isHovered ? 'scaleY(1.08)' : 'scaleY(1)',
                      transformOrigin: 'bottom',
                    }}
                  />
                ))}
              </div>

              {/* Bottom threat indicator bar */}
              <div
                className="absolute bottom-0 left-0 right-0 h-[3px] rounded-full"
                style={{
                  background: color,
                  boxShadow: seg.ai_score > 50 ? `0 0 6px ${color}` : 'none',
                }}
              />

              {/* Hover tooltip */}
              {isHovered && (
                <div
                  className="absolute bottom-full mb-2 left-1/2 -translate-x-1/2 bg-[var(--bg-primary)] border border-[var(--panel-border)] rounded-lg px-2 py-1.5 text-[9px] font-mono whitespace-nowrap z-50 pointer-events-none"
                  style={{ color }}
                >
                  <div className="font-bold">{seg.ai_score}% AI</div>
                  <div className="text-[var(--text-muted)]">{seg.start_sec.toFixed(1)}–{seg.end_sec.toFixed(1)}s</div>
                </div>
              )}
            </div>
          );
        })}

        {/* Overlay gradient */}
        <div className="absolute inset-0 pointer-events-none bg-gradient-to-t from-black/10 to-transparent rounded-xl" />
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-6 mt-4 flex-wrap">
        {[
          { label: 'Authentic', color: '#00E5CC' },
          { label: 'Suspicious', color: 'var(--accent-yellow)' },
          { label: 'High Risk', color: 'var(--accent-orange)' },
          { label: 'Synthetic', color: 'var(--accent-red)' },
        ].map(({ label, color }) => (
          <div key={label} className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-sm" style={{ background: color }} />
            <span className="text-[10px] font-mono uppercase tracking-wider opacity-70">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WaveformHeatmap;
