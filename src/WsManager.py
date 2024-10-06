from typing import List, Dict
from fastapi import WebSocket

class WsManager:
    def __init__(self):
        # 複数の部屋を管理するために辞書を使用する
        self.active_connections: Dict[str, List[WebSocket]] = {}
        
        #複数の端末情報を管理するために辞書をしようする
        self.device_data: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        websocket.close()
        self.active_connections[room_id].remove(websocket)
        if not self.active_connections[room_id]:  # もし部屋に接続が無ければ部屋を削除
            del self.active_connections[room_id]

    async def broadcast(self, message: str, room_id: str):
        for connection in self.active_connections.get(room_id, []):
            try:
                await connection.send_text(message)
            except:
                self.active_connections[room_id].remove(connection)  # room_id のリストから削除
                if not self.active_connections[room_id]:  # リストが空なら部屋自体を削除
                    del self.active_connections[room_id]


    