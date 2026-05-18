import subprocess
import json
import os

class VideoMetadataForensics:
    """Scans video containers for AI generator markers and metadata anomalies."""
    
    _AI_MARKERS = [
        "sora", "runway", "luma", "pika", "heygen", "synthesia", 
        "d-id", "kling", "vidu", "gen-2", "gen-3", "stable video", 
        "dream machine", "cogvideo", "flux", "topaz"
    ]

    def get_metadata(self, video_path: str) -> dict:
        """Extracts container metadata using ffprobe."""
        try:
            cmd = [
                "ffprobe", "-v", "quiet", 
                "-print_format", "json", 
                "-show_format", "-show_streams", 
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            
            fmt = data.get("format", {})
            tags = fmt.get("tags", {})
            
            # Look for AI software in tags
            ai_score = 0.0
            found_markers = []
            
            # Check 'encoder', 'software', 'comment', 'description'
            search_fields = ["encoder", "software", "comment", "description", "title", "producer"]
            for field in search_fields:
                val = str(tags.get(field, "")).lower()
                for marker in self._AI_MARKERS:
                    if marker in val:
                        ai_score = 0.98
                        found_markers.append(f"{field}: {marker}")

            # Check for missing typical metadata
            # Real mobile videos usually have 'com.apple.quicktime' or 'android' tags
            is_mobile = any("apple" in str(v).lower() or "android" in str(v).lower() for v in tags.values())
            
            return {
                "tags": tags,
                "ai_score": ai_score,
                "markers": found_markers,
                "is_mobile_likely": is_mobile,
                "format_name": fmt.get("format_name"),
                "bit_rate": fmt.get("bit_rate")
            }
        except Exception as e:
            print(f"[VideoMetadata] Failed to probe {video_path}: {e}")
            return {"ai_score": 0.0, "markers": [], "error": str(e)}

    def check_c2pa(self, video_path: str) -> dict:
        """Check for C2PA manifest in the video container (supported formats)."""
        try:
            import c2pa
        except ImportError:
            return {"has_c2pa": False, "error": "c2pa library not installed"}
            
        try:
            # Note: c2pa-python support for video is evolving.
            # Determine mime from extension
            ext = os.path.splitext(video_path)[1].lower()
            mime = "video/mp4"
            if ext == ".mov": mime = "video/quicktime"
            elif ext == ".avi": mime = "video/x-msvideo"
            
            with open(video_path, "rb") as f:
                reader = c2pa.Reader(mime, f)
                manifest = reader.json()
                if manifest:
                    m_data = json.loads(manifest)
                    is_ai = "c2pa.genai" in manifest.lower() or "generative" in manifest.lower()
                    return {
                        "has_c2pa": True, 
                        "is_ai": is_ai, 
                        "manifest": m_data
                    }
        except Exception:
            pass # Most videos won't have it
            
        return {"has_c2pa": False}
