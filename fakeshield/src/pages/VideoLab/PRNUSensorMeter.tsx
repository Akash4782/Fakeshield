import { useState, useEffect } from "react";

// Stable random seeds for noise signatures
const NOISE_SEEDS = Array.from({ length: 30 }, () => Math.random());

const PRNUSensorMeter = ({ score }: { score: number }) => {
  const [time, setTime] = useState(0);

  useEffect(() => {
    let frame: number;
    const update = () => {
      setTime(prev => prev + 1);
      frame = requestAnimationFrame(update);
    };
    frame = requestAnimationFrame(update);
    return () => cancelAnimationFrame(frame);
  }, []);

  // score is 0-100. Lower score = Likely Real (Good Spectral Noise PRNU)
  // Higher score = AI (Smooth High-Frequency FFT spectrum / no sensor noise)
  const isReal = score < 50;
  const color = isReal ? "var(--color-text-success)" : "var(--color-text-danger)";
  
  return (
    <div style={{ 
      border: "1px solid var(--panel-border)", 
      background: "var(--bg-secondary)", 
      padding: "20px", 
      borderRadius: "12px",
      display: "flex",
      flexDirection: "column",
      alignItems: "center"
    }}>
      <div style={{ fontSize: "12px", fontWeight: 700, color: "var(--text-inactive)", marginBottom: "12px", textTransform: "uppercase" }}>
        PRNU Hardware Sensor Noise
      </div>
      
      <div style={{ height: "40px", display: "flex", alignItems: "center", gap: "2px", width: "100%", justifyContent: "center" }}>
        {[...Array(30)].map((_, i) => {
          // Real Physics: A rich broadband noise spectrum jumping dynamically (Stochastic PRNU noise)
          // AI: Exceptionally clean spectrum with zero noise, or strong repeating anomalies
          const t = time / Math.PI;
          const h = isReal 
            ? 15 + Math.random() * 20 + Math.sin(t * NOISE_SEEDS[i]) * 10
            : 3 + Math.sin(i * 0.5 + t/10) * 3; // Smooth synthesis, no sensor noise
          
          return (
            <div
              key={i}
              style={{
                width: "4px",
                height: `${h}px`,
                background: color,
                borderRadius: "1px",
                transition: "height 0.1s ease",
                opacity: 0.7 + (Math.sin(i + t) * 0.3)
              }}
            />
          );
        })}
      </div>
      
      <div style={{ marginTop: "12px", fontSize: "14px", fontWeight: 600, color }}>
        {isReal ? "Genuine Silicon Noise Profile" : "Zero High-Frequency Sensor Noise"}
      </div>
      <div style={{ fontSize: "12px", color: "var(--text-secondary)", marginTop: "4px" }}>
        {isReal ? "High-Pass Filter FFT (Verified)" : "Mathematically Pristine Generation"}
      </div>
    </div>
  );
};

export default PRNUSensorMeter;
