import customtkinter
from utils.tasks import TaskManager
from utils.common import (
    random_sleep
)
from loguru import logger

manager = TaskManager()

print(1)


# 创建窗口
root = customtkinter.CTk()
root.geometry("400x300")
root.title("AutoTorchlight")

# 设置日志面板
log_panel = LogPanel(root)
item_panel = ItemPanel(root)

# 添加功能按钮
CommonButton(root, "自动拾取", "f12", auto_pick, time_sleep=0.15)
CommonButton(root, "实时扫描", "f11", ocr_scan, time_sleep=2) 

# 调整布局
root.grid_rowconfigure(1, weight=1)  # 日志区域可扩展
root.grid_rowconfigure(2, weight=1)  # 物品区域可扩展
root.grid_columnconfigure(0, weight=1)

# 窗口属性
root.attributes("-topmost", True)
root.attributes("-alpha", 0.8)
root.mainloop()