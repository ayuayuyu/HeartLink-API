from typing import List, Dict
from fastapi import WebSocket

class WsManager:
    def __init__(self):
        self.heart = '0'  # 初期心拍数
        self.heartMax = '0'#心拍数の最大値
        # 複数の部屋を管理するために辞書を使用します
        self.active_connections: Dict[str, List[WebSocket]] = {}

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
                self.active_connections.remove(connection)

    def set_heart(self, heart_value: str):
        self.heart = heart_value

    def get_heart(self):
        return self.heart
    
    def set_heartMax(self, heart_value: str):
        self.heartMax = heart_value

    def get_heartMax(self):
        return self.heartMax