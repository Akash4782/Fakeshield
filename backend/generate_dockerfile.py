reqs = [line.strip() for line in open('requirements.txt').readlines() if line.strip() and not line.startswith('#')]

base_dockerfile = '''# Use an official Python runtime as a parent image
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \\
    PYTHONUTF8=1 \\
    PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \\
    FAKESHIELD_SKIP_WARMUP=0

WORKDIR /app

RUN apt-get update && apt-get install -y \\
    build-essential \\
    cmake \\
    libgl1-mesa-glx \\
    libglib2.0-0 \\
    libsndfile1 \\
    ffmpeg \\
    libmagic1 \\
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

'''

runs = '\n'.join([f"RUN pip install --no-cache-dir '{req}'" for req in reqs])

end_dockerfile = '''
COPY . .
EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
'''

with open('Dockerfile', 'w') as f:
    f.write(base_dockerfile + runs + end_dockerfile)
