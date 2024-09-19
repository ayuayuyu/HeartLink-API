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
    allow_origins=["*"],  # 特定のオリジンを許可する場合はここで指定します
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

heart :str= '0'
class Datas(BaseModel):
    heartRate: str

@app.get("/")
async def get():
    return HTMLResponse("Hello World!")

    
@app.post("/data")
async def create_data(data: Datas):
    global heart
    print(f"心拍数: {data.heartRate}")
    heart = data.heartRate
    # 受け取ったデータをWebSocketを使ってクライアントに送信
     # ここでデバッグ用に送信しようとしているデータを確認
    print(f"送信する心拍数: {heart}")
    await manager.broadcast(heart,12345)
    return {"status": "Message sent via WebSocket"}


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    await manager.connect(websocket, room_id)
    try:
        while True:
            # クライアントからメッセージを受信
            await websocket.receive_text()
            print(f"送信する心拍数: {heart}")
            # クライアントから受信したメッセージをルーム内の全クライアントにブロードキャスト
            await manager.broadcast(f"{heart}", room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        

