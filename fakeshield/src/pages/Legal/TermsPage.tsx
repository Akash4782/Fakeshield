import React, { useEffect } from 'react';
import { ArrowLeft, Gavel, Scale, AlertCircle, ShieldCheck } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import logo from '../../assets/logo.png';
import Footer from '../../components/Footer';

const TermsPage: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)', fontFamily: "'Inter', sans-serif" }}>
      {/* Navbar */}
      <nav className="fixed top-0 left-0 right-0 z-50" style={{ background: 'var(--panel-bg)', backdropFilter: 'blur(20px)', borderBottom: '1px solid var(--panel-border)' }}>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-20 md:h-28 flex items-center justify-between">
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
            <div className="flex items-center gap-3 sm:gap-5 md:gap-8 cursor-pointer min-w-0" onClick={() => navigate('/')}>
              <img src={logo} alt="FakeShield" className="h-14 md:h-24 shrink-0" />
              <span className="hidden sm:block text-2xl md:text-4xl font-black tracking-tighter truncate" style={{ color: 'var(--text-heading)' }}>FAKESHIELD</span>
            </div>
          </div>
        </div>
      </nav>

      <main className="flex-grow pt-32 md:pt-40 pb-20 md:pb-24 px-4 sm:px-6">
        <div className="max-w-4xl mx-auto">
          <div className="mb-16">
            <h1 className="text-5xl md:text-7xl font-black mb-6 tracking-tight" style={{ color: 'var(--text-heading)' }}>
              Terms of <span className="text-[#00E5CC]">Service.</span>
            </h1>
            <p style={{ color: 'var(--text-secondary)' }} className="font-medium">Agreement for Forensic Verification Services | v2.1.0</p>
          </div>

          <div className="space-y-16">
            <section>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center text-[#00E5CC]" style={{ background: 'var(--btn-secondary-bg)' }}>
                  <Gavel size={20} />
                </div>
                <h2 className="text-2xl font-bold" style={{ color: 'var(--text-heading)' }}>1. Forensic Integrity</h2>
              </div>
              <div className="space-y-6 leading-relaxed font-medium" style={{ color: 'var(--text-secondary)' }}>
                <p>
                  By using FakeShield, you agree to use our forensic tools for legitimate verification and investigative purposes. 
                  Any attempt to reverse-engineer our detection algorithms or use the platform to "test" how to bypass 
                  AI detection is strictly prohibited.
                </p>
              </div>
            </section>

            <section>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center text-[#00E5CC]" style={{ background: 'var(--btn-secondary-bg)' }}>
                  <AlertCircle size={20} />
                </div>
                <h2 className="text-2xl font-bold" style={{ color: 'var(--text-heading)' }}>2. Acceptable Use</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { title: 'No Harassment', desc: 'Do not use verification results to target or harass individuals.' },
                  { title: 'Source Integrity', desc: 'Only upload media for which you have legal access or investigative rights.' },
                  { title: 'No Automated Scraping', desc: 'Accessing the engine via unauthorized bots or scrapers is a breach of service.' },
                  { title: 'Reporting Accuracy', desc: 'Recognize that scores are forensic probabilities, not absolute legal facts.' }
                ].map((item, i) => (
                  <div key={i} className="p-6 rounded-[2rem]" style={{ background: 'var(--btn-secondary-bg)', border: '1px solid var(--panel-border)' }}>
                    <h4 className="font-bold mb-2" style={{ color: 'var(--text-primary)' }}>{item.title}</h4>
                    <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>{item.desc}</p>
                  </div>
                ))}
              </div>
            </section>

            <section>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-10 h-10 rounded-xl flex items-center justify-center text-[#00E5CC]" style={{ background: 'var(--btn-secondary-bg)' }}>
                  <Scale size={20} />
                </div>
                <h2 className="text-2xl font-bold" style={{ color: 'var(--text-heading)' }}>3. Results & Accountability</h2>
              </div>
              <div className="space-y-6 leading-relaxed font-medium" style={{ color: 'var(--text-secondary)' }}>
                <p>
                  While FakeShield utilizes state-of-the-art neural engines, forensic analysis is inherently probabilistic. 
                  Our confidence scores, verdict labels, and improvement suggestions are technical indicators intended to 
                  support investigations and content review. They do not constitute absolute legal proof or mandatory 
                  editing instructions. Users are responsible for how they interpret and act upon these forensic signals.
                </p>
                <div className="border-l-4 border-[#00E5CC] pl-6 py-2 italic text-sm">
                  "The user retains all ownership of original content, while FakeShield retains ownership of the forensic 
                  signals and reports generated by our engines."
                </div>
              </div>
            </section>

            <section className="pt-8 border-t border-slate-100">
              <div className="p-6 md:p-8 rounded-[2rem] md:rounded-[2.5rem] bg-[#00E5CC] text-slate-900 flex flex-col md:flex-row items-center gap-8 shadow-xl shadow-[#00E5CC]/20">
                 <ShieldCheck size={48} className="text-slate-900" />
                 <div>
                   <h3 className="text-xl font-bold mb-2">Compliance & Liability</h3>
                   <p className="text-slate-800 text-sm leading-relaxed font-medium">
                     FakeShield is a tool for investigative assistance and content review support. We do not provide legal advice, 
                     and we are not liable for decisions made based on forensic confidence scores, verdicts, reports, or 
                     improvement suggestions.
                   </p>
                 </div>
              </div>
            </section>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default TermsPage;
