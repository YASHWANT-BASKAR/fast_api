import os
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# ✅ Enable CORS (Optional, but recommended for frontend clients)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connected WebSocket clients
clients: List[WebSocket] = []

@app.websocket("/ws")  # ✅ Ensure the route is "/ws"
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            for client in clients:
                await client.send_text(f"Echo: {data}")  # Send back received data
    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        clients.remove(websocket)

# ✅ Ensure Render uses the correct PORT
if __name__ == "__main__":
    port = os.getenv("PORT", "10000")  # Default to 10000 if not set
    port = int(port)
    print(f"🚀 Starting WebSocket server on port {port}")
    uvicorn.run("server:app", host="0.0.0.0", port=port)
