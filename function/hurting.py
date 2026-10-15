import numpy as np
import pyautogui
import time
import random

class Hurting():
    def __init__(self):
        # 初始化參數
        self.status = True # 當前狀態，True:待機 False: 狩獵中
        self.command = []
        self.map = [] # 記錄當前地圖
        self.obj = [] # 紀錄當前物件
        self.att_range = {'x':80, 'y':150}
        # 動態加載參數
        self.monster = ''
        self.player = ''
        self.mon_label = ''
        self.mon_y, self.mon_x = 0, 0
        self.ply_y, self.ply_x = 0, 0
        self.facing = ''

    def main(self, map, obj):
        # 初始化
        self.map = map
        self.obj = obj

        # 取得資料
        self.monster = self.obj['Monster']
        self.player = self.obj['Player']
        self.mon_label = self.monster[0]['label']
        self.mon_y, self.mon_x = self.monster[0]['center']
        self.ply_y, self.ply_x = self.player[0]['center']

        # 判斷行動
        if self.mon_label == '0':
            return None
        if self.moving():
            return None
        if self.att():
            return None
############################################
# 判斷行動
    def moving(self): # 計算路徑與移動
        if abs(self.mon_y-self.ply_y)<self.att_range['y']: # 判斷是否可以攻擊
            return False
        if abs(self.mon_x-self.ply_x)>self.att_range['x']: # 判斷是否可以攻擊
            return False
        # 同平台
        print(f'moving: {abs(self.mon_y-self.ply_y)} {self.att_range['y']}')

        self.ctrl_searching()
        # 高處
        # 低處
        return True
    
    def att(self):
        if abs(self.mon_y-self.ply_y)>self.att_range['y']: # 判斷是否可以攻擊
            return False
        if abs(self.mon_x-self.ply_x)>self.att_range['x']: # 判斷是否可以攻擊
            return False
        # 判斷方向
        self.ctrl_facing()

        # 判斷是否為可攻擊距離
        self.ctrl_att()
        return True

############################################
# 行動相關參數
    # 執行指令
    def execute_command(self, key, times, source):
        times = times+random.uniform(0.000001, 0.00001) # 加入隨機值，避免被封鎖
        times = times if times <=1 else 1 # 避免長時間霸佔輸入
        pyautogui.keyDown(key)
        time.sleep(times)
        pyautogui.keyUp(key)
        print(f'Exe- Key: {key} Times: {times} Source:{source}')

    # 面對怪物方向
    def ctrl_facing(self):        
        if self.mon_y > self.ply_y and self.facing == 'left':
            self.execute_command('right', 0, 'ctrl_facing')
            self.facing = 'right'
            return None
        if self.mon_y > self.ply_y and self.facing == 'right':
            self.execute_command('left', 0, 'ctrl_facing')
            self.facing = 'left'
            return None

    def ctrl_att(self):
        # print(self.monster[0]['center'], self.player[0]['center'], abs(self.mon_y-self.ply_y))
        self.execute_command('z', 0.2, 'ctrl_att')
        
    def ctrl_searching(self):
        # 假設為同平台
        moving = (self.mon_y-self.ply_y)/11 
        if moving<0:
            moving = moving+1
            self.execute_command('left', abs(moving)*0.1, 'ctrl_searching')
            return None
        moving = moving-1
        self.execute_command('right', abs(moving)*0.1, 'ctrl_searching')