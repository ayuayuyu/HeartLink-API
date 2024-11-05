from typing import List, Dict
from fastapi import WebSocket

class WsManager:
    def __init__(self):
        # 複数の部屋を管理するために辞書を使用する
        self.active_connections: List[WebSocket] = []
        
        #複数の端末情報を管理するために辞書をしようする
        self.device_data: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        websocket.close()
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                self.active_connections.remove(connection)  # room_id のリストから削除

    