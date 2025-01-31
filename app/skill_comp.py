from app.skill_base import raw2keymouse
from app.skill_atom import (
    click_img
)
from app.raw import (
    raw_wanjie,
    raw_wanjie_l,
    raw_jianshi,
)
from utils.common import random_sleep
import pyautogui
import time

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

def auto_jianshi_ocr(cnt = 7):
    """
    param cnt: 门票数量
    """
    while cnt >= 8:
        cnt -= 8

        pyautogui.press("d")
        random_sleep(0.2)

        click_img("yj_1")
        click_img("open")


        