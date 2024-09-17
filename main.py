from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from src.WsManager import WsManager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
manager = WsManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 特定のオリジンを許可する場合はここで指定します
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get():
    return HTMLResponse("Hello World!")

@app.post("/msg/{room_id}")
async def msg(msg: str, room_id: str) -> None:
    await WsManager.send_personal_message(msg, room_id)

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{data}", room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        

