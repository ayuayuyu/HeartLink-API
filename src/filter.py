from typing import List

class filter:
    def __init__(self):
        self.heart = '0'  # 初期心拍数
        # self.heartMax = '0'#心拍数の最大値
        # self.heartMin = '1000000'#心拍数の最小値
        self.roomId = "0"#roomIdの取得
        self.deviceId_1= "null"
        self.deviceId_2= "null"
        self.count = 0
        self.status = "iteration"
        
    #心拍数のセット
    def set_heart(self, heart_value: str):
        self.heart = heart_value
    #心拍数を取得
    def get_heart(self):
        return self.heart
    #心拍数の最大値をセット
    def set_heartMax(self, heart_value: str):
        self.heartMax = heart_value
    #心拍数の最大値を取得
    def get_heartMax(self):
        return self.heartMax
    #心拍数の最小値をセット
    def set_heartMin(self, heart_value: str):
        self.heartMin = heart_value
    #心拍数の最小値を取得
    def get_heartMin(self):
        return self.heartMin
    
    def set_roomId(self, room_id:str):
        self.roomId = room_id
    
    def get_roomId(self):
        return self.roomId
    
    def get_count(self):
        return self.count
    
    def set_count(self,value:int):
        self.count = value    
        
    def set_deviceId_1(self, deviceId: str):
        self.deviceId_1 = deviceId
        
    def get_deviceId_1(self):
        return self.deviceId_1
    
    def set_deviceId_2(self, deviceId: str):
        self.deviceId_2 = deviceId
        
    def get_deviceId_2(self):
        return self.deviceId_2
    
    def set_status(self, status:str):
        self.status = status
    
    def get_status(self):
        return self.status
    
    #最大値比較
    def max(self, heart_value: str):
        try:
            #str型をfloat型に変換して比較する
            if float(self.heartMax) < float(self.heart):
                self.set_heartMax(heart_value)
        except ValueError:
            #str型をint型に変換して比較する
            if int(self.heartMax) < int(self.heart):
                self.set_heartMax(heart_value)
        print(f"heartMax: {self.heartMax}")
        
    #最小値比較
    def min(self, heart_value: str):
        try:
            #str型をfloat型に変換して比較する
            if float(self.heartMin) > float(self.heart):
                self.set_heartMin(heart_value)
        except ValueError:
            #str型をint型に変換して比較する
            if int(self.heartMin) > int(self.heart):
                self.set_heartMin(heart_value)
        print(f"heartMin: {self.heartMin}")
    
    #すべてセットする
    def allSet(self, heart_value: str):
        self.set_heart(heart_value)
        self.max(heart_value)
        self.min(heart_value)
        
    #すべて初期値にする
    def reSet(self, heart_value: str):
        self.set_heart(heart_value)
        self.set_heartMax(heart_value)
        self.set_heartMin("100000")