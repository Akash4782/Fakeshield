const footerLinks = {
  Product: ['Forensic Labs', 'Threat Radar', 'API Access', 'Security'],
  Company: ['About', 'Blog', 'Press Kit', 'Careers'],
  Legal: ['Privacy', 'Terms', 'DPA'],
};
import logo from '../assets/logo.png';

const Footer = () => {
  return (
    <footer
      style={{
        padding: '5rem 0',
        borderTop: `1px solid var(--border-subtle)`,
        background: 'var(--bg-primary)',
        transition: 'background 0.3s ease',
      }}
    >
      <div style={{ maxWidth: '80rem', margin: '0 auto', padding: '0 1.5rem' }}>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
            gap: '3rem',
            marginBottom: '5rem',
          }}
        >
          <div style={{ gridColumn: 'span 2' }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '1.5rem' }}>
              <img
                src={logo}
                alt="FakeShield Logo"
                style={{
                  height: '6.5rem',
                  width: 'auto',
                  filter: 'brightness(1.1) contrast(1.1)'
                }}
              />
            </div>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', lineHeight: 1.7, maxWidth: '18rem' }}>
              The global standard in synthetic media detection and forensic verification. Defending digital integrity since 2021.
            </p>
          </div>

          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h4 style={{ color: 'var(--text-heading)', fontWeight: 700, marginBottom: '1.5rem', fontSize: '0.9375rem' }}>
                {category}
              </h4>
              <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {links.map(link => (
                  <li key={link}>
                    <a
                      href="#"
                      style={{
                        color: 'var(--text-muted)',
                        textDecoration: 'none',
                        fontSize: '0.875rem',
                        transition: 'color 0.2s',
                      }}
                      onMouseOver={e => (e.currentTarget.style.color = '#00E5CC')}
                      onMouseOut={e => (e.currentTarget.style.color = 'var(--text-muted)')}
                    >
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '1.5rem',
            paddingTop: '3rem',
            borderTop: `1px solid var(--border-subtle)`,
          }}
        >
          <p style={{ color: 'var(--footer-copyright)', fontSize: '0.875rem' }}>
            © 2026 FakeShield Inc. All rights reserved.
          </p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
            <a href="#" style={{ color: 'var(--footer-copyright)', textDecoration: 'none', transition: 'color 0.2s' }}
              onMouseOver={e => (e.currentTarget.style.color = 'var(--text-heading)')}
              onMouseOut={e => (e.currentTarget.style.color = 'var(--footer-copyright)')}>
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.599 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z" />
              </svg>
            </a>
            <a href="#" style={{ color: 'var(--footer-copyright)', textDecoration: 'none', transition: 'color 0.2s' }}
              onMouseOver={e => (e.currentTarget.style.color = 'var(--text-heading)')}
              onMouseOut={e => (e.currentTarget.style.color = 'var(--footer-copyright)')}>
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
