import os

excluded_dirs = {"venv", "__pycache__", "data", "scripts"}
backend_path = "C:/Users/senor/Documents/x-bot-spt-ext/backend"

for root, dirs, files in os.walk(backend_path):
    if any(excluded in root for excluded in excluded_dirs):
        continue
    if "__init__.py" in files:
        print(f"✅ {root}/__init__.py found")
    else:
        print(f"❌ Missing __init__.py in {root}")
