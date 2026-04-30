import React from 'react';

interface AudioVisualSyncProps {
  lipTimeline: number[];
  audioSpeaking: number[];
}

const AudioVisualSync: React.FC<AudioVisualSyncProps> = ({ lipTimeline, audioSpeaking }) => {
  
  return (
    <div className="space-y-4 pt-4 border-t border-white/5">
      <h4 className="text-[10px] font-black uppercase tracking-widest opacity-40">Audio-Visual Sync Audit</h4>
      
      <div className="grid grid-cols-1 gap-2">
        {/* Audio Speaking Track */}
        <div className="flex items-center gap-2">
          <span className="text-[10px] w-12 opacity-50 uppercase font-bold shrink-0">Audio</span>
          <div className="flex-1 h-3 flex gap-0.5">
            {audioSpeaking.slice(0, 40).map((v, i) => (
              <div 
                key={i} 
                className={`flex-1 rounded-sm ${v > 0.5 ? 'bg-green-500/60 shadow-[0_0_8px_rgba(34,197,94,0.3)]' : 'bg-white/5'}`}
              />
            ))}
          </div>
        </div>

        {/* Lip Movement Track */}
        <div className="flex items-center gap-2">
          <span className="text-[10px] w-12 opacity-50 uppercase font-bold shrink-0">Lips</span>
          <div className="flex-1 h-3 flex gap-0.5">
            {lipTimeline.slice(0, 40).map((v, i) => (
              <div 
                key={i} 
                className={`flex-1 rounded-sm ${v > 0.02 ? 'bg-blue-500/60 shadow-[0_0_8px_rgba(59,130,246,0.3)]' : 'bg-white/5'}`}
              />
            ))}
          </div>
        </div>

        {/* Sync Status */}
        <div className="flex items-center gap-2">
          <span className="text-[10px] w-12 opacity-50 uppercase font-bold shrink-0">Sync</span>
          <div className="flex-1 h-3 flex gap-0.5">
            {audioSpeaking.slice(0, 40).map((v, i) => {
              const isSpeaking = v > 0.5;
              const isMoving = lipTimeline[i] > 0.02;
              const mismatched = isSpeaking !== isMoving;
              return (
                <div 
                  key={i} 
                  className={`flex-1 rounded-sm ${mismatched ? 'bg-red-500/60 shadow-[0_0_8px_rgba(239,68,68,0.3)]' : 'bg-white/5 opacity-20'}`}
                />
              );
            })}
          </div>
        </div>
      </div>

      <p className="text-[9px] opacity-40 leading-relaxed italic">
        *Red indicators highlight asynchronous phoneme-to-viseme mapping often found in first-generation lip-sync deepfakes.
      </p>
    </div>
  );
};

export default AudioVisualSync;
