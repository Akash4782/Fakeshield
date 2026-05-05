import React, { useState, useEffect } from 'react';
import { Check, Shield, Zap, Crown, ArrowRight, Loader, QrCode, CreditCard, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../../hooks/useTheme';

const SubscriptionPage: React.FC = () => {
  const { theme } = useTheme();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [paymentStep, setPaymentStep] = useState<'plans' | 'payment' | 'success'>('plans');
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes in seconds
  const [transactionId, setTransactionId] = useState('');
  const [orderId] = useState(() => `FS-${new Date().getFullYear()}-${Math.floor(100000 + Math.random() * 900000)}`);
  const user = JSON.parse(localStorage.getItem('fakeshield_user') || '{}');
  
  // --- MERCHANT ACCOUNT CONFIGURATION ---
  // Change these values to update where the money goes and what message is shown
  const MERCHANT_CONFIG = {
    upiId: 'virdisaab419@okhdfcbank',
    name: 'FakeShield Forensics',
    amount: '999.00',
    note: 'Invoice FS-999: Pro Shield Activation'
  };

  useEffect(() => {
    if (paymentStep === 'payment' && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft(prev => prev - 1);
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [paymentStep, timeLeft]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const handleUpgrade = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8001/api/v1/auth/upgrade?email=${user.email}`, {
        method: 'POST',
      });
      
      if (response.ok) {
        // Update local storage for immediate UI synchronization
        const updatedUser = { ...user, subscription_tier: 'paid' };
        localStorage.setItem('fakeshield_user', JSON.stringify(updatedUser));
        
        // Multi-step simulated verification
        await new Promise(resolve => setTimeout(resolve, 2000));

        setPaymentStep('success');
      } else {
        alert('Verification failed. Please ensure the payment was successful or try again.');
      }
    } catch (err) {
      console.error(err);
      alert('Network error during verification. Our servers are checking your transaction.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadInvoice = () => {
    const invoiceContent = `
=========================================
      FAKESHIELD FORENSICS - INVOICE
=========================================
Date: ${new Date().toLocaleDateString()}
Order ID: ${orderId}
Transaction Ref (UTR): ${transactionId}
Customer Email: ${user.email || 'N/A'}

-----------------------------------------
ITEM DESCRIPTION              AMOUNT
-----------------------------------------
Pro Shield License (1 Year)   ₹999.00
Full Access to:
- Image Forensic Lab
- Audio Deepfake Lab
- Video Consistency Lab
- Neural Pattern Matching
-----------------------------------------
TOTAL PAID:                   ₹999.00
-----------------------------------------

Status: COMPLETED & VERIFIED
This is a computer-generated invoice.
No signature required.

Secure your digital perimeter with FakeShield.
=========================================
    `;
    const blob = new Blob([invoiceContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Invoice_${orderId}.txt`;
    link.click();
    window.URL.revokeObjectURL(url);
  };

  const plans = [
    {
      name: 'Free Tier',
      price: '₹0',
      description: 'Perfect for individual text verification',
      features: [
        'Access to Text Lab',
        'Basic AI Detection',
        'Linguistic Analysis',
        'Standard Response Time'
      ],
      restricted: [
        'Image Forensics',
        'Audio Deepfake Detection',
        'Video Consistency Lab',
        'Neural Pattern Matching'
      ],
      buttonText: 'Current Plan',
      isCurrent: user.subscription_tier !== 'paid',
      highlight: false
    },
    {
      name: 'Pro Shield',
      price: '₹999',
      period: '/year',
      description: 'The complete forensic arsenal for professionals',
      features: [
        'Everything in Free',
        'Full Image Forensic Lab',
        'Audio Deepfake Lab',
        'Video Consistency Lab',
        'Deep Forensic Metadata Analysis',
        'Advanced Analytics'
      ],
      buttonText: 'Upgrade to Pro',
      isCurrent: user.subscription_tier === 'paid',
      highlight: true
    }
  ];

  return (
    <div className="min-h-screen pt-24 pb-20 px-4" style={{ background: '#F8FAFC', color: 'var(--text-primary)' }}>
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16 animate-fade-in">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#00E5CC]/10 border border-[#00E5CC]/20 mb-6">
            <div className="w-1.5 h-1.5 rounded-full bg-[#00E5CC] animate-pulse"></div>
            <span className="text-[10px] font-bold text-[#00E5CC] uppercase tracking-widest">Enterprise Forensics</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-black mb-4 font-display text-slate-900">
            Secure Your <span className="text-[#00E5CC]">Forensic Perimeter</span>
          </h1>
          <p className="text-base text-slate-500 max-w-2xl mx-auto leading-relaxed">
            Protect your digital integrity with state-of-the-art AI detection engines. 
            Select a coverage plan that fits your investigative workflow.
          </p>
        </div>

        {paymentStep === 'plans' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {plans.map((plan, idx) => (
              <div 
                key={idx}
                className={`relative rounded-[2.5rem] p-10 transition-all duration-500 transform hover:-translate-y-2 ${plan.highlight ? 'shadow-2xl z-10' : 'shadow-sm'}`}
                style={{ 
                  background: 'white', 
                  border: plan.highlight ? '1px solid #00E5CC' : '1px solid #E2E8F0',
                }}
              >
                {plan.highlight && (
                  <div className="absolute top-8 right-10 flex items-center gap-2">
                    <Crown size={16} className="text-[#00E5CC]" />
                    <span className="text-[10px] font-bold text-[#00E5CC] uppercase tracking-[0.2em]">Priority</span>
                  </div>
                )}
                
                <div className="mb-10">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2 block">{plan.name}</span>
                  <div className="flex items-baseline gap-1">
                    <span className="text-5xl font-black text-slate-900">{plan.price}</span>
                    {plan.period && <span className="text-slate-400 font-medium ml-1">{plan.period}</span>}
                  </div>
                  <p className="mt-4 text-slate-500 text-sm leading-relaxed">{plan.description}</p>
                </div>

                <div className="space-y-4 mb-12">
                  <div className="h-px bg-slate-100 w-full mb-6"></div>
                  {plan.features.map((feature, fIdx) => (
                    <div key={fIdx} className="flex items-center gap-3">
                      <div className="w-5 h-5 rounded-full bg-[#00E5CC]/10 flex items-center justify-center">
                        <Check size={12} className="text-[#00E5CC]" />
                      </div>
                      <span className="text-sm font-medium text-slate-700">{feature}</span>
                    </div>
                  ))}
                  {plan.restricted?.map((feature, rIdx) => (
                    <div key={rIdx} className="flex items-center gap-3 opacity-40">
                      <div className="w-5 h-5 rounded-full bg-slate-100 flex items-center justify-center">
                        <div className="w-1.5 h-[1.5px] bg-slate-400"></div>
                      </div>
                      <span className="text-sm line-through text-slate-400">{feature}</span>
                    </div>
                  ))}
                </div>

                <button
                  onClick={() => {
                    if (plan.isCurrent) {
                      navigate('/dashboard');
                    } else if (plan.highlight) {
                      setPaymentStep('payment');
                    }
                  }}
                  className={`w-full py-4 rounded-2xl font-black text-xs uppercase tracking-widest transition-all duration-300 flex items-center justify-center gap-2 ${
                    plan.isCurrent 
                    ? 'bg-slate-900 text-white hover:bg-black cursor-pointer shadow-lg hover:-translate-y-1' 
                    : plan.highlight 
                      ? 'bg-[#00E5CC] text-black shadow-xl shadow-[#00E5CC]/20 hover:bg-[#00d1ba] hover:-translate-y-1' 
                      : 'bg-slate-900 text-white hover:bg-black'
                  }`}
                >
                  {plan.isCurrent ? 'Current Plan' : plan.buttonText}
                  <ArrowRight size={14} />
                </button>
              </div>
            ))}
          </div>
        ) : paymentStep === 'payment' ? (
          <div className="max-w-4xl mx-auto rounded-[3rem] bg-white shadow-2xl border border-slate-100 overflow-hidden animate-fade-in-up">
            <div className="flex flex-col md:flex-row">
              {/* Left Side: Order Summary */}
              <div className="flex-1 p-10 md:p-12 bg-slate-50 border-r border-slate-100">
                <button 
                  onClick={() => setPaymentStep('plans')}
                  className="mb-10 text-[10px] font-bold text-slate-400 hover:text-slate-900 flex items-center gap-2 transition-all uppercase tracking-widest"
                >
                  ← Adjust Plan
                </button>
                
                <div className="space-y-8">
                  <div>
                    <h2 className="text-3xl font-black text-slate-900 mb-2">Secure Checkout</h2>
                    <p className="text-slate-500 text-sm leading-relaxed">Verification protocol initialized. Please complete the UPI transfer below.</p>
                  </div>
                  
                  <div className="p-6 bg-white rounded-3xl space-y-4 border border-slate-200 shadow-sm">
                    <div className="flex justify-between items-center">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Selected Tier</span>
                      <span className="text-sm font-bold text-slate-900">Pro Shield (Yearly)</span>
                    </div>
                    <div className="h-px bg-slate-100"></div>
                    <div className="flex justify-between items-center">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Total Liability</span>
                      <span className="text-2xl font-black text-[#00E5CC]">₹999.00</span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                     <div className="flex flex-col gap-2 p-4 rounded-2xl bg-white border border-slate-100 shadow-sm">
                        <Shield size={18} className="text-[#00E5CC]" />
                        <span className="text-[10px] font-bold text-slate-800 uppercase tracking-tighter">Bank-Grade Encryption</span>
                     </div>
                     <div className="flex flex-col gap-2 p-4 rounded-2xl bg-white border border-slate-100 shadow-sm">
                        <Zap size={18} className="text-indigo-500" />
                        <span className="text-[10px] font-bold text-slate-800 uppercase tracking-tighter">Instant Activation</span>
                     </div>
                  </div>
                </div>
              </div>

              {/* Right Side: QR Payment */}
              <div className="flex-1 p-8 md:p-10 flex flex-col">
                <div className="flex justify-between items-start mb-6 pb-4 border-b border-slate-100">
                  <div>
                    <button 
                      onClick={() => setPaymentStep('plans')}
                      className="text-[10px] font-bold text-slate-400 hover:text-slate-900 flex items-center gap-1 transition-all uppercase tracking-widest mb-1"
                    >
                      <ArrowLeft size={10} /> Go Back (QrPayX)
                    </button>
                    <p className="text-[10px] text-slate-400 font-mono">Order Id: {orderId}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Total Amount</p>
                    <p className="text-sm font-black text-slate-900">₹999.00</p>
                  </div>
                </div>

                <div className="flex-1 flex flex-col items-center justify-center py-4">
                  <div className="mb-6 text-center">
                    <p className="text-[11px] font-bold text-slate-700 mb-4 px-4">
                      Scan QR code using BHIM or your preferred UPI app
                    </p>
                    
                    <div className="flex items-center justify-center gap-6 mb-10 h-7 px-4">
                      <div className="flex items-center justify-center min-w-0">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c7/Google_Pay_Logo_%282020%29.svg" alt="GPay" className="h-[20px] object-contain" />
                      </div>
                      <div className="flex items-center justify-center min-w-0">
                        <img src="https://cdn.worldvectorlogo.com/logos/paytm-1.svg" alt="Paytm" className="h-[22px] object-contain" />
                      </div>
                      <div className="flex items-center justify-center min-w-0">
                        <img src="https://cdn.worldvectorlogo.com/logos/phonepe-1.svg" alt="PhonePe" className="h-[22px] object-contain" />
                      </div>
                      <div className="flex items-center justify-center min-w-0">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/2/29/Amazon_Pay_logo.svg" alt="Amazon Pay" className="h-[18px] object-contain" />
                      </div>
                    </div>

                    <div className="relative group mx-auto w-fit">
                      <div className="absolute -inset-4 bg-[#00E5CC]/10 rounded-[2.5rem] blur-2xl group-hover:bg-[#00E5CC]/20 transition-all duration-500"></div>
                      <div className="relative w-52 h-52 bg-white p-4 rounded-3xl border-2 border-slate-100 flex flex-col items-center justify-center overflow-hidden shadow-inner">
                        <img 
                          src={`https://api.qrserver.com/v1/create-qr-code/?size=300x300&ecc=H&data=${encodeURIComponent(`upi://pay?pa=${MERCHANT_CONFIG.upiId}&am=${MERCHANT_CONFIG.amount}&cu=INR&tn=${MERCHANT_CONFIG.note}`)}`}
                          alt="Payment QR Code"
                          className="w-full h-full object-contain"
                        />
                        
                        {/* Smaller Shield Logo Overlay - Ensures perfect scan-ability with ECC=H */}
                        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                          <div className="w-10 h-10 bg-white rounded-full p-1.5 shadow-xl border border-slate-50 flex items-center justify-center">
                            <div className="w-full h-full bg-[#00E5CC] rounded-full flex items-center justify-center">
                              <Shield size={16} className="text-white" />
                            </div>
                          </div>
                        </div>

                        <div className="absolute bottom-2 right-2 bg-white p-1 rounded-md shadow-sm border border-slate-100">
                           <div className="w-4 h-4 bg-[#00E5CC] rounded-[2px] flex items-center justify-center">
                             <Shield size={10} className="text-white" />
                           </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-6">
                      <p className={`text-[11px] font-bold ${timeLeft < 60 ? 'text-rose-500' : 'text-slate-600'}`}>
                        This QR code will expire in {formatTime(timeLeft)}
                      </p>
                    </div>
                  </div>

                  <div className="w-full space-y-4">
                    <button
                      onClick={handleUpgrade}
                      disabled={isLoading || timeLeft === 0}
                      className="w-full bg-[#00E5CC] text-black font-black py-4 rounded-2xl shadow-xl shadow-[#00E5CC]/20 hover:bg-[#00d1ba] hover:-translate-y-1 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isLoading ? <Loader size={20} className="animate-spin mx-auto" /> : (timeLeft === 0 ? 'QR EXPIRED' : 'CONFIRM TRANSACTION')}
                    </button>
                    
                    <p className="text-[9px] text-slate-400 text-center leading-relaxed">
                      By confirming, you agree that your transaction will be <br /> 
                      manually verified against our merchant logs.
                    </p>
                  </div>
                </div>

                <div className="mt-auto pt-6 border-t border-slate-100 flex items-center justify-between opacity-40 grayscale hover:grayscale-0 transition-all duration-500 h-5 px-2">
                  <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg" alt="Visa" className="h-full object-contain" />
                  <img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Mastercard-logo.svg" alt="Mastercard" className="h-full object-contain" />
                  <img src="https://cdn.worldvectorlogo.com/logos/rupay-logo.svg" alt="RuPay" className="h-full object-contain" />
                  <img src="https://upload.wikimedia.org/wikipedia/commons/a/ab/PCI_DSS_logo.svg" alt="PCI DSS" className="h-full object-contain" />
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="max-w-2xl mx-auto text-center py-20 px-10 rounded-[3rem] bg-white shadow-2xl border border-slate-100 animate-fade-in-up">
            <div className="w-24 h-24 bg-[#00E5CC]/10 rounded-full flex items-center justify-center mx-auto mb-8">
              <Shield size={48} className="text-[#00E5CC] animate-pulse" />
            </div>
            <h2 className="text-4xl font-black text-slate-900 mb-4 font-display">Upgrade Successful!</h2>
            <p className="text-slate-500 mb-10 leading-relaxed text-lg">
              The Forensic Perimeter is now fully active. Your access to <span className="font-bold text-slate-900">Pro Shield</span> features has been synchronized.
            </p>
            <div className="bg-slate-50 rounded-3xl p-6 mb-10 border border-slate-100">
              <div className="flex justify-between items-center mb-2">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Order Status</span>
                <span className="text-xs font-bold text-[#00E5CC]">PRO ACTIVATED</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Reference</span>
                <span className="text-xs font-mono text-slate-600">{transactionId}</span>
              </div>
            </div>
            <div className="flex flex-col sm:flex-row gap-4 mb-10">
              <button 
                onClick={() => navigate('/dashboard')}
                className="flex-1 py-5 rounded-2xl bg-slate-900 text-white font-black uppercase tracking-widest hover:bg-black transition-all shadow-xl hover:-translate-y-1"
              >
                Launch Dashboard
              </button>
              <button 
                onClick={handleDownloadInvoice}
                className="flex-1 py-5 rounded-2xl bg-white border-2 border-slate-100 text-slate-900 font-black uppercase tracking-widest hover:border-[#00E5CC] transition-all hover:-translate-y-1 flex items-center justify-center gap-2"
              >
                Download Invoice
              </button>
            </div>
            <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">
              Security Clearance: PRO-LEVEL-ACCESS-GRANTED
            </p>
          </div>
        )}
      </div>

      <style>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(-20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fade-in-up {
          from { opacity: 0; transform: translateY(40px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in { animation: fade-in 1s ease-out forwards; }
        .animate-fade-in-up { animation: fade-in-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
      `}</style>
    </div>
  );
};

export default SubscriptionPage;
