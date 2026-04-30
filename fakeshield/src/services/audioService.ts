const API_BASE = "http://localhost:8001/api/v1/audio";

export interface AudioSignalScores {
  wavlm:    number;
  wav2vec:  number;
  spectral: number;
  prosody:  number;
  speaker:  number;
  codec:    number;
}

export interface AudioTimelineSegment {
  segment:    number;
  start_sec:  number;
  end_sec:    number;
  ai_score:   number;
  level:      "low" | "medium" | "high" | "critical";
  signals:    AudioSignalScores;
}

export interface AudioReason {
  signal:   string;
  severity: string;
  message:  string;
  evidence: string;
  score:    number;
}

export interface AudioMetadata {
  duration_sec:    number;
  num_chunks:      number;
  format_hint:     string;
  file_size_bytes: number;
}

export interface WavLMDetail {
  max?: number;
  var?: number;
  model?: string;
  reason?: string;
}

export interface Wav2VecDetail {
  max_chunk_score?: number;
  min_chunk_score?: number;
  score_variance?: number;
  chunks_analyzed?: number;
  ai_label_index?: number;
  reason?: string;
}

export interface ProsodyDetail {
  f0_std_semitones?: number;
  f0_range_semitones?: number;
  f0_kurtosis?: number;
  rhythm_ioi_cv?: number;
  pause_cv?: number;
  speaking_rate_variance?: number;
  voiced_frame_count?: number;
  reason?: string;
}

export interface SpeakerDetail {
  mean_sim?: number;
  std_sim?: number;
  min_sim?: number;
  identity_jumps?: number;
  is_unnatural_constancy?: boolean;
  is_identity_drift?: boolean;
  reason?: string;
}

export interface SpectralDetail {
  mfcc_delta_std?: number;
  flatness_variance?: number;
  flatness_mean?: number;
  hf_energy_ratio?: number;
  lf_energy_ratio?: number;
  centroid_variance?: number;
  mel_frame_diff?: number;
  global_score?: number;
  chunk_mean?: number;
  reason?: string;
}

export interface CodecDetail {
  snr_proxy_db?: number;
  dc_offset?: number;
  spectral_ripple_peaks?: number;
  enf_strength?: number;
  near_clip_ratio?: number;
  lp_residual_variance?: number;
  sub_scores?: {
    snr?: number;
    dc_offset?: number;
    spectral_ripple?: number;
    enf?: number;
    clipping?: number;
    dithering?: number;
  };
  reason?: string;
}

export interface RobustnessReport {
  stability_score: number;
  is_stable: boolean;
  scores: {
    original: number;
    telephony: number;
    compressed: number;
  };
  max_delta: number;
  variance: number;
}

export interface AudioResult {
  verdict:             string;
  threat_level:        "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  ai_probability:      number;
  confidence:          "LOW" | "MEDIUM" | "HIGH";
  agreement:           string;
  fusion_rule:         string;
  forensic_summary:    string;
  recommended_action:  string;
  primary_reasons:     AudioReason[];
  supporting_reasons:  AudioReason[];
  exonerating_factors: string[];
  audio_metadata:      AudioMetadata;
  timeline:            AudioTimelineSegment[];
  signal_scores:       AudioSignalScores;
  stability_score:     number;
  stability_report:    RobustnessReport;
  signal_details: {
    wavlm:    WavLMDetail;
    wav2vec:  Wav2VecDetail;
    spectral: SpectralDetail;
    prosody:  ProsodyDetail;
    speaker:  SpeakerDetail;
    codec:    CodecDetail;
  };
}

// Allowed MIME types and extensions
const ALLOWED_EXTENSIONS = ["wav", "mp3", "flac", "ogg", "m4a", "mp4"];

function getFileExtension(filename: string): string {
  const parts = filename.split(".");
  return parts.length > 1 ? parts[parts.length - 1].toLowerCase() : "";
}

