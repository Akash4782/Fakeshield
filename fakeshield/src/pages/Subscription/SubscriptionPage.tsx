import React, { useEffect, useState } from 'react';
import { Check, Shield, Zap, Crown, ArrowRight, Loader2, ArrowLeft, CreditCard } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth.tsx';
import { API_BASE_URL } from '../../config';

interface RazorpayOrderResponse {
  key_id: string;
  order_id: string;
  amount: number;
  currency: string;
  name: string;
  description: string;
  prefill?: {
    name?: string;
    email?: string;
    contact?: string;
  };
}

interface PaymentConfig {
  amount: number;
  currency: string;
  name: string;
  duration_days: number;
}

interface RazorpaySuccessResponse {
  razorpay_payment_id: string;
  razorpay_order_id: string;
  razorpay_signature: string;
}

interface RazorpayCheckoutOptions extends RazorpayOrderResponse {
  key: string;
  order_id: string;
  handler: (response: RazorpaySuccessResponse) => void;
  theme?: { color: string };
  modal?: { ondismiss: () => void };
}

declare global {
  interface Window {
    Razorpay?: new (options: RazorpayCheckoutOptions) => {
      open: () => void;
      on: (event: string, handler: (response: unknown) => void) => void;
    };
  }
}

const loadRazorpayCheckout = () =>
  new Promise<void>((resolve, reject) => {
    if (window.Razorpay) {
      resolve();
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Unable to load Razorpay Checkout.'));
    document.body.appendChild(script);
  });

const DEFAULT_PAYMENT_CONFIG: PaymentConfig = {
  amount: 100,
  currency: 'INR',
  name: 'FakeShield Pro Shield',
  duration_days: 120,
};

const formatPaymentAmount = (amountPaise: number, currency: string) =>
  new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
  }).format(amountPaise / 100);

