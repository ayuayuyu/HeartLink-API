from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json

from src.WsManager import WsManager
from src.filter import filter
from src.models import Datas
from src.models import Device
from src.models import Status

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

@app.post("/reset")
async def reset_endpoint(reset: Reset):
    manager.set_heart(reset.value)
    manager.set_heartMax(reset.value)
    await manager.broadcast(manager.get_heart(),'12345')
    print(f"heartMax: {manager.get_heartMax()} , heartRate: {manager.get_heart()}")
    
@app.post("/max")
async def max_endpoint():
    return manager.get_heartMax()

@app.post("/data")
#それぞれの心拍数を取得するエンドポイント
async def data_endpoint(data: Datas):
    print(f"心拍数: {data.heartRate}")
    #それぞれのデバイスIDと心拍をdictで一つにまとめる
    manager.device_data[data.id]= data.heartRate
    
    #JSON方式
    json_data = {
        "id1": filters.get_deviceId_1(),
        "heartRate1": manager.device_data.get(filters.get_deviceId_1()),
        "id2": filters.get_deviceId_2(),
        "heartRate2": manager.device_data.get(filters.get_deviceId_2()),
    }
    # 全クライアントにメッセージを送信(JSON方式)
    await manager.broadcast(json.dumps(json_data),filters.get_roomId())
    return {"message":"HartRate"}


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    filters.set_roomId(room_id)
    await manager.connect(websocket, room_id)
    try:
        while True:
            # クライアントからのメッセージ受信
            data = await websocket.receive_text()
            #JSON形式
            json_data = {
                "id1": filters.get_deviceId_1(),
                "heartRate1": data,
                "id2": filters.get_deviceId_2(),
                "heartRate2": data,
            }
            # ルーム内の全クライアントにブロードキャスト(JSON形式)
            await manager.broadcast(json.dumps(json_data), room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)