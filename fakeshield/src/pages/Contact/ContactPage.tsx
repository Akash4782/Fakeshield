import React, { useState, useEffect } from 'react';
import { Mail, Phone, MapPin, MessageSquare, ArrowLeft, Send, CheckCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import logo from '../../assets/logo.png';
import Footer from '../../components/Footer';

const ContactPage: React.FC = () => {
  const navigate = useNavigate();
  const [sent, setSent] = useState(false);
  const [form, setForm] = useState({ name: '', email: '', phone: '', message: '' });

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate API call
    setSent(true);
    setTimeout(() => {
      setSent(false);
      setForm({ name: '', email: '', phone: '', message: '' });
      navigate('/');
    }, 4000);
  };

  const inputStyle = "w-full px-4 py-3 rounded-xl border border-slate-200 bg-white text-slate-900 text-sm outline-none focus:border-[#00E5CC] transition-all";

  return (
    <div className="min-h-screen flex flex-col bg-white" style={{ fontFamily: "'Inter', sans-serif" }}>
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-6 h-28 flex items-center justify-between">
          <div className="flex items-center gap-12">
            <button 
              onClick={() => navigate(-1)}
              className="w-12 h-12 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400 hover:text-white hover:bg-[#00E5CC] transition-all duration-500 shadow-sm hover:shadow-lg hover:shadow-[#00E5CC]/20"
            >
              <ArrowLeft size={20} />
            </button>
            <div className="flex items-center gap-10 cursor-pointer" onClick={() => navigate('/')}>
              <img src={logo} alt="FakeShield" className="h-24" />
              <span className="text-4xl font-black tracking-tighter text-slate-900">FAKESHIELD</span>
            </div>
          </div>
        </div>
      </header>

      <main className="flex-grow pt-40 pb-24">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-20">
            
            {/* Left Side: Info */}
            <div className="space-y-12">
              <div>
                <h1 className="text-5xl font-black text-slate-900 mb-6 tracking-tight">Let's talk <br /><span className="text-[#00E5CC]">Forensics.</span></h1>
                <p className="text-lg text-slate-500 leading-relaxed max-w-md">
                  Have a specific use case or need enterprise-grade verification? 
                  Our team is ready to help you deploy FakeShield across your organization.
                </p>
              </div>

              <div className="space-y-8">
                <div className="flex items-start gap-6">
                  <div className="w-12 h-12 rounded-2xl bg-slate-50 flex items-center justify-center text-[#00E5CC] flex-shrink-0">
                    <Mail size={24} />
                  </div>
                  <div>
                    <h4 className="font-bold text-slate-900 mb-1">Email us</h4>
                    <p className="text-slate-500 text-sm mb-2">For support or general inquiries.</p>
                    <a href="mailto:virdiakash77@gmail.com" className="text-[#00E5CC] font-bold text-sm hover:underline">virdiakash77@gmail.com</a>
                  </div>
                </div>

                <div className="flex items-start gap-6">
                  <div className="w-12 h-12 rounded-2xl bg-slate-50 flex items-center justify-center text-[#00E5CC] flex-shrink-0">
                    <Phone size={24} />
                  </div>
                  <div>
                    <h4 className="font-bold text-slate-900 mb-1">Call us</h4>
                    <p className="text-slate-500 text-sm mb-2">Available Mon-Fri, 9am - 6pm IST.</p>
                    <p className="text-slate-900 font-bold text-sm">+91 7973066831</p>
                  </div>
                </div>

                <div className="flex items-start gap-6">
                  <div className="w-12 h-12 rounded-2xl bg-slate-50 flex items-center justify-center text-[#00E5CC] flex-shrink-0">
                    <svg width="24" height="24" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                  </div>
                  <div>
                    <h4 className="font-bold text-slate-900 mb-1">LinkedIn</h4>
                    <p className="text-slate-500 text-sm mb-2">Professional networking & inquiries.</p>
                    <a href="https://www.linkedin.com/in/akash-virdi-399ab4253/" target="_blank" rel="noopener noreferrer" className="text-[#00E5CC] font-bold text-sm hover:underline">Akash Virdi</a>
                  </div>
                </div>
              </div>

              <div className="p-8 rounded-[2.5rem] bg-[#00E5CC] text-slate-900 relative overflow-hidden shadow-lg shadow-[#00E5CC]/20">
                <div className="absolute top-0 right-0 w-32 h-32 bg-white/20 blur-3xl rounded-full translate-x-10 -translate-y-10"></div>
                <MessageSquare className="text-slate-900 mb-4" size={32} />
                <h4 className="text-xl font-bold mb-2">Technical Support</h4>
                <p className="text-slate-800 text-sm leading-relaxed font-medium">
                  Existing customers can access 24/7 technical assistance through the Console Dashboard.
                </p>
              </div>
            </div>

            {/* Right Side: Form */}
            <div className="relative">
              {sent ? (
                <div className="h-full min-h-[600px] flex flex-col items-center justify-center text-center p-12 bg-slate-50 rounded-[3rem] border border-slate-100 animate-in fade-in zoom-in duration-500">
                  <div className="w-20 h-20 rounded-full bg-[#00E5CC]/10 flex items-center justify-center text-[#00E5CC] mb-8">
                    <CheckCircle size={40} />
                  </div>
                  <h2 className="text-3xl font-black text-slate-900 mb-4">Transmission Received.</h2>
                  <p className="text-slate-500 mb-8 max-w-xs">Our engineering team has received your message. We'll be in touch within 24 hours.</p>
                  <div className="flex gap-2">
                    <div className="w-2 h-2 rounded-full bg-[#00E5CC] animate-bounce"></div>
                    <div className="w-2 h-2 rounded-full bg-[#00E5CC] animate-bounce [animation-delay:0.2s]"></div>
                    <div className="w-2 h-2 rounded-full bg-[#00E5CC] animate-bounce [animation-delay:0.4s]"></div>
                  </div>
                </div>
              ) : (
                <div className="p-10 md:p-12 bg-white rounded-[3rem] border border-slate-100 shadow-2xl shadow-slate-200/50">
                  <h3 className="text-2xl font-black text-slate-900 mb-8">Send a Message</h3>
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-400 uppercase tracking-wider ml-1">Your Name</label>
                        <input 
                          required
                          type="text" 
                          placeholder="Akash Virdi"
                          className={inputStyle}
                          value={form.name}
                          onChange={e => setForm({...form, name: e.target.value})}
                        />
                      </div>
                      <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-400 uppercase tracking-wider ml-1">Phone Number</label>
                        <input 
                          type="tel" 
                          placeholder="+91-0000000000"
                          className={inputStyle}
                          value={form.phone}
                          onChange={e => setForm({...form, phone: e.target.value})}
                        />
                      </div>
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider ml-1">Email Address</label>
                      <input 
                        required
                        type="email" 
                        placeholder="virdiakash77@gmail.com"
                        className={inputStyle}
                        value={form.email}
                        onChange={e => setForm({...form, email: e.target.value})}
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-bold text-slate-400 uppercase tracking-wider ml-1">How can we help?</label>
                      <textarea 
                        required
                        rows={5}
                        placeholder="Tell us about your project, team, or forensic requirements..."
                        className={inputStyle + " resize-none"}
                        value={form.message}
                        onChange={e => setForm({...form, message: e.target.value})}
                      />
                    </div>

                    <button 
                      type="submit"
                      className="w-full py-5 rounded-2xl bg-[#00E5CC] text-slate-900 font-bold text-base hover:brightness-110 transition-all flex items-center justify-center gap-3 group shadow-xl shadow-[#00E5CC]/20"
                    >
                      Initialize Contact <Send size={18} className="group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
                    </button>

                    <p className="text-center text-xs text-slate-400 leading-relaxed px-8">
                      By submitting this form, you agree to our privacy policy and terms of service.
                    </p>
                  </form>
                </div>
              )}
            </div>

          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default ContactPage;
