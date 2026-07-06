import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth.tsx';
import { API_BASE_URL } from '../../config';

const CTASection = () => {
  const { isAuthenticated } = useAuth();
  const [showContact, setShowContact] = useState(false);
  const [sent, setSent] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({ name: '', email: '', phone: '', message: '' });

  // Close on Esc
  useEffect(() => {
    if (!showContact) return;
    const h = (e: KeyboardEvent) => { if (e.key === 'Escape') setShowContact(false); };
    window.addEventListener('keydown', h);
    return () => window.removeEventListener('keydown', h);
  }, [showContact]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting) return;

    setSubmitting(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/contact`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(result.detail || 'Unable to send your message. Please try again.');
      }
      setSent(true);
      setForm({ name: '', email: '', phone: '', message: '' });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to send your message. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const inputStyle: React.CSSProperties = {
    width: '100%',
    padding: '0.75rem 1rem',
    borderRadius: '0.5rem',
    border: '1px solid var(--panel-border)',
    background: 'var(--bg-secondary)',
    color: 'var(--text-primary)',
    fontSize: '0.875rem',
    outline: 'none',
    transition: 'border-color 0.2s',
  };

  return (
    <>
      {/* Contact Sales Modal */}
      {showContact && (
        <div
          className="fixed inset-0 z-[999] flex items-center justify-center p-4"
          style={{ background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(6px)' }}
          onClick={() => setShowContact(false)}
        >
          <div
            className="w-full max-w-md rounded-2xl border flex flex-col overflow-hidden"
            style={{
              background: 'var(--bg-primary)',
              borderColor: 'var(--panel-border)',
              boxShadow: '0 32px 80px rgba(0,0,0,0.6)',
            }}
            onClick={e => e.stopPropagation()}
          >
            {/* accent */}
            <div style={{ height: 2, background: 'linear-gradient(90deg, #00E5CC 0%, transparent 60%)' }} />

            <div style={{ padding: '2rem' }}>
              {sent ? (
                <div style={{ textAlign: 'center', padding: '2rem 0' }}>
                  <div style={{ width: 48, height: 48, borderRadius: '50%', background: 'rgba(34,197,94,0.1)', border: '1px solid rgba(34,197,94,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1rem' }}>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2">
                      <path d="M20 6L9 17l-5-5" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  </div>
                  <p style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-heading)' }}>Message sent</p>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>We'll get back to you within 24 hours.</p>
                </div>
              ) : (
                <>
                  {/* header */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-heading)' }}>Contact Sales</h3>
                    <button onClick={() => setShowContact(false)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-secondary)', padding: 4, display: 'flex' }}>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M18 6L6 18M6 6l12 12" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </button>
                  </div>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '1.5rem', lineHeight: 1.6 }}>
                    Get in touch for enterprise pricing, custom deployments, or API access.
                  </p>

                  <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.875rem' }}>
                      <div>
                        <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.375rem' }}>Full Name</label>
                        <input
                          required
                          minLength={2}
                          maxLength={100}
                          value={form.name}
                          onChange={e => setForm(p => ({ ...p, name: e.target.value }))}
                          placeholder="Akash Virdi"
                          style={inputStyle}
                          onFocus={e => e.target.style.borderColor = '#00E5CC'}
                          onBlur={e => e.target.style.borderColor = 'var(--panel-border)'}
                        />
                      </div>
                      <div>
                        <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.375rem' }}>Phone Number</label>
                        <input
                          type="tel"
                          maxLength={30}
                          value={form.phone}
                          onChange={e => setForm(p => ({ ...p, phone: e.target.value }))}
                          placeholder="+91-7973066831"
                          style={inputStyle}
                          onFocus={e => e.target.style.borderColor = '#00E5CC'}
                          onBlur={e => e.target.style.borderColor = 'var(--panel-border)'}
                        />
                      </div>
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.375rem' }}>Email Address</label>
                      <input
                        required
                        type="email"
                        value={form.email}
                        onChange={e => setForm(p => ({ ...p, email: e.target.value }))}
                        placeholder="virdiakash77@gmail.com"
                        style={inputStyle}
                        onFocus={e => e.target.style.borderColor = '#00E5CC'}
                        onBlur={e => e.target.style.borderColor = 'var(--panel-border)'}
                      />
                    </div>

                    <div>
                      <label style={{ display: 'block', fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.375rem' }}>How can we help?</label>
                      <textarea
                        required
                        minLength={10}
                        maxLength={5000}
                        rows={3}
                        value={form.message}
                        onChange={e => setForm(p => ({ ...p, message: e.target.value }))}
                        placeholder="Tell us about your use case, team size, or integration needs..."
                        style={{ ...inputStyle, resize: 'vertical', minHeight: '5rem', fontFamily: 'inherit' }}
                        onFocus={e => e.target.style.borderColor = '#00E5CC'}
                        onBlur={e => e.target.style.borderColor = 'var(--panel-border)'}
                      />
                    </div>

                    <div style={{ height: 1, background: 'var(--panel-border)', margin: '0.25rem 0' }} />

                    {error && (
                      <p role="alert" style={{ margin: 0, color: '#ef4444', fontSize: '0.75rem', textAlign: 'center', fontWeight: 600 }}>
                        {error}
                      </p>
                    )}

                    <div style={{ display: 'flex', gap: '0.75rem' }}>
                      <button
                        type="button"
                        onClick={() => setShowContact(false)}
                        style={{
                          flex: 1, padding: '0.625rem', borderRadius: '0.5rem',
                          border: '1px solid var(--panel-border)', background: 'transparent',
                          color: 'var(--text-secondary)', fontWeight: 600, fontSize: '0.8rem', cursor: 'pointer',
                        }}
                      >Cancel</button>
                      <button
                        type="submit"
                        disabled={submitting}
                        style={{
                          flex: 1, padding: '0.625rem', borderRadius: '0.5rem',
                          border: 'none', background: '#00E5CC', color: '#000',
                          fontWeight: 700, fontSize: '0.8rem', cursor: submitting ? 'not-allowed' : 'pointer',
                          opacity: submitting ? 0.65 : 1,
                        }}
                      >{submitting ? 'Sending...' : 'Send Message'}</button>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.375rem', justifyContent: 'center' }}>
                      <span style={{ fontSize: '0.5625rem', fontFamily: 'monospace', padding: '2px 6px', borderRadius: 4, border: '1px solid var(--panel-border)', color: 'var(--text-secondary)' }}>Esc</span>
                      <span style={{ fontSize: '0.625rem', color: 'var(--text-secondary)' }}>to close</span>
                    </div>
                  </form>
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* CTA Section */}
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
                <Link
                  to="/signup"
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
                </Link>

                <button
                  onClick={() => { setError(''); setSent(false); setShowContact(true); }}
                  style={{
                    background: 'transparent',
                    border: '1px solid var(--btn-secondary-border)',
                    color: 'var(--text-heading)',
                    fontWeight: 700,
                    padding: '1rem 2.5rem',
                    borderRadius: '0.75rem',
                    cursor: 'pointer',
                    transition: 'all 0.3s',
                  }}
                  onMouseOver={e => (e.currentTarget.style.background = 'var(--btn-secondary-hover)')}
                  onMouseOut={e => (e.currentTarget.style.background = 'transparent')}
                >
                  Contact Sales
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default CTASection;
