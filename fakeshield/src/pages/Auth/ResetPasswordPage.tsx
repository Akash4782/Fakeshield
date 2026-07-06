import React, { useState, useRef } from 'react';
import { Lock, ArrowRight, ArrowLeft, Loader, Eye, EyeOff, CheckCircle, Mail } from 'lucide-react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useTheme } from '../../hooks/useTheme';
import { useAuth } from '../../hooks/useAuth.tsx';
import { API_BASE_URL } from '../../config';

const OTP_LENGTH = 6;

const ResetPasswordPage: React.FC = () => {
  const { theme }        = useTheme();
  const { login }        = useAuth();
  const navigate         = useNavigate();
  const location         = useLocation();
  const emailHint        = (location.state as any)?.email ?? '';

  const [email,      setEmail]       = useState(emailHint);
  const [otp,        setOtp]         = useState<string[]>(Array(OTP_LENGTH).fill(''));
  const [newPass,    setNewPass]     = useState('');
  const [confirmPass,setConfirmPass] = useState('');
  const [showPass,   setShowPass]    = useState(false);
  const [isLoading,  setIsLoading]   = useState(false);
  const [error,      setError]       = useState('');
  const [success,    setSuccess]     = useState(false);

  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  /* ── OTP input helpers ─────────────────────────────────────── */
  const handleOtpChange = (index: number, val: string) => {
    const digit = val.replace(/\D/, '').slice(-1);
    const next  = [...otp];
    next[index] = digit;
    setOtp(next);
    if (digit && index < OTP_LENGTH - 1) inputRefs.current[index + 1]?.focus();
  };

  const handleOtpKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handleOtpPaste = (e: React.ClipboardEvent) => {
    e.preventDefault();
    const pasted = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, OTP_LENGTH);
    if (!pasted) return;
    const next = [...otp];
    pasted.split('').forEach((ch, i) => { next[i] = ch; });
    setOtp(next);
    const lastFilled = Math.min(pasted.length, OTP_LENGTH - 1);
    inputRefs.current[lastFilled]?.focus();
  };

  /* ── Submit ────────────────────────────────────────────────── */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const token = otp.join('');
    if (!email)                    { setError('Please enter your email address.'); return; }
    if (token.length < OTP_LENGTH) { setError('Please enter the full 6-digit code.'); return; }
    if (newPass.length < 8)        { setError('Password must be at least 8 characters.'); return; }
    if (newPass !== confirmPass)   { setError('Passwords do not match.'); return; }

    setIsLoading(true);
    try {
      const res  = await fetch(`${API_BASE_URL}/auth/reset-password`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ email, token, new_password: newPass }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Reset failed. Please try again.');

      setSuccess(true);
      // Auto-login and redirect after a short pause
      if (data.access_token) {
        login(data.access_token, data.user, false);
        setTimeout(() => navigate('/dashboard'), 2200);
      }
    } catch (e: any) {
      setError(e.message);
    } finally {
      setIsLoading(false);
    }
  };

  const passwordStrength = (p: string) => {
    let score = 0;
    if (p.length >= 8)             score++;
    if (/[A-Z]/.test(p))           score++;
    if (/[0-9]/.test(p))           score++;
    if (/[^A-Za-z0-9]/.test(p))    score++;
    return score; // 0-4
  };
  const strength      = passwordStrength(newPass);
  const strengthLabel = ['', 'Weak', 'Fair', 'Good', 'Strong'][strength];
  const strengthColor = ['', '#ef4444', '#f59e0b', '#3b82f6', '#00E5CC'][strength];

  return (
    <div
      className="min-h-screen flex items-center justify-center font-sans p-4"
      style={{ background: 'var(--page-bg)', color: 'var(--text-primary)' }}
    >
      {/* Blobs */}
      <div className="absolute top-[12%] right-[15%] w-16 h-16 bg-[#00E5CC] rounded-full blur-lg opacity-15 animate-pulse hidden md:block" />
      <div className="absolute bottom-[15%] left-[15%] w-20 h-20 bg-[var(--accent-purple)] rounded-full blur-xl opacity-15 animate-bounce hidden md:block" />

      <div
        className="relative z-10 w-full max-w-[440px] rounded-[2rem] shadow-[0_40px_80px_rgba(0,0,0,0.15)] p-8 md:p-10"
        style={{ background: 'var(--panel-bg)', backdropFilter: 'blur(20px)', border: '1px solid var(--panel-border)' }}
      >
        {/* Back */}
        <Link
          to="/forgot-password"
          className="inline-flex items-center gap-1.5 text-xs mb-6 font-semibold transition-colors hover:text-[#00E5CC]"
          style={{ color: 'var(--text-muted)' }}
        >
          <ArrowLeft size={14} /> Back
        </Link>

        {!success ? (
          <>
            {/* Header */}
            <div className="mb-7 animate-fade-in">
              <div className="w-14 h-14 rounded-2xl flex items-center justify-center mb-4 bg-gradient-to-br from-[#00E5CC]/20 to-[var(--accent-purple)]/20 border border-[#00E5CC]/30">
                <Lock size={26} className="text-[#00E5CC]" />
              </div>
              <h1 className="text-2xl font-bold" style={{ color: 'var(--text-heading)' }}>Reset your password</h1>
              <p className="mt-2 text-sm" style={{ color: 'var(--text-muted)' }}>
                {emailHint
                  ? <>Enter the code sent to <strong className="text-[#00E5CC]">{emailHint}</strong></>
                  : 'Enter the 6-digit code from your email.'}
              </p>
              <div className="h-1 w-10 bg-gradient-to-r from-[#00E5CC] to-[var(--accent-purple)] mt-4 rounded-full" />
            </div>

            <form className="space-y-5" onSubmit={handleSubmit}>
              {error && (
                <div className="text-red-400 text-sm text-center bg-red-500/10 py-2 px-3 rounded-xl border border-red-500/20 animate-fade-in">
                  {error}
                </div>
              )}

              {/* Email (only editable if they didn't come from the forgot page) */}
              {!emailHint && (
                <div className="relative group">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-[var(--text-muted)] group-focus-within:text-[#00E5CC] transition-colors">
                    <Mail size={18} strokeWidth={2.5} />
                  </div>
                  <input
                    type="email"
                    required
                    placeholder="Registered Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full rounded-2xl py-4 pl-11 pr-4 outline-none transition-all focus:ring-2 focus:ring-[#00E5CC]/40"
                    style={{ background: 'var(--bg-secondary)', color: 'var(--text-primary)', border: '1px solid var(--panel-border)' }}
                  />
                </div>
              )}

              {/* OTP Inputs */}
              <div>
                <label className="block text-xs font-semibold mb-3" style={{ color: 'var(--text-muted)' }}>
                  VERIFICATION CODE
                </label>
                <div className="flex gap-2 justify-between" onPaste={handleOtpPaste}>
                  {otp.map((digit, i) => (
                    <input
                      key={i}
                      ref={(el) => { inputRefs.current[i] = el; }}
                      id={`otp-${i}`}
                      type="text"
                      inputMode="numeric"
                      maxLength={1}
                      value={digit}
                      onChange={(e) => handleOtpChange(i, e.target.value)}
                      onKeyDown={(e) => handleOtpKeyDown(i, e)}
                      className="w-12 h-13 text-center text-xl font-bold rounded-xl outline-none focus:ring-2 focus:ring-[#00E5CC]/50 focus:scale-105 transition-all"
                      style={{
                        background: digit ? 'linear-gradient(135deg, rgba(0,229,204,0.1), rgba(139,92,246,0.1))' : 'var(--bg-secondary)',
                        border: digit ? '2px solid #00E5CC' : '1px solid var(--panel-border)',
                        color: 'var(--text-primary)',
                        aspectRatio: '1',
                        height: '52px',
                      }}
                    />
                  ))}
                </div>
              </div>

              {/* New Password */}
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-[var(--text-muted)] group-focus-within:text-[#00E5CC] transition-colors">
                  <Lock size={18} strokeWidth={2.5} />
                </div>
                <input
                  id="new-password"
                  type={showPass ? 'text' : 'password'}
                  required
                  placeholder="New Password (min. 8 chars)"
                  value={newPass}
                  onChange={(e) => setNewPass(e.target.value)}
                  className="w-full rounded-2xl py-4 pl-11 pr-12 outline-none transition-all focus:ring-2 focus:ring-[#00E5CC]/40"
                  style={{ background: 'var(--bg-secondary)', color: 'var(--text-primary)', border: '1px solid var(--panel-border)' }}
                />
                <button
                  type="button"
                  onClick={() => setShowPass(!showPass)}
                  className="absolute inset-y-0 right-0 pr-4 flex items-center text-[var(--text-muted)] hover:text-[#00E5CC] transition-colors"
                >
                  {showPass ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>

              {/* Password strength bar */}
              {newPass.length > 0 && (
                <div className="space-y-1 animate-fade-in">
                  <div className="flex gap-1">
                    {[1, 2, 3, 4].map((bar) => (
                      <div
                        key={bar}
                        className="h-1 flex-1 rounded-full transition-all duration-300"
                        style={{ background: bar <= strength ? strengthColor : 'var(--panel-border)' }}
                      />
                    ))}
                  </div>
                  <p className="text-xs font-medium" style={{ color: strengthColor }}>{strengthLabel}</p>
                </div>
              )}

              {/* Confirm Password */}
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-[var(--text-muted)] group-focus-within:text-[#00E5CC] transition-colors">
                  <Lock size={18} strokeWidth={2.5} />
                </div>
                <input
                  id="confirm-password"
                  type={showPass ? 'text' : 'password'}
                  required
                  placeholder="Confirm New Password"
                  value={confirmPass}
                  onChange={(e) => setConfirmPass(e.target.value)}
                  className="w-full rounded-2xl py-4 pl-11 pr-4 outline-none transition-all focus:ring-2 focus:ring-[#00E5CC]/40"
                  style={{
                    background: 'var(--bg-secondary)',
                    color: 'var(--text-primary)',
                    border: confirmPass
                      ? confirmPass === newPass
                        ? '1px solid #00E5CC'
                        : '1px solid #ef4444'
                      : '1px solid var(--panel-border)',
                  }}
                />
              </div>

              <button
                id="reset-submit"
                type="submit"
                disabled={isLoading}
                className="w-full bg-gradient-to-r from-[#00E5CC] to-[var(--accent-purple)] text-white font-bold py-4 rounded-2xl shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-2 group border-none disabled:opacity-70 disabled:hover:translate-y-0"
              >
                {isLoading ? <Loader size={18} className="animate-spin" /> : 'Reset Password'}
                {!isLoading && <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />}
              </button>
            </form>
          </>
        ) : (
          /* Success state */
          <div className="flex flex-col items-center text-center py-4 gap-5 animate-fade-in">
            <div className="w-16 h-16 rounded-2xl flex items-center justify-center bg-gradient-to-br from-[#00E5CC]/20 to-[var(--accent-purple)]/20 border border-[#00E5CC]/30">
              <CheckCircle size={32} className="text-[#00E5CC]" />
            </div>
            <h2 className="text-2xl font-bold" style={{ color: 'var(--text-heading)' }}>Password Reset!</h2>
            <p className="text-sm leading-relaxed" style={{ color: 'var(--text-muted)' }}>
              Your password has been updated successfully. Redirecting you to the dashboard…
            </p>
            <Link
              to="/dashboard"
              className="mt-2 w-full bg-gradient-to-r from-[#00E5CC] to-[var(--accent-purple)] text-white font-bold py-4 rounded-2xl shadow-lg flex items-center justify-center gap-2 group hover:-translate-y-1 transition-all"
            >
              Go to Dashboard <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </Link>
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

export default ResetPasswordPage;
