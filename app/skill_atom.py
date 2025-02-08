import pyautogui
import time
from utils.common import random_sleep

# 150ms
def click_img(img, sleep_time=0):
    img_path = f"img/{img}.png"
    try_cnt = 3       # 设定重试，有时加载过程较长

    if sleep_time:
        random_sleep(sleep_time)
    try:
        for i in range(try_cnt):
            location = pyautogui.locateOnScreen(img_path, confidence=0.6)  # confidence 参数需要 OpenCV
            if location is not None:
                center = pyautogui.center(location)
                x, y = center.x, center.y

                print(f"找到图片{img_path}，位置为: ({x}, {y})")

                # 移动鼠标并点击
                pyautogui.moveTo(x, y, 0.2, pyautogui.easeInQuad)
                pyautogui.click()
                return 1
            else:
                print(f"未找到图片 {img_path}")

            time.sleep((i+1)*0.3)
    except Exception as e:
        raise e