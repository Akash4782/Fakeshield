import React from 'react';
const CTASection = () => {
  return (
    <section style={{ padding: '5rem 1.5rem' }}>
      <div style={{ maxWidth: '64rem', margin: '0 auto' }}>
        <div className="gradient-border-wrapper">
          <div
            className="gradient-border-inner"
            style={{
              padding: '5rem 2.5rem',
              textAlign: 'center',
              position: 'relative',
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                position: 'absolute',
                inset: 0,
                background: 'var(--accent-blue-transparent)',
                pointerEvents: 'none',
              }}
            />

            <h2
              className="font-display"
              style={{
                fontSize: 'clamp(2rem, 5vw, 3rem)',
                fontWeight: 700,
                color: 'var(--text-heading)',
                marginBottom: '1.5rem',
              }}
            >
              Ready to secure your media?
            </h2>
            <p
              style={{
                color: 'var(--text-secondary)',
                fontSize: '1.125rem',
                maxWidth: '36rem',
                margin: '0 auto 2.5rem',
              }}
            >
              Join the world's leading organizations using FakeShield to maintain trust and authenticity.
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '1rem' }}>
              <a
                href="#"
                className="btn-glow"
                style={{
                  background: 'var(--cta-btn-bg)',
                  color: 'var(--cta-btn-color)',
                  fontWeight: 700,
                  padding: '1rem 2.5rem',
                  borderRadius: '0.75rem',
                  textDecoration: 'none',
                  display: 'inline-block',
                  transition: 'all 0.3s',
                }}
              >
                Get Started for Free
              </a>
              <a
                href="#"
                style={{
                  background: 'transparent',
                  border: `1px solid var(--btn-secondary-border)`,
                  color: 'var(--text-heading)',
                  fontWeight: 700,
                  padding: '1rem 2.5rem',
                  borderRadius: '0.75rem',
                  textDecoration: 'none',
                  display: 'inline-block',
                  transition: 'all 0.3s',
                }}
                onMouseOver={e => (e.currentTarget.style.background = 'var(--btn-secondary-hover)')}
                onMouseOut={e => (e.currentTarget.style.background = 'transparent')}
              >
                Contact Sales
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CTASection;
