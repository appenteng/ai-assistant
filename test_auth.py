import requests
import json

BASE_URL = "http://localhost:8000/api"

print("🔐 Testing Authentication System...")

# Test 1: Register
print("\n1. Testing Registration...")
register_data = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "full_name": "Test User"
}

response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✅ User registered: {response.json()['username']}")
else:
    print(f"   ❌ Error: {response.text}")

# Test 2: Login
print("\n2. Testing Login...")
login_data = {
    "username": "testuser",
    "password": "testpass123"
}

response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    token = response.json()["access_token"]
    print(f"   ✅ Login successful!")
    print(f"   Token: {token[:50]}...")
else:
    print(f"   ❌ Error: {response.text}")

# Test 3: Get Current User
print("\n3. Testing Get Current User...")
if 'token' in locals():
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ User data: {response.json()['username']}")
    else:
        print(f"   ❌ Error: {response.text}")