const SubscriptionPage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated, token, user: authUser, updateUser } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [paymentStep, setPaymentStep] = useState<'plans' | 'payment' | 'success'>('plans');
  const [paymentConfig, setPaymentConfig] = useState<PaymentConfig>(DEFAULT_PAYMENT_CONFIG);
  const [transactionId, setTransactionId] = useState('');
  const [orderId, setOrderId] = useState(() => `FS-${new Date().getFullYear()}-${Math.floor(100000 + Math.random() * 900000)}`);
  const user = authUser || JSON.parse(localStorage.getItem('fakeshield_user') || '{}');
  const paymentAmount = formatPaymentAmount(paymentConfig.amount, paymentConfig.currency);
  const planDurationMonths = Math.round(paymentConfig.duration_days / 30);
  const planPeriodLabel = `${planDurationMonths} months`;
  const subscriptionExpiry = user.subscription_expires_at
    ? new Date(user.subscription_expires_at).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      })
    : null;

  useEffect(() => {
    const loadPaymentConfig = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/auth/payments/razorpay/config`);
        if (!response.ok) return;
        const config: PaymentConfig = await response.json();
        setPaymentConfig(config);
      } catch (err) {
        console.warn('Using default payment config because backend config could not be loaded.', err);
      }
    };

    loadPaymentConfig();
  }, []);

  const handleUpgrade = async () => {
    if (!token) {
      navigate('/login', { state: { from: '/subscription' } });
      return;
    }

    setIsLoading(true);
    try {
      await loadRazorpayCheckout();

      const orderResponse = await fetch(`${API_BASE_URL}/auth/payments/razorpay/order`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!orderResponse.ok) {
        const error = await orderResponse.json().catch(() => ({}));
        throw new Error(error.detail || 'Could not create Razorpay order.');
      }

      const order: RazorpayOrderResponse = await orderResponse.json();
      setOrderId(order.order_id);
      setPaymentConfig({
        amount: order.amount,
        currency: order.currency,
        name: order.description,
        duration_days: paymentConfig.duration_days,
      });

      const Razorpay = window.Razorpay;
      if (!Razorpay) {
        throw new Error('Razorpay Checkout did not load.');
      }

      const razorpay = new Razorpay({
        ...order,
        key: order.key_id,
        order_id: order.order_id,
        handler: async (response) => {
          setIsLoading(true);
          try {
            const verifyResponse = await fetch(`${API_BASE_URL}/auth/payments/razorpay/verify`, {
              method: 'POST',
              headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(response),
            });

            if (!verifyResponse.ok) {
              const error = await verifyResponse.json().catch(() => ({}));
              throw new Error(error.detail || 'Payment verification failed.');
            }

            const verified = await verifyResponse.json();
            if (!verified.user || verified.user.subscription_tier !== 'paid') {
              throw new Error('Payment verified, but the server did not activate Pro. Please contact support.');
            }
            updateUser(verified.user);
            setTransactionId(response.razorpay_payment_id);
            setOrderId(response.razorpay_order_id);
            setPaymentStep('success');
          } catch (err) {
            console.error(err);
            alert(err instanceof Error ? err.message : 'Payment verification failed.');
          } finally {
            setIsLoading(false);
          }
        },
        theme: { color: '#00E5CC' },
        modal: {
          ondismiss: () => setIsLoading(false),
        },
      });

      razorpay.on('payment.failed', (response) => {
        console.error('Razorpay payment failed', response);
        alert('Payment failed or was cancelled. Please try again.');
        setIsLoading(false);
      });

      razorpay.open();
    } catch (err) {
      console.error(err);
      alert(err instanceof Error ? err.message : 'Unable to start Razorpay checkout.');
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
Pro Shield License (${planPeriodLabel})   ${paymentAmount}
Full Access to:
- Image Forensic Lab
- Audio Deepfake Lab
- Video Consistency Lab
- Neural Pattern Matching
-----------------------------------------
TOTAL PAID:                   ${paymentAmount}
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
      price: paymentAmount,
      period: `/${planPeriodLabel}`,
      description: `The complete forensic arsenal for ${planPeriodLabel}`,
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
    <div className="min-h-screen pt-16 md:pt-24 pb-16 md:pb-20 px-4" style={{ background: '#F8FAFC', color: 'var(--text-primary)' }}>
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-10 md:mb-16 animate-fade-in">
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
                className={`relative rounded-[2rem] md:rounded-[2.5rem] p-6 sm:p-8 md:p-10 transition-all duration-500 transform hover:-translate-y-2 ${plan.highlight ? 'shadow-2xl z-10' : 'shadow-sm'}`}
                style={{ 
                  background: 'white', 
                  border: plan.highlight ? '1px solid #00E5CC' : '1px solid #E2E8F0',
                }}
              >
                {plan.highlight && (
                  <div className="absolute top-6 right-6 md:top-8 md:right-10 flex items-center gap-2">
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
                    } else if (!isAuthenticated) {
                      navigate('/login', { state: { from: '/subscription' } });
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
          <div className="max-w-4xl mx-auto rounded-[2rem] md:rounded-[3rem] bg-white shadow-2xl border border-slate-100 overflow-hidden animate-fade-in-up">
            <div className="flex flex-col md:flex-row">
              {/* Left Side: Order Summary */}
              <div className="flex-1 p-6 sm:p-8 md:p-12 bg-slate-50 md:border-r border-slate-100">
                <button 
                  onClick={() => setPaymentStep('plans')}
                  className="mb-10 text-[10px] font-bold text-slate-400 hover:text-slate-900 flex items-center gap-2 transition-all uppercase tracking-widest"
                >
                  ← Adjust Plan
                </button>
                
                <div className="space-y-8">
                  <div>
                    <h2 className="text-3xl font-black text-slate-900 mb-2">Secure Checkout</h2>
                    <p className="text-slate-500 text-sm leading-relaxed">Verification protocol initialized. Complete payment securely through Razorpay Checkout.</p>
                  </div>
                  
                  <div className="p-6 bg-white rounded-3xl space-y-4 border border-slate-200 shadow-sm">
                    <div className="flex justify-between items-center">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Selected Tier</span>
                      <span className="text-sm font-bold text-slate-900">Pro Shield ({planPeriodLabel})</span>
                    </div>
                    <div className="h-px bg-slate-100"></div>
                    <div className="flex justify-between items-center">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Total Liability</span>
                      <span className="text-2xl font-black text-[#00E5CC]">{paymentAmount}</span>
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

              {/* Right Side: Razorpay Payment */}
              <div className="flex-1 p-6 sm:p-8 md:p-10 flex flex-col min-w-0">
                <div className="flex justify-between items-start mb-6 pb-4 border-b border-slate-100">
                  <div>
                    <button 
                      onClick={() => setPaymentStep('plans')}
                      className="text-[10px] font-bold text-slate-400 hover:text-slate-900 flex items-center gap-1 transition-all uppercase tracking-widest mb-1"
                    >
                      <ArrowLeft size={10} /> Go Back (Razorpay)
                    </button>
                    <p className="text-[10px] text-slate-400 font-mono">Order Id: {orderId}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Total Amount</p>
                    <p className="text-sm font-black text-slate-900">{paymentAmount}</p>
                  </div>
                </div>

                <div className="flex-1 flex flex-col items-center justify-center py-4">
                  <div className="mb-8 text-center">
                    <p className="text-[11px] font-bold text-slate-700 mb-6 px-4">
                      Razorpay supports UPI, cards, net banking, wallets, and other enabled payment methods.
                    </p>

                    <div className="relative group mx-auto w-fit">
                      <div className="absolute -inset-4 bg-[#00E5CC]/10 rounded-[2.5rem] blur-2xl group-hover:bg-[#00E5CC]/20 transition-all duration-500"></div>
                      <div className="relative w-44 h-44 sm:w-52 sm:h-52 bg-white p-6 rounded-3xl border-2 border-slate-100 flex flex-col items-center justify-center overflow-hidden shadow-inner">
                        <div className="w-20 h-20 bg-[#00E5CC]/10 rounded-full flex items-center justify-center mb-5">
                          <CreditCard size={42} className="text-[#00E5CC]" />
                        </div>
                        <p className="text-xs font-black uppercase tracking-widest text-slate-900">Razorpay Secure Checkout</p>
                        <p className="text-[10px] text-slate-400 mt-2">Order created server-side</p>
                      </div>
                    </div>
                  </div>

                  <div className="w-full space-y-4">
                    <button
                      onClick={handleUpgrade}
                      disabled={isLoading}
                      className="w-full bg-[#00E5CC] text-black font-black py-4 rounded-2xl shadow-xl shadow-[#00E5CC]/20 hover:bg-[#00d1ba] hover:-translate-y-1 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isLoading ? <Loader2 size={20} className="animate-spin mx-auto" /> : 'PAY WITH RAZORPAY'}
                    </button>
                    
                    <p className="text-[9px] text-slate-400 text-center leading-relaxed">
                      Your subscription activates only after Razorpay signature <br /> 
                      and captured payment status are verified by our server. Access lasts {planPeriodLabel}.
                    </p>
                  </div>
                </div>

                <div className="mt-auto pt-6 border-t border-slate-100 flex flex-wrap items-center justify-center gap-4 sm:justify-between opacity-40 grayscale hover:grayscale-0 transition-all duration-500 min-h-5 px-2">
                  <img src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg" alt="Visa" className="h-full object-contain" />
                  <img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Mastercard-logo.svg" alt="Mastercard" className="h-full object-contain" />
                  <img src="https://cdn.worldvectorlogo.com/logos/rupay-logo.svg" alt="RuPay" className="h-full object-contain" />
                  <img src="https://upload.wikimedia.org/wikipedia/commons/a/ab/PCI_DSS_logo.svg" alt="PCI DSS" className="h-full object-contain" />
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="max-w-2xl mx-auto text-center py-12 md:py-20 px-6 md:px-10 rounded-[2rem] md:rounded-[3rem] bg-white shadow-2xl border border-slate-100 animate-fade-in-up">
            <div className="w-24 h-24 bg-[#00E5CC]/10 rounded-full flex items-center justify-center mx-auto mb-8">
              <Shield size={48} className="text-[#00E5CC] animate-pulse" />
            </div>
            <h2 className="text-4xl font-black text-slate-900 mb-4 font-display">Upgrade Successful!</h2>
            <p className="text-slate-500 mb-10 leading-relaxed text-lg">
              The Forensic Perimeter is now fully active. Your <span className="font-bold text-slate-900">Pro Shield</span> access is active for {planPeriodLabel}.
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
              {subscriptionExpiry && (
                <div className="flex justify-between items-center mt-2 pt-2 border-t border-slate-200">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Valid Until</span>
                  <span className="text-xs font-bold text-slate-700">{subscriptionExpiry}</span>
                </div>
              )}
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
