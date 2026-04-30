import React, { useEffect, useRef } from 'react';
import { useTheme } from '../../hooks/useTheme';

const ThreatRadar: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { theme } = useTheme();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const parent = canvas.parentElement;
    if (!parent) return;

    // Set canvas dimensions based on parent
    const width = parent.clientWidth * 2;
    const height = (parent.clientHeight || 220) * 2;
    canvas.width = width;
    canvas.height = height;
    ctx.scale(2, 2);

    const centerX = width / 4;
    const centerY = height / 4;
    const radius = 60;

    const drawRadar = () => {
      // Clear
      ctx.clearRect(0, 0, width, height);
      
      // Get CSS variables
      const style = getComputedStyle(document.body);
      const accentRed = style.getPropertyValue('--accent-red').trim() || '#FF2D55';
      const accentRedTrans = style.getPropertyValue('--accent-red-transparent').trim() || 'rgba(255, 45, 85, 0.2)';
      const panelBorder = style.getPropertyValue('--panel-border').trim() || 'rgba(255, 255, 255, 0.05)';

      // Background circles
      ctx.strokeStyle = panelBorder;
      ctx.lineWidth = 1;
      for (let i = 1; i <= 3; i++) {
        ctx.beginPath();
        ctx.arc(centerX, centerY, (radius / 3) * i, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Axes (6 for Text Forensics)
      const axes = 6;
      ctx.beginPath();
      for (let i = 0; i < axes; i++) {
        const angle = (Math.PI * 2 / axes) * i - Math.PI / 2;
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX + Math.cos(angle) * radius, centerY + Math.sin(angle) * radius);
      }
      ctx.stroke();

      // Data Shape (Simulating real text forensics output)
      // Indexes: 0=DeBERTa, 1=RoBERTa, 2=Perplexity, 3=Stylometric, 4=Consistency, 5=Repetition
      const values = [0.85, 0.72, 0.94, 0.35, 0.88, 0.40]; 
      
      ctx.beginPath();
      ctx.fillStyle = accentRedTrans;
      ctx.strokeStyle = accentRed;
      ctx.lineWidth = 2;

      for (let i = 0; i <= axes; i++) {
        const val = values[i % axes];
        const angle = (Math.PI * 2 / axes) * i - Math.PI / 2;
        const x = centerX + Math.cos(angle) * (radius * val);
        const y = centerY + Math.sin(angle) * (radius * val);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.fill();
      ctx.stroke();

      // Glow effect
      ctx.shadowBlur = theme === 'dark' ? 10 : 0;
      ctx.shadowColor = accentRed;
      ctx.stroke();
    };

    drawRadar();

    // Handle resizing
    const handleResize = () => {
      const newWidth = parent.clientWidth * 2;
      const newHeight = (parent.clientHeight || 220) * 2;
      canvas.width = newWidth;
      canvas.height = newHeight;
      ctx.scale(2, 2);
      drawRadar();
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [theme]);

  return (
    <div className="flex-1 relative flex items-center justify-center w-full h-full min-h-[220px]">
      <canvas ref={canvasRef} className="w-full h-full" />
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <span className="absolute top-2 text-[10px] text-[var(--accent-red)] font-bold">DEBERTA-V3</span>
        <span className="absolute bottom-2 text-[10px] font-bold" style={{ color: 'var(--text-secondary)' }}>STYLOMETRICS</span>
        <span className="absolute top-8 right-8 text-[10px] font-bold" style={{ color: 'var(--text-secondary)' }}>ROBERTA</span>
        <span className="absolute top-8 left-8 text-[10px] text-[var(--accent-red)] font-bold">REPETITION</span>
        <span className="absolute bottom-8 right-8 text-[10px] text-[var(--accent-red)] font-bold">PERPLEXITY</span>
        <span className="absolute bottom-8 left-8 text-[10px] font-bold" style={{ color: 'var(--text-secondary)' }}>CONSISTENCY</span>
      </div>
    </div>
  );
};

export default ThreatRadar;
