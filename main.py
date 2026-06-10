from fastapi import FastAPI, WebSocket

app = FastAPI()

connections = []

@app.get("/")
def home():
    return {"message": "Server is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    # first message = username
    username = await websocket.receive_text()

    try:
        while True:
            message = await websocket.receive_text()
            full_message = f"{username}: {message}"

            for conn in connections:
                await conn.send_text(full_message)

    except:
        connections.remove(websocket)