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
from src.models import PlayerName
from src.models import Players
from src.models import Names


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
async def id_endpoint(device:Device):
    """
    デバイスのIDを受け取るエンドポイント
    """
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
async def connect_endpoint():
    """
    pixelが繋がったどうか知るためのエンドポイント
    """
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
async def reset_endpoint():
    """
    フロント側から受け取るstatus
    すべてをリセットするエンドポイント
    """
    filters.allReset()
    return {"status": "reset"}
    
@app.get("/ok")
async def connect_start():
    """
    pixel側から受け取るstatus
    """
    count = filters.get_okCount() + 1
    filters.set_okCount(count)
    if filters.get_okCount() == 2:
        filters.set_status("ok")
    return {"status": "ok"}
    
@app.get("/start")
async def connect_start():
    """
    フロント側から受け取るstatus
    """
    filters.set_status("start")
    return {"status": "start"}

@app.get("/end")
async def connect_start():
    """
    フロント側から受け取るstatus
    """
    filters.set_status("end")
    return {"status": "end"}
    
    
    
@app.post("/status")
async def ok_endpoint(data: Status):
    """
    状態によって返すことを変える
    """
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
    
@app.post("/sendname")
async def name_endpoint(data: PlayerName):
    """
    フロント側から名前とplayer番号を受け取るエンドポイント
    """
    print(f"getName: {data.name} getPlayer: {data.player}")
    if (data.player == "1"):
        filters.set_deviceId_1(data.name)
        return {"player1": data.name}
    elif(data.player == "2"):
        filters.set_deviceId_2(data.name)
        return {"player2": data.name}
    else:
        return {"erro": data.name}

@app.post("/name")
async def name_endpoint(data: Names):
    """
    名前を受け取るエンドポイント
    """
    if data.player == "1":
        filters.set_name1(data.name)
        print(f"name: {filters.get_name1()}")
        return {"name": {filters.get_name1()}}
    elif data.player == "2":
        filters.set_name2(data.name)
        print(f"name: {filters.get_name2()}")
        return {"name": {filters.get_name2()}}
    else:
        return {"name": "erro"}
    
@app.post("/topicId")
async def topicId_endpoint(data:Players):
    if data.player == "1":
        print(f"player:{data.player}")
        if filters.get_indexCount1() == 0:
            filters.set_topicId(0,data.id)
            filters.set_indexCount1(1)
            return {"id" : {data.id}}
        else:
            return {"id": "erro"}
    elif data.player == "2":
        print(f"player:{data.player}")
        if filters.get_indexCount2() == 0:
            filters.set_topicId(1,data.id)
            filters.set_indexCount2(1)
            return {"id" : {data.id}}
        else:
            return {"id": "erro"}
    else:
        return{"player": "erro"}
    
@app.get("/resetTopicId")
async def resetTopicId_endpoint():
    filters.set_indexCount1(0)
    filters.set_indexCount2(0)
    return {"status: reset"}

@app.get("/getName")
async def getName_endpoint():
    return {"player1": {filters.get_name1()} ,"player2": {filters.get_name2()}}
    
        
@app.post("/data")
#それぞれの心拍数を取得するエンドポイント
async def data_endpoint(data: Datas):
    print(f"心拍数: {data.heartRate}")
    #それぞれのデバイスIDと心拍をdictで一つにまとめる
    manager.device_data[data.player]= data.heartRate
    
    #JSON方式
    json_data = {
        "player1": filters.get_deviceId_1(),
        "heartRate1": manager.device_data.get(filters.get_deviceId_1()),
        "player2": filters.get_deviceId_2(),
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
    


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
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
            await manager.broadcast(json.dumps(json_data))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
