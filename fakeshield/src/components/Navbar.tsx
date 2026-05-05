import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../hooks/useTheme';
import { useAuth } from '../hooks/useAuth.tsx';
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
  const { isAuthenticated } = useAuth();

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
          className="hidden md:flex items-center gap-8 text-sm font-medium text-[var(--text-secondary)]"
        >
          <a href="/#features" className="hover:text-[var(--text-heading)] transition-colors">
            Forensic Labs
          </a>
          <a href="/#threat-radar" className="hover:text-[var(--text-heading)] transition-colors">
            Threat Radar
          </a>
          <a href="/#how-it-works" className="hover:text-[var(--text-heading)] transition-colors">
            Features
          </a>
          <a href="/#enterprise" className="hover:text-[var(--text-heading)] transition-colors">
            Enterprise
          </a>
        </div>

        {/* Right side: Theme toggle + CTA Buttons */}
        <div className="flex items-center gap-4 md:gap-6">
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
            className="hidden sm:block text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-heading)] transition-colors px-2"
          >
            Log in
          </Link>
          <Link
            to="/signup"
            className="btn-glow bg-[var(--cta-btn-bg)] text-[var(--cta-btn-color)] text-xs md:text-sm font-bold py-2 md:py-2.5 px-4 md:px-6 rounded-full transition-all"
          >
            Get Started
          </Link>

          {/* Mobile Hamburger */}
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="md:hidden p-2 text-[var(--text-secondary)]"
          >
            <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path d={menuOpen ? "M6 18L18 6M6 6l12 12" : "M4 6h16M4 12h16M4 18h16"} strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" />
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="md:hidden bg-[var(--glass-bg)] border-t border-[var(--glass-border)] px-6 py-6 flex flex-col gap-4 animate-in fade-in slide-in-from-top-4 duration-300">
          {[
            { label: 'Forensic Labs', href: '/#features' },
            { label: 'Threat Radar', href: '/#threat-radar' },
            { label: 'Features', href: '/#how-it-works' },
            { label: 'Enterprise', href: '/#enterprise' },
            { label: 'Log in', href: '/login' }
          ].map(item => (
            <a
              key={item.label}
              href={item.href}
              onClick={() => setMenuOpen(false)}
              className="text-sm font-medium text-[var(--text-secondary)] hover:text-[var(--text-heading)] transition-colors py-2"
            >
              {item.label}
            </a>
          ))}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
