import numpy as np
import cv2
import threading
import pyautogui

#
import time
import function.window.main as TK
import function.yolo.main as yolo
import function.capture_screen as capture_screen
import function.reward as get_reward
import function.keyboard as keyboard
import function.storage_status as storage_status
import function.process_obj as process_obj
import function.draw_map as draw_map
import function.hurting as hunting
import model.DQN_model as model
import test_fn
import setting

#########################

def init():
    global obj_cs, obj_hunting, obj_storage_status
    obj_cs = capture_screen.Caputre_Screen(screen_number=setting.screen_number, # 螢幕擷取
                                       tesseract_dir=setting.tesseract_dir, 
                                       value_coordinate=setting.value_coordinate)
    obj_hunting = hunting.Hurting()
    obj_storage_status = storage_status.Storage()

def input_thread_func(display):
    global screen_img
    while True:
        if screen_img is None:
            time.sleep(0.1) # 若還沒有影像就稍等一下
            continue

        # 使用 display.root.after() 讓影像更新在主執行緒中進行
        display.root.after(0, 
                            display.update_image,  
                            cv2.resize(screen_img, (1344, 756), interpolation=cv2.INTER_AREA)
                            # screen_img
                            )
def gui():
    obj_LD = TK.LiveImageDisplay()
    # 啟動一個執行緒在背景等候，並定期更新影像
    t = threading.Thread(target=input_thread_func, args=(obj_LD,), daemon=True)
    t.start()
    # 主執行緒進入 Tkinter 的主事件迴圈
    obj_LD.run()

def screen():
    global obj_cs

    while True:
        # 擷取螢幕
        obj_cs.get_caputre()
        time.sleep(screen_sec)
#####
def search_point(img, ply, mon):
    # 定義點的位置和顏色
    point_thickness = -1 # -1 表示填充整個圓點
    point_radius = 10 # 點的半徑

    try:
        print(mon)
        y1, x1 = mon['center']
        mon_position = (int(y1), int(x1))  # 點的位置 (x, y)
        mon_point = (0, 0, 255)    # 紅色 (B, G, R)
        cv2.circle(img, mon_position, point_radius, mon_point, point_thickness)
    except:
        None

    try:
        print(ply)
        y2, x2 = ply['center']
        ply_position = (int(y2), int(x2))  # 點的位置 (x, y)
        ply_point = (255, 0, 0)    # 紅色 (B, G, R)
        cv2.circle(img, ply_position, point_radius, ply_point, point_thickness)
    except:
        None

    return img
####
def main():
    global screen_img, screen_sec, obj_cs, obj_hunting, obj_storage_status
    obj_yolo_detect = yolo.Main() # Yolo檢測
    
    while True:
        time_start = time.time() # 紀錄開始時間

        _screen_img, result = obj_yolo_detect.load_image(obj_cs.img) # 取得YOLO檢測結果
        result = np.append(result, obj_storage_status.result_player)
        result = process_obj.main(result) # 處理與計算物件距離
        result = obj_storage_status.main(result)
        corrent_map = draw_map.main(obj=result)
        
        # 顯示當前目標位置
        try:
            screen_img = search_point(_screen_img, result['Player'][0], result['Monster'][0])
        except:
            screen_img = _screen_img

        # # 狩獵
        # try:
        #     obj_hunting.main(map=corrent_map, obj=result)
        # except:
        #     None
            
        # print(result)

        # 計算執行時間
        print(f'{time.time()-time_start}\n')
        np.savetxt('test.txt', corrent_map, fmt='%d') # 檢查地圖

        # time.sleep(0.1)

# 全域變數
screen_img = np.zeros((100,  100))
screen_size = [1920, 1080, 0.7] #寬 長 縮放倍率
screen_sec = 0.1 # 設定擷取速度(秒)
obj_cs = object # 螢幕擷取
obj_hunting = object # 狩獵
obj_storage_status = object # 暫存物件狀態

if __name__ == "__main__":
    # 初始化
    init()

    # 先啟動 GUI 和更新執行緒
    threading.Thread(target=gui, daemon=True).start()
    time.sleep(1) # 等待 GUI 初始化一段時間

    # 畫面擷取執行續
    threading.Thread(target=screen, daemon=True).start()


    # 執行 main
    main()
'''
1秒110個pixel
'''