import main as TK
import cv2
import threading

def input_thread_func(display):
    while True:
        img_path = input('Path: ')
        if not img_path:
            # 如果輸入空字串代表結束
            break
        img = cv2.imread(img_path)
        if img is not None:
            # 使用 display.root.after() 讓影像更新在主執行緒中進行
            display.root.after(0, display.update_image, img)
        else:
            print("Image not found or invalid path.")

obj_LD = TK.LiveImageDisplay()

# 啟動一個執行緒在背景等候使用者輸入
t = threading.Thread(target=input_thread_func, args=(obj_LD,), daemon=True)
t.start()

# 主執行緒進入 Tkinter 的主事件迴圈
obj_LD.run()
