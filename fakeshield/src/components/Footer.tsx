import { Link } from 'react-router-dom';
import logo from '../assets/logo.png';

const Footer = () => {
  return (
    <footer style={{ background: 'var(--panel-bg)', borderTop: '1px solid var(--panel-border)', padding: '4rem 0 3rem' }}>
      <div style={{ maxWidth: '80rem', margin: '0 auto', padding: '0 1.5rem' }}>

        {/* columns */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr', gap: '3rem', marginBottom: '4rem' }}>

          {/* logo + tagline */}
          <div>
            <Link to="/">
              <img src={logo} alt="FakeShield" style={{ height: '5.5rem', width: 'auto', marginBottom: '1.25rem' }} />
            </Link>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem', lineHeight: 1.7, maxWidth: '16rem' }}>
              AI-powered deepfake detection across text, image, audio, and video.
            </p>
          </div>

          {/* Product */}
          <div>
            <h4 style={{ color: 'var(--text-primary)', fontSize: '0.6875rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '1.25rem' }}>Product</h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
              {[
                { label: 'Features', href: '/#labs' },
                { label: 'Pricing', href: '/subscription' },
                { label: 'Dashboard', href: '/dashboard' },
                { label: 'Analytics', href: '/dashboard' },
              ].map(l => (
                <li key={l.label}>
                  {l.href.startsWith('#') || l.href.startsWith('/#') ? (
                    <a href={l.href} style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '0.8125rem', transition: 'color 0.2s' }}
                      onMouseOver={e => e.currentTarget.style.color = 'var(--text-primary)'}
                      onMouseOut={e => e.currentTarget.style.color = 'var(--text-secondary)'}
                    >{l.label}</a>
                  ) : (
                    <Link to={l.href} style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '0.8125rem', transition: 'color 0.2s' }}
                      onMouseOver={e => e.currentTarget.style.color = 'var(--text-primary)'}
                      onMouseOut={e => e.currentTarget.style.color = 'var(--text-secondary)'}
                    >{l.label}</Link>
                  )}
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 style={{ color: 'var(--text-primary)', fontSize: '0.6875rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '1.25rem' }}>Company</h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
              {[
                { label: 'About Us', href: '/about' },
                { label: 'Contact', href: '/contact' },
                { label: 'GitHub', href: 'https://github.com/Akash4782' },
              ].map(l => (
                <li key={l.label}>
                  {l.href.startsWith('http') ? (
                    <a href={l.href} target="_blank" rel="noopener noreferrer"
                      style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '0.8125rem', transition: 'color 0.2s' }}
                      onMouseOver={e => e.currentTarget.style.color = 'var(--text-primary)'}
                      onMouseOut={e => e.currentTarget.style.color = 'var(--text-secondary)'}
                    >{l.label}</a>
                  ) : (
                    <Link to={l.href}
                      style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '0.8125rem', transition: 'color 0.2s' }}
                      onMouseOver={e => e.currentTarget.style.color = 'var(--text-primary)'}
                      onMouseOut={e => e.currentTarget.style.color = 'var(--text-secondary)'}
                    >{l.label}</Link>
                  )}
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 style={{ color: 'var(--text-primary)', fontSize: '0.6875rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '1.25rem' }}>Legal</h4>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
              {[
                { label: 'Privacy Policy', href: '/privacy' },
                { label: 'Terms of Service', href: '/terms' },
                { label: 'FAQs', href: '/faq' },
              ].map(l => (
                <li key={l.label}>
                  <Link to={l.href} style={{ color: 'var(--text-secondary)', textDecoration: 'none', fontSize: '0.8125rem', transition: 'color 0.2s' }}
                    onMouseOver={e => e.currentTarget.style.color = 'var(--text-primary)'}
                    onMouseOut={e => e.currentTarget.style.color = 'var(--text-secondary)'}
                  >{l.label}</Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* bottom bar */}
        <div style={{ borderTop: '1px solid var(--panel-border)', paddingTop: '2rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.8125rem' }}>© 2026 FakeShield. All rights reserved.</p>
          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            {/* GitHub */}
            <a href="https://github.com/Akash4782" target="_blank" rel="noopener noreferrer"
              title="GitHub Profile"
              style={{ 
                color: 'var(--text-muted)', 
                transition: 'color 0.2s',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '32px',
                height: '32px',
                borderRadius: '50%'
              }}
              onMouseOver={e => e.currentTarget.style.color = 'var(--text-primary)'}
              onMouseOut={e => e.currentTarget.style.color = 'var(--text-muted)'}>
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            </a>
            {/* LinkedIn */}
            <a href="https://www.linkedin.com/in/akash-virdi-399ab4253/" target="_blank" rel="noopener noreferrer"
              title="LinkedIn Profile"
              style={{ 
                color: 'var(--text-muted)', 
                transition: 'color 0.2s',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '32px',
                height: '32px',
                borderRadius: '50%'
              }}
              onMouseOver={e => e.currentTarget.style.color = 'var(--text-primary)'}
              onMouseOut={e => e.currentTarget.style.color = 'var(--text-muted)'}>
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
            </a>
            {/* Email Contact */}
            <a href="mailto:virdiakash77@gmail.com"
              title="Send an email to Akash Virdi"
              style={{ 
                color: 'var(--text-muted)', 
                transition: 'color 0.2s',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '32px',
                height: '32px',
                borderRadius: '50%'
              }}
              onMouseOver={e => e.currentTarget.style.color = 'var(--text-primary)'}
              onMouseOut={e => e.currentTarget.style.color = 'var(--text-muted)'}>
              <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </a>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer;
