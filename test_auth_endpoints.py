# test_auth_endpoints.py
import requests
import json

BASE_URL = "http://localhost:8000/api"

print("🔐 Testing Authentication Endpoints...")

# Test data
test_user = {
    "email": "testuser@example.com",
    "username": "testuser123",
    "password": "TestPass123!",
    "full_name": "Test User"
}


def test_register():
    """Test user registration"""
    print("\n1. Testing Registration...")
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=test_user
    )

    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")

    if response.status_code == 201:
        print("   ✅ Registration successful!")
        return True
    else:
        print("   ❌ Registration failed")
        return False


def test_login():
    """Test user login"""
    print("\n2. Testing Login...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )

    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Login successful!")
        print(f"   Token received: {data['access_token'][:50]}...")
        return data["access_token"]
    else:
        print(f"   ❌ Login failed: {response.text}")
        return None


def test_profile(token):
    """Test getting user profile"""
    print("\n3. Testing Profile Access...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers=headers
    )

    print(f"   Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Profile access successful!")
        print(f"   User: {data['email']} ({data['username']})")
        return data
    else:
        print(f"   ❌ Profile access failed: {response.text}")
        return None


def test_check_availability():
    """Test email/username availability checks"""
    print("\n4. Testing Availability Checks...")

    # Check email
    response = requests.get(f"{BASE_URL}/auth/check-email/{test_user['email']}")
    print(f"   Email '{test_user['email']}' available: {response.json()['available']}")

    # Check username
    response = requests.get(f"{BASE_URL}/auth/check-username/{test_user['username']}")
    print(f"   Username '{test_user['username']}' available: {response.json()['available']}")


def main():
    """Run all tests"""
    print("=" * 50)
    print("🧪 Starting Authentication Tests")
    print("=" * 50)

    # First, check if server is running
    try:
        health = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Server is running: {health.status_code}")
    except:
        print("❌ Server is not running! Start it with: python main.py")
        return

    # Run tests
    if test_register():
        token = test_login()
        if token:
            test_profile(token)
        test_check_availability()

    print("\n" + "=" * 50)
    print("🎉 Tests completed!")
    print("\n📝 Manual testing commands:")
    print(f'curl -X POST "http://localhost:8000/api/auth/register" \\')
    print(f'  -H "Content-Type: application/json" \\')
    print(f'  -d \'{json.dumps(test_user)}\'')
    print(f'\ncurl -X POST "http://localhost:8000/api/auth/login" \\')
    print(f'  -H "Content-Type: application/x-www-form-urlencoded" \\')
    print(f'  -d "username={test_user["email"]}&password={test_user["password"]}"')


if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")