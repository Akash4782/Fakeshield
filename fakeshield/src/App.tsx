import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './hooks/useTheme';
import LandingPage from './pages/Landing/LandingPage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import ForensicLab from './pages/ForensicLab/ForensicLab';
import TextLabPage from './pages/TextLab/TextLabPage';
import AudioLabPage from './pages/AudioLab/AudioLabPage';
import ImageLabPage from './pages/ImageLab/ImageLabPage';
import VideoLabPage from './pages/VideoLab/VideoLabPage';
import AnalyticsPage from './pages/Analytics/AnalyticsPage';
import LoginPage from './pages/Auth/LoginPage';
import SignupPage from './pages/Auth/SignupPage';
import SettingsPage from './pages/Settings/SettingsPage';
import './App.css';

// Simple Error Boundary
class ErrorBoundary extends React.Component<{children: React.ReactNode}, {hasError: boolean, error: any}> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error: any) { return { hasError: true, error }; }
  componentDidCatch(error: any, errorInfo: any) { console.error("[ErrorBoundary] Caught:", error, errorInfo); }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '40px', color: '#EF4444', background: '#020617', minHeight: '100vh', fontFamily: 'monospace' }}>
          <h1 style={{ fontSize: '2rem', marginBottom: '1rem' }}>Forensic Console Exception</h1>
          <p style={{ color: '#94a3b8' }}>A critical runtime error occurred in the linguistic engine visualization.</p>
          <div style={{ marginTop: '20px', padding: '20px', background: '#0B0E14', border: '1px solid #334155', borderRadius: '12px' }}>
            <p><strong>Error:</strong> {this.state.error?.message}</p>
            <pre style={{ marginTop: '10px', fontSize: '12px', opacity: 0.7, overflowX: 'auto' }}>{this.state.error?.stack}</pre>
          </div>
          <button onClick={() => window.location.reload()} style={{ marginTop: '20px', padding: '10px 20px', background: '#00E5CC', color: '#020617', fontWeight: 'bold', borderRadius: '8px' }}>
            Re-initialize UI
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/lab" element={<ForensicLab />} />
            <Route path="/text-lab" element={<TextLabPage />} />
            <Route path="/image-lab" element={<ImageLabPage />} />
            <Route path="/audio-lab" element={<AudioLabPage />} />
            <Route path="/video-lab" element={<VideoLabPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
