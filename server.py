import os
import uvicorn
from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

# Store connected WebSocket clients
clients: List[WebSocket] = []

@app.websocket("/ws")
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

# 🔹 Get PORT dynamically from Render's environment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Get PORT from Render, default 10000
    uvicorn.run(app, host="0.0.0.0", port=port)
