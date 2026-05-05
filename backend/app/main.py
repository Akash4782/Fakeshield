import os
import sys
import io
import warnings

# 1. Environment & Protobuf Fixes (Must be at the absolute top)
try:
    import google.protobuf.runtime_version as rv
    rv.ValidateProtobufRuntimeVersion = lambda *args, **kwargs: None
except (ImportError, AttributeError):
    pass

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["PYTHONUTF8"] = "1"
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*The name tf.losses.*")
warnings.filterwarnings("ignore", message=".*use_fast is unset.*")
warnings.filterwarnings("ignore", message=".*does not have a fast version.*")
warnings.filterwarnings("ignore", message=".*Multiple distributions found for package optimum.*")

# 1.1 DLL Bypass: Block broken torchaudio at sys.modules level (WinError 127 fix)
# The AST feature extractor does `import torchaudio.compliance.kaldi` at module scope.
# On this Windows system, torchaudio's native DLL is broken. We insert dummy modules
# into sys.modules so the import succeeds silently, then tell transformers that
# torchaudio/speech is unavailable so it uses its built-in numpy fallback instead.
import types
import importlib.machinery as _ilm

def _block_torchaudio():
    """Prevent broken torchaudio DLL from crashing the process."""
    _dummy = types.ModuleType("torchaudio")
    _dummy.__version__ = "0.0.0"
    _dummy.__path__ = []
    _dummy.__file__ = "blocked_by_fakeshield"
    _dummy.__loader__ = None
    _dummy.__package__ = "torchaudio"
    _dummy.__spec__ = _ilm.ModuleSpec("torchaudio", None, origin="blocked")
    sys.modules["torchaudio"] = _dummy

    for _sub in [
        "torchaudio.functional", "torchaudio.transforms",
        "torchaudio.compliance", "torchaudio.compliance.kaldi",
        "torchaudio.sox_effects", "torchaudio.backend",
        "torchaudio._extension", "torchaudio._extension.utils",
    ]:
        _m = types.ModuleType(_sub)
        _m.__spec__ = _ilm.ModuleSpec(_sub, None, origin="blocked")
        _m.__path__ = []
        _m.__package__ = _sub.rsplit(".", 1)[0]
        sys.modules[_sub] = _m

# DLL Bypass: Attempt to import torchaudio. If it fails with a DLL error, apply the block.
try:
    import torchaudio
except OSError:
    _block_torchaudio()

# Patch transformers availability checks so AST uses numpy mel-filterbank path
try:
    import transformers.utils.import_utils as _tf_import_utils
    _tf_import_utils.is_torchaudio_available = lambda: False
    _tf_import_utils._torchaudio_available = False
    # is_speech_available checks torchaudio — must also be False
    if hasattr(_tf_import_utils, "is_speech_available"):
        _tf_import_utils.is_speech_available = lambda: False
except Exception:
    pass

# 2. Force UTF-8 encoding for Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except Exception:
        pass

def robust_print(msg, **kwargs):
    """Prints message while handling potential UnicodeEncodeErrors on legacy terminals."""
    try:
        print(msg, **kwargs)
    except UnicodeEncodeError:
        # Fallback: strip non-ascii
        clean_msg = msg.encode('ascii', 'ignore').decode('ascii')
        print(clean_msg, **kwargs)

# 3. Suppress Heavy Logging from AI Libraries
import transformers
transformers.logging.set_verbosity_error()

from dotenv import load_dotenv
load_dotenv()

import os
import importlib
import importlib.metadata
# importlib.metadata (already handled)
import sys

def _patch_metadata(mod):
    _orig_version = mod.version
    def _patched_version(pkg_name):
        try:
            v = _orig_version(pkg_name)
            if v: return v
        except Exception:
            pass
        
        name = pkg_name.lower()
        if name == "torch":
            try:
                import torch
                return torch.__version__.split('+')[0]
            except Exception: return "2.2.1"
        if name == "transformers": return "4.38.2"
        if name == "protobuf":     return "4.25.3"
        return "1.0.0"
    mod.version = _patched_version

_patch_metadata(importlib.metadata)

# Also patch importlib_metadata backport if it exists
try:
    import importlib_metadata
    _patch_metadata(importlib_metadata)
except ImportError:
    pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.text_router import router as text_router
from app.routers.image_router import router as image_router
from app.routers.video_router import router as video_router
from app.routers.audio_router import router as audio_router
from app.routers.auth_router import router as auth_router
from app.routers.dashboard_router import router as dashboard_router
# Forensic warm-up functions moved to background task to prevent startup hangs
# (Imports moved inside the task below)

app = FastAPI(
    title="FakeShield API",
    description="Industry-level multimodal deepfake detection",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text_router)
app.include_router(image_router)
app.include_router(video_router, prefix="/api/v1")
app.include_router(audio_router, prefix="/api/v1")
app.include_router(auth_router)
app.include_router(dashboard_router)

import asyncio

@app.on_event("startup")
async def startup_event():
    from app.database import init_db
    try:
        await init_db()
    except Exception as e:
        robust_print(f"[DB] Database initialization failed: {e}")
        robust_print("[DB] Proceeding in OFFLINE mode (history and users will be unavailable).")
    
    robust_print("[START] Initializing FakeShield Engine (Background Warmup Enabled)...", flush=True)
    async def run_universal_warmup():
        """Pre-loads all forensic labs in background to ensure zero-latency navigation."""
        if os.environ.get("FAKESHIELD_SKIP_WARMUP") == "1":
            robust_print("[WARMUP] Skipped by environment flag.")
            return
            
        # 1. Text Lab (v16 Elite)
        try:
            from app.models.new_forensic_engine import load_models as load_text_models
            robust_print("[WARMUP] [1/3] Pre-loading Text Forensic Suite...", flush=True)
            await asyncio.to_thread(load_text_models)
            robust_print("[WARMUP] Text Lab ready.", flush=True)
        except Exception as e:
            robust_print(f"[WARMUP] Text load error: {e}")
            
        # 2. Image Lab (DINOv2 + ViT Ensemble)
        try:
            from app.models.image_detector import load_image_models
            robust_print("[WARMUP] [2/3] Pre-loading Image Forensic Suite...", flush=True)
            await asyncio.to_thread(load_image_models)
            robust_print("[WARMUP] Image Lab ready.", flush=True)
        except Exception as e:
            robust_print(f"[WARMUP] Image load error: {e}")
 
        # 3. Audio Lab (WavLM ITW)
        try:
            from app.models.audio.signal_wavlm import _load_model as load_wavlm
            robust_print("[WARMUP] [3/3] Pre-loading Audio Forensic Suite...", flush=True)
            await asyncio.to_thread(load_wavlm)
            robust_print("[WARMUP] Audio Lab ready.", flush=True)
        except Exception as e:
            robust_print(f"[WARMUP] Audio load error: {e}")

        robust_print("="*50)
        robust_print("--- [ALL ENGINES WARMED UP] ---")
        robust_print("="*50)

    # Launch universal warmup in background
    asyncio.create_task(run_universal_warmup())
    robust_print("-" * 50, flush=True)
    robust_print("FakeShield API is now ONLINE and listening on port 8001.", flush=True)
    robust_print("-" * 50, flush=True)

@app.get("/")
def root():
    return {
        "project": "FakeShield",
        "version": "2.0.0",
        "docs":    "/docs",
        "panels":  ["text", "image", "audio", "video"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
