
import sys
import os

# Add the current directory to sys.path so we can import 'app'
sys.path.append(os.getcwd())

try:
    from app.services.video.better_spatial import warm_up_spatial_models, _models
    
    print("Starting spatial model warm-up...")
    warm_up_spatial_models()
    
    print("\nRegistration Check:")
    for key, data in _models.items():
        print(f" [LOADED] {key}: {data['id']} on {data['device']}")
        
    if len(_models) >= 2:
        print("\n✅ SUCCESS: All spatial models loaded successfully.")
    else:
        print(f"\n❌ FAILURE: Only {len(_models)}/2 models loaded.")
        sys.exit(1)

except Exception as e:
    print(f"\n❌ CRITICAL ERROR during verification: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
