import importlib.metadata

pkgs = importlib.metadata.distributions()
for pkg in pkgs:
    try:
        name = pkg.metadata['Name']
        version = pkg.metadata['Version']
        # print(f"{name}: {version}")
    except Exception as e:
        print(f"Error in {pkg.metadata.get('Name', 'Unknown')}: {e}")
