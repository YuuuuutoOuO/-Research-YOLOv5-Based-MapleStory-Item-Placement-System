'''
鍵盤輸出
'''
import pyautogui
import time

def move_left():
    pyautogui.keyDown('left')
    time.sleep(0.1)
    pyautogui.keyUp('left')

def move_right():
    pyautogui.keyDown('right')
    time.sleep(0.1)
    pyautogui.keyUp('right')

def jump():
    pyautogui.press('up')

def attack():
    pyautogui.press('z')

def recover():
    pyautogui.press('q')