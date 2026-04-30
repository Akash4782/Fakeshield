
import sys
import os
import contextlib
import io

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from app.services.video.better_spatial import warm_up_spatial_models, _models

print("Starting clean spatial model warm-up...")

# Capture output to check for 'RETRY' or 'Unrecognized'
f = io.StringIO()
with contextlib.redirect_stdout(f):
    warm_up_spatial_models()
output = f.getvalue()

print("\n--- CAPTURED OUTPUT ---")
print(output)
print("--- END OF OUTPUT ---\n")

print("Registration Check:")
for key, data in _models.items():
    print(f" [LOADED] {key}: {data['id']}")

if "RETRY" in output or "Unrecognized" in output:
    print("\n❌ FAILURE: Logs still contain noisy error messages or retry cycles.")
    sys.exit(1)
else:
    print("\n✅ SUCCESS: Models loaded cleanly without noisy errors.")
