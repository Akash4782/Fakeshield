import { useState } from 'react';
import { useTheme } from '../hooks/useTheme';
import { Link } from 'react-router-dom';
import logo from '../assets/logo.png';

const SunIcon = () => (
  <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="5" />
    <line x1="12" y1="1" x2="12" y2="3" />
    <line x1="12" y1="21" x2="12" y2="23" />
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
    <line x1="1" y1="12" x2="3" y2="12" />
    <line x1="21" y1="12" x2="23" y2="12" />
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
  </svg>
);

const MoonIcon = () => (
  <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
  </svg>
);

const Navbar = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const { theme, toggleTheme } = useTheme();

  return (
    <nav
      className="glass-nav"
      style={{
        position: 'fixed',
        top: 0,
        width: '100%',
        zIndex: 50,
      }}
    >
      <div
        style={{
          maxWidth: '80rem',
          margin: '0 auto',
          padding: '0 1.5rem',
          height: '5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Link to="/" style={{ display: 'flex', alignItems: 'center', textDecoration: 'none' }}>
          <img
            src={logo}
            alt="FakeShield Logo"
            style={{
              height: '6.5rem',
              width: 'auto',
              filter: theme === 'dark' ? 'brightness(1.1) contrast(1.1)' : 'none',
            }}
          />
        </Link>

        {/* Desktop Nav Links */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '2rem',
            fontSize: '0.875rem',
            fontWeight: 500,
            color: 'var(--text-secondary)',
          }}
        >
          <a href="#labs" style={{ color: 'inherit', textDecoration: 'none', transition: 'color 0.2s' }}
            onMouseOver={e => (e.currentTarget.style.color = 'var(--text-heading)')}
            onMouseOut={e => (e.currentTarget.style.color = 'var(--text-secondary)')}>
            Forensic Labs
          </a>
          <a href="#threat-radar" style={{ color: 'inherit', textDecoration: 'none', transition: 'color 0.2s' }}
            onMouseOver={e => (e.currentTarget.style.color = 'var(--text-heading)')}
            onMouseOut={e => (e.currentTarget.style.color = 'var(--text-secondary)')}>
            Threat Radar
          </a>
          <a href="#features" style={{ color: 'inherit', textDecoration: 'none', transition: 'color 0.2s' }}
            onMouseOver={e => (e.currentTarget.style.color = 'var(--text-heading)')}
            onMouseOut={e => (e.currentTarget.style.color = 'var(--text-secondary)')}>
            Features
          </a>
          <a href="#" style={{ color: 'inherit', textDecoration: 'none', transition: 'color 0.2s' }}
            onMouseOver={e => (e.currentTarget.style.color = 'var(--text-heading)')}
            onMouseOut={e => (e.currentTarget.style.color = 'var(--text-secondary)')}>
            Enterprise
          </a>
        </div>

        {/* Right side: Theme toggle + CTA Buttons */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {/* Theme Toggle */}
          <button
            className="theme-toggle"
            onClick={(e) => toggleTheme(e)}
            title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {theme === 'dark' ? <SunIcon /> : <MoonIcon />}
          </button>

          <Link
            to="/login"
            style={{
              fontSize: '0.875rem',
              fontWeight: 500,
              color: 'var(--text-secondary)',
              textDecoration: 'none',
              padding: '0 1rem',
              transition: 'color 0.2s',
            }}
            onMouseOver={e => (e.currentTarget.style.color = 'var(--text-heading)')}
            onMouseOut={e => (e.currentTarget.style.color = 'var(--text-secondary)')}
          >
            Log in
          </Link>
          <Link
            to="/signup"
            className="btn-glow"
            style={{
              background: 'var(--cta-btn-bg)',
              color: 'var(--cta-btn-color)',
              fontSize: '0.875rem',
              fontWeight: 600,
              padding: '0.625rem 1.5rem',
              borderRadius: '9999px',
              textDecoration: 'none',
              transition: 'all 0.3s',
            }}
          >
            Get Started
          </Link>

          {/* Mobile Hamburger */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            style={{
              display: 'none',
              background: 'none',
              border: 'none',
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              padding: '0.25rem',
            }}
            className="mobile-menu-btn"
          >
            <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d="M4 6h16M4 12h16M4 18h16" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div
          style={{
            background: 'var(--glass-bg)',
            borderTop: `1px solid var(--glass-border)`,
            padding: '1rem 1.5rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
          }}
        >
          {['Forensic Labs', 'Threat Radar', 'Features', 'Enterprise'].map(item => (
            <a
              key={item}
              href="#"
              style={{
                color: 'var(--text-secondary)',
                textDecoration: 'none',
                fontSize: '0.875rem',
                fontWeight: 500,
                padding: '0.5rem 0',
              }}
            >
              {item}
            </a>
          ))}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
