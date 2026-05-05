import os
import sys
import subprocess
import time

def run_backend():
    print("Starting FakeShield Backend (Safe Mode)...")
    log_file = open("backend_critical.log", "w", encoding="utf-8")
    
    try:
        # Using -u for unbuffered output
        process = subprocess.Popen(
            ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--no-access-log"],
            cwd=os.getcwd(),
            stdout=log_file,
            stderr=log_file,
            text=True,
            env=os.environ.copy()
        )
        print(f"Backend started with PID: {process.pid}")
        return process
    except Exception as e:
        print(f"Failed to start backend: {e}")
        return None

if __name__ == "__main__":
    p = run_backend()
    if p:
        try:
            while True:
                if p.poll() is not None:
                    print(f"Backend process exited with code: {p.returncode}")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            p.terminate()
