import React from 'react';
const steps = [
  {
    id: '01',
    title: 'Upload & Ingest',
    description: 'Drag and drop any file or provide a live URL for immediate spectral processing.',
  },
  {
    id: '02',
    title: 'Neural Analysis',
    description: 'Our proprietary models cross-reference the asset against millions of known AI training sets.',
  },
  {
    id: '03',
    title: 'Forensic Report',
    description: 'Download a certified report detailing every identified marker and confidence level.',
  },
];

const HowItWorks = () => {
  return (
    <section style={{ padding: '8rem 0' }}>
      <div style={{ maxWidth: '80rem', margin: '0 auto', padding: '0 1.5rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '5rem' }}>
          <h2
            className="font-display"
            style={{ fontSize: 'clamp(1.75rem, 4vw, 2.5rem)', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '1rem' }}
          >
            The Verification Workflow
          </h2>
          <p style={{ color: 'var(--text-secondary)', maxWidth: '42rem', margin: '0 auto' }}>
            A seamless transition from ingestion to reporting, built for efficiency and legal-grade defensibility.
          </p>
        </div>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '3rem',
            position: 'relative',
          }}
        >
          <div
            style={{
              position: 'absolute',
              top: '2rem',
              left: '15%',
              right: '15%',
              height: '1px',
              background: 'linear-gradient(to right, transparent, var(--panel-border), transparent)',
            }}
          />

          {steps.map(step => (
            <div key={step.id} style={{ textAlign: 'center', position: 'relative' }}>
              <div
                style={{
                  width: '4rem',
                  height: '4rem',
                  background: 'var(--bg-primary)',
                  border: `1px solid var(--border-subtle)`,
                  borderRadius: '1rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 1.5rem',
                  boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
                  position: 'relative',
                  zIndex: 10,
                  transition: 'background 0.3s',
                }}
              >
                <span className="font-display" style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-heading)' }}>
                  {step.id}
                </span>
              </div>
              <h3 className="font-display" style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.75rem' }}>
                {step.title}
              </h3>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', lineHeight: 1.7 }}>
                {step.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
