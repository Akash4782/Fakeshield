import io
import json
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure the backend directory is in the path
sys.path.append(os.getcwd())

# Mock c2pa library since it might have binary dependencies not easily testable in all environments
mock_c2pa = MagicMock()
sys.modules['c2pa'] = mock_c2pa

# Mocking heavy AI model loading to speed up tests
with patch('app.models.image_detector.load_image_models', return_value=None):
    from app.models.image_detector import sig_c2pa, analyze_image
    from PIL import Image

class TestC2PAIntegration(unittest.TestCase):
    def setUp(self):
        # Create a dummy JPEG image
        img = Image.new('RGB', (100, 100), color=(73, 109, 137))
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        self.dummy_bytes = buf.getvalue()

    def test_sig_c2pa_ai_detected(self):
        """Test that sig_c2pa correctly identifies an AI image from a manifest."""
        mock_manifest = {
            "active_manifest": "m1",
            "manifests": {
                "m1": {
                    "title": "DALL-E 3 Generated Image",
                    "claim_generator": "OpenAI DALL-E 3",
                    "assertions": [
                        {"label": "c2pa.genai", "data": {}}
                    ]
                }
            }
        }
        mock_c2pa.Reader.return_value.json.return_value = json.dumps(mock_manifest)

        is_ai, reason, meta = sig_c2pa(self.dummy_bytes)
        
        self.assertTrue(is_ai)
        self.assertIn("GenAI assertion", reason)
        self.assertEqual(meta["generator"], "OpenAI DALL-E 3")

    def test_sig_c2pa_no_manifest(self):
        """Test that sig_c2pa returns false when no manifest is found."""
        mock_c2pa.Reader.return_value.json.return_value = None
        
        is_ai, reason, meta = sig_c2pa(self.dummy_bytes)
        
        self.assertFalse(is_ai)
        self.assertIsNone(reason)
        self.assertEqual(meta, {})

    @patch('app.models.image_detector.sig_gemini_watermark')
    @patch('app.models.image_detector.sig_tampered_watermark')
    def test_analyze_image_c2pa_short_circuit(self, mock_tamper, mock_gemini):
        """Test that analyze_image short-circuits when C2PA AI is detected."""
        mock_gemini.return_value = (False, None)
        mock_tamper.return_value = (False, None)
        
        # Mock C2PA AI detection
        mock_manifest = {
            "active_manifest": "m1",
            "manifests": {
                "m1": {
                    "title": "AI Image",
                    "claim_generator": "Adobe Firefly",
                    "assertions": [{"label": "c2pa.genai"}]
                }
            }
        }
        mock_c2pa.Reader.return_value.json.return_value = json.dumps(mock_manifest)
        
        result = analyze_image(self.dummy_bytes)
        
        self.assertEqual(result["verdict"], "AI GENERATED")
        self.assertEqual(result["ai_probability"], 1.0)
        self.assertEqual(result["confidence"], 100.0)
        self.assertIn("C2PA GenAI assertion found", result["reasons"][0])
        self.assertEqual(result["metadata"]["software"], "Adobe Firefly")

if __name__ == '__main__':
    unittest.main()
