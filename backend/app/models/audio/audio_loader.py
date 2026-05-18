# audio_loader.py
"""
Audio loading, normalization, Voice Activity Detection, and chunking.
VAD is critical — silence segments will fool every signal if included.
"""
import numpy as np
import librosa
import soundfile as sf
import io
from dataclasses import dataclass


TARGET_SR = 16000  # all models expect 16kHz
CHUNK_SEC = 5.0    # analyse in 5-second chunks for timeline


@dataclass
class AudioData:
    waveform: np.ndarray   # float32, mono, 16kHz
    sr: int
    duration_sec: float
    num_chunks: int
    chunks: list           # list of np.ndarray (5s each)
    chunk_times: list      # list of (start_sec, end_sec) tuples
    format_hint: str       # "wav", "mp3", "flac", etc.
    file_size_bytes: int


def load_audio(audio_bytes: bytes, filename: str = "audio.wav") -> AudioData:
    """
    Load audio from bytes. Handles wav, mp3, flac, ogg, m4a.
    Resamples to 16kHz mono. Returns AudioData with chunks.
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "wav"
    
    try:
        # Try soundfile first (lossless formats)
        buf = io.BytesIO(audio_bytes)
        y, sr = sf.read(buf, dtype="float32", always_2d=False)
        
        # Convert stereo to mono
        if y.ndim > 1:
            y = y.mean(axis=1)
    
    except Exception:
        # Fall back to librosa (handles mp3, m4a via ffmpeg)
        buf = io.BytesIO(audio_bytes)
        try:
            y, sr = librosa.load(buf, sr=None, mono=True)
        except Exception as e:
            raise ValueError(f"Cannot decode audio: {e}")
    
    # Resample to 16kHz
    if sr != TARGET_SR:
        y = librosa.resample(y, orig_sr=sr, target_sr=TARGET_SR)
        sr = TARGET_SR
    
    # Peak normalize (prevent clipping issues)
    peak = np.max(np.abs(y))
    if peak > 0:
        y = y / peak * 0.95
    
    # Voice Activity Detection — remove silent sections
    y_voiced, voice_segments = _apply_vad(y, sr)
    
    duration = len(y_voiced) / sr
    
    # Chunk into fixed-size windows
    chunks, chunk_times = _make_chunks(y_voiced, sr, CHUNK_SEC, voice_segments)
    
    return AudioData(
        waveform=y_voiced,
        sr=sr,
        duration_sec=round(duration, 2),
        num_chunks=len(chunks),
        chunks=chunks,
        chunk_times=chunk_times,
        format_hint=ext,
        file_size_bytes=len(audio_bytes),
    )


def _apply_vad(y: np.ndarray, sr: int) -> tuple[np.ndarray, list]:
    """
    Simple energy-based Voice Activity Detection.
    Removes frames below energy threshold.
    Returns voiced-only waveform and segment timestamps.
    """
    frame_len = int(sr * 0.025)   # 25ms frames
    hop_len   = int(sr * 0.010)   # 10ms hop
    
    # RMS energy per frame
    frames = librosa.util.frame(y, frame_length=frame_len, hop_length=hop_len)
    rms = np.sqrt(np.mean(frames ** 2, axis=0))
    
    # Threshold: 15% of mean RMS
    threshold = np.mean(rms) * 0.15
    voiced_mask = rms > threshold
    
    # Reconstruct voiced-only signal
    voiced_chunks = []
    segments = []
    
    i = 0
    while i < len(voiced_mask):
        if voiced_mask[i]:
            j = i
            while j < len(voiced_mask) and voiced_mask[j]:
                j += 1
            
            start_sample = i * hop_len
            end_sample   = min(j * hop_len + frame_len, len(y))
            
            voiced_chunks.append(y[start_sample:end_sample])
            segments.append((start_sample / sr, end_sample / sr))
            i = j
        else:
            i += 1
    
    if not voiced_chunks:
        return y, [(0.0, len(y) / sr)]
    
    return np.concatenate(voiced_chunks), segments


def _make_chunks(
    y: np.ndarray,
    sr: int,
    chunk_sec: float,
    voice_segments: list,
) -> tuple[list, list]:
    """Split waveform into fixed-size chunks for timeline analysis."""
    chunk_size = int(chunk_sec * sr)
    chunks = []
    times = []
    
    offset = 0
    seg_idx = 0
    
    for i in range(0, len(y), chunk_size):
        chunk = y[i:i + chunk_size]
        if len(chunk) < sr * 0.5:  # skip chunks shorter than 0.5s
            continue
        
        # Pad last chunk if needed
        if len(chunk) < chunk_size:
            chunk = np.pad(chunk, (0, chunk_size - len(chunk)))
        
        # Approximate real timestamp from voice segments
        start_t = voice_segments[min(seg_idx, len(voice_segments)-1)][0] if voice_segments else i / sr
        end_t   = start_t + chunk_sec
        
        chunks.append(chunk)
        times.append((round(start_t, 2), round(end_t, 2)))
        seg_idx = min(seg_idx + 1, len(voice_segments) - 1)
    
    return chunks, times
