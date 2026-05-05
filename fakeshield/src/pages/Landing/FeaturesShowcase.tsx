import React, { useState, useEffect, useRef } from 'react';

// ── Per-lab detailed content ──────────────────────────────────────────────────
const LAB_DETAILS = {
  text: {
    title: 'Text Lab',
    subtitle: 'LLM Authorship & Linguistic Forensics',
    color: '#00E5CC',
    colorLight: 'rgba(0,229,204,0.07)',
    colorBorder: 'rgba(0,229,204,0.18)',
    badge: 'Free & Pro',
    badgeBg: 'rgba(0,229,204,0.1)',
    badgeColor: '#00E5CC',
    description:
      'Runs your content through a 7-layer forensic pipeline that cross-validates six independent models, covering low-level perplexity scoring all the way to high-level semantic drift analysis. Distinguishes AI-generated prose from human writing with sub-5% false-positive rates.',
    engines: [
      { name: 'Binoculars (Perplexity)',  desc: 'Token-level log-probability analysis vs. reference corpus' },
      { name: 'Classifier Ensemble',      desc: 'Fine-tuned RoBERTa + DeBERTa on 8M AI/human samples' },
      { name: 'Stylometry Engine',        desc: 'Function-word frequency, sentence cadence & punctuation profiling' },
      { name: 'Semantic Trajectory',      desc: 'mpnet-v2 drift variance that tracks thought flow consistency' },
      { name: 'Structural Entropy',       desc: 'Parse-tree depth & dependency variance analysis' },
      { name: 'Gemini Reasoning Judge',   desc: 'Chain-of-thought arbitration for ambiguous borderline cases' },
    ],
    stats: [
      { label: 'Accuracy',  value: '94.2%' },
      { label: 'Avg. Time', value: '~8s' },
      { label: 'Models',    value: '6' },
      { label: 'Min Words', value: '80' },
    ],
    usecases: ['Academic plagiarism detection', 'News authenticity verification', 'Legal document review', 'AI-spam filtering'],
    path: '/text-lab',
  },
  image: {
    title: 'Image Lab',
    subtitle: 'Pixel-Level AI Generation Forensics',
    color: '#8b5cf6',
    colorLight: 'rgba(139,92,246,0.07)',
    colorBorder: 'rgba(139,92,246,0.18)',
    badge: 'Pro Required',
    badgeBg: 'rgba(245,158,11,0.1)',
    badgeColor: '#f59e0b',
    description:
      'Computes nine independent forensic signals simultaneously, covering sensor noise fingerprinting through to C2PA provenance verification. Detects images from Stable Diffusion, DALL-E, Midjourney, and GAN-based generators with per-pixel heat maps.',
    engines: [
      { name: 'RIGID / DINOv2',        desc: 'Perturbation sensitivity testing via reference invariance' },
      { name: 'SigLIP / ViT Ensemble', desc: 'Neural classifier trained on 12M synthetic vs. real pairs' },
      { name: 'ELA (Error Level)',      desc: 'JPEG compression uniformity analysis across the image grid' },
      { name: 'PRNU Noise Analysis',   desc: 'Photo-response non-uniformity sensor fingerprinting' },
      { name: 'FFT Spectral Audit',    desc: 'Power-law deviation detection in the frequency domain using the 1/f squared test' },
      { name: 'C2PA Provenance',       desc: 'Content Credentials standard with cryptographic origin verification' },
    ],
    stats: [
      { label: 'Accuracy',   value: '96.1%' },
      { label: 'Avg. Time',  value: '~4s' },
      { label: 'Signals',    value: '9' },
      { label: 'Max Size',   value: '20MB' },
    ],
    usecases: ['Deepfake profile detection', 'Evidence integrity checks', 'Stock photo verification', 'News image forensics'],
    path: '/image-lab',
  },
  audio: {
    title: 'Audio Lab',
    subtitle: 'Voice Clone & TTS Detection',
    color: '#10b981',
    colorLight: 'rgba(16,185,129,0.07)',
    colorBorder: 'rgba(16,185,129,0.18)',
    badge: 'Pro Required',
    badgeBg: 'rgba(245,158,11,0.1)',
    badgeColor: '#f59e0b',
    description:
      'Analyses audio using WavLM and Wav2Vec2 neural networks trained on ASVspoof challenge data. Runs a temporal forensic scan across all chunks to detect unnatural prosody, codec artifacts, and speaker identity drift.',
    engines: [
      { name: 'WavLM ITW Classifier',  desc: 'In-the-wild trained model for real-world voice clone detection' },
      { name: 'Wav2Vec2 ASVspoof',     desc: 'Anti-spoofing challenge model — SV2019/2021 dataset trained' },
      { name: 'Prosody Engine',        desc: 'F0 pitch stability, energy variance, and speech rhythm analysis' },
      { name: 'Speaker Drift Tracker', desc: 'Cosine similarity across speaker embedding windows' },
      { name: 'Spectral Heuristics',   desc: 'Vocoder artifact detection in mel-frequency domain' },
      { name: 'Codec Forensics',       desc: 'MP3/AAC re-encoding pattern detection from synthetic generation' },
    ],
    stats: [
      { label: 'Accuracy',  value: '92.7%' },
      { label: 'Avg. Time', value: '~12s' },
      { label: 'Engines',   value: '6' },
      { label: 'Max Size',  value: '50MB' },
    ],
    usecases: ['Vishing fraud detection', 'Podcast verification', 'Legal voice recording analysis', 'Call center fraud'],
    path: '/audio-lab',
  },
  video: {
    title: 'Video Lab',
    subtitle: 'Temporal Deepfake & Face-Swap Analysis',
    color: '#ef4444',
    colorLight: 'rgba(239,68,68,0.07)',
    colorBorder: 'rgba(239,68,68,0.18)',
    badge: 'Pro Required',
    badgeBg: 'rgba(245,158,11,0.1)',
    badgeColor: '#f59e0b',
    description:
      'Samples frames across the full timeline and runs five independent forensic signals, including RAFT optical flow for pixel-mass discontinuity and rPPG to detect the absence of a biological heartbeat. Detects Sora, Gen-3, and face-swap deepfakes.',
    engines: [
      { name: 'Spatial Neural (CLIP)',  desc: 'Per-frame GAN & diffusion artifact detection via zero-shot gap' },
      { name: 'Temporal Flow (RAFT)',   desc: 'Optical flow discontinuity revealing non-physical pixel motion' },
      { name: 'Audio-Lip Sync',         desc: 'Phoneme-to-viseme alignment audit across the full timeline' },
      { name: 'Forensic Noise (PRNU)', desc: 'Frame-level sensor noise inconsistency detection across edited regions' },
      { name: 'rPPG Biometrics',        desc: 'Remote photoplethysmography that detects absence of biological skin pulse' },
      { name: 'VLM Reasoning',          desc: 'Vision-language model physics & geometry consistency check' },
    ],
    stats: [
      { label: 'Accuracy',   value: '89.4%' },
      { label: 'Avg. Time',  value: '~30s' },
      { label: 'Signals',    value: '5' },
      { label: 'Frames',     value: '8–24' },
    ],
    usecases: ['Political deepfake verification', 'Court evidence auth', 'Viral video checks', 'CEO impersonation fraud'],
    path: '/video-lab',
  },
} as const;

