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
