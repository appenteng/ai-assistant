# check_files.py - Verify all required files exist
import os

print("🔍 Checking project structure...")

required_files = [
    ("main.py", "Root application file"),
    ("requirements.txt", "Dependencies"),
    ("app/__init__.py", "App package marker"),
    ("app/services/__init__.py", "Services package"),
    ("app/services/travel_service.py", "Travel service"),
    ("app/schemas/__init__.py", "Schemas package"),
    ("app/schemas/travel.py", "Travel schemas"),
    ("app/agents/__init__.py", "Agents package"),
    ("app/agents/base_agent.py", "Base agent"),
    ("app/agents/travel_agent.py", "Travel agent"),
]

all_good = True
for file_path, description in required_files:
    if os.path.exists(file_path):
        print(f"✅ {file_path:30} - {description}")
    else:
        print(f"❌ {file_path:30} - MISSING: {description}")
        all_good = False

print("\n" + "=" * 50)
if all_good:
    print("🎉 All files exist! Project structure is good.")
else:
    print("⚠️  Some files are missing. Let's create them.")

# Try a simple import test
print("\n🧪 Testing imports from root...")
try:
    import app

    print("✅ 'app' imports")

    from app.services import travel_service

    print("✅ 'travel_service' imports")

    print("\n🎉 Ready to run tests!")

except ImportError as e:
    print(f"❌ Import failed: {e}")

input("\nPress Enter to continue...")