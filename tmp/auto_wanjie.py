
import customtkinter
import pyautogui
from pynput import keyboard as pykeyboard
import keyboard
import pynput
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Controller as MouseController

import threading
from loguru import logger
import os
import sys
import time
import random
from collections import defaultdict
from PIL import ImageGrab
# import pytesseract

from pynput.mouse import Button, Controller
import time

# 创建 Controller 实例
mouse = Controller()

global_record_t = time.time()
record_event = True

def on_press(key):
    global global_record_t, record_event
    if key == pykeyboard.Key.f5:  # 检测到按下 esc 键时退出程序
        print("F5键被按下，程序正常退出。")
        os._exit(0)  # 退出程序
    if record_event:
        cur_t = time.time()
        # event_log.append({
        #     'event': 'key_press',
        #     'key': str(key),
        #     'time': cur_t
        # })
        if str(key).startswith("'"):
            print(f"['key', {str(key)}, {cur_t-global_record_t}]")
        else:
            print(f"['key', '{str(key)}', {cur_t-global_record_t}]")
        global_record_t = cur_t

def on_click(x, y, button, pressed):
    global global_record_t, record_event
    if pressed and record_event:
        cur_t = time.time()
        # event_log.append({
        #     'event': 'mouse_click',
        #     'position': (x, y),
        #     'button': str(button),
        #     'time': cur_t
        # })
        print(f"['click', ({x}, {y}, '{button}'), {cur_t-global_record_t}]")
        global_record_t = cur_t

def start_listening():
    with (
        MouseListener(on_click=on_click) as mouse_listener,
        KeyboardListener(on_press=on_press) as keyboard_listener
    ):
        print("Recording started...")
        mouse_listener.join()
        keyboard_listener.join()

threading.Thread(target=start_listening).start()

"""
tmp: utils
"""
# 0.1 -> +-0.1
def get_random(ratio):
    return (random.random()-0.5)*ratio*2


def random_sleep(t, roll = 0.05):
    time.sleep(t + max(min(t*get_random(roll), 1), -1))


def raw2keymouse(s):
    """
    根据录制的事件文本，完成自动控制；适用于机械重复化的操作
    """
    for line in s.strip().split("\n"):
        press_t = 0.5
        func, pos, tt = eval(line)
        if type(tt) == tuple:
            sleep_t, press_t = tt
        else:
            sleep_t = tt
        random_sleep(sleep_t)
        if func == "click":
            x,y,btn = pos
            btn = btn.split(".")[-1]

            pyautogui.moveTo(x, y, 0.2, pyautogui.easeInQuad)

            if btn == 'left':
                mouse.press(Button.left)
                time.sleep(0.2)
                mouse.release(Button.left)
                # pyautogui.click(x=x, y=y)
            else:
                mouse.press(Button.right)  # 按下右键
                time.sleep(press_t)     # 右键移动，需要较长的时长
                mouse.release(Button.right)  # 松开右键
            # print(f"pyautogui.click(x={x}, y={y}, button={btn})")
        elif func == "key":
            pyautogui.press(pos)
            # print(f"pyautogui.press({pos})")
        else:
            print(f"error func: {func=}")

if __name__ == "__main__":
    from app.raw import *

    cnt = 3597
    while cnt >= 4:
        cnt -= 4
        raw2keymouse(raw_k7_jianshi)
    time.sleep(1000)
    # time.sleep(1)
    # pyautogui.click(x=1434, y=756, button='right')