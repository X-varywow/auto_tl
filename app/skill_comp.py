from app.skill_base import raw2keymouse
from app.skill_atom import (
    click_img
)
from app.raw import (
    raw_wanjie,
    raw_wanjie_l,
    raw_k7_jianshi,
    common_quit,
    common_into
)
from utils.common import random_sleep
import pyautogui
import time
from pynput.mouse import Button, Controller
mouse = Controller()

def auto_pick():
    pyautogui.press("a")

def auto_wanjie(cnt = 1000):
    """
    param cnt: 门票数量
    """
    while cnt >= 4:
        cnt -= 4
        raw2keymouse(raw_wanjie)
    time.sleep(1000)

def auto_jianshi(cnt = 9):
    while cnt >= 8:
        cnt -= 8
        raw2keymouse(raw_k7_jianshi)
    time.sleep(1000)


def auto_jianshi_ocr(cnt = 9):
    """
    param cnt: 门票数量
    """
    random_sleep(3)
    while cnt >= 8:
        cnt -= 8
        print(f"当前剩余门票： {cnt}")

        raw2keymouse(common_into)

        click_img("yj_1", 1)
        click_img("yj_1_boss", 2)
        click_img("open", 1)

        pyautogui.click()
        pyautogui.moveTo(970, 350, 0.2, pyautogui.easeInQuad)
        mouse.press(Button.right)  # 按下右键
        random_sleep(0.5)     # 右键移动，需要较长的时长
        mouse.release(Button.right)  # 松开右键

        random_sleep(10)
        raw2keymouse(common_quit)


if __name__ == "__main__":
    auto_jianshi()
