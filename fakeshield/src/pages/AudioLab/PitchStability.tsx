import React from 'react';

interface PitchStabilityProps {
  f0_std: number;
}

const PitchStability: React.FC<PitchStabilityProps> = ({ f0_std }) => {
  // f0_std < 1.5 is AI, 2.5-5.0 is Human
  const isStable = f0_std < 1.8;
  const percentage = Math.min(100, Math.max(0, (f0_std / 8) * 100));

  return (
    <div className="p-4 rounded-xl border border-[var(--panel-border)] bg-[var(--bg-secondary)]">
      <h5 className="text-[10px] font-mono uppercase tracking-[0.2em] text-[var(--text-muted)] mb-3 flex justify-between items-center">
        <span>Prosody Stability</span>
        <span className={isStable ? 'text-[var(--accent-red)]' : 'text-green-500'}>
          {isStable ? 'UNNATURAL' : 'NATURAL'}
        </span>
      </h5>
      
      <div className="flex items-center gap-4">
        <div className="flex-1 h-3 bg-[var(--panel-border)] rounded-full overflow-hidden relative">
          <div 
            className="h-full rounded-full transition-all duration-1000"
            style={{ 
              width: `${percentage}%`,
              background: isStable ? 'var(--accent-red)' : '#00E5CC',
              boxShadow: `0 0 10px ${isStable ? 'var(--accent-red)' : '#00E5CC'}40`
            }}
          />
          {/* Target range marker 2.5-5.0 */}
          <div className="absolute top-0 left-[31%] w-[31%] h-full border-x border-dashed border-white/20 bg-white/5"></div>
        </div>
        <span className="text-xs font-mono font-bold w-12 text-right">{f0_std.toFixed(2)} st</span>
      </div>
      <p className="text-[9px] font-mono text-[var(--text-muted)] mt-2 leading-tight">
        {isStable 
          ? 'Pitch variance is suspiciously low, indicating robotic synthesizer output.' 
          : 'Natural prosodic variation detected within human speech parameters.'}
      </p>
    </div>
  );
};

export default PitchStability;
