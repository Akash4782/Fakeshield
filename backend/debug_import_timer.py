import time

def timed_import(name):
    t0 = time.time()
    print(f"Importing {name}...", end="", flush=True)
    try:
        __import__(name)
        print(f" OK ({time.time()-t0:.2f}s)")
    except Exception as e:
        print(f" FAIL: {e}")

timed_import("fastapi")
timed_import("google.generativeai")
timed_import("torch")
timed_import("transformers")
timed_import("app.models.new_forensic_engine")
timed_import("app.models.image_detector")
timed_import("app.models.audio.audio_warmup")
timed_import("app.routers.text_router")
timed_import("app.main")
