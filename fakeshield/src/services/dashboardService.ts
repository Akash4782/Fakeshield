/**
 * dashboardService.ts
 * Saves scan results to MongoDB via the dashboard router.
 * Called by each lab after a successful analysis.
 */

import { API_BASE_URL } from '../config';

const API_BASE = `${API_BASE_URL}/dashboard`;

export interface SaveScanPayload {
  lab: 'text' | 'image' | 'audio' | 'video';
  filename: string;
  verdict: string;
  confidence: number;      // 0–1 or 0–100, we normalize to 0–1
  threat_level: string;
  scan_id: string;
  extra?: Record<string, unknown>;
}

/**
 * Save a completed scan result to the user's history in MongoDB.
 * Fails silently — never blocks the lab UI.
 */
export async function saveScanToHistory(token: string, payload: SaveScanPayload): Promise<void> {
  try {
    const normalized = {
      ...payload,
      // normalize confidence to 0–1
      confidence: payload.confidence > 1 ? payload.confidence / 100 : payload.confidence,
    };
    await fetch(`${API_BASE}/save`, {
      method:  'POST',
      headers: {
        'Content-Type':  'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(normalized),
    });
  } catch {
    // Silently ignore — the lab should still work even if history save fails
  }
}
