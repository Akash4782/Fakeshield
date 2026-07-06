import React, { useEffect } from 'react';
import { Shield, ArrowRight, ArrowLeft, Github, Linkedin, Mail, Terminal, Code2, Database, BrainCircuit, Activity } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import logo from '../../assets/logo.png';
import akashPortrait from '../../assets/akash-virdi.png';
import Footer from '../../components/Footer';

const AboutPage: React.FC = () => {
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
          <button 
            onClick={() => navigate('/login')}
            className="hidden sm:flex text-sm font-bold transition-colors items-center gap-2 shrink-0"
            style={{ color: 'var(--text-secondary)' }}
            onMouseEnter={(e) => e.currentTarget.style.color = 'var(--text-primary)'}
            onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-secondary)'}
          >
            Launch Terminal <ArrowRight size={14} />
          </button>
        </div>
      </nav>

      <main className="flex-grow">
        {/* Section 1: Hero - Narrative driven */}
        <section className="pt-32 md:pt-40 pb-20 md:pb-24 px-4 sm:px-6" style={{ borderBottom: '1px solid var(--panel-border)' }}>
          <div className="max-w-4xl mx-auto">
            <h1 className="text-5xl md:text-8xl font-black mb-12 tracking-tight leading-[0.9]">
              Authentication <br />
              <span className="text-[#00E5CC]">is broken.</span>
            </h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
              <div className="space-y-8">
                <p className="text-lg leading-relaxed font-medium" style={{ color: 'var(--text-secondary)' }}>
                  We inhabit a reality where digital evidence is no longer absolute. Synthesized video, cloned audio, and algorithmic revisionism can now rewrite history in real-time. FakeShield is not a generic corporate platform. It is a precision forensic instrument engineered to extract objective truth from synthetic noise.
                </p>
                <p className="text-lg leading-relaxed font-medium" style={{ color: 'var(--text-secondary)' }}>
                  Our mission is to establish a definitive defense layer against the erosion of digital trust. By integrating deep neural architecture with advanced signal processing, we empower investigators and security experts with the transparency required for high-stakes verification. We do more than identify AI; we reveal the mathematical artifacts of its creation.
                </p>
              </div>
              <div className="flex flex-col gap-6 p-8 rounded-[2.5rem] border shadow-xl" style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)' }}>
                <div className="flex gap-2.5 mb-2">
                  <div className="w-3 h-3 rounded-full bg-[#ff5f56]"></div>
                  <div className="w-3 h-3 rounded-full bg-[#ffbd2e]"></div>
                  <div className="w-3 h-3 rounded-full bg-[#27c93f]"></div>
                </div>
                <div className="space-y-4 font-mono text-[11px] leading-relaxed">
                  <p style={{ color: 'var(--text-muted)' }}>// FAKESHIELD FORENSIC CORE V14.6.2</p>
                  <p className="text-emerald-600 font-bold">$ fs_engine --scan --multi-modal --target=source_media.mp4</p>
                  <div className="pl-4 space-y-1">
                    <p style={{ color: 'var(--text-secondary)' }}>[INFO] Loading forensic models... DONE (2.4s)</p>
                    <p style={{ color: 'var(--text-secondary)' }}>[INFO] Analyzing FFT spectrum... NOISE_FLOOR_INCONSISTENCY</p>
                    <p style={{ color: 'var(--text-secondary)' }}>[INFO] Extracting optical flow vectors... ANOMALY_DETECTED</p>
                    <p className="text-rose-500 font-bold">[CRITICAL] Neural artifacts found in Y-Channel at [452:12, 890:44]</p>
                    <p className="text-rose-500 font-bold">[CRITICAL] Temporal flickering detected in facial region</p>
                  </div>
                  <p className="text-amber-600 font-bold">$ fs_verify --report --detailed</p>
                  <p style={{ color: 'var(--text-primary)' }}>[RESULT] Confidence Score: 98.92% (SYNTHETIC)</p>
                  <p className="text-[#00E5CC] animate-pulse font-bold">_ system awaiting instruction...</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Section 2: Technical Philosophy - No generic boxes */}
        <section className="py-32 px-6">
          <div className="max-w-6xl mx-auto">
            <div className="flex flex-col md:flex-row gap-20">
              <motion.div
                className="md:w-1/3 h-fit md:sticky md:top-36 md:self-start"
                initial={{ opacity: 0, x: -24 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true, amount: 0.5 }}
                transition={{ duration: 0.6, ease: 'easeOut' }}
              >
                <h2 className="text-xs font-bold text-[#00E5CC] uppercase tracking-[0.3em] mb-4">Engineering</h2>
                <h3 className="text-3xl font-black mb-6" style={{ color: 'var(--text-heading)' }}>How we verify.</h3>
                <p className="leading-relaxed" style={{ color: 'var(--text-secondary)' }}>
                  Generic AI detectors look for "vibes". We look for mathematical impossibility.
                </p>
              </motion.div>
              <div className="md:w-2/3 relative space-y-12 md:space-y-20 md:pl-10">
                <div className="hidden md:block absolute left-0 top-8 bottom-8 w-px bg-gradient-to-b from-transparent via-[#00E5CC]/50 to-transparent" />
                <motion.article
                  className="group relative rounded-3xl border p-7 md:p-9"
                  style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}
                  initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.35 }} transition={{ duration: 0.55, ease: 'easeOut' }}
                  whileHover={{ y: -6, boxShadow: '0 22px 45px -28px rgba(0, 229, 204, 0.55)' }}
                >
                  <span className="hidden md:block absolute -left-[45px] top-12 w-2.5 h-2.5 rounded-full bg-[#00E5CC] ring-4 ring-[#00E5CC]/15 transition-transform group-hover:scale-150" />
                  <div className="text-5xl font-black mb-6 transition-colors" style={{ color: 'var(--text-muted)' }}>01</div>
                  <h4 className="text-xl font-bold mb-4" style={{ color: 'var(--text-primary)' }}>Frequency Domain Analysis</h4>
                  <p className="leading-relaxed max-w-lg" style={{ color: 'var(--text-secondary)' }}>
                    Synthetic audio and images leave distinct footprints in the frequency spectrum. 
                    We analyze DCT (Discrete Cosine Transform) coefficients to identify patterns 
                    consistent with GAN and Diffusion generators.
                  </p>
                </motion.article>
                <motion.article
                  className="group relative rounded-3xl border p-7 md:p-9"
                  style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}
                  initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.35 }} transition={{ duration: 0.55, ease: 'easeOut' }}
                  whileHover={{ y: -6, boxShadow: '0 22px 45px -28px rgba(0, 229, 204, 0.55)' }}
                >
                  <span className="hidden md:block absolute -left-[45px] top-12 w-2.5 h-2.5 rounded-full bg-[#00E5CC] ring-4 ring-[#00E5CC]/15 transition-transform group-hover:scale-150" />
                  <div className="text-5xl font-black mb-6 transition-colors" style={{ color: 'var(--text-muted)' }}>02</div>
                  <h4 className="text-xl font-bold mb-4" style={{ color: 'var(--text-primary)' }}>Neural Artifact Localization</h4>
                  <p className="leading-relaxed max-w-lg" style={{ color: 'var(--text-secondary)' }}>
                    Generative models struggle with consistency in low-level features—lighting gradients, 
                    pupil reflection, and background noise. Our engines isolate these regions for 
                    pixel-perfect scrutiny.
                  </p>
                </motion.article>
                <motion.article
                  className="group relative rounded-3xl border p-7 md:p-9"
                  style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}
                  initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true, amount: 0.35 }} transition={{ duration: 0.55, ease: 'easeOut' }}
                  whileHover={{ y: -6, boxShadow: '0 22px 45px -28px rgba(0, 229, 204, 0.55)' }}
                >
                  <span className="hidden md:block absolute -left-[45px] top-12 w-2.5 h-2.5 rounded-full bg-[#00E5CC] ring-4 ring-[#00E5CC]/15 transition-transform group-hover:scale-150" />
                  <div className="text-5xl font-black mb-6 transition-colors" style={{ color: 'var(--text-muted)' }}>03</div>
                  <h4 className="text-xl font-bold mb-4" style={{ color: 'var(--text-primary)' }}>Multi-Signal Consensus</h4>
                  <p className="leading-relaxed max-w-lg" style={{ color: 'var(--text-secondary)' }}>
                    A video might pass a texture check but fail on frame-to-frame temporal consistency. 
                    FakeShield correlates signals across time and space to provide a unified confidence score.
                  </p>
                </motion.article>
              </div>
            </div>
          </div>
        </section>

        {/* Section 3: The Stack - Developer vibe */}
        <section className="py-16 px-6 relative overflow-hidden" style={{ background: '#00E5CC' }}>
          <div className="max-w-6xl mx-auto relative z-10">
             <div className="mb-12">
               <h2 className="text-3xl font-black mb-4 tracking-tight" style={{ color: '#000000' }}>The Forensic Core.</h2>
               <p className="max-w-xl font-medium text-sm leading-relaxed" style={{ color: '#1e293b' }}>
                 Engineered for absolute signal integrity and multi-modal detection performance. 
                 Zero abstractions. Zero bloat. Just pure forensic engineering.
               </p>
             </div>
 
             <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {[
                  { 
                    logo: 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg', 
                    title: 'Frontend', 
                    desc: 'React 18 + TS', 
                    tech: 'Type-safe UI architecture' 
                  },
                  { 
                    logo: 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg', 
                    title: 'Backend', 
                    desc: 'FastAPI + Python', 
                    tech: 'Async forensic pipeline' 
                  },
                  { 
                    logo: 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytorch/pytorch-original.svg', 
                    title: 'Intelligence', 
                    desc: 'PyTorch ML', 
                    tech: 'Neural artifact analysis' 
                  },
                  { 
                    logo: 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg', 
                    title: 'Database', 
                    desc: 'MongoDB Atlas', 
                    tech: 'Encrypted document store' 
                  },
                ].map((item, i) => (
                  <div key={i} className="p-7 bg-white rounded-3xl shadow-xl shadow-black/5 hover:-translate-y-1 transition-all duration-300 group">
                    <div className="w-10 h-10 mb-6 transition-transform duration-500 group-hover:scale-110">
                      <img src={item.logo} alt={item.title} className="w-full h-full object-contain" />
                    </div>
                    <h5 className="text-[9px] font-black text-[#00E5CC] uppercase tracking-[0.2em] mb-2">{item.title}</h5>
                    <p className="font-bold text-base mb-3" style={{ color: '#000000' }}>{item.desc}</p>
                    <div className="h-[2px] w-6 bg-slate-100 group-hover:w-10 transition-all duration-500 mb-3"></div>
                    <p className="text-[11px] font-mono italic leading-tight" style={{ color: '#64748b' }}>{item.tech}</p>
                  </div>
                ))}
             </div>
          </div>
        </section>

        {/* Section 4: The Developer - Portfolio style */}
        <section className="py-32 px-6">
          <div className="max-w-4xl mx-auto">
            <div className="flex flex-col md:flex-row gap-16 items-center">
               <div className="relative group">
                 <div className="absolute -inset-4 bg-[#00E5CC]/25 rounded-[3rem] blur-2xl opacity-40 group-hover:opacity-80 transition-all duration-700"></div>
                 <div className="relative w-52 h-64 rounded-[2.5rem] overflow-hidden transition-all duration-500 group-hover:-translate-y-1 group-hover:shadow-2xl" style={{ background: 'var(--btn-secondary-bg)', border: '1px solid var(--panel-border)', boxShadow: '0 20px 45px -25px rgba(0, 229, 204, 0.55)' }}>
                    <img src={akashPortrait} alt="Akash Virdi under a moonlit sky" className="w-full h-full object-cover object-center transition-transform duration-700 group-hover:scale-105" />
                 </div>
               </div>
               <div className="flex-grow">
                 <h2 className="text-4xl font-black mb-6" style={{ color: 'var(--text-heading)' }}>Akash Virdi</h2>
                 <p className="text-lg leading-relaxed mb-8" style={{ color: 'var(--text-secondary)' }}>
                   I built FakeShield because I believe digital verification shouldn't be a black box. 
                   As an engineer, I'm focused on creating tools that empower investigators to peel back 
                   the layers of AI-generated media and see the math underneath.
                 </p>
                <div className="flex flex-wrap gap-3">
                    <a href="https://github.com/Akash4782" target="_blank" rel="noreferrer" className="flex items-center gap-2.5 px-5 py-2.5 rounded-xl text-sm font-bold shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all" style={{ background: 'var(--panel-bg)', border: '1px solid var(--panel-border)', color: 'var(--text-primary)' }}>
                      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" className="w-4 h-4" alt="GitHub" />
                      GitHub
                    </a>
                    <a href="https://www.linkedin.com/in/akash-virdi-399ab4253/" target="_blank" rel="noreferrer" className="flex items-center gap-2.5 px-5 py-2.5 rounded-xl text-sm font-bold shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all" style={{ background: 'var(--panel-bg)', border: '1px solid var(--panel-border)', color: 'var(--text-primary)' }}>
                      <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" className="w-4 h-4" alt="LinkedIn" />
                      LinkedIn
                    </a>
                    <a href="mailto:virdiakash77@gmail.com" className="flex items-center gap-2.5 px-5 py-2.5 rounded-xl text-sm font-bold shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all" style={{ background: 'var(--panel-bg)', border: '1px solid var(--panel-border)', color: 'var(--text-primary)' }}>
                      <div className="w-4 h-4 bg-rose-500 rounded-md flex items-center justify-center">
                        <Mail size={10} className="text-white" />
                      </div>
                      Email
                    </a>
                 </div>
               </div>
            </div>
          </div>
        </section>

        {/* Section 5: Stats / Progress Bar - Dev aesthetic */}
        <section className="pb-32 px-6">
          <div className="max-w-4xl mx-auto p-6 md:p-12 rounded-[2rem] md:rounded-[3rem] border bg-slate-50/50" style={{ background: 'var(--panel-bg)', borderColor: 'var(--panel-border)' }}>
             <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                {[
                  { label: 'Latency', value: '<2.4s' },
                  { label: 'Accuracy', value: '98.9%' },
                  { label: 'Uptime', value: '99.9%' },
                  { label: 'Coverage', value: 'Multi-Modal' }
                ].map((stat, i) => (
                  <div key={i}>
                    <div className="text-[10px] font-black uppercase tracking-widest mb-1" style={{ color: 'var(--text-muted)' }}>{stat.label}</div>
                    <div className="text-xl font-bold" style={{ color: 'var(--text-heading)' }}>{stat.value}</div>
                    <div className="mt-3 h-1 w-full rounded-full overflow-hidden" style={{ background: 'var(--panel-border)' }}>
                      <div className="h-full bg-[#00E5CC]" style={{ width: i === 0 ? '85%' : i === 1 ? '98%' : '100%' }}></div>
                    </div>
                  </div>
                ))}
             </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default AboutPage;
