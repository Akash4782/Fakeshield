import React from 'react';
const labs = [
  {
    id: 'text',
    title: 'Text Lab',
    color: '#00E5CC',
    colorLight: 'rgba(0, 229, 204, 0.1)',
    colorBorder: 'rgba(0, 229, 204, 0.2)',
    description: 'Analyze large language model (LLM) signatures, syntax patterns, and hallucination markers.',
    icon: (
      <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
      </svg>
    ),
  },
  {
    id: 'image',
    title: 'Image Lab',
    color: 'var(--accent-purple)',
    colorLight: 'var(--accent-purple-transparent)',
    colorBorder: 'var(--accent-purple-border)',
    description: 'Pixel-level forensic inspection for GAN artifacts, diffusion noise, and lighting inconsistencies.',
    icon: (
      <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
      </svg>
    ),
  },
  {
    id: 'audio',
    title: 'Audio Lab',
    color: '#10b981',
    colorLight: 'rgba(16,185,129,0.1)',
    colorBorder: 'rgba(16,185,129,0.2)',
    description: 'Voice cloning detection through vocal tract modeling and frequency discrepancy analysis.',
    icon: (
      <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
      </svg>
    ),
  },
  {
    id: 'video',
    title: 'Video Lab',
    color: '#ef4444',
    colorLight: 'rgba(239,68,68,0.1)',
    colorBorder: 'rgba(239,68,68,0.2)',
    description: 'Real-time deepfake video analysis identifying temporal inconsistencies and biometric mismatches.',
    icon: (
      <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
      </svg>
    ),
  },
];

const LabCard = ({ lab }: { lab: typeof labs[0] }) => {
  return (
    <div
      className="card-border"
      style={{
        padding: '2rem',
        borderRadius: '1rem',
        cursor: 'default',
        background: 'var(--panel-bg)',
        border: '1px solid var(--panel-border)',
      }}
    >
      <div
        style={{
          width: '3rem',
          height: '3rem',
          background: lab.colorLight,
          borderRadius: '0.75rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          marginBottom: '1.5rem',
          border: `1px solid ${lab.colorBorder}`,
          color: lab.color,
          transition: 'background 0.3s',
        }}
      >
        {lab.icon}
      </div>
      <h3
        className="font-display"
        style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.75rem' }}
      >
        {lab.title}
      </h3>
      <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.7, marginBottom: '1.5rem' }}>
        {lab.description}
      </p>
      <a
        href="#"
        style={{
          color: lab.color,
          fontSize: '0.875rem',
          fontWeight: 600,
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.25rem',
          textDecoration: 'none',
          transition: 'gap 0.2s',
        }}
      >
        Learn more
        <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M9 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
        </svg>
      </a>
    </div>
  );
};

const FeaturesShowcase = () => {
  return (
    <section id="labs" style={{ padding: '8rem 0', position: 'relative' }}>
      <div style={{ maxWidth: '80rem', margin: '0 auto', padding: '0 1.5rem' }}>
        <div style={{ marginBottom: '5rem' }}>
          <h2
            className="font-display"
            style={{ fontSize: 'clamp(1.75rem, 4vw, 2.5rem)', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '1rem' }}
          >
            Precision Detection Labs
          </h2>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '36rem' }}>
            Every asset undergoes a multi-layered spectral analysis to identify generative artifacts invisible to the human eye.
          </p>
        </div>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
            gap: '1.5rem',
          }}
        >
          {labs.map(lab => (
            <LabCard key={lab.id} lab={lab} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesShowcase;
