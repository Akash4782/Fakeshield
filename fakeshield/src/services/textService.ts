import { API_BASE_URL } from '../config';
const API_BASE = `${API_BASE_URL}/text`;

export interface SignalScores {
  neural:       number;
  statistical:  number;
  rhythm:       number;
  flow:         number;
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
  token: string | null = null,
  onProgress?: (msg: string) => void
): Promise<TextResult> {

  onProgress?.("Initializing Forensic Engines...");
  const submitRes = await fetch(`${API_BASE}/analyze/async`, {
    method:  "POST",
    headers: { 
      "Content-Type": "application/json",
      ...(token ? { "Authorization": `Bearer ${token}` } : {})
    },
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

        let statusRes;
        let retries = 3;
        while (retries > 0) {
          try {
            statusRes = await fetch(`${API_BASE}/status/${job_id}`, {
              headers: {
                ...(token ? { "Authorization": `Bearer ${token}` } : {})
              }
            });
            if (statusRes.ok) break;
            throw new Error(`HTTP ${statusRes.status}`);
          } catch (e) {
            retries--;
            if (retries === 0) throw e;
            await new Promise(r => setTimeout(r, 1000));
          }
        }

        const status = await statusRes.json();

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
      reject(new Error("Analysis timed out after 5 minutes. Initializing heavy AI models locally can take some time. Please try again."));
    }, 300000);
  });
}

// ── Direct sync scan (for backward compatibility) ─────────────
export async function scanTextSync(text: string, token: string | null = null): Promise<TextResult> {
  const res = await fetch(`${API_BASE}/analyze`, {
    method:  "POST",
    headers: { 
      "Content-Type": "application/json",
      ...(token ? { "Authorization": `Bearer ${token}` } : {})
    },
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
export async function downloadForensicReport(scanId: string, token: string | null = null): Promise<void> {
  const url = `${API_BASE}/report/${scanId}.pdf`;
  
  try {
    const res = await fetch(url, {
      headers: {
        ...(token ? { "Authorization": `Bearer ${token}` } : {})
      }
    });

    if (!res.ok) throw new Error("Failed to download report");

    const blob = await res.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.setAttribute('download', `FakeShield_Report_${scanId.substring(0, 8)}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.parentNode?.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);
  } catch (err) {
    console.error("Download error:", err);
    throw err;
  }
}
