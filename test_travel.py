# test_travel.py - Place this in ROOT folder (same as main.py)
print("🧪 Testing Travel Service from ROOT...")

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("1. Testing imports...")
    from app.services.travel_service import TravelService
    from app.schemas.travel import TripType

    print("✅ Import successful!")

    print("\n2. Creating service...")
    service = TravelService()
    print("✅ Service created")

    print("\n3. Testing basic functionality...")

    # Test 1: Detect trip type
    destinations = ["Bali, Indonesia", "Swiss Alps", "Tokyo, Japan", "Costa Rica"]
    for dest in destinations:
        trip_type = service.detect_trip_type(dest)
        print(f"   {dest:20} → {trip_type.value}")

    # Test 2: Plan a simple trip
    print("\n4. Planning a trip to Paris...")
    plan = service.plan_trip("Paris, France", days=4, travelers=2)
    print(f"   ✅ Destination: {plan['destination']}")
    print(f"   ✅ Days: {plan['days']}")
    print(f"   ✅ Trip type: {plan['trip_type']}")
    print(f"   ✅ Total cost: ${plan['total_cost']:.2f}")
    print(f"   ✅ Itinerary has {len(plan['itinerary'])} days")

    # Test 3: Show cost breakdown
    print("\n5. Cost breakdown:")
    for category, cost in plan['cost_breakdown'].items():
        if category != "total":
            print(f"   {category:15} ${cost:.2f}")

    # Test 4: Get recommendations
    print(f"\n6. Recommendations ({len(plan['recommendations'])}):")
    for i, rec in enumerate(plan['recommendations'][:3], 1):
        print(f"   {i}. {rec}")

    # Test 5: Search destinations
    print("\n7. Searching destinations...")
    search_results = service.search_destinations("new")
    print(f"   Found {len(search_results)} destinations with 'new':")
    for dest in search_results[:3]:
        print(f"   - {dest}")

    print("\n🎉 ALL TESTS PASSED!")
    print("✅ Enhanced Travel Service is working!")

except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\n📁 Current directory:", os.getcwd())
    print("📁 Python path:")
    for path in sys.path:
        if "ai_assistant" in path:
            print(f"   → {path}")

except Exception as e:
    print(f"\n❌ Error: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()

input("\nPress Enter to exit...")