# test_backend.py - Test backend endpoints
import requests
import json

BASE_URL = "http://localhost:8000/api"


def test_auth():
    """Test authentication endpoints"""
    print("🔐 Testing Authentication...")

    # Test data
    test_user = {
        "email": "testuser@example.com",
        "username": "testuser123",
        "password": "TestPass123!"
    }

    # 1. Register
    print("\n1. Testing registration...")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            print("   ✅ Registration successful!")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # 2. Login
    print("\n2. Testing login...")
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={"username": test_user["email"], "password": test_user["password"]}
        )
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"   ✅ Login successful!")
            print(f"   Token received: {token[:50]}...")
            return token
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    return None


def test_travel_endpoints(token):
    """Test travel endpoints with authentication"""
    print("\n✈️ Testing Travel Endpoints...")

    if not token:
        print("   ❌ No token, skipping protected endpoints")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 1. Test protected travel endpoint
    print("\n1. Testing protected travel planning...")
    try:
        response = requests.get(
            f"{BASE_URL}/travel/plan-simple?destination=Tokyo&days=5",
            headers=headers
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Travel planning works!")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Destination: {data.get('plan', {}).get('destination')}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

    # 2. Test public destination search
    print("\n2. Testing public destinations...")
    try:
        response = requests.get(f"{BASE_URL}/travel/destinations")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Got destinations!")
            data = response.json()
            print(f"   Categories: {list(data.keys())}")
    except Exception as e:
        print(f"   ❌ Error: {e}")


def test_user_endpoints(token):
    """Test user endpoints"""
    print("\n👤 Testing User Endpoints...")

    if not token:
        print("   ❌ No token, skipping user endpoints")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 1. Test user dashboard
    print("\n1. Testing user dashboard...")
    try:
        response = requests.get(f"{BASE_URL}/user/dashboard", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Dashboard works!")
            print(f"   User: {data.get('user', {}).get('email')}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")


def main():
    """Run all tests"""
    print("=" * 50)
    print("🧪 BACKEND TESTING")
    print("=" * 50)

    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Server is running: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running! Start it with: python main.py")
        return

    # Run tests
    token = test_auth()
    if token:
        test_travel_endpoints(token)
        test_user_endpoints(token)

    print("\n" + "=" * 50)
    print("🎉 Backend testing complete!")
    print("\n📝 Manual testing commands for PowerShell:")
    print('   Invoke-RestMethod -Uri "http://localhost:8000/api/auth/register" \')
    print('   -Method POST -ContentType "application/json" \')
    print('   -Body ''{"email":"test@example.com","username":"testuser","password":"TestPass123!"}''')
    print('\n   $response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" \')
    print('   -Method POST -ContentType "application/x-www-form-urlencoded" \')
    print('   -Body "username=test@example.com&password=TestPass123!"')
    print('\n   Invoke-RestMethod -Uri "http://localhost:8000/api/auth/me" \')
    print('   -Method GET -Headers @{Authorization = "Bearer $($response.access_token)"}')

    if __name__ == "__main__":
        main()
    input("\nPress Enter to exit...")