type LabId = keyof typeof LAB_DETAILS;
const LAB_IDS = Object.keys(LAB_DETAILS) as LabId[];

// ── Icon helper ───────────────────────────────────────────────────────────────
const PATHS: Record<LabId, string> = {
  text:  'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
  image: 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z',
  audio: 'M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z',
  video: 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z',
};

const LabIcon: React.FC<{ id: LabId; color: string; size?: number }> = ({ id, color, size = 22 }) => (
  <svg width={size} height={size} fill="none" stroke={color} strokeWidth="2" viewBox="0 0 24 24">
    <path d={PATHS[id]} strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

// ── Expanded detail panel (renders below the cards row) ───────────────────────
const ExpandedPanel: React.FC<{ labId: LabId; onClose: () => void }> = ({ labId, onClose }) => {
  const lab = LAB_DETAILS[labId];
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    ref.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }, [labId]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onClose]);

  return (
    <div
      ref={ref}
      style={{
        gridColumn: '1 / -1',
        borderRadius: '0.75rem',
        border: '1px solid var(--panel-border)',
        background: 'var(--panel-bg)',
        overflow: 'hidden',
        animation: 'expandDown 0.2s ease-out',
      }}
    >
      <div style={{ display: 'flex' }}>
        {/* left accent bar */}
        <div style={{ width: 3, background: lab.color, flexShrink: 0 }} />

        <div style={{ flex: 1, padding: '1.75rem 2rem' }}>

          {/* row 1: title + close */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
              <span style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-heading)' }}>{lab.title}</span>
              <span style={{
                fontSize: '0.6rem', fontWeight: 700, padding: '2px 8px', borderRadius: 4,
                background: lab.badgeBg, color: lab.badgeColor,
              }}>{lab.badge}</span>
            </div>
            <button onClick={onClose} style={{
              background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-secondary)',
              padding: 4, display: 'flex',
            }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M18 6L6 18M6 6l12 12" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
          </div>

          {/* subtitle */}
          <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: '1.25rem', maxWidth: '52rem' }}>
            {lab.description}
          </p>

          {/* stats as inline key-values, not colored boxes */}
          <div style={{ display: 'flex', gap: '2rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
            {lab.stats.map(s => (
              <div key={s.label} style={{ display: 'flex', alignItems: 'baseline', gap: '0.375rem' }}>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{s.label}:</span>
                <span style={{ fontSize: '0.8125rem', fontWeight: 700, color: 'var(--text-heading)' }}>{s.value}</span>
              </div>
            ))}
          </div>

          {/* divider */}
          <div style={{ height: 1, background: 'var(--panel-border)', marginBottom: '1.25rem' }} />

          {/* engines as a plain table */}
          <p style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.75rem' }}>
            Detection engines
          </p>
          <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '1.25rem' }}>
            <tbody>
              {lab.engines.map((eng, i) => (
                <tr key={i} style={{ borderBottom: i < lab.engines.length - 1 ? '1px solid var(--panel-border)' : 'none' }}>
                  <td style={{ padding: '0.5rem 0', paddingRight: '1.5rem', verticalAlign: 'top', whiteSpace: 'nowrap' }}>
                    <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-heading)' }}>{eng.name}</span>
                  </td>
                  <td style={{ padding: '0.5rem 0', verticalAlign: 'top' }}>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{eng.desc}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* use cases as inline text */}
          <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', lineHeight: 1.7, marginBottom: '1.5rem' }}>
            <span style={{ fontWeight: 700, color: 'var(--text-heading)' }}>Use cases: </span>
            {lab.usecases.join(', ')}.
          </p>

          {/* footer */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <a href={lab.path} style={{
              display: 'inline-flex', alignItems: 'center', gap: '0.375rem',
              padding: '0.5rem 1rem', borderRadius: '0.5rem',
              background: lab.color, color: '#000',
              fontWeight: 700, fontSize: '0.8rem', textDecoration: 'none',
            }}>
              Open {lab.title}
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M5 12h14M12 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </a>
            <button onClick={onClose} style={{
              padding: '0.5rem 1rem', borderRadius: '0.5rem',
              border: '1px solid var(--panel-border)', background: 'transparent',
              color: 'var(--text-secondary)', fontWeight: 600, fontSize: '0.8rem', cursor: 'pointer',
            }}>Close</button>
          </div>

        </div>
      </div>
    </div>
  );
};

