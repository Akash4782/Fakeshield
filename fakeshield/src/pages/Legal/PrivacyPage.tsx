import React, { useEffect } from 'react';
import { ArrowLeft, Shield, Lock, Eye, FileText, Server } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import logo from '../../assets/logo.png';
import Footer from '../../components/Footer';

const PrivacyPage: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-white" style={{ fontFamily: "'Inter', sans-serif" }}>
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/70 backdrop-blur-xl border-b border-slate-100">
        <div className="max-w-6xl mx-auto px-6 h-28 flex items-center justify-between">
          <div className="flex items-center gap-12">
            <button
              onClick={() => navigate(-1)}
              className="w-12 h-12 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400 hover:text-white hover:bg-[#00E5CC] transition-all duration-500 shadow-sm hover:shadow-lg hover:shadow-[#00E5CC]/20"
            >
              <ArrowLeft size={20} />
            </button>
            <div className="flex items-center gap-8 cursor-pointer" onClick={() => navigate('/')}>
              <img src={logo} alt="FakeShield" className="h-24" />
              <span className="text-4xl font-black tracking-tighter text-slate-900">FAKESHIELD</span>
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-grow pt-40 pb-24 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="mb-16">
            <h1 className="text-5xl md:text-7xl font-black mb-6 tracking-tight text-slate-900">
              Privacy <span className="text-[#00E5CC]">Policy</span>
            </h1>
            <p className="text-slate-500 font-medium">Last updated: May 2026 | Version 1.4.0</p>
          </div>

          <div className="space-y-16">
            <section>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-[#00E5CC]">
                  <Shield size={20} />
                </div>
                <h2 className="text-2xl font-bold text-slate-900">Forensic Data Integrity</h2>
              </div>
              <div className="space-y-6 text-slate-600 leading-relaxed font-medium">
                <p>
                  At FakeShield, we treat your data as forensic evidence. Our primary objective is verification, not data collection. 
                  When you upload media for analysis, it is processed through our ephemeral neural pipeline, with comprehensive results securely stored in your private forensic database for historical reference.
                </p>
                <div className="p-8 rounded-[2rem] bg-slate-50 border border-slate-100">
                  <h3 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-[#00E5CC]"></div>
                    Zero Training Policy
                  </h3>
                  <p className="text-sm">
                    Unlike other AI platforms, FakeShield <span className="text-[#00E5CC] font-bold">never</span> uses your uploaded data to train or fine-tune our models.
                    Your forensic signals remain your proprietary information.
                  </p>
                </div>
              </div>
            </section>

            <section>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-[#00E5CC]">
                  <Lock size={20} />
                </div>
                <h2 className="text-2xl font-bold text-slate-900">Information We Collect</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-6 rounded-3xl border border-slate-100 bg-white shadow-sm">
                  <h4 className="font-bold mb-3 text-slate-900">Account Data</h4>
                  <p className="text-sm text-slate-500">Email, name, and encrypted credentials required for secure console access.</p>
                </div>
                <div className="p-6 rounded-3xl border border-slate-100 bg-white shadow-sm">
                  <h4 className="font-bold mb-3 text-slate-900">Metadata Signals</h4>
                  <p className="text-sm text-slate-500">Technical signals extracted during forensic scans (DCT coefficients, frame-rates, etc).</p>
                </div>
              </div>
            </section>

            <section>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-[#00E5CC]">
                  <Server size={20} />
                </div>
                <h2 className="text-2xl font-bold text-slate-900">Storage & Security</h2>
              </div>
              <div className="space-y-6 text-slate-600 leading-relaxed font-medium">
                <p>
                  All data is encrypted at rest using AES-256 and in transit via TLS 1.3. Forensic reports and scan history are stored in persistent, 
                  isolated document silos within our MongoDB Atlas infrastructure, ensuring you can review previous investigations at any time.
                </p>
                <ul className="list-none space-y-4">
                  {[
                    'Persistent storage of forensic reports and classification signals',
                    'Automatic deletion of raw media files post-analysis (unless explicitly archived)',
                    'Multi-factor authentication for all administrative access',
                    'Regular third-party security audits and penetration testing'
                  ].map((item, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <div className="mt-1.5 w-1.5 h-1.5 rounded-full bg-[#00E5CC] flex-shrink-0"></div>
                      <span className="text-sm">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </section>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default PrivacyPage;
