import React, { useState, useEffect } from 'react';
import { User, Lock, ArrowRight, Loader, Eye, EyeOff } from 'lucide-react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useGoogleLogin } from '@react-oauth/google';
import { useTheme } from '../../hooks/useTheme';
import { useAuth } from '../../hooks/useAuth.tsx';
import { API_BASE_URL } from '../../config';

const OAUTH_REMEMBER_KEY = 'fakeshield_oauth_remember';

const LoginPage: React.FC = () => {
  const { theme } = useTheme();
  const { login, isAuthenticated } = useAuth();
  const navigate  = useNavigate();
  const location  = useLocation();
  const from = (location.state as any)?.from?.pathname || '/dashboard';

  const [formData,    setFormData]    = useState({ email: '', password: '' });
  const [rememberMe,  setRememberMe]  = useState(
    () => sessionStorage.getItem(OAUTH_REMEMBER_KEY) === 'true'
  );
  const [showPass,    setShowPass]    = useState(false);
  const [error,       setError]       = useState('');
  const [isLoading,   setIsLoading]   = useState(false);

  // Redirect if already authenticated
  useEffect(() => { if (isAuthenticated) navigate(from, { replace: true }); }, [isAuthenticated]);

  // Handle GitHub OAuth callback
  useEffect(() => {
    const code = new URLSearchParams(window.location.search).get('code');
    if (code) handleGitHubCallback(code);
  }, []);

  const handleGitHubCallback = async (code: string) => {
    const shouldRemember = sessionStorage.getItem(OAUTH_REMEMBER_KEY) === 'true';
    setIsLoading(true);
    try {
      const res  = await fetch(`${API_BASE_URL}/auth/oauth`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider: 'GitHub', code, remember_me: shouldRemember }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'GitHub login failed');
      login(data.access_token, data.user, shouldRemember);
      sessionStorage.removeItem(OAUTH_REMEMBER_KEY);
      navigate(from);
    } catch (e: any) { setError(e.message); }
    finally { setIsLoading(false); }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    try {
      const res  = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...formData, remember_me: rememberMe }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Login failed');

      // Pass rememberMe so useAuth stores in correct storage
      login(data.access_token, data.user, rememberMe);
      navigate(from);
    } catch (e: any) { setError(e.message); }
    finally { setIsLoading(false); }
  };

  const handleGoogleLogin = useGoogleLogin({
    onSuccess: async (tokenResponse) => {
      setIsLoading(true);
      try {
        const gRes  = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
          headers: { Authorization: `Bearer ${tokenResponse.access_token}` },
        });
        const gUser = await gRes.json();
        const res   = await fetch(`${API_BASE_URL}/auth/oauth`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ provider: 'Google', email: gUser.email, name: gUser.name, profile_pic: gUser.picture, remember_me: rememberMe }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error('Google login failed');
        login(data.access_token, data.user, rememberMe);
        navigate(from);
      } catch (e: any) { setError(e.message); }
      finally { setIsLoading(false); }
    },
    onError: () => setError('Google Login Failed'),
  });

  const handleGitHubLogin = () => {
    const GITHUB_CLIENT_ID = 'Ov23lihg68uHO6roOUFU';
    sessionStorage.setItem(OAUTH_REMEMBER_KEY, String(rememberMe));
    window.location.href = `https://github.com/login/oauth/authorize?client_id=${GITHUB_CLIENT_ID}&scope=user:email`;
  };

  return (
    <div
      className="min-h-screen flex items-start justify-center font-sans overflow-y-auto pt-[0vh] pb-20 p-4"
      style={{ background: 'var(--page-bg)', color: 'var(--text-primary)' }}
    >
      {/* Decorative Spheres */}
      <div className="absolute top-[20%] left-[30%] w-12 h-12 bg-[#00E5CC] rounded-full blur-sm opacity-20 animate-bounce hidden md:block" />
      <div className="absolute bottom-[30%] right-[32%] w-16 h-16 bg-[var(--accent-purple)] rounded-full blur-md opacity-20 animate-pulse hidden md:block" />
      <div className="absolute top-[40%] right-[25%] w-8 h-8 bg-[var(--text-active)] rounded-full blur-sm opacity-20 animate-bounce delay-300 hidden md:block" />

      {/* Card */}
      <div
        className="relative z-10 w-full max-w-[420px] rounded-[2rem] shadow-[0_50px_100px_rgba(0,0,0,0.15)] p-6 md:p-10 transform hover:rotate-2 transition-all duration-700 ease-out"
        style={{
          perspective: '1000px',
          transform: window.innerHeight < 750
            ? 'perspective(1000px) rotateX(10deg) rotateY(-5deg) scale(0.85)'
            : 'perspective(1000px) rotateX(10deg) rotateY(-5deg)',
          background: 'var(--panel-bg)',
          backdropFilter: 'blur(20px)',
          border: '1px solid var(--panel-border)',
        }}
      >
        {/* Header */}
        <div className="mb-4 md:mb-10 animate-fade-in text-left">
          <h1 className="text-2xl md:text-3xl font-bold font-display leading-tight" style={{ color: 'var(--text-heading)' }}>
            FakeShield <br />
            Forensic Suite
          </h1>
          <div className="h-1 w-12 bg-gradient-to-r from-[#00E5CC] to-[var(--accent-purple)] mt-3 md:mt-4 rounded-full" />
        </div>

        <form className="space-y-4 md:space-y-6" onSubmit={handleLogin}>
          {/* Error Banner */}
          {error && (
            <div className="text-red-400 text-sm text-center bg-red-500/10 py-2 px-3 rounded-xl border border-red-500/20 animate-fade-in">
              {error}
            </div>
          )}

          {/* Email Input */}
          <div className="relative group overflow-hidden">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-[var(--text-muted)] group-focus-within:text-[#00E5CC] transition-colors">
              <User size={20} strokeWidth={2.5} />
            </div>
            <input
              id="login-email"
              type="email"
              required
              placeholder="Email Address"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full bg-opacity-50 border-none rounded-2xl py-4 pl-12 pr-4 outline-none transition-all shadow-sm hover:shadow-md"
              style={{ background: 'var(--bg-secondary)', color: 'var(--text-primary)', border: '1px solid var(--panel-border)' }}
            />
          </div>

          {/* Password Input */}
          <div className="relative group overflow-hidden">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-[var(--text-muted)] group-focus-within:text-[#00E5CC] transition-colors">
              <Lock size={20} strokeWidth={2.5} />
            </div>
            <input
              id="login-password"
              type={showPass ? 'text' : 'password'}
              required
              placeholder="Password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="w-full bg-opacity-50 border-none rounded-2xl py-4 pl-12 pr-12 outline-none transition-all shadow-sm hover:shadow-md"
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

          {/* Login Button */}
          <button
            id="login-submit"
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-[#00E5CC] to-[var(--accent-purple)] text-white font-bold py-4 rounded-2xl shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-2 group border-none disabled:opacity-70 disabled:hover:translate-y-0"
          >
            {isLoading ? <Loader size={18} className="animate-spin" /> : 'Log in'}
            {!isLoading && <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />}
          </button>

          {/* Divider */}
          <div className="relative py-4">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t" style={{ borderColor: 'var(--panel-border)' }} />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="px-2 font-semibold tracking-wider" style={{ background: 'var(--bg-primary)', color: 'var(--text-muted)' }}>
                Or continue with
              </span>
            </div>
          </div>

          {/* Social Logins */}
          <div className="grid grid-cols-2 gap-4">
            <button
              type="button"
              onClick={() => handleGoogleLogin()}
              className="flex items-center justify-center gap-3 py-3 px-4 rounded-2xl border transition-all group hover:bg-slate-800"
              style={{ borderColor: 'var(--panel-border)', background: 'var(--btn-secondary-bg)' }}
            >
              <svg className="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05" />
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.66l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
              </svg>
              <span className="text-sm font-bold" style={{ color: 'var(--text-secondary)' }}>Google</span>
            </button>
            <button
              type="button"
              onClick={handleGitHubLogin}
              className="flex items-center justify-center gap-3 py-3 px-4 rounded-2xl border transition-all group hover:bg-slate-800"
              style={{ borderColor: 'var(--panel-border)', background: 'var(--btn-secondary-bg)' }}
            >
              <svg className="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" fill="currentColor" style={{ color: 'var(--text-primary)' }}>
                <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
              </svg>
              <span className="text-sm font-bold" style={{ color: 'var(--text-secondary)' }}>GitHub</span>
            </button>
          </div>

          {/* Remember Me + Forgot Password */}
          <div className="flex items-center justify-between text-xs pt-4 font-medium" style={{ color: 'var(--text-muted)' }}>
            {/* Custom Remember Me toggle */}
            <label
              className="flex items-center gap-2 cursor-pointer select-none group"
              htmlFor="remember-me"
            >
              <input
                id="remember-me"
                type="checkbox"
                className="sr-only"
                checked={rememberMe}
                onChange={(event) => setRememberMe(event.target.checked)}
              />
              <div
                className="relative w-9 h-5 rounded-full transition-colors duration-200 flex-shrink-0"
                style={{ background: rememberMe ? '#00E5CC' : 'var(--panel-border)' }}
              >
                <div
                  className="absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow transition-transform duration-200"
                  style={{ transform: rememberMe ? 'translateX(16px)' : 'translateX(0)' }}
                />
              </div>
              <span className={`transition-colors ${rememberMe ? 'text-[#00E5CC]' : 'hover:text-[#00E5CC]'}`}>
                Remember me
              </span>
            </label>

            <Link
              to="/forgot-password"
              className="hover:text-[#00E5CC] transition-colors font-semibold"
            >
              Forgot Password?
            </Link>
          </div>

          <div className="text-center pt-4">
            <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
              Don't have an account?{' '}
              <Link to="/signup" className="font-bold text-[#00E5CC] hover:text-[var(--accent-purple)] transition-colors">
                Create one here
              </Link>
            </p>
          </div>
        </form>

        {/* Decorative Corner Badge */}
        <div className="absolute -top-6 -right-6 w-12 h-12 bg-[#00E5CC] rounded-full flex items-center justify-center text-white shadow-lg animate-bounce duration-3000 border-none">
          <div className="w-6 h-6 border-4 border-white rounded-full"></div>
        </div>
      </div>

      <style>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(-10px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in { animation: fade-in 0.6s ease-out forwards; }
      `}</style>
    </div>
  );
};

export default LoginPage;
