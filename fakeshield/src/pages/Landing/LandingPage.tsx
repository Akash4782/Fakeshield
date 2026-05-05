import React from 'react';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import HeroSection from './HeroSection';
import FeaturesShowcase from './FeaturesShowcase';
import ThreatRadar from './ThreatRadar';
import HowItWorks from './HowItWorks';
import CTASection from './CTASection';

const companies = [
  { icon: 'square', name: 'SECURE-INTEL' },
  { icon: 'circle', name: 'GLOBAL-NEWS' },
  { icon: 'diamond', name: 'NEXUS-CORP' },
  { icon: 'rounded', name: 'VERIFY.AI' },
];

const SocialProof = () => (
  <section
    style={{
      padding: '5rem 0',
      borderTop: `1px solid var(--border-subtle)`,
    }}
  >
    <div style={{ maxWidth: '80rem', margin: '0 auto', padding: '0 1.5rem' }}>
      <p
        style={{
          textAlign: 'center',
          color: 'var(--text-muted)',
          fontSize: '0.75rem',
          fontWeight: 500,
          textTransform: 'uppercase',
          letterSpacing: '0.2em',
          marginBottom: '3rem',
        }}
      >
        Powering global verification teams
      </p>
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'center',
          alignItems: 'center',
          gap: '3rem',
          opacity: 'var(--social-opacity)',
          filter: 'grayscale(1)',
          transition: 'all 0.5s',
        }}
        onMouseOver={e => {
          (e.currentTarget as HTMLDivElement).style.opacity = '1';
          (e.currentTarget as HTMLDivElement).style.filter = 'grayscale(0)';
        }}
        onMouseOut={e => {
          (e.currentTarget as HTMLDivElement).style.opacity = 'var(--social-opacity)';
          (e.currentTarget as HTMLDivElement).style.filter = 'grayscale(1)';
        }}
      >
        {companies.map(c => (
          <div
            key={c.name}
            className="font-display"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              fontWeight: 700,
              fontSize: '1.125rem',
              color: 'var(--text-secondary)',
            }}
          >
            <span
              style={{
                width: '1.5rem',
                height: '1.5rem',
                background: 'var(--text-secondary)',
                borderRadius: c.icon === 'circle' ? '50%' : c.icon === 'rounded' ? '0.5rem' : c.icon === 'diamond' ? '0' : '0.25rem',
                transform: c.icon === 'diamond' ? 'rotate(45deg)' : 'none',
                display: 'inline-block',
              }}
            />
            {c.name}
          </div>
        ))}
      </div>
    </div>
  </section>
);

const LandingPage = () => {
  return (
    <div style={{ background: 'var(--bg-primary)', minHeight: '100vh', transition: 'background 0.3s ease' }}>
      <Navbar />
      <main>
        <HeroSection />
        <SocialProof />
        <div id="features">
          <FeaturesShowcase />
        </div>
        <ThreatRadar />
        <div id="how-it-works">
          <HowItWorks />
        </div>
        <div id="enterprise">
          <CTASection />
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default LandingPage;
