
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Working!"}

@app.get("/test")
def test():
    return {"status": "ok"}

@app.get("/travel")
def travel(destination: str = "Paris"):
    return {"plan": f"Trip to {destination} planned!"}

if __name__ == "__main__":
    print("🚀 Simple test server starting...")
    uvicorn.run(app, host="0.0.0.0", port=8000)