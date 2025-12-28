# fix_imports.py
import os

print("🛠️ Fixing imports...")

# 1. Ensure services/__init__.py exports correctly
with open("app/services/__init__.py", "w") as f:
    f.write('''from .travel_service import TravelService
from .ai_service import AIService

__all__ = ["TravelService", "AIService"]
''')
print("✅ Updated app/services/__init__.py")

# 2. Create travel_service.py if missing
if not os.path.exists("app/services/travel_service.py"):
    with open("app/services/travel_service.py", "w") as f:
        f.write('''
class TravelService:
    def plan_trip(self, destination, days):
        return {
            "destination": destination,
            "days": days,
            "itinerary": [f"Day {i+1}: Explore" for i in range(days)],
            "cost": days * 150
        }
''')
    print("✅ Created app/services/travel_service.py")

# 3. Test the fix
try:
    from app.services import TravelService
    print("✅ Import now works!")
    service = TravelService()
    print(f"✅ Can create instance: {service.plan_trip('Paris', 3)}")
except Exception as e:
    print(f"❌ Still failing: {e}")

print("\n✅ Done. Try your test again.")