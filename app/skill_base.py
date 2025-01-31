import pyautogui
from utils.common import random_sleep
from pynput.mouse import Button, Controller
import time

mouse = Controller()

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