# ultra_simple.py
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/")
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Assistant - ULTRA SIMPLE</title>
        <style>
            body {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                font-family: Arial;
                text-align: center;
                padding: 50px;
            }
            .box {
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 20px;
                margin: 20px;
                display: inline-block;
            }
            button {
                background: #4361ee;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 10px;
                font-size: 16px;
                cursor: pointer;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <h1>🤖 AI Assistant</h1>
        <p>Finally working! 🎉</p>

        <div class="box">
            <h3>💬 Chat</h3>
            <p>Ask me anything!</p>
            <button onclick="alert('Hello from AI Assistant!')">Say Hello</button>
        </div>

        <div class="box">
            <h3>✈️ Travel</h3>
            <p>Plan your next trip</p>
            <button onclick="alert('Trip planning coming soon!')">Plan Trip</button>
        </div>

        <p><small>Visual proof that we're making progress!</small></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


if __name__ == "__main__":
    print("🚀 ULTRA SIMPLE version starting...")
    print("🌐 Open: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)