import cv2
import numpy as np
import pyautogui

img_path = r"C:\Users\Administrator\Desktop\auto_tl\img\yj_1.png"

# 截取屏幕
screenshot = pyautogui.screenshot()
screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# 加载目标图片
template = cv2.imread(img_path, cv2.IMREAD_COLOR)

# 获取模板图片的宽度和高度
h, w = template.shape[:2]

# 使用 OpenCV 进行模板匹配
result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

# 获取最大匹配值和位置
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# 设置置信度阈值
confidence_threshold = 0.8
if max_val >= confidence_threshold:
    # 获取匹配位置
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # 计算中心点
    center_x = (top_left[0] + bottom_right[0]) // 2
    center_y = (top_left[1] + bottom_right[1]) // 2

    # 打印结果
    print(f"找到图片 a.png，位置为: ({center_x}, {center_y})，置信度: {max_val:.2f}")

    # 移动鼠标并点击
    pyautogui.moveTo(center_x, center_y, duration=0.5)
    # pyautogui.click()
    print("已点击目标位置。")
else:
    print(f"未找到图片 a.png，最大置信度: {max_val:.2f}")