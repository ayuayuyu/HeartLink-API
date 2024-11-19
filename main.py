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
from src.models import Array
from src.models import indexTopics


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
    resetのstatusを受け取る（フロント側）
    すべてをリセットするエンドポイント
    """
    filters.allReset()
    return {"status": "reset"}
    
@app.get("/ok")
async def connect_start():
    """
    okのstatusを受け取る（フロント側）
    statusをokに変更するエンドポイント
    """
    count = filters.get_okCount() + 1
    filters.set_okCount(count)
    if filters.get_okCount() == 2:
        filters.set_status("ok")
    return {"status": "ok"}
    
@app.get("/start")
async def connect_start():
    """
    startのstatusを受け取る（フロント側）
    statusをstartに変更するエンドポイント
    """
    filters.set_status("start")
    return {"status": "start"}

@app.get("/end")
async def connect_start():
    """
    endのstatusを受け取る（フロント側）
    statusをendに変更するエンドポイント
    """
    filters.set_status("end")
    return {"status": "end"}
    
    
    
@app.post("/status")
async def ok_endpoint(data: Status):
    """
    状態を管理するエンドポイント（フロント側）
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
    フロント側から名前とplayer番号を受け取るエンドポイント（フロント側）
    """
    print(f"getName: {data.name} getPlayer: {data.player}")
    if (data.player == "1"):
        filters.set_name1(data.name)
        return {"player1": data.name}
    elif(data.player == "2"):
        filters.set_name2(data.name)
        return {"player2": data.name}
    else:
        return {"erro": data.name}
    
@app.post("/topicId")
async def topicId_endpoint(data:Players):
    """
    お題のidを取得するエンドポイント（フロント側）
    """
    if data.player == "1":
        print(f"player:{data.player}")
        if data.index == 0:
            filters.set_topicId(0,data.id)
            return {"id" : {data.id}}
        if data.index == 2:
            filters.set_topicId(2,data.id)
            return {"id" : {data.id}}
        else:
            return {"id": "erro"}
    elif data.player == "2":
        print(f"player:{data.player}")
        if data.index == 1:
            filters.set_topicId(1,data.id)
            return {"id" : {data.id}}
        if data.index == 3:
            filters.set_topicId(3,data.id)
            return {"id" : {data.id}}
        else:
            return {"id": "erro"}
    else:
        return{"player": "erro"}
    
@app.get("/resetTopicId")
async def resetTopicId_endpoint():
    filters.set_indexCount(0)
    return {"status: reset"}

@app.post("/indexTopicId")
async def resetTopicId_endpoint(data: indexTopics):
    if filters.get_indexStatus() == data.index:
        if filters.get_indexCounts() == 2:
            filters.set_indexCount(filters.get_indexCount()+1)
            filters.set_indexStatus(filters.get_indexStatus()+1)
            print(f"indexCount: {filters.get_indexCount()}, indexCounts: {filters.get_indexCounts()}")
        elif filters.get_indexCounts() == 0 or filters.get_indexCounts() == 1:
            if data.player == "1":
                filters.set_indexCounts(filters.get_indexCounts()+1)
                return {"status": "player1_count"}
            elif data.player == "2":
                filters.set_indexCounts(filters.get_indexCounts()+1)
                return {"status": "player2_count"}
        else:
            return {"status": "index count erro"}
    else:
        return{"status": "Not fount topicIndex"}

@app.post("/topicArray")
async def topicArray_endpoint(array:Array):
    if array.index == 0:
        filters.set_topicArrays(array.player,array.index,array.array)
    elif array.index == 1:
        filters.set_topicArrays(array.player,array.index,array.array)
    elif array.index == 2:
        filters.set_topicArrays(array.player,array.index,array.array)
    elif array.index == 3:
        filters.set_topicArrays(array.player,array.index,array.array)
    else:
        return{"array": "erro"}
    
@app.get("/getTopicArray")
async def getTopicArray_endpoint():
    return {"array1": {"0":filters.get_topicArray1(0),"1":filters.get_topicArray1(1),"2":filters.get_topicArray1(2),"3":filters.get_topicArray1(3)}, "array2": {"0":filters.get_topicArray2(0),"1":filters.get_topicArray2(1),"2":filters.get_topicArray2(2),"3":filters.get_topicArray2(3)}}
    

@app.get("/getName")
async def getName_endpoint():
    """
    名前を取得するエンドポイント（フロント側）
    """
    return {"player1": {filters.get_name1()} ,"player2": {filters.get_name2()}}
    
        
@app.post("/data")
async def data_endpoint(data: Datas):
    """
    それぞれの心拍数を取得するエンドポイント（バック側）
    """
    print(f"心拍数: {data.heartRate}")
    #それぞれのデバイスIDと心拍をdictで一つにまとめる
    manager.device_data[data.player]= data.heartRate
    
    #JSON方式
    json_data = {
        "player1": filters.get_name1(),
        "heartRate1": manager.device_data.get(filters.get_deviceId_1()),
        "player2": filters.get_name2(),
        "heartRate2": manager.device_data.get(filters.get_deviceId_2()),
        "topicId": filters.get_topicId(),
        "index" : filters.get_indexCount(),
    }
    # 全クライアントにメッセージを送信(JSON方式)
    await manager.broadcast(json.dumps(json_data))
    print(f"get_status: {filters.get_status()}")
    if filters.get_status() == "iteration":
        print("iteration")
        return {"status":"iteration"}
    elif filters.get_status() == "end":
        print("end")
        return {"status":"end"}
    


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket通信をするエンドポイント（フロント側）
    """
    await manager.connect(websocket)
    try:
        while True:
            # クライアントからのメッセージ受信
            data = await websocket.receive_text()
            #JSON形式
            json_data = {
                "player1": filters.get_name1(),
                "heartRate1": data,
                "player2": filters.get_name2(),
                "heartRate2": data,
                "topicId": filters.get_topicId(),
                "index" : filters.get_indexCount(),
            }
            # ルーム内の全クライアントにブロードキャスト(JSON形式)
            await manager.broadcast(json.dumps(json_data))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
