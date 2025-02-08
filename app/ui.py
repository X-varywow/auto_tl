from utils.thread_manager import TaskManager
from collections import defaultdict
import keyboard
import customtkinter
from app.skill_ocr import ocr_scan
from app.skill_comp import (
    auto_pick,
    auto_wanjie,
    auto_jianshi_ocr
)
import time
import os
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput import keyboard as pykeyboard
import threading
from pynput.mouse import Button, Controller

manager = TaskManager()
global_btn = {}



"""
监听键鼠事件，并设置退出
"""

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
            log_to_panel(f"['key', {str(key)}, {cur_t-global_record_t}]")
        else:
            log_to_panel(f"['key', '{str(key)}', {cur_t-global_record_t}]")
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
        log_to_panel(f"['click', ({x}, {y}, '{button}'), {cur_t-global_record_t}]")
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
part1. panel
"""

class LogPanel:
    def __init__(self, root):
        self.text = customtkinter.CTkTextbox(root, height=30, state="disabled")
        self.text.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def log(self, msg):
        self.text.configure(state="normal")
        self.text.insert("end", msg + "\n")
        self.text.yview("end")
        self.text.configure(state="disabled")

log_panel = None

def log_to_panel(msg):
    if log_panel:
        log_panel.log(msg)
    else:
        print(msg)



items = defaultdict(int)

class ItemPanel:
    def __init__(self, root):
        self.text = customtkinter.CTkTextbox(root, height=10, state="disabled")
        self.text.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def update_items(self, items):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        for item, count in items.items():
            self.text.insert("end", f"{item}: {count}\n")
        self.text.yview("end")
        self.text.configure(state="disabled")


class BtnPanel(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)



"""
part2. 控件
"""


class CommonButton:
    """
    启动一个线程，完成传入的 func, 并提供开关，绑定按键;
    通用的功能注册，都用按键形式完成；

    params; time_sleep; if None, means call once per click;
    """

    def __init__(self, root, info, key, func, time_sleep=None):
        self.button = customtkinter.CTkButton(root, text=f"{info} ON", command=self.ToggleButton)
        self.button.grid(row=len(global_btn)//2, column=len(global_btn)%2, padx=10, pady=10, sticky="w")
        global_btn[key] = self.button

        self.run = False
        self.info = info
        time_sleep = time_sleep if time_sleep else 999999

        manager.add_task(
            task_name = info,
            task_function = func,
            sleep_time = time_sleep

        )
        # manager.start_task(info)
        keyboard.add_hotkey(key, self.ToggleButton)  # 绑定快捷键

    def ToggleButton(self):
        if self.run:
            self.run = False
            manager.stop_task(self.info)
            self.button.configure(text=f"{self.info} ON")
            log_to_panel(f"{self.info} 已关闭")
        else:
            self.run = True
            manager.start_task(self.info)
            self.button.configure(text=f"{self.info} STOP")
            log_to_panel(f"{self.info} 已打开")


"""
part3. 主程
"""

if __name__ == "__main__":

    # 创建窗口
    root = customtkinter.CTk()
    root.geometry("400x300")
    root.title("AutoTorchlight")

    # 设置日志面板
    btn_panel = BtnPanel(root)
    log_panel = LogPanel(root)
    item_panel = ItemPanel(root)

    # 添加功能按钮
    CommonButton(btn_panel, "自动拾取", "f12", auto_pick, time_sleep=0.15)
    CommonButton(btn_panel, "实时扫描", "f11", ocr_scan, time_sleep=2) 
    CommonButton(btn_panel, "自动K7万界", "f10", auto_wanjie, time_sleep=99999) 
    CommonButton(btn_panel, "自动K7监视", "f9", auto_jianshi_ocr, time_sleep=99999)

    # 调整布局
    # root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)  # 日志区域可扩展
    root.grid_rowconfigure(2, weight=1)  # 物品区域可扩展
    root.grid_columnconfigure(0, weight=1)

    # 窗口属性
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.88)
    root.mainloop()