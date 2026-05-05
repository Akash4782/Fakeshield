import React, { useState, useEffect } from 'react';
import { ArrowLeft, Plus, Minus, Search, BrainCircuit, Activity, Zap, Database } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import logo from '../../assets/logo.png';
import Footer from '../../components/Footer';

const FAQItem: React.FC<{ question: string; answer: string; icon: React.ReactNode }> = ({ question, answer, icon }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className={`p-8 rounded-[2.5rem] border transition-all duration-500 ${isOpen ? 'bg-slate-50 border-[#00E5CC]/30' : 'bg-white border-slate-100 hover:border-slate-200'}`}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between gap-6 text-left"
      >
        <div className="flex items-center gap-6">
          <div className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-colors duration-500 ${isOpen ? 'bg-[#00E5CC] text-white' : 'bg-slate-50 text-slate-400'}`}>
            {icon}
          </div>
          <h3 className="text-lg font-bold text-slate-900 leading-tight">{question}</h3>
        </div>
        <div className={`w-8 h-8 rounded-full border flex items-center justify-center transition-all duration-500 ${isOpen ? 'bg-slate-900 border-slate-900 text-white' : 'border-slate-200 text-slate-400'}`}>
          {isOpen ? <Minus size={16} /> : <Plus size={16} />}
        </div>
      </button>
      <div className={`overflow-hidden transition-all duration-500 ${isOpen ? 'max-h-96 opacity-100 mt-8' : 'max-h-0 opacity-0'}`}>
        <p className="text-slate-500 font-medium leading-relaxed pl-[4.5rem]">
          {answer}
        </p>
      </div>
    </div>
  );
};

const FAQPage: React.FC = () => {
  const navigate = useNavigate();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const faqs = [
    {
      icon: <BrainCircuit size={20} />,
      question: "How accurate is the FakeShield detection engine?",
      answer: "Our core engines achieve 98.9% accuracy on validated benchmarks. However, forensics is about probability. We provide a 'Confidence Score' based on multiple signals (Frequency analysis, facial mesh consistency, and temporal artifacts) rather than a simple Yes/No."
    },
    {
      icon: <Zap size={20} />,
      question: "Can FakeShield detect real-time deepfakes?",
      answer: "Yes. Our Live Monitor lab is designed for real-time stream analysis with sub-2.4s latency, making it ideal for verifying live video calls or breaking news broadcasts."
    },
    {
      icon: <Activity size={20} />,
      question: "What file formats do you support for analysis?",
      answer: "We support all standard formats: MP4, MOV, AVI for video; MP3, WAV, FLAC for audio; and JPG, PNG, WEBP for images. Enterprise users can also process raw forensic dumps."
    },
    {
      icon: <Database size={20} />,
      question: "Are the reports valid for legal proceedings?",
      answer: "FakeShield provides forensic signals and technical documentation that can be used to support an investigation. While our reports are built on established signal processing standards, their admissibility depends on your local jurisdiction and expert testimony."
    }
  ];

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
          <div className="mb-16 text-center">
            <h1 className="text-5xl md:text-7xl font-black mb-8 tracking-tight text-slate-900">
              Common <span className="text-[#00E5CC]">Questions.</span>
            </h1>
          </div>

          <div className="space-y-4">
            {faqs.map((faq, i) => (
              <FAQItem key={i} {...faq} />
            ))}
          </div>

          <div className="mt-20 p-12 rounded-[3rem] bg-[#00E5CC] text-slate-900 text-center relative overflow-hidden">
             <div className="relative z-10">
               <h2 className="text-3xl font-black mb-4">Still have doubts?</h2>
               <p className="font-medium mb-8 opacity-80">Our technical support team is ready to assist with complex cases.</p>
               <button 
                onClick={() => navigate('/contact')}
                className="px-10 py-4 bg-slate-900 text-white rounded-2xl font-bold hover:scale-105 transition-all"
               >
                 Open Support Ticket
               </button>
             </div>
             <div className="absolute -bottom-10 -right-10 w-48 h-48 bg-white/20 blur-3xl rounded-full"></div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default FAQPage;
