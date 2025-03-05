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

# ✅ Use Render's dynamically assigned PORT instead of hardcoded 10000
if __name__ == "__main__":
    port = int(os.environ["PORT"])  # Ensure we ONLY use Render's assigned PORT
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
