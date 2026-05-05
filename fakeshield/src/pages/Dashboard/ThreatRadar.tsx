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

    const scale = window.devicePixelRatio || 1;
    const width = parent.clientWidth;
    const height = (parent.clientHeight || 220);
    
    canvas.width = width * scale;
    canvas.height = height * scale;
    ctx.scale(scale, scale);

    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.38;

    const drawRadar = () => {
      ctx.clearRect(0, 0, width, height);
      
      const style = getComputedStyle(document.body);
      const accentCyan = '#00E5CC';
      const accentRed = '#ef4444';
      const borderSubtle = theme === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
      const textMuted = theme === 'dark' ? '#64748b' : '#94a3b8';

      // 1. Technical Grid (Human-engineered look)
      ctx.strokeStyle = borderSubtle;
      ctx.lineWidth = 0.5;
      ctx.setLineDash([2, 2]); // Dashed lines for a technical look

      // Circles with labels
      ctx.font = '7px "JetBrains Mono", monospace';
      ctx.fillStyle = textMuted;
      ctx.textAlign = 'center';

      for (let i = 1; i <= 4; i++) {
        const r = (radius / 4) * i;
        ctx.beginPath();
        ctx.arc(centerX, centerY, r, 0, Math.PI * 2);
        ctx.stroke();
        
        // Scale labels
        ctx.fillText(`${i * 25}%`, centerX, centerY - r + 8);
      }
      ctx.setLineDash([]); // Reset

      // Axes with crosshairs
      const axesCount = 6;
      for (let i = 0; i < axesCount; i++) {
        const angle = (Math.PI * 2 / axesCount) * i - Math.PI / 2;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX + Math.cos(angle) * radius, centerY + Math.sin(angle) * radius);
        ctx.stroke();

        // Axis ticks
        for (let j = 1; j <= 4; j++) {
            const tr = (radius / 4) * j;
            const tx = centerX + Math.cos(angle) * tr;
            const ty = centerY + Math.sin(angle) * tr;
            ctx.beginPath();
            ctx.moveTo(tx - 2, ty);
            ctx.lineTo(tx + 2, ty);
            ctx.stroke();
        }
      }

      // 2. Data Mapping (Precise Polygon)
      const dataPoints = [0.85, 0.62, 0.45, 0.78, 0.34, 0.92]; // Specific forensic signals
      
      // Shadow/Glow area
      ctx.beginPath();
      ctx.fillStyle = 'rgba(0, 229, 204, 0.1)';
      for (let i = 0; i <= axesCount; i++) {
        const val = dataPoints[i % axesCount];
        const angle = (Math.PI * 2 / axesCount) * i - Math.PI / 2;
        const x = centerX + Math.cos(angle) * (radius * val);
        const y = centerY + Math.sin(angle) * (radius * val);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.fill();

      // Main line
      ctx.beginPath();
      ctx.strokeStyle = accentCyan;
      ctx.lineWidth = 1.5;
      for (let i = 0; i <= axesCount; i++) {
        const val = dataPoints[i % axesCount];
        const angle = (Math.PI * 2 / axesCount) * i - Math.PI / 2;
        const x = centerX + Math.cos(angle) * (radius * val);
        const y = centerY + Math.sin(angle) * (radius * val);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      // 3. Data Vertices (The "Programmer" touch)
      dataPoints.forEach((val, i) => {
        const angle = (Math.PI * 2 / axesCount) * i - Math.PI / 2;
        const x = centerX + Math.cos(angle) * (radius * val);
        const y = centerY + Math.sin(angle) * (radius * val);

        // Dot
        ctx.beginPath();
        ctx.fillStyle = val > 0.7 ? accentRed : accentCyan;
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fill();

        // Coordinate Label
        ctx.font = 'bold 8px monospace';
        ctx.fillStyle = val > 0.7 ? accentRed : textMuted;
        ctx.fillText(val.toFixed(2), x + 10, y - 5);
      });

      // 4. Center Crosshair
      ctx.strokeStyle = accentCyan;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(centerX - 5, centerY); ctx.lineTo(centerX + 5, centerY);
      ctx.moveTo(centerX, centerY - 5); ctx.lineTo(centerX, centerY + 5);
      ctx.stroke();
    };

    drawRadar();

    const handleResize = () => {
      const newWidth = parent.clientWidth;
      const newHeight = (parent.clientHeight || 220);
      canvas.width = newWidth * scale;
      canvas.height = newHeight * scale;
      ctx.scale(scale, scale);
      drawRadar();
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, [theme]);

  const labels = [
    { text: 'IMG-GRID', top: '2%', left: '50%', color: 'var(--text-heading)' },
    { text: 'AUD-SPEC', top: '25%', left: '85%', color: 'var(--text-secondary)' },
    { text: 'VID-MESH', top: '75%', left: '85%', color: 'var(--text-secondary)' },
    { text: 'TXT-LLM', top: '95%', left: '50%', color: 'var(--text-heading)' },
    { text: 'META-V04', top: '75%', left: '15%', color: 'var(--text-secondary)' },
    { text: 'RPPG-SIG', top: '25%', left: '15%', color: 'var(--accent-red)' },
  ];

  return (
    <div className="flex-1 relative flex items-center justify-center w-full h-full min-h-[220px]">
      <canvas ref={canvasRef} className="w-full h-full" />
      
      {/* Technical Labels */}
      {labels.map((label, idx) => (
        <div 
          key={idx}
          className="absolute flex flex-col items-center pointer-events-none"
          style={{ 
            top: label.top, 
            left: label.left, 
            transform: 'translate(-50%, -50%)',
          }}
        >
          <span className="text-[10px] font-mono font-bold tracking-widest whitespace-nowrap" style={{ color: label.color }}>
            {label.text}
          </span>
          <div className="w-1 h-1 bg-[var(--panel-border)] rounded-full mt-1"></div>
        </div>
      ))}

      {/* Decorative corner indicators */}
      <div className="absolute top-2 left-2 w-4 h-4 border-t border-l border-[var(--panel-border)]"></div>
      <div className="absolute top-2 right-2 w-4 h-4 border-t border-r border-[var(--panel-border)]"></div>
      <div className="absolute bottom-2 left-2 w-4 h-4 border-b border-l border-[var(--panel-border)]"></div>
      <div className="absolute bottom-2 right-2 w-4 h-4 border-b border-r border-[var(--panel-border)]"></div>
    </div>
  );
};

export default ThreatRadar;
