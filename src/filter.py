from typing import List

class filter:
    def __init__(self):
        self.heart = '0'  # 初期心拍数
        self.name1= "null"
        self.name2= "null"
        self.deviceId_1= "null"
        self.deviceId_2= "null"
        self.count = 0
        self.status = "iteration"
        self.okCount = 0
        self.indexCount1 = 0
        self.indexCount2 = 0
        self.topicId = []
        
    #心拍数のセット
    def set_heart(self, heart_value: str):
        self.heart = heart_value
    #心拍数を取得
    def get_heart(self):
        return self.heart
    
    def get_topicId(self):
        return self.topicId

    def set_topicId(self, index, value):
        # 必要に応じてリストの長さを拡張
        while len(self.topicId) <= index:
            self.topicId.append([])  # 空のリストを追加
        self.topicId[index].append(value)  # 指定インデックスに値を追加

    
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
    
    def get_okCount(self):
        return self.okCount
    
    def set_okCount(self,value:int):
        self.okCount = value  
    
    def allReset(self):
        self.heart = '0'  # 初期心拍数
        self.name1= "null"
        self.name2= "null"
        self.deviceId_1= "null"
        self.deviceId_2= "null"
        self.count = 0
        self.status = "iteration"
        self.okCount = 0
        self.indexCount1 = 0
        self.indexCount2 = 0
        self.topicId = []