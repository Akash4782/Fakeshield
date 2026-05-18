import threading

# Global lock to prevent race conditions during parallel Transformer model loading.
# This ensures only one model is being initialized at a time, protecting 
# against "meta tensor" crashes when accelerate is installed.
MODEL_LOAD_LOCK = threading.Lock()
