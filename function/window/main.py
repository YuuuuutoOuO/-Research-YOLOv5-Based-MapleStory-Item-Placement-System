import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2

class LiveImageDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Real-time Image Display")
        self.root.geometry("1920x1080")
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

    def update_image(self, img_array):
        """
        接收一個透過 OpenCV 取得的 NumPy 陣列影像（BGR格式），
        先轉為 PIL Image 再顯示至 Tkinter 視窗。
        
        注意：不要在此函式呼叫 root.update() 或 root.update_idletasks()，
        讓 mainloop() 自然處理事件。
        """
        if isinstance(img_array, np.ndarray):
            # OpenCV BGR -> RGB
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(img_rgb)
        else:
            pil_image = img_array

        tk_image = ImageTk.PhotoImage(pil_image)
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image

    def run(self):
        self.root.mainloop()

# 模擬外部更新影像的方式
if __name__ == '__main__':
    display = LiveImageDisplay()
    
    # 在外部程式中取得影像後，使用 after(0, ...) 更新 GUI
    def mock_external_update():
        # 模擬取得新影像
        img = cv2.imread("C:/Users/corps/Pictures/f7c7bbca22d2dc54977ccdc21b28d405.jpg")  # 請自行提供圖片路徑
        # 將更新作業以事件的方式丟回主線程
        display.root.after(0, display.update_image, img)
        
        # 若需持續更新，可再次排程 mock_external_update()
        display.root.after(1000, mock_external_update)  # 每秒更新一次

    # 啟動週期性更新
    mock_external_update()

    display.run()
