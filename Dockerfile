FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
    FAKESHIELD_SKIP_WARMUP=0

WORKDIR /app

# System dependencies (Adding build-essential for C extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsndfile1 \
    ffmpeg \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

# Step 1: Core Framework
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" python-multipart python-dotenv pydantic "pydantic-settings" email-validator motor "passlib[bcrypt]" PyJWT google-generativeai spacy && \
    python -m spacy download en_core_web_sm

# Step 2: Heavy ML Engines (CPU Only)
RUN pip install --no-cache-dir torch torchaudio torchvision --index-url https://download.pytorch.org/whl/cpu

# Step 3: Transformers & Scipy
RUN pip install --no-cache-dir transformers accelerate "sentence-transformers" scikit-learn numpy scipy

# Step 4: Image & Audio Utilities
RUN pip install --no-cache-dir Pillow piexif opencv-python-headless "soundfile>=0.12.0" "librosa>=0.10.0" "resampy>=0.4.2"

# Step 5: Isolate Pyannote (Very Heavy)
RUN pip install --no-cache-dir "pyannote.audio>=3.1.0"

# Step 6: Isolate C2PA (Might need build tools)
RUN pip install --no-cache-dir c2pa-python

# Step 7: Final Misc
RUN pip install --no-cache-dir "protobuf~=4.25.3" python-magic email-validator

# Step 8: Catch-all for requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
