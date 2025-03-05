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

# ✅ Ensure Render's assigned PORT is being used correctly
if __name__ == "__main__":
    port = os.getenv("PORT")  # Get PORT from Render

    # 🚨 Debugging: Print the PORT variable to logs
    if port is None:
        print("🚨 ERROR: PORT environment variable is not set!")
        raise ValueError("PORT environment variable is missing!")

    port = int(port)  # Convert to integer
    print(f"🚀 Starting server on port {port}")

    # ✅ Explicitly force Uvicorn to use the correct PORT
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
