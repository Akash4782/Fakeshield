import React, { useState } from 'react';
import { Mail, ArrowRight, ArrowLeft, Loader, CheckCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useTheme } from '../../hooks/useTheme';
import { API_BASE_URL } from '../../config';

const ForgotPasswordPage: React.FC = () => {
  const { theme } = useTheme();

  const [email,     setEmail]     = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error,     setError]     = useState('');
  const [sent,      setSent]      = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const res  = await fetch(`${API_BASE_URL}/auth/forgot-password`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ email }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Request failed. Please try again.');
      setSent(true);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center font-sans p-4"
      style={{ background: 'var(--page-bg)', color: 'var(--text-primary)' }}
    >
      {/* Decorative Spheres */}
      <div className="absolute top-[15%] left-[20%] w-14 h-14 bg-[#00E5CC] rounded-full blur-md opacity-15 animate-pulse hidden md:block" />
      <div className="absolute bottom-[20%] right-[20%] w-20 h-20 bg-[var(--accent-purple)] rounded-full blur-xl opacity-15 animate-bounce hidden md:block" />

      <div
        className="relative z-10 w-full max-w-[420px] rounded-[2rem] shadow-[0_40px_80px_rgba(0,0,0,0.15)] p-8 md:p-10"
        style={{
          background:    'var(--panel-bg)',
          backdropFilter:'blur(20px)',
          border:        '1px solid var(--panel-border)',
        }}
      >
        {/* Back Link */}
        <Link
          to="/login"
          className="inline-flex items-center gap-1.5 text-xs mb-6 font-semibold transition-colors hover:text-[#00E5CC]"
          style={{ color: 'var(--text-muted)' }}
        >
          <ArrowLeft size={14} /> Back to Login
        </Link>

        {!sent ? (
          <>
            {/* Header */}
            <div className="mb-7 animate-fade-in">
              <div className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4 bg-gradient-to-br from-[#00E5CC]/20 to-[var(--accent-purple)]/20 border border-[#00E5CC]/30">
                <Mail size={26} className="text-[#00E5CC]" />
              </div>
              <h1 className="text-2xl font-bold" style={{ color: 'var(--text-heading)' }}>Forgot your password?</h1>
              <p className="mt-2 text-sm leading-relaxed" style={{ color: 'var(--text-muted)' }}>
                No worries — enter your email and we'll send you a&nbsp;6-digit reset code.
              </p>
              <div className="h-1 w-10 bg-gradient-to-r from-[#00E5CC] to-[var(--accent-purple)] mt-4 rounded-full" />
            </div>

            <form className="space-y-4" onSubmit={handleSubmit}>
              {error && (
                <div className="text-red-400 text-sm text-center bg-red-500/10 py-2 px-3 rounded-xl border border-red-500/20 animate-fade-in">
                  {error}
                </div>
              )}

              {/* Email Input */}
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-[var(--text-muted)] group-focus-within:text-[#00E5CC] transition-colors">
                  <Mail size={18} strokeWidth={2.5} />
                </div>
                <input
                  id="forgot-email"
                  type="email"
                  required
                  placeholder="Your registered email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full rounded-2xl py-4 pl-11 pr-4 outline-none transition-all focus:ring-2 focus:ring-[#00E5CC]/40"
                  style={{ background: 'var(--bg-secondary)', color: 'var(--text-primary)', border: '1px solid var(--panel-border)' }}
                />
              </div>

              <button
                id="forgot-submit"
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-[#00E5CC] to-[var(--accent-purple)] text-white font-bold py-4 rounded-2xl shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-2 group border-none disabled:opacity-70 disabled:hover:translate-y-0"
              >
                {isLoading ? <Loader size={18} className="animate-spin" /> : 'Send Reset Code'}
                {!isLoading && <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />}
              </button>
            </form>
          </>
        ) : (
          /* Success state */
          <div className="flex flex-col items-center text-center py-4 animate-fade-in gap-4">
            <div className="w-16 h-16 rounded-2xl flex items-center justify-center bg-gradient-to-br from-[#00E5CC]/20 to-[var(--accent-purple)]/20 border border-[#00E5CC]/30">
              <CheckCircle size={32} className="text-[#00E5CC]" />
            </div>
            <h2 className="text-xl font-bold" style={{ color: 'var(--text-heading)' }}>Check your inbox!</h2>
            <p className="text-sm leading-relaxed" style={{ color: 'var(--text-muted)' }}>
              We've sent a 6-digit code to <strong className="text-[#00E5CC]">{email}</strong>.
              <br />Enter it on the next page to reset your password.
            </p>
            <p className="text-xs mt-1" style={{ color: 'var(--text-muted)' }}>
              The code expires in&nbsp;<strong>15 minutes</strong>. Check your spam folder if you don't see it.
            </p>
            <Link
              to="/reset-password"
              state={{ email }}
              className="mt-3 w-full bg-gradient-to-r from-[#00E5CC] to-[var(--accent-purple)] text-white font-bold py-4 rounded-2xl shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-2 group"
            >
              Enter Reset Code <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </Link>
            <button
              type="button"
              onClick={() => { setSent(false); setEmail(''); }}
              className="text-xs mt-1 hover:text-[#00E5CC] transition-colors"
              style={{ color: 'var(--text-muted)' }}
            >
              Use a different email?
            </button>
          </div>
        )}
      </div>

      <style>{`
        @keyframes fade-in { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
        .animate-fade-in { animation: fade-in 0.5s ease-out forwards; }
      `}</style>
    </div>
  );
};

export default ForgotPasswordPage;
