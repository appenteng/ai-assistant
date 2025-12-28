# test_auth.py
import sys
import os

sys.path.insert(0, os.getcwd())

print("🧪 Testing Authentication System...")

try:
    # Test imports
    from app.models.user import User
    from app.models.token import Token
    from app.utils.auth import hash_password, verify_password, validate_email, validate_password
    from app.core.database import init_db

    print("✅ All imports successful!")

    # Test password hashing
    password = "TestPass123!"
    hashed = hash_password(password)
    print(f"✅ Password hashing works: {verify_password(password, hashed)}")

    # Test email validation
    emails = ["test@example.com", "invalid-email", "user@domain.co.uk"]
    for email in emails:
        is_valid = validate_email(email)
        print(f"   Email '{email}': {'✅ Valid' if is_valid else '❌ Invalid'}")

    # Test password validation
    passwords = [
        ("weak", "abc"),
        ("medium", "Password123"),
        ("strong", "StrongPass123!")
    ]

    for name, pwd in passwords:
        result = validate_password(pwd)
        print(f"   Password '{name}': {result['strength'].upper()}")
        if result['errors']:
            print(f"     Errors: {result['errors']}")

    # Initialize database (creates tables)
    print("\n📦 Initializing database...")
    init_db()
    print("✅ Database initialized!")

    print("\n🎉 Authentication system is ready!")
    print("\nNext steps:")
    print("1. Run 'python main.py' to start server")
    print("2. Test endpoints:")
    print("   - POST /api/auth/register")
    print("   - POST /api/auth/login")
    print("   - GET /api/auth/me (with token)")

except ImportError as e:
    print(f"❌ Import Error: {e}")
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()

input("\nPress Enter to exit...")