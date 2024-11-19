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
        self.indexCount = 0
        self.indexCounts = 0
        self.indexStatus = 0
        # self.topicId = [[] for _ in range(4)]
        self.topicId = [0,0,0,0]
        self.topicArray1 = [[],[],[],[]]
        self.topicArray2 = [[],[],[],[]]
    def get_topicId(self):
        return self.topicId

    # def set_topicId(self, index, value):
    #     self.topicId[index].append(value)  # 指定インデックスに値を追加
    
    def get_topicArray1(self, index:int):
        return self.topicArray1[index] # インデックスが範囲外の場合、デフォルト値として None を返す

    def set_topicArray1(self, index:int, value:list):
        # 必要に応じてリストの長さを拡張
        self.topicArray1[index]= value  # 指定インデックスに値を追加
        
    def get_topicArray2(self,index:int):
        return self.topicArray2[index]

    def set_topicArray2(self,index:int, value:list):
        # 必要に応じてリストの長さを拡張
        self.topicArray2[index] = value  # 指定インデックスに値を追加
        
    def set_topicId(self, index: int, value: str):
        # インデックスがリストの範囲内かどうかをチェック
        if 0 <= index < len(self.topicId):
            self.topicId[index] = value
        else:
            print(f"Error: index {index} is out of range.")
            
    def set_name1(self, deviceId: str):
        self.name1 = deviceId
        
    def get_name1(self):
        return self.name1
    
    def set_name2(self, deviceId: str):
        self.name2 = deviceId
        
    def get_name2(self):
        return self.name2    
    
    def get_indexCount(self):
        return self.indexCount
    def set_indexCount(self,value):
        self.indexCount = value
        
    def get_indexCounts(self):
        return self.indexCounts
    def set_indexCounts(self,value):
        self.indexCounts = value
        
    def get_indexStatus(self):
        return self.indexStatus
    def set_indexStatus(self,value):
        self.indexStatus = value
    #心拍数のセット
    def set_heart(self, heart_value: str):
        self.heart = heart_value
    #心拍数を取得
    def get_heart(self):
        return self.heart
    
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
        
    def set_topicArrays(self,player:str,index:int,array:list):
        if player == "1":
            self.set_topicArray1(index,array)
            return {"player":player,"index": index,"array": array}
        elif player == "2":
            self.set_topicArray2(index,array)
            return {"player":player,"index": index,"array": array}
    
    def allReset(self):
        self.heart = '0'  # 初期心拍数
        self.name1= "null"
        self.name2= "null"
        self.deviceId_1= "null"
        self.deviceId_2= "null"
        self.count = 0
        self.status = "iteration"
        self.okCount = 0
        self.indexCount = 0
        self.indexCounts = 0
        self.indexStatus = 0
        # self.topicId = [[] for _ in range(4)]
        self.topicId = [0,0,0,0]
        self.topicArray1 = [[],[],[],[]]
        self.topicArray2 = [[],[],[],[]]
    def get_topicId(self):
        return self.topicId