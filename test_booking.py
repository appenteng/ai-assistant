import requests
import json

BASE_URL = "http://localhost:8000/api"

print("✈️ Testing Flight & Hotel Booking System...")

# Test 1: Search Flights
print("\n1. Testing Flight Search...")
response = requests.get(f"{BASE_URL}/flights/search?origin=JFK&destination=LAX&departure_date=2024-06-15")
if response.status_code == 200:
    data = response.json()
    print(f"   ✅ Found {len(data['data']['flights'])} flights")
    print(f"   Cheapest: ${data['data']['cheapest_price']}")
else:
    print(f"   ❌ Error: {response.status_code}")

# Test 2: Search Hotels
print("\n2. Testing Hotel Search...")
response = requests.get(f"{BASE_URL}/hotels/search?location=Paris&check_in=2024-06-15&check_out=2024-06-18")
if response.status_code == 200:
    data = response.json()
    print(f"   ✅ Found {len(data['data']['hotels'])} hotels")
    print(f"   Lowest price: ${data['data']['lowest_price']}/night")
else:
    print(f"   ❌ Error: {response.status_code}")

# Test 3: Popular Routes
print("\n3. Testing Popular Routes...")
response = requests.get(f"{BASE_URL}/flights/popular-routes")
if response.status_code == 200:
    data = response.json()
    print(f"   ✅ Found {len(data['routes'])} popular routes")
else:
    print(f"   ❌ Error: {response.status_code}")

print("\n🎉 Booking system test complete!")