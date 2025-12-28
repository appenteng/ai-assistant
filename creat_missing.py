# create_missing.py - Create missing essential files
import os


def create_file(path, content=""):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"📄 Created: {path}")


print("🛠️ Creating missing files...")

# Create essential __init__.py files
init_files = [
    "app/__init__.py",
    "app/services/__init__.py",
    "app/schemas/__init__.py",
    "app/agents/__init__.py",
    "app/api/__init__.py"
]

for file in init_files:
    if not os.path.exists(file):
        create_file(file)

# Create travel_service.py if missing
if not os.path.exists("ai_assistant/app/services/travel_service.py"):
    create_file("ai_assistant/app/services/travel_service.py", '''"""
Travel Service - Basic version
"""
from typing import Dict, List
import random

class TravelService:
    def __init__(self):
        self.destinations = {
            "beach": ["Bali", "Maldives", "Hawaii"],
            "city": ["Paris", "Tokyo", "New York"],
            "mountain": ["Swiss Alps", "Rocky Mountains"]
        }

    def plan_trip(self, destination: str, days: int) -> Dict:
        """Basic trip planning"""
        return {
            "destination": destination,
            "days": days,
            "itinerary": [f"Day {i+1}: Explore {destination}" for i in range(days)],
            "estimated_cost": days * 150
        }

    def get_popular_destinations(self) -> Dict[str, List[str]]:
        """Get popular destinations"""
        return self.destinations
''')

print("\n✅ Created essential files.")
print("\nNow run: python test_travel.py")