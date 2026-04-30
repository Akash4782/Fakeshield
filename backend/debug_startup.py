print("1. Importing os, sys", flush=True)
import os
import sys
print("2. Importing FastAPI", flush=True)
from fastapi import FastAPI
print("3. Importing Text Router...", flush=True)
from app.routers.text_router import router as text_router
print("   Text Router OK", flush=True)
print("4. Importing Image Router...", flush=True)
from app.routers.image_router import router as image_router
print("   Image Router OK", flush=True)
print("5. Importing Video Router...", flush=True)
from app.routers.video_router import router as video_router
print("   Video Router OK", flush=True)
print("6. Importing Audio Router...", flush=True)
from app.routers.audio_router import router as audio_router
print("   Audio Router OK", flush=True)
print("Startup Import Test Finished Successfully.", flush=True)
