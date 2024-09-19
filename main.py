from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from src.WsManager import WsManager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
manager = WsManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 運用時には特定のオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Datas(BaseModel):
    heartRate: str

@app.get("/")
async def get():
    return HTMLResponse("Hello World!")


@app.post("/data")
async def create_data(data: Datas):
    print(f"心拍数: {data.heartRate}")
    manager.set_heart(data.heartRate)  # 心拍数をマネージャーにセット
    # WebSocketを使ってクライアントに心拍数をブロードキャスト
    try:
        await manager.broadcast(manager.get_heart(), '12345')
    except Exception as e:
        print(f"Error broadcasting message: {e}")
    return {"status": "Message sent via WebSocket"}


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    await manager.connect(websocket, room_id)
    try:
        while True:
            # クライアントからのメッセージ受信
            await websocket.receive_text()
            print(f"送信する心拍数: {manager.get_heart()}")
            # ルーム内の全クライアントにブロードキャスト
            await manager.broadcast(manager.get_heart(), room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
    finally:
        try:
            await websocket.close()
        except Exception as e:
            print(f"Error during closing handshake: {e}")
