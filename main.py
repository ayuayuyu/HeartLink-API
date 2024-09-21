from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from src.WsManager import WsManager
from src.filter import filter
from src.models import Datas

app = FastAPI()
manager = WsManager()
filters = filter()

# CORSの設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可する場合
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可 (GET, POSTなど)
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
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
    filters.allSet(data.heartRate)
    # WebSocketに心拍数を送る
    await manager.broadcast(data.heartRate,'12345')
    return filters.get_heart()


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    try:
        while True:
            # クライアントからのメッセージ受信
            data = await websocket.receive_text()
            print(f"送信する心拍数: {data}")
            # 通常、最大値、最小値のすべての値をリセットする
            filters.reSet(data)
            
            # 送信するデータの構築 (心拍数の現在値、最大値、最小値)
            # broadcast_data = {
            #     "current_heart": filters.get_heart,
            #     "max_heart": filters.get_heartMax,
            #     "min_heart": filters.get_heartMin
            # }
            # ルーム内の全クライアントにブロードキャスト
            await manager.broadcast(data , room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
