import React from 'react';
const ThreatRadar = () => {
  return (
    <section
      id="threat-radar"
      style={{
        padding: '8rem 0',
        background: 'var(--bg-secondary)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Top & bottom decorative lines */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '1px',
          background: 'linear-gradient(to right, transparent, var(--panel-border), transparent)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: '1px',
          background: 'linear-gradient(to right, transparent, var(--panel-border), transparent)',
        }}
      />

      <div
        style={{
          maxWidth: '80rem',
          margin: '0 auto',
          padding: '0 1.5rem',
          display: 'flex',
          flexWrap: 'wrap',
          alignItems: 'center',
          gap: '4rem',
        }}
      >
        {/* Text Content */}
        <div style={{ flex: '1', minWidth: '280px' }}>
          <h2
            className="font-display"
            style={{ fontSize: 'clamp(1.75rem, 4vw, 2.5rem)', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '1.5rem' }}
          >
            Live Threat Radar
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.125rem', lineHeight: 1.7, marginBottom: '2rem' }}>
            Monitor the global landscape of synthetic misinformation. Our radar detects trending deepfake campaigns before they go viral,
            allowing for preemptive debunking.
          </p>
          <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2.5rem' }}>
            {[
              'Global Heatmap of Synthetic Media Peaks',
              'Real-time Social Media Propagation Tracking',
              'Automated Metadata Extraction & Verification',
            ].map(item => (
              <li key={item} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
                <div
                  style={{
                    marginTop: '0.375rem',
                    width: '0.375rem',
                    height: '0.375rem',
                    borderRadius: '50%',
                    background: 'var(--accent-blue, #00E5CC)',
                    flexShrink: 0,
                  }}
                />
                <span style={{ color: 'var(--text-primary)' }}>{item}</span>
              </li>
            ))}
          </ul>
          <a
            href="/dashboard"
            style={{
              background: 'var(--btn-secondary-bg)',
              border: `1px solid var(--btn-secondary-border)`,
              color: 'var(--text-heading)',
              fontWeight: 600,
              padding: '0.75rem 2rem',
              borderRadius: '0.5rem',
              cursor: 'pointer',
              transition: 'background 0.3s',
              textDecoration: 'none',
              display: 'inline-block',
            }}
          >
            Explore the Radar
          </a>
        </div>

        {/* Radar Visualization */}
        <div style={{ flex: '1', minWidth: '280px', display: 'flex', justifyContent: 'center' }}>
          <div
            style={{
              width: 'min(100%, 400px)',
              aspectRatio: '1',
              borderRadius: '50%',
              border: '1px solid var(--border-subtle)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '2rem',
              position: 'relative',
            }}
          >
            <div
              className="animate-ping"
              style={{
                position: 'absolute',
                inset: 0,
                borderRadius: '50%',
                border: '1px solid rgba(0, 229, 204, 0.2)',
                opacity: 0.2,
              }}
            />
            <div
              style={{
                width: '100%',
                height: '100%',
                borderRadius: '50%',
                border: '1px solid var(--panel-border)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                position: 'relative',
                overflow: 'hidden',
              }}
            >
              <div
                className="animate-spin-slow"
                style={{
                  position: 'absolute',
                  inset: 0,
                  borderRadius: '50%',
                  background: 'conic-gradient(from 0deg, transparent 75%, rgba(0, 229, 204, 0.1) 100%)',
                }}
              />
              <div className="animate-pulse" style={{ position: 'absolute', top: '20%', right: '30%', width: '0.75rem', height: '0.75rem', background: '#ef4444', borderRadius: '50%', filter: 'blur(2px)' }} />
              <div style={{ position: 'absolute', bottom: '40%', left: '20%', width: '0.5rem', height: '0.5rem', background: '#00E5CC', borderRadius: '50%', filter: 'blur(1px)' }} />
              <div style={{ position: 'absolute', top: '60%', right: '10%', width: '0.75rem', height: '0.75rem', background: '#00E5CC', borderRadius: '50%', filter: 'blur(2px)' }} />

              <div style={{ textAlign: 'center', position: 'relative', zIndex: 5 }}>
                <span className="font-display" style={{ display: 'block', fontSize: '2.5rem', fontWeight: 700, color: 'var(--text-heading)', lineHeight: 1 }}>
                  94.8%
                </span>
                <span style={{ fontSize: '0.625rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 700 }}>
                  Confidence Score
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ThreatRadar;
