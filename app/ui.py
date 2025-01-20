from utils.thread_manager import TaskManager
import keyboard
import customtkinter

manager = TaskManager()
global_btn = {}


"""
part1. 控件
"""


class CommonButton:
    """
    启动一个线程，完成传入的 func, 并提供开关，绑定按键;
    通用的功能注册，都用按键形式完成；

    params; time_sleep; if None, means call once per click;
    """

    def __init__(self, root, info, key, func, time_sleep=None):
        self.button = customtkinter.CTkButton(root, text=f"{info} ON", command=self.ToggleButton)
        self.button.grid(row=0, column=len(global_btn), padx=10, pady=10, sticky="w")
        global_btn[key] = self.button

        self.run = False
        self.info = info
        time_sleep = time_sleep if time_sleep else 999999

        manager.add_task(
            task_name = info,
            task_function = func,
            sleep_time = time_sleep

        )
        manager.start_task(info)

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
part2. panel
"""