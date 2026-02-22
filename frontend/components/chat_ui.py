from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List

router = APIRouter()

# ----------------------------
# Dummy Chat AI Logic
# ----------------------------
def ai_response(message: str):
    """
    Simulated AI response logic.
    Replace this with your real AI model/API.
    """
    if "fever" in message.lower():
        return "It seems like you have a fever. Please take rest and drink fluids."
    elif "headache" in message.lower():
        return "For headache, make sure to rest in a quiet place and stay hydrated."
    else:
        return "I am here to assist you. Can you describe your symptoms in more detail?"


# ----------------------------
# Chat UI (HTML)
# ----------------------------
@router.get("/chat", response_class=HTMLResponse)
async def chat_ui():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hospital Chat AI</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            #chatbox { width: 100%; height: 400px; border: 1px solid #ccc; overflow-y: scroll; padding: 10px; }
            #userInput { width: 80%; padding: 10px; }
            #sendBtn { padding: 10px; }
            .message { margin: 5px 0; }
            .user { color: blue; }
            .ai { color: green; }
        </style>
    </head>
    <body>
        <h2>AI Chat Assistant</h2>
        <div id="chatbox"></div>
        <input type="text" id="userInput" placeholder="Type your message..." />
        <button id="sendBtn">Send</button>

        <script>
            const chatbox = document.getElementById("chatbox");
            const input = document.getElementById("userInput");
            const btn = document.getElementById("sendBtn");

            btn.onclick = async () => {
                const message = input.value;
                if (!message) return;
                chatbox.innerHTML += '<div class="message user"><b>You:</b> ' + message + '</div>';
                input.value = "";

                const response = await fetch("/api/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: "message=" + encodeURIComponent(message)
                });
                const data = await response.json();
                chatbox.innerHTML += '<div class="message ai"><b>AI:</b> ' + data.reply + '</div>';
                chatbox.scrollTop = chatbox.scrollHeight;
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# ----------------------------
# Chat API (JSON)
# ----------------------------
@router.post("/chat", response_class=JSONResponse)
async def chat_api(message: str = Form(...)):
    reply = ai_response(message)
    return {"reply": reply}