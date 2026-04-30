const API_BASE = "http://localhost:8001/api/v1/text";

export interface SignalScores {
  binoculars:     number;
  classifier:     number;
  stylometry:     number;
  retrieval:      number;
  statistical:    number;
  lexical:        number;
  human_shield:   number;
  reasoning:      string;
}

export interface StructuralDetails {
  avg_depth:          number;
  depth_variance:     number;
  structural_entropy: number;
  sentence_cadence_cv: number;
}

export interface SemanticDetails {
  semantic_consistency:   number;
  drift_variance:         number;
  trajectory_smoothness:  string;
}

export interface SentenceHighlight {
  sentence:  string;
  ai_score:  number | null;
  perplexity: number;
  label:     "AI" | "LIKELY_AI" | "UNCERTAIN" | "HUMAN" | "too_short";
}

export interface LinguisticProfile {
  syntactic_complexity:  string;
  lexical_diversity:     string;
  pacing_consistency:    string;
  entropy_bits_per_char: number;
  burstiness_raw:        number;
}

export interface TextResult {
  scan_id:             string;
  verdict:             string;
  threat_level:        "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  score:               number; // aggregate
  confidence:          string; // e.g. "HIGH"
  confidence_level:    string;
  signals:             SignalScores;
  structural_details:  StructuralDetails;
  semantic_details:    SemanticDetails;
  linguistic_profile:  LinguisticProfile;
  sentence_highlights: SentenceHighlight[];
  indicators:          string[];
  forensic_reasoning?: string;
  word_count:          number;
  processing_time:     string;
  rule_applied?:       string;
  engine_version:      string;
}

// ── Async scan with polling ───────────────────────────────────
export async function scanTextAsync(
  text: string,
  onProgress?: (msg: string) => void
): Promise<TextResult> {

  onProgress?.("Initializing Forensic Engines...");
  const submitRes = await fetch(`${API_BASE}/analyze/async`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({
      text,
      include_highlights: true,
      mode: "deep"
    }),
  });

  if (!submitRes.ok) throw new Error("Submission failed");
  const { job_id } = await submitRes.json();

  // v10.1 Agentic Progress Messages
  const messages = [
    "Loading spaCy structural engine...",
    "Parsing dependency trees...",
    "Computing structural entropy...",
    "Loading mpnet-v2 semantic cross-encoders...",
    "Tracking thought flow trajectory...",
    "Computing semantic drift variance...",
    "Initializing Performer (Binoculars) engine...",
    "Performing statistical log-prob audit...",
    "Promoting to Gemini Reasoning Judge...",
    "Executing v10.1 Fusion logic...",
    "Compiling forensic dataset...",
  ];
  let msgIdx = 0;

  return new Promise((resolve, reject) => {
    const interval = setInterval(async () => {
      try {
        onProgress?.(messages[msgIdx % messages.length]);
        msgIdx++;

        const statusRes = await fetch(`${API_BASE}/status/${job_id}`);
        const status    = await statusRes.json();

        if (status.status === "complete") {
          clearInterval(interval);
          resolve(status.data as TextResult);
        } else if (status.status === "error") {
          clearInterval(interval);
          reject(new Error(status.data));
        }
      } catch (e) {
        clearInterval(interval);
        reject(e);
      }
    }, 2500);

    setTimeout(() => {
      clearInterval(interval);
      reject(new Error("Analysis timed out after 90 seconds (Deep Scan requires more time)"));
    }, 95000);
  });
}

// ── Direct sync scan (for backward compatibility) ─────────────
export async function scanTextSync(text: string): Promise<TextResult> {
  const res = await fetch(`${API_BASE}/analyze`, {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({
      text,
      include_highlights: true,
      mode: "deep"
    }),
  });
  if (!res.ok) throw new Error("Scan failed");
  const json = await res.json();
  return json.data as TextResult;
}

// ── PDF Forensic Report Export ────────────────────────────────
export async function downloadForensicReport(scanId: string): Promise<void> {
  const url = `${API_BASE}/report/${scanId}`;
  const response = await fetch(url);
  if (!response.ok) throw new Error("Could not generate report");
  
  const blob = await response.blob();
  const downloadUrl = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = downloadUrl;
  link.setAttribute('download', `fakeshield_${scanId}.pdf`);
  document.body.appendChild(link);
  link.click();
  link.remove();
}
