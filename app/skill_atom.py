import pyautogui
import time


# 150ms
def click_img(img):
    img_path = f"img/{img}.png"
    try:
        # 使用 locateOnScreen 查找图片位置
        location = pyautogui.locateOnScreen(img_path, confidence=0.8)  # confidence 参数需要 OpenCV
        if location is not None:
            # 获取图片的中心点坐标
            center = pyautogui.center(location)
            x, y = center.x, center.y

            # 打印坐标
            print(f"找到图片{img_path}，位置为: ({x}, {y})")

            # 移动鼠标并点击
            pyautogui.moveTo(x, y, duration=0.5)  # 移动到目标位置
            pyautogui.click()  # 点击
        else:
            print(f"未找到图片 {img_path}")
    except Exception as e:
        print(f"发生错误: {e}")