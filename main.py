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
    allow_origins="*",  # すべてのオリジンを許可する場合
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可 (GET, POSTなど)
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)
    
@app.get("/")
async def get():
    return HTMLResponse("Hello World!")

@app.post("/id")
# デバイスのIDを受け取るエンドポイント
async def id_endpoint(device:Device):
    print("device", device)
    #一つ目のデバイスIDを取得する
    if filters.get_count() == 0 :
        filters.set_deviceId_1(device.id)
        print(f"id1: {device.id}")
        filters.set_count(1)
        return {"player": "1"}
    #二つ目のデバイスIDを取得する
    elif filters.get_count() == 1:
        filters.set_deviceId_2(device.id)
        filters.set_count(2)
        print(f"id2: {device.id}")
        return {"player": "2"}
    
    
@app.get("/connect")
#pixelが繋がったどうか知るためのエンドポイント
async def connect_endpoint():
    print(f"count: {filters.get_count()}")
    if filters.get_count() == 0:
        return {"connect": "0"}
    elif filters.get_count() == 1:
        return {"connect": "1"}
    elif filters.get_count() == 2:
        return {"connect": "2"}
    else:
        return {"connect": "erro"}
    
@app.get("/reset")
#フロント側から受け取るstatus
# すべてをリセットするエンドポイント
async def reset_endpoint():
    filters.set_count(0)
    return {"status": "reset"}
    
@app.get("/ok")
#pixel側から受け取るstatus
async def connect_start():
    count = filters.get_okCount() + 1
    filters.set_okCount(count)
    if filters.get_okCount() == 2:
        filters.set_status("ok")
    return {"status": "ok"}
    
@app.get("/start")
#フロント側から受け取るstatus
async def connect_start():
    filters.set_status("start")
    return {"status": "start"}

@app.get("/end")
#フロント側から受け取るstatus
async def connect_start():
    filters.set_status("end")
    return {"status": "end"}
    
    
    
@app.post("/status")
# 状態によって返すことを変える
async def ok_endpoint(data: Status):
    print(f"status: {data.status}")
    print(f"get_status: {filters.get_status()}")
    if data.status == filters.get_status():
        filters.set_status(data.status)
        print(f"{filters.get_status()}")
        return {"status": filters.get_status()}
    else:
        #当てはまらないstatusが送られてきたときはerroを返す
        print("status : iteration")
        return {"status": "iteration"}
    
    
        
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
    print(f"get_status: {filters.get_status()}")
    if filters.get_status() == "iteration":
        print("iteration")
        return {"status":"iteration"}
    elif filters.get_status() == "end":
        print("end")
        return {"status":"end"}
    


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
