import os
import sys
import subprocess

# Set environment variables for clean startup
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONWARNINGS"] = "ignore:Multiple distributions found for package optimum"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Handle optional arguments
if "--fast" in sys.argv:
    os.environ["FAKESHIELD_SKIP_WARMUP"] = "1"
    print(">> Fast Mode enabled: Skipping forensic model pre-loading.")

# Define the command to run (using uvicorn directly for Windows stability)
cmd = ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--no-access-log"]

# Change directory to the script's directory (backend)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"Starting FakeShield Backend v10.0 (UTF-8 Mode)...")
try:
    subprocess.run(cmd, check=True)
except KeyboardInterrupt:
    print("\nBackend stopped by user.")
except Exception as e:
    print(f"\nBackend crashed: {e}")
