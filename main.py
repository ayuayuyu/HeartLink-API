from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from src.WsManager import WsManager
from src.filter import filter
from src.models import Datas

app = FastAPI()
manager = WsManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 運用時には特定のオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

@app.get("/")
async def get():
    return HTMLResponse("Hello World!")

    
@app.post("/max")
async def max_endpoint():
    return manager.get_heartMax()

@app.post("/data")
async def create_data(data: Datas):
    print(f"心拍数: {data.heartRate}")
    # 心拍数をセットする(通常、最大値、最小値)
    filter.allSet(data.heartRate)
    # WebSocketに心拍数を送る
    await manager.broadcast(filter.get_heart,'12345')
    return filter.get_heart()


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            # クライアントからのメッセージ受信
            data = await websocket.receive_text()
            print(f"送信する心拍数: {data}")
            # 通常、最大値、最小値のすべての値をリセットする
            filter.reSet(data)
            # ルーム内の全クライアントにブロードキャスト
            await manager.broadcast(data, room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