// ── Individual card ───────────────────────────────────────────────────────────
const LabCard: React.FC<{
  id: LabId;
  active: boolean;
  onToggle: (id: LabId) => void;
}> = ({ id, active, onToggle }) => {
  const lab = LAB_DETAILS[id];
  return (
    <div style={{
      padding: '2rem', borderRadius: '1rem', cursor: 'default',
      background: active ? lab.colorLight : 'var(--panel-bg)',
      border: `1px solid ${active ? lab.colorBorder : 'var(--panel-border)'}`,
      transition: 'border-color 0.2s, background 0.2s',
    }}>
      <div style={{
        width: '3rem', height: '3rem', background: lab.colorLight, borderRadius: '0.75rem',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        marginBottom: '1.5rem', border: `1px solid ${lab.colorBorder}`,
      }}>
        <LabIcon id={id} color={lab.color} />
      </div>
      <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.75rem' }}>{lab.title}</h3>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.7, marginBottom: '1.5rem' }}>{lab.description}</p>
      <button
        onClick={() => onToggle(id)}
        style={{
          background: 'none', border: 'none', padding: 0, cursor: 'pointer',
          color: lab.color, fontSize: '0.875rem', fontWeight: 600,
          display: 'inline-flex', alignItems: 'center', gap: '0.35rem',
        }}
      >
        {active ? 'Collapse' : 'Learn more'}
        <svg
          width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"
          style={{ transform: active ? 'rotate(90deg)' : 'none', transition: 'transform 0.2s' }}
        >
          <path d="M9 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" />
        </svg>
      </button>
    </div>
  );
};

// ── Main section ──────────────────────────────────────────────────────────────
const FeaturesShowcase = () => {
  const [active, setActive] = useState<LabId | null>(null);

  const toggle = (id: LabId) => setActive(prev => prev === id ? null : id);

  return (
    <>
      <style>{`
        @keyframes expandDown {
          from { opacity: 0; transform: translateY(-8px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>
      <section id="labs" style={{ padding: '8rem 0', position: 'relative' }}>
        <div style={{ maxWidth: '80rem', margin: '0 auto', padding: '0 1.5rem' }}>
          <div style={{ marginBottom: '5rem' }}>
            <h2 style={{ fontSize: 'clamp(1.75rem, 4vw, 2.5rem)', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '1rem' }}>
              Precision Detection Labs
            </h2>
            <p style={{ color: 'var(--text-secondary)', maxWidth: '36rem' }}>
              Every asset undergoes a multi-layered spectral analysis to identify generative artifacts invisible to the human eye.
            </p>
          </div>

          {/* Grid — cards + expanded panel both live here */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1.5rem' }}>
            {LAB_IDS.map(id => (
              <LabCard key={id} id={id} active={active === id} onToggle={toggle} />
            ))}

            {/* Expanded panel spans all 4 columns */}
            {active && (
              <ExpandedPanel
                key={active}
                labId={active}
                onClose={() => setActive(null)}
              />
            )}
          </div>
        </div>
      </section>
    </>
  );
};

export default FeaturesShowcase;
