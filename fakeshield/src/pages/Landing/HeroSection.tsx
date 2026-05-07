import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth.tsx';

const HeroSection = () => {
  const { isAuthenticated } = useAuth();
  const [typedText1, setTypedText1] = useState('');
  const [typedText2, setTypedText2] = useState('');
  const fullText1 = "Defend Truth in the";
  const fullText2 = "Age of Synthetic Media";

  useEffect(() => {
    let index = 0;
    const maxLen = Math.max(fullText1.length, fullText2.length);
    const intervalId = setInterval(() => {
      // Type both at the same time
      if (index <= fullText2.length) {
        setTypedText2(fullText2.substring(0, index));
      }
      if (index <= fullText1.length) {
        // Line 1 in reverse order
        setTypedText1(fullText1.substring(fullText1.length - index));
      }

      if (index > maxLen) {
        clearInterval(intervalId);
      }
      index++;
    }, 70);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <header
      style={{
        position: 'relative',
        overflow: 'hidden',
        paddingTop: '6rem',
        paddingBottom: '5rem',
      }}
    >
      <style>{`
        .cursor {
          display: inline-block;
          width: 2px;
          height: 0.8em;
          background-color: #00E5CC;
          margin-left: 4px;
          animation: blink 1s step-end infinite;
          vertical-align: middle;
        }
        @keyframes blink {
          from, to { opacity: 1; }
          50% { opacity: 0; }
        }
      `}</style>
      {/* Background Glow */}
      <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }}>
        <div
          className="animate-glow-pulse"
          style={{
            position: 'absolute',
            top: '-10%',
            left: '50%',
            transform: 'translateX(-50%)',
            width: 'min(800px, 90vw)',
            height: '500px',
            background: 'radial-gradient(circle, rgba(0, 229, 204, 0.25) 0%, transparent 75%)',
            borderRadius: '50%',
            filter: 'blur(120px)',
          }}
        />
      </div>

      <div
        className="animate-fade-in-up"
        style={{
          maxWidth: '80rem',
          margin: '0 auto',
          padding: '0 1.5rem',
          position: 'relative',
          zIndex: 10,
          textAlign: 'center',
        }}
      >
        {/* Badge */}
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.25rem 0.75rem',
            borderRadius: '9999px',
            border: '1px solid var(--border-hover)',
            background: 'var(--btn-secondary-bg)',
            color: 'var(--accent-blue, #00E5CC)',
            fontSize: '0.8125rem',
            fontWeight: 500,
            marginBottom: '2rem',
          }}
        >
          <span style={{ position: 'relative', display: 'flex', width: '0.5rem', height: '0.5rem' }}>
            <span
              className="animate-ping"
              style={{
                position: 'absolute',
                inset: 0,
                borderRadius: '50%',
                background: '#00E5CC',
                opacity: 0.75,
              }}
            />
            <span
              style={{
                position: 'relative',
                display: 'inline-flex',
                borderRadius: '50%',
                width: '0.5rem',
                height: '0.5rem',
                background: '#00E5CC',
              }}
            />
          </span>
          Version 1.0 Now Live: FakeShield Forensic Suite
        </div>

        {/* Heading */}
        <h1
          className="font-display"
          style={{
            fontSize: 'clamp(2.5rem, 6vw, 4.5rem)',
            fontWeight: 700,
            letterSpacing: '-0.03em',
            color: 'var(--text-heading)',
            marginBottom: '1.5rem',
            lineHeight: 1.1,
          }}
        >
          <span style={{ display: 'inline-block', minHeight: '1.2em', verticalAlign: 'bottom' }}>
            {typedText1}
            {typedText1.length > 0 && typedText1.length < fullText1.length && <span className="cursor"></span>}
          </span>
          <br />
          <span className="text-gradient" style={{ display: 'inline-block', minHeight: '1.2em', verticalAlign: 'bottom' }}>
            {typedText2}
            {typedText2.length > 0 && typedText2.length < fullText2.length && <span className="cursor"></span>}
          </span>
        </h1>

        {/* Subheading */}
        <p
          style={{
            maxWidth: '42rem',
            margin: '0 auto 2.5rem',
            color: 'var(--text-secondary)',
            fontSize: 'clamp(1rem, 2vw, 1.125rem)',
            lineHeight: 1.7,
          }}
        >
          FakeShield is the world's most advanced forensic suite for deepfake detection.
          Engineered for governments, journalists, and enterprise security.
        </p>

        {/* CTA Buttons */}
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '1rem',
            marginBottom: '5rem',
          }}
        >
          <Link
            to="/signup"
            state={{ from: { pathname: "/dashboard" } }}
            className="btn-glow"
            style={{
              background: 'var(--cta-btn-bg, #00E5CC)',
              color: 'var(--cta-btn-color, #fff)',
              fontWeight: 600,
              padding: '1rem 2.5rem',
              borderRadius: '0.75rem',
              textDecoration: 'none',
              display: 'inline-block',
              boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
              transition: 'all 0.3s',
            }}
          >
            Start Forensic Scan
          </Link>

          <a
            href="#labs"
            style={{
              background: 'transparent',
              border: `1px solid var(--btn-secondary-border)`,
              color: 'var(--text-heading)',
              fontWeight: 600,
              padding: '1rem 2.5rem',
              borderRadius: '0.75rem',
              textDecoration: 'none',
              display: 'inline-block',
              transition: 'all 0.3s',
            }}
            onMouseOver={e => (e.currentTarget.style.background = 'var(--btn-secondary-hover)')}
            onMouseOut={e => (e.currentTarget.style.background = 'transparent')}
          >
            View Live Demo
          </a>
        </div>

        {/* Dashboard Preview */}
        <div
          style={{
            position: 'relative',
            maxWidth: '64rem',
            margin: '0 auto',
            padding: '4px',
            borderRadius: '1rem',
            background: `linear-gradient(to bottom, var(--dashboard-border), transparent)`,
            boxShadow: '0 40px 80px rgba(0,0,0,0.3)',
          }}
        >
          <div
            style={{
              background: 'transparent',
              borderRadius: 'calc(1rem - 4px)',
              overflow: 'hidden',
              border: `1px solid var(--border-subtle)`,
            }}
          >
            <img
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuDr2dD-4DYN3QQBtR8avOu0rXOwo4Koe55gHFX7UtbcB4Ezsx9qGI5J6avwW94q-PJKDlI4FImklmxNCUle8mUxiWssXRgJg4ebLGzPvDc8rU_iyMLPt9WtvuU_SCNiyaYONBTjgxGsobxUxKGkWvUlidy1R9Ne6IqJcZ7AWYFMquco-g-ydjgdq9DQoVRTrhsX2KdaDiXu146vfdB6CC-Fv1cFybTUnCcXhZSqN_j-yzudPBRQkELoakmOAYTOQrbN8joNjneJR-Q"
              alt="FakeShield Dashboard"
              style={{ 
                width: '100%', 
                height: 'auto', 
                transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)', 
                display: 'block',
                transform: 'scale(1.05) translateY(-1%)'
              }}
            />
          </div>
          {/* Floating glows - moved behind and adjusted */}
          <div
            style={{
              position: 'absolute',
              bottom: '-4rem',
              right: '-4rem',
              width: 'min(24rem, 70vw)',
              height: 'min(24rem, 70vw)',
              background: 'radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, transparent 70%)',
              borderRadius: '50%',
              filter: 'blur(80px)',
              pointerEvents: 'none',
              zIndex: -1,
            }}
          />
          <div
            style={{
              position: 'absolute',
              top: '-4rem',
              left: '-4rem',
              width: 'min(24rem, 70vw)',
              height: 'min(24rem, 70vw)',
              background: 'radial-gradient(circle, rgba(0, 229, 204, 0.3) 0%, transparent 70%)',
              borderRadius: '50%',
              filter: 'blur(80px)',
              pointerEvents: 'none',
              zIndex: -1,
            }}
          />
        </div>
      </div>
    </header>
  );
};

export default HeroSection;
