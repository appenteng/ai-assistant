# test_config.py
import sys

sys.path.insert(0, '.')

print("🧪 Testing config fix...")

try:
    from app.core.config import settings

    print("✅ Config loaded successfully!")
    print(f"App: {settings.app_name}")
    print(f"Debug: {settings.debug}")
    print(f"Secret Key: {'Set' if settings.SECRET_KEY else 'Not set'}")
    print(f"Database URL: {settings.DATABASE_URL}")

    # Check if we can import other modules
    from app.core.database import init_db

    print("✅ Database module imports")

    from app.services.travel_service import TravelService

    print("✅ Travel service imports")

    print("\n🎉 All imports work! Server should start now.")

except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()

input("\nPress Enter...")