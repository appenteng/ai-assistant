# test_database.py
from app.core.database import init_db, SessionLocal
from app.models.trip import Trip
import json

print("🧪 Testing database setup...")

# Initialize database
init_db()
print("✅ Database initialized")

# Test creating a trip
db = SessionLocal()
try:
    # Create test trip
    test_trip = Trip(
        destination="Test Destination",
        days=3,
        budget=1000,
        itinerary=json.dumps(["Day 1: Test", "Day 2: Test", "Day 3: Test"]),
        preferences={"test": True}
    )

    db.add(test_trip)
    db.commit()
    db.refresh(test_trip)

    print(f"✅ Created test trip with ID: {test_trip.id}")

    # Query it back
    fetched_trip = db.query(Trip).filter(Trip.id == test_trip.id).first()
    print(f"✅ Fetched trip: {fetched_trip.destination}")
    print(f"✅ Trip data: {fetched_trip.to_dict()}")

    # Count total trips
    trip_count = db.query(Trip).count()
    print(f"✅ Total trips in database: {trip_count}")

finally:
    db.close()

print("🎉 Database test completed successfully!")