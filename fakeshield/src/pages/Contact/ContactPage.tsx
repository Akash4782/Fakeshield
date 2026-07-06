import React, { useState, useEffect } from 'react';
import { Mail, Phone, MapPin, MessageSquare, ArrowLeft, Send, CheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import logo from '../../assets/logo.png';
import Footer from '../../components/Footer';
import { API_BASE_URL } from '../../config';

const ContactPage: React.FC = () => {
  const navigate = useNavigate();
  const [sent, setSent] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({ name: '', email: '', phone: '', message: '' });

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

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

  const inputStyle = "w-full px-4 py-3 rounded-xl border bg-[var(--panel-bg)] text-[var(--text-primary)] text-sm outline-none focus:border-[#00E5CC] transition-all";

  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'var(--bg-primary)', fontFamily: "'Inter', sans-serif" }}>
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50" style={{ background: 'var(--panel-bg)', backdropFilter: 'blur(20px)', borderBottom: '1px solid var(--panel-border)' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-20 md:h-28 flex items-center justify-between">
          <div className="flex items-center gap-3 sm:gap-6 md:gap-12 min-w-0">
            <button 
              onClick={() => navigate(-1)}
              className="w-10 h-10 md:w-12 md:h-12 rounded-xl flex items-center justify-center transition-all duration-500 shadow-sm hover:shadow-lg shrink-0"
              style={{ background: 'var(--btn-secondary-bg)', color: 'var(--text-muted)', border: '1px solid var(--panel-border)' }}
              onMouseEnter={(e) => { e.currentTarget.style.background = '#00E5CC'; e.currentTarget.style.color = '#000000'; }}
              onMouseLeave={(e) => { e.currentTarget.style.background = 'var(--btn-secondary-bg)'; e.currentTarget.style.color = 'var(--text-muted)'; }}
            >
              <ArrowLeft size={20} />
            </button>
            <div className="flex items-center gap-3 sm:gap-5 md:gap-10 cursor-pointer min-w-0" onClick={() => navigate('/')}>
              <img src={logo} alt="FakeShield" className="h-14 md:h-24 shrink-0" />
              <span className="hidden sm:block text-2xl md:text-4xl font-black tracking-tighter truncate" style={{ color: 'var(--text-heading)' }}>FAKESHIELD</span>
            </div>
          </div>
        </div>
      </header>

      <main className="flex-grow pt-32 md:pt-40 pb-20 md:pb-24">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20">
            
            {/* Left Side: Info */}
            <div className="space-y-12">
              <div>
                <h1 className="text-5xl font-black mb-6 tracking-tight" style={{ color: 'var(--text-heading)' }}>Let's talk <br /><span className="text-[#00E5CC]">Forensics.</span></h1>
                <p className="text-lg leading-relaxed max-w-md" style={{ color: 'var(--text-secondary)' }}>
                  Have a specific use case or need enterprise-grade verification? 
                  Our team is ready to help you deploy FakeShield across your organization.
                </p>
              </div>

              <div className="space-y-8">
                <div className="flex items-start gap-6">
                  <div className="w-12 h-12 rounded-2xl flex items-center justify-center text-[#00E5CC] flex-shrink-0" style={{ background: 'var(--btn-secondary-bg)' }}>
                    <Mail size={24} />
                  </div>
                  <div>
                    <h4 className="font-bold mb-1" style={{ color: 'var(--text-primary)' }}>Email us</h4>
                    <p className="text-sm mb-2" style={{ color: 'var(--text-secondary)' }}>For support or general inquiries.</p>
                    <a href="mailto:virdiakash77@gmail.com" className="text-[#00E5CC] font-bold text-sm hover:underline">virdiakash77@gmail.com</a>
                  </div>
                </div>

                <div className="flex items-start gap-6">
                  <div className="w-12 h-12 rounded-2xl flex items-center justify-center text-[#00E5CC] flex-shrink-0" style={{ background: 'var(--btn-secondary-bg)' }}>
                    <Phone size={24} />
                  </div>
                  <div>
                    <h4 className="font-bold mb-1" style={{ color: 'var(--text-primary)' }}>Call us</h4>
                    <p className="text-sm mb-2" style={{ color: 'var(--text-secondary)' }}>Available Mon-Fri, 9am - 6pm IST.</p>
                    <p className="font-bold text-sm" style={{ color: 'var(--text-primary)' }}>+91 7973066831</p>
                  </div>
                </div>

                <div className="flex items-start gap-6">
                  <div className="w-12 h-12 rounded-2xl flex items-center justify-center text-[#00E5CC] flex-shrink-0" style={{ background: 'var(--btn-secondary-bg)' }}>
                    <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                  </div>
                  <div>
                    <h4 className="font-bold mb-1" style={{ color: 'var(--text-primary)' }}>LinkedIn</h4>
                    <p className="text-sm mb-2" style={{ color: 'var(--text-secondary)' }}>Professional networking & inquiries.</p>
                    <a href="https://www.linkedin.com/in/akash-virdi-399ab4253/" target="_blank" rel="noopener noreferrer" className="text-[#00E5CC] font-bold text-sm hover:underline">Akash Virdi</a>
                  </div>
                </div>
              </div>

              <div className="p-8 rounded-[2.5rem] text-slate-900 relative overflow-hidden shadow-lg shadow-[#00E5CC]/20" style={{ background: '#00E5CC' }}>
                <div className="absolute top-0 right-0 w-32 h-32 bg-white/20 blur-3xl rounded-full translate-x-10 -translate-y-10"></div>
                <MessageSquare className="text-slate-900 mb-4" size={32} />
                <h4 className="text-xl font-bold mb-2">Technical Support</h4>
                <p className="text-slate-800 text-sm leading-relaxed font-medium">
                  Existing customers can access 24/7 technical assistance through the Console Dashboard.
                </p>
              </div>
            </div>

            {/* Right Side: Form */}
            <div className="relative">
              {sent ? (
                <div className="h-full min-h-[420px] md:min-h-[600px] flex flex-col items-center justify-center text-center p-6 md:p-12 rounded-[2rem] md:rounded-[3rem] border animate-in fade-in zoom-in duration-500" style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}>
                  <div className="w-20 h-20 rounded-full flex items-center justify-center text-[#00E5CC] mb-8" style={{ background: 'rgba(0, 229, 204, 0.1)' }}>
                    <CheckCircle size={40} />
                  </div>
                  <h2 className="text-3xl font-black mb-4" style={{ color: 'var(--text-heading)' }}>Transmission Received.</h2>
                  <p className="mb-8 max-w-xs" style={{ color: 'var(--text-secondary)' }}>Our engineering team has received your message. We'll be in touch within 24 hours.</p>
                  <div className="flex gap-2">
                    <div className="w-2 h-2 rounded-full bg-[#00E5CC] animate-bounce"></div>
                    <div className="w-2 h-2 rounded-full bg-[#00E5CC] animate-bounce [animation-delay:0.2s]"></div>
                    <div className="w-2 h-2 rounded-full bg-[#00E5CC] animate-bounce [animation-delay:0.4s]"></div>
                  </div>
                </div>
              ) : (
                <div className="p-6 sm:p-8 md:p-12 rounded-[2rem] md:rounded-[3rem] border shadow-2xl" style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' }}>
                  <h3 className="text-2xl font-black mb-8" style={{ color: 'var(--text-heading)' }}>Send a Message</h3>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <label className="text-xs font-bold uppercase tracking-wider ml-1" style={{ color: 'var(--text-muted)' }}>Your Name</label>
                        <input 
                          required
                          type="text" 
                          placeholder="Akash Virdi"
                          className={inputStyle}
                          value={form.name}
                          onChange={e => setForm({...form, name: e.target.value})}
                        />
                      </div>
                      <div className="space-y-2">
                        <label className="text-xs font-bold uppercase tracking-wider ml-1" style={{ color: 'var(--text-muted)' }}>Phone Number</label>
                        <input 
                          type="tel" 
                          placeholder="+91-0000000000"
                          className={inputStyle}
                          value={form.phone}
                          onChange={e => setForm({...form, phone: e.target.value})}
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-bold uppercase tracking-wider ml-1" style={{ color: 'var(--text-muted)' }}>Email Address</label>
                      <input 
                        required
                        type="email" 
                        placeholder="virdiakash77@gmail.com"
                        className={inputStyle}
                        value={form.email}
                        onChange={e => setForm({...form, email: e.target.value})}
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-bold uppercase tracking-wider ml-1" style={{ color: 'var(--text-muted)' }}>How can we help?</label>
                      <textarea 
                        required
                        rows={5}
                        placeholder="Tell us about your project, team, or forensic requirements..."
                        className={inputStyle + " resize-none"}
                        value={form.message}
                        onChange={e => setForm({...form, message: e.target.value})}
                      />
                    </div>

                    <button 
                      type="submit"
                      disabled={submitting}
                      className="w-full py-5 rounded-2xl text-slate-900 font-bold text-base hover:brightness-110 transition-all flex items-center justify-center gap-3 group shadow-xl shadow-[#00E5CC]/20 disabled:cursor-not-allowed disabled:opacity-60"
                      style={{ background: '#00E5CC' }}
                    >
                      {submitting ? 'Sending Message...' : 'Initialize Contact'}
                      {!submitting && <Send size={18} className="group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />}
                    </button>

                    {error && (
                      <p role="alert" className="text-center text-sm font-medium text-red-500">{error}</p>
                    )}

                    <p className="text-center text-xs leading-relaxed px-8" style={{ color: 'var(--text-muted)' }}>
                      By submitting this form, you agree to our privacy policy and terms of service.
                    </p>
                  </form>
                </div>
              )}
            </div>

          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ContactPage;
