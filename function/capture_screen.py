'''
擷取當前螢幕
'''
import mss
import numpy as np
import cv2
import pytesseract
import re

class Caputre_Screen(): 
    # 初始化
    def __init__(self, screen_number, tesseract_dir, value_coordinate):
        self.screen_number = screen_number
        self.value_coordinate = value_coordinate
        self.img = []
        self.last_value = {'hp':'0', 'mp':'0', 'exp':'0'}

    # 擷取螢幕
    def get_caputre(self):
        screen_number = self.screen_number
        # 使用 mss 擷取螢幕畫面
        with mss.mss() as sct:
            # 獲取所有顯示器的相關資訊
            monitors = sct.monitors

            # 確認螢幕號碼有效
            if screen_number < 1 or screen_number > len(monitors) - 1:
                print(f"螢幕 {screen_number} 不存在！默認擷取主螢幕。")
                screen_number = 1

            # 獲取指定螢幕的範圍
            monitor = monitors[screen_number]

            # 擷取指定螢幕
            screenshot = sct.grab(monitor)

            # 將擷取的畫面轉換為 NumPy 陣列
            img = np.array(screenshot)

            # 將 BGRA 轉換為 BGR，這樣我們就可以用 OpenCV 處理
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

            self.img = img

    # 取得腳色當前素質
    def get_value(self):
        # 設定 Tesseract 的路徑（如果你是 Windows 並且 Tesseract 沒有在 PATH 中）
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        value_coordinate = self.value_coordinate
        img = self.img
        last_exp = self.last_value['exp']

        # 剪裁下方的 HP, MP, EXP 區域
        hp_coor = value_coordinate['hp']
        mp_coor = value_coordinate['mp']
        exp_coor = value_coordinate['exp']
        hp_region = img[hp_coor[0]:hp_coor[1], hp_coor[2]:hp_coor[3]]  # 裁剪出 HP 條的位置
        mp_region = img[mp_coor[0]:mp_coor[1], mp_coor[2]:mp_coor[3]]  # 裁剪出 MP 條的位置
        exp_region = img[exp_coor[0]:exp_coor[1], exp_coor[2]:exp_coor[3]]  # 裁剪出 EXP 條的位置

        # 轉換為灰階以便進行 OCR
        hp_gray = cv2.cvtColor(hp_region, cv2.COLOR_BGR2GRAY)
        mp_gray = cv2.cvtColor(mp_region, cv2.COLOR_BGR2GRAY)
        exp_gray = cv2.cvtColor(exp_region, cv2.COLOR_BGR2GRAY)

        # 使用 Tesseract 進行文字識別，使用 psm 7 進行單行識別
        hp_text = pytesseract.image_to_string(hp_gray, config='--psm 7') 
        mp_text = pytesseract.image_to_string(mp_gray, config='--psm 7')
        exp_text = pytesseract.image_to_string(exp_gray, config='--psm 7')
        # 去除所有非文字的資訊，保留數字和字母
        hp_text = re.sub(r'[^0-9A-Za-z]', '', hp_text)
        mp_text = re.sub(r'[^0-9A-Za-z]', '', mp_text)
        exp_text = re.sub(r'[^0-9A-Za-z]', '', exp_text)
        print(f'HP: {hp_text} MP: {mp_text} EXP: {exp_text} ({int(exp_text)-int(last_exp)})')
        # 更新資訊
        self.last_value['exp'] = exp_text

        return {'HP': hp_text, 'MP': mp_text, 'EXP': exp_text}

        # # Debug
        # # 顯示裁剪的區域以便檢查
        # cv2.imshow("HP Region", hp_gray)
        # cv2.imshow("MP Region", mp_gray)
        # cv2.imshow("EXP Region", exp_gray)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
