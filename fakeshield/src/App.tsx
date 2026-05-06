import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { ThemeProvider } from './hooks/useTheme';
import { AuthProvider, useAuth } from './hooks/useAuth.tsx';
import LandingPage from './pages/Landing/LandingPage';
import DashboardPage from './pages/Dashboard/DashboardPage';
import TextLabPage from './pages/TextLab/TextLabPage';
import AudioLabPage from './pages/AudioLab/AudioLabPage';
import ImageLabPage from './pages/ImageLab/ImageLabPage';
import VideoLabPage from './pages/VideoLab/VideoLabPage';
import AboutPage from './pages/About/AboutPage';
import ContactPage from './pages/Contact/ContactPage';
import SubscriptionPage from './pages/Subscription/SubscriptionPage';
import LoginPage from './pages/Auth/LoginPage';
import SignupPage from './pages/Auth/SignupPage';
import SettingsPage from './pages/Settings/SettingsPage';
import PrivacyPage from './pages/Legal/PrivacyPage';
import TermsPage from './pages/Legal/TermsPage';
import FAQPage from './pages/Legal/FAQPage';
import './App.css';

// Protected Route Component
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#020617]">
        <div className="w-16 h-16 border-4 border-[#00E5CC] border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

// Paid Route Component
const PaidRoute = ({ children }: { children: React.ReactNode }) => {
  const { user, isAuthenticated, isLoading } = useAuth();
  if (isLoading) return null;
  if (!isAuthenticated) return <Navigate to="/" replace />;
  if (user?.subscription_tier !== 'paid') return <Navigate to="/subscription" replace />;
  return <>{children}</>;
};

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
            <Route path="/subscription" element={<ProtectedRoute><SubscriptionPage /></ProtectedRoute>} />
            <Route path="/text-lab" element={<ProtectedRoute><TextLabPage /></ProtectedRoute>} />
            <Route path="/image-lab" element={<PaidRoute><ImageLabPage /></PaidRoute>} />
            <Route path="/audio-lab" element={<PaidRoute><AudioLabPage /></PaidRoute>} />
            <Route path="/video-lab" element={<PaidRoute><VideoLabPage /></PaidRoute>} />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/privacy" element={<PrivacyPage />} />
            <Route path="/terms" element={<TermsPage />} />
            <Route path="/faq" element={<FAQPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/settings" element={<ProtectedRoute><SettingsPage /></ProtectedRoute>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;
