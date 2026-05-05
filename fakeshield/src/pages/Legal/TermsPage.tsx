import React, { useEffect } from 'react';
import { ArrowLeft, Gavel, Scale, AlertCircle, Terminal, ShieldCheck } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import logo from '../../assets/logo.png';
import Footer from '../../components/Footer';

const TermsPage: React.FC = () => {
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
              Terms of <span className="text-[#00E5CC]">Service.</span>
            </h1>
            <p className="text-slate-500 font-medium">Agreement for Forensic Verification Services | v2.1.0</p>
          </div>

          <div className="space-y-16">
            <section>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-[#00E5CC]">
                  <Gavel size={20} />
                </div>
                <h2 className="text-2xl font-bold text-slate-900">1. Forensic Integrity</h2>
              </div>
              <div className="space-y-6 text-slate-600 leading-relaxed font-medium">
                <p>
                  By using FakeShield, you agree to use our forensic tools for legitimate verification and investigative purposes. 
                  Any attempt to reverse-engineer our detection algorithms or use the platform to "test" how to bypass 
                  AI detection is strictly prohibited.
                </p>
              </div>
            </section>

            <section>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-[#00E5CC]">
                  <AlertCircle size={20} />
                </div>
                <h2 className="text-2xl font-bold text-slate-900">2. Acceptable Use</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { title: 'No Harassment', desc: 'Do not use verification results to target or harass individuals.' },
                  { title: 'Source Integrity', desc: 'Only upload media for which you have legal access or investigative rights.' },
                  { title: 'No Automated Scraping', desc: 'Accessing the engine via unauthorized bots or scrapers is a breach of service.' },
                  { title: 'Reporting Accuracy', desc: 'Recognize that scores are forensic probabilities, not absolute legal facts.' }
                ].map((item, i) => (
                  <div key={i} className="p-6 rounded-[2rem] bg-slate-50 border border-slate-100">
                    <h4 className="font-bold text-slate-900 mb-2">{item.title}</h4>
                    <p className="text-sm text-slate-500">{item.desc}</p>
                  </div>
                ))}
              </div>
            </section>

            <section>
              <div className="flex items-center gap-4 mb-6">
                <div className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-[#00E5CC]">
                  <Scale size={20} />
                </div>
                <h2 className="text-2xl font-bold text-slate-900">3. Results & Accountability</h2>
              </div>
              <div className="space-y-6 text-slate-600 leading-relaxed font-medium">
                <p>
                  While FakeShield utilizes state-of-the-art neural engines, forensic analysis is inherently probabilistic. 
                  Our confidence scores are technical indicators intended to support investigations and do not constitute 
                  absolute legal proof. Users are responsible for how they interpret and act upon these forensic signals.
                </p>
                <div className="border-l-4 border-[#00E5CC] pl-6 py-2 italic text-sm">
                  "The user retains all ownership of original content, while FakeShield retains ownership of the forensic 
                  signals and reports generated by our engines."
                </div>
              </div>
            </section>

            <section className="pt-8 border-t border-slate-100">
              <div className="p-8 rounded-[2.5rem] bg-[#00E5CC] text-slate-900 flex flex-col md:flex-row items-center gap-8 shadow-xl shadow-[#00E5CC]/20">
                 <ShieldCheck size={48} className="text-slate-900" />
                 <div>
                   <h3 className="text-xl font-bold mb-2">Compliance & Liability</h3>
                   <p className="text-slate-800 text-sm leading-relaxed font-medium">
                     FakeShield is a tool for investigative assistance. We do not provide legal advice, 
                     and we are not liable for decisions made based on forensic confidence scores.
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
