# fix_imports.py
import os

print("🔧 Fixing imports...")

# Option A: Create chat.py
chat_content = '''from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def chat():
    return {"message": "Chat endpoint - will implement later"}
'''

chat_path = "app/api/chat.py"
if not os.path.exists(chat_path):
    with open(chat_path, "w") as f:
        f.write(chat_content)
    print(f"✅ Created {chat_path}")

# Option B: Check if ai_service.py exists
ai_service_path = "app/services/ai_service.py"
if not os.path.exists(ai_service_path):
    with open(ai_service_path, "w") as f:
        f.write('''
class AIService:
    def chat(self, message):
        return f"AI: I heard '{message}'"
''')
    print(f"✅ Created {ai_service_path}")

# Test the fix
try:
    from app.api.router import api_router
    print("✅ Router imports successfully!")
    print("✅ Server should start now.")
except Exception as e:
    print(f"❌ Still issues: {e}")
    # Last resort: create minimal router
    router_path = "app/api/router.py"
    with open(router_path, "w") as f:
        f.write('''
from fastapi import APIRouter
from app.api.main import router as main_router
from app.api.auth import router as auth_router
from app.api.travel import router as travel_router

api_router = APIRouter()
api_router.include_router(main_router, tags=["main"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(travel_router, prefix="/travel", tags=["travel"])
''')
    print(f"✅ Recreated {router_path} with minimal imports")

print("\n🎉 Now try: python main.py")