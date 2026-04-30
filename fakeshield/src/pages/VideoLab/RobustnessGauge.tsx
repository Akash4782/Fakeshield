interface RobustnessData {
  original_score: number;
  compressed_score: number;
  jpeg_quality: number;
  frames_tested: number;
}

const RobustnessGauge = ({ data }: { data: RobustnessData }) => {
  if (!data?.original_score) return null;
  
  const original = data.original_score * 100;
  const compressed = data.compressed_score * 100;
  const delta = Math.abs(original - compressed);
  
  // High delta = Brittle (Potential False Positive or AI weakness)
  // Low delta = Resilient (Solid Forensic Detection)
  const isResilient = delta < 15;
  const color = isResilient ? "var(--color-text-info)" : "var(--color-text-warning)";
  
  return (
    <div style={{ 
      border: "1px solid var(--panel-border)", 
      background: "var(--bg-secondary)", 
      padding: "20px", 
      borderRadius: "12px",
    }}>
      <div style={{ fontSize: "12px", fontWeight: 700, color: "var(--text-inactive)", marginBottom: "12px", textTransform: "uppercase" }}>
        Compression Stability
      </div>
      
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: "14px", marginBottom: "8px" }}>
        <span style={{ color: "var(--text-secondary)" }}>Stability Index</span>
        <span style={{ fontWeight: 700, color }}>{((1 - delta/100) * 100).toFixed(0)}%</span>
      </div>
      
      <div style={{ height: "8px", borderRadius: "4px", background: "var(--color-border-tertiary)", overflow: "hidden" }}>
        <div style={{
          height: "100%",
          width: `${(1 - delta/100) * 100}%`,
          background: color,
          borderRadius: "4px",
          transition: "width 0.6s ease"
        }} />
      </div>
      
      <div style={{ marginTop: "12px", fontSize: "13px", color: "var(--text-secondary)" }}>
        Analysis performed at JPEG {data.jpeg_quality} quality. Forensic verdict remained {isResilient ? "stable" : "volatile"} across {data.frames_tested} stress frames.
      </div>
    </div>
  );
};

export default RobustnessGauge;
