const API_BASE = "http://localhost:8001/api/v1/image";

export interface ImageAnalysisResponse {
  // Core verdict
  verdict: string;          // "AI GENERATED" | "UNCERTAIN" | "LIKELY HUMAN"
  threat_level: string;     // "CRITICAL" | "MEDIUM" | "LOW"
  confidence: number;       // 0-100 scale
  ai_probability: number;   // 0-1 scale

  // All 8 forensic signals (0-1 scale)
  signals: {
    rigid:      number;
    fft:        number;
    exif:       number;
    classifier: number;
    clip:       number;
    noise:      number;
    ela:        number;
    aug:        number;
  };

  // EXIF Metadata
  metadata: {
    camera: string;
    gps: string;
    lens: string;
    software: string;
    dimensions: string;
  };

  // Explainability
  reasons: string[];

  // Visualizations (base64 data URLs)
  fft_spectrum_url?: string;
  heatmap_url?: string;
  ela_image?: string;

  // Per-generator accuracy reference
  per_generator_accuracy?: Record<string, { accuracy: string; notes: string }>;

  processing_time: string;
  engine_version: string;
}

export async function analyzeImage(
  imageBase64: string,
  includeGradcam: boolean = true
): Promise<{ status: string; data: ImageAnalysisResponse }> {
  const response = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      image: imageBase64,
      include_gradcam: includeGradcam,
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || "Image analysis failed");
  }

  return response.json();
}
