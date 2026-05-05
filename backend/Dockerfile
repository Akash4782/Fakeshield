# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONUTF8=1 \
    PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
    FAKESHIELD_SKIP_WARMUP=0

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for OpenCV and Audio processing
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose the port Hugging Face expects (7860)
EXPOSE 7860

# Command to run the application
# We use host 0.0.0.0 and port 7860 as required by Hugging Face
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