export function isValidAudioFile(file: File): { valid: boolean; error?: string } {
  const ext = getFileExtension(file.name);
  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    return { valid: false, error: `Unsupported format ".${ext}". Supported: WAV, MP3, FLAC, OGG, M4A` };
  }
  if (file.size > 50 * 1024 * 1024) {
    return { valid: false, error: "File too large. Maximum 50MB." };
  }
  if (file.size === 0) {
    return { valid: false, error: "File is empty." };
  }
  return { valid: true };
}

export async function analyzeAudioAsync(
  file: File,
  onProgress?: (status: string) => void
): Promise<AudioResult> {
  // Validate before upload
  const validation = isValidAudioFile(file);
  if (!validation.valid) {
    throw new Error(validation.error);
  }

  // Step 1: Upload
  onProgress?.("Uploading audio for forensic scanning...");
  const formData = new FormData();
  // Append with explicit filename to ensure server receives it
  formData.append("file", file, file.name);

  let submitRes: Response;
  try {
    submitRes = await fetch(`${API_BASE}/analyze/async`, {
      method: "POST",
      body:   formData,
      // Do NOT set Content-Type header — browser sets it with boundary automatically
    });
  } catch (networkErr: any) {
    throw new Error(`Cannot reach forensic backend at ${API_BASE}. Is the server running? (${networkErr.message})`);
  }

  if (!submitRes.ok) {
    let errDetail = `Upload failed (HTTP ${submitRes.status})`;
    try {
      const errBody = await submitRes.json();
      errDetail = errBody.detail || errDetail;
    } catch {
      try {
        errDetail = await submitRes.text() || errDetail;
      } catch { /* ignore */ }
    }
    throw new Error(errDetail);
  }

  const submitData = await submitRes.json();
  const job_id: string = submitData.job_id;

  if (!job_id) {
    throw new Error("Server did not return a job ID. Check backend logs.");
  }

  // Step 2: Poll for completion
  const messages = [
    "Running WavLM in-the-wild deepfake classifier...",
    "Running Wav2Vec2 ASVspoof classifier...",
    "Analyzing spectral artifacts & MFCCs...",
    "Computing prosody & rhythmic regularity...",
    "Measuring intra-speaker identity drift...",
    "Scanning for codec & resampling signatures...",
    "Running robustness stress-test...",
    "Fusing signals with adaptive engine...",
    "Building temporal forensic timeline...",
    "Generating human-readable explanations...",
  ];
  let msgIdx = 0;

  return new Promise((resolve, reject) => {
    let solved = false;

    const interval = setInterval(async () => {
      if (solved) return;
      try {
        onProgress?.(messages[msgIdx % messages.length]);
        msgIdx++;

        const statusRes = await fetch(`${API_BASE}/status/${job_id}`);

        if (!statusRes.ok) {
          if (statusRes.status === 404) {
            // Job expired or doesn't exist
            solved = true;
            clearInterval(interval);
            reject(new Error("Analysis job not found on server. Please try again."));
            return;
          }
          // Transient error — keep polling
          return;
        }

        const status = await statusRes.json();

        if (status.status === "complete") {
          solved = true;
          clearInterval(interval);
          if (!status.result) {
            reject(new Error("Server returned empty result. Check backend logs."));
            return;
          }
          resolve(status.result as AudioResult);
        } else if (status.status === "error") {
          solved = true;
          clearInterval(interval);
          reject(new Error(status.error || "Backend analysis failed. Check server logs."));
        }
        // status "processing" → keep polling
      } catch (e: any) {
        // Network error during polling — don't abort, just log and retry
        console.warn("Poll attempt failed, retrying:", e?.message);
      }
    }, 2500);

    // Timeout after 180s — audio forensics with multiple models can take time
    setTimeout(() => {
      if (!solved) {
        solved = true;
        clearInterval(interval);
        reject(new Error("Audio forensic analysis timed out after 3 minutes. The file may be too long or server is overloaded."));
      }
    }, 180000);
  });
}
