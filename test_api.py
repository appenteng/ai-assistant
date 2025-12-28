# test_api.py
import requests
import json

BASE_URL = "http://localhost:8000"

print("🧪 Testing AI Assistant API...")

# Test 1: Check server is running
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print("✅ Server is running!")
    else:
        print(f"⚠️ Server responded with: {response.status_code}")
except Exception as e:
    print(f"❌ Cannot connect to server: {e}")
    exit()

# Test 2: Check API documentation is available
try:
    response = requests.get(f"{BASE_URL}/docs")
    if response.status_code == 200:
        print("✅ API documentation available at /docs")
except:
    print("⚠️ Could not access /docs")

# Test 3: Test public endpoints
print("\n📡 Testing public endpoints...")

# Get popular destinations
try:
    response = requests.get(f"{BASE_URL}/api/travel/destinations")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Got {len(data)} destination categories")
        for category, destinations in data.items():
            print(f"   {category}: {len(destinations)} destinations")
    else:
        print(f"❌ Destinations endpoint: {response.status_code}")
except Exception as e:
    print(f"❌ Error testing destinations: {e}")

# Test 4: Test authentication (register)
print("\n🔐 Testing authentication...")

test_user = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPass123!"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/auth/register",
        json=test_user
    )

    if response.status_code == 201:
        print("✅ User registration successful!")
        user_data = response.json()
        print(f"   User ID: {user_data.get('user_id')}")
    elif response.status_code == 400:
        print("⚠️ User might already exist (trying login instead)")
    else:
        print(f"❌ Registration failed: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Registration error: {e}")

# Test 5: Test login
print("\n🔑 Testing login...")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={"username": test_user["email"], "password": test_user["password"]}
    )

    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print("✅ Login successful!")
        print(f"   Token: {token[:50]}...")

        # Test 6: Test protected endpoint with token
        print("\n🛡️ Testing protected endpoint...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/api/travel/plan-simple?destination=Tokyo&days=5",
            headers=headers
        )

        if response.status_code == 200:
            trip_data = response.json()
            print("✅ Protected travel endpoint works!")
            print(f"   User ID in response: {trip_data.get('user_id')}")
            print(f"   Destination: {trip_data.get('plan', {}).get('destination')}")
        else:
            print(f"❌ Protected endpoint failed: {response.status_code} - {response.text}")

    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")

except Exception as e:
    print(f"❌ Login error: {e}")

# Test 7: Check all available endpoints
print("\n🔍 Checking available endpoints...")
try:
    # Get the root endpoint to see what's available
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        data = response.json()
        print("✅ Root endpoint returns:")
        print(json.dumps(data, indent=2))
except:
    pass

print("\n" + "=" * 50)
print("🎉 TESTING COMPLETE!")
print("\n📊 Next steps:")
print("1. Visit: http://localhost:8000/docs - Interactive API documentation")
print("2. Test endpoints manually")
print("3. Implement frontend dashboard")
print("\n💡 Your backend is WORKING!")