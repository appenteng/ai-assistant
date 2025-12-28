import os

print("🛠️ Setting up dashboard...")

# Create templates folder
os.makedirs("templates", exist_ok=True)

# Create simple_main.py
with open("simple_main.py", "w") as f:
    f.write('''from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/test")
def test():
    return {"message": "Working!"}

if __name__ == "__main__":
    print("✅ Server starting at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
''')

# Create minimal dashboard.html
with open("templates/dashboard.html", "w") as f:
    f.write('''<!DOCTYPE html>
<html>
<head>
    <title>AI Assistant</title>
    <style>body {background: blue; color: white; text-align: center; padding: 50px;}</style>
</head>
<body>
    <h1>🎉 AI Assistant Dashboard</h1>
    <p>It's working! You can see this page!</p>
    <button onclick="alert('Hello!')">Click me</button>
</body>
</html>''')

print("✅ Files created. Now run: python simple_main.py")