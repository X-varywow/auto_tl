from PIL import ImageGrab
from paddleocr import PaddleOCR
import numpy as np
import pyautogui

ocr_client = PaddleOCR()

def ocr_loot():
    res = {}

    screen_width, screen_height = pyautogui.size()
    scan_region = (screen_width - 300, screen_height - 200, screen_width, screen_height)

    screenshot = ImageGrab.grab(bbox=scan_region)
    img_array = np.array(screenshot)
    text = ocr_client.ocr(img_array, det=False, cls=False)
    
    for line in text.splitlines():
        if line.strip():  # 忽略空行
            res[line.strip()] += 1

    return res


def auto_trade(amount_limit, cost_limit, page_limit = 30):
    res = []
    page_cnt = 0

    def check_end():
        ocr_end()

    while check_end() and page_cnt < page_limit:
        page_cnt += 1
        data = ocr_window()
        res.append(data)

    res.sort()
    while check_begin():
        buy(res[0], amount_limit, cost_limit)
