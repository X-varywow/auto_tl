import threading
import time
from tabulate import tabulate
from utils.common import random_sleep

class TaskManager:
    def __init__(self):
        self.tasks = {}                 # 存储任务的状态和线程信息
        self.lock = threading.Lock()    # 保护任务状态dict的并发安全

    def add_task(self, task_name, task_function, sleep_time=1):
        """添加一个新任务"""
        if task_name in self.tasks:
            print(f"Task '{task_name}' already exists.")
            return
        
        # 创建任务状态
        task_info = {
            "running": False,  # 任务是否开启
            "thread": None,    # 任务线程
            "stop_event": threading.Event(),  # 后续循坏判定的标识，通过内存地址绑定到对应的
            "function": task_function,  # 任务的执行函数
            "sleep_time": sleep_time
        }
        
        with self.lock:
            self.tasks[task_name] = task_info

    def start_task(self, task_name):
        """启动指定任务"""
        with self.lock:
            if task_name not in self.tasks:
                print(f"Task '{task_name}' does not exist.")
                return
            task_info = self.tasks[task_name]
            if task_info["running"]:
                print(f"Task '{task_name}' is already running.")
                return

            # 重置停止事件，设置任务为运行状态
            task_info["stop_event"].clear()
            task_info["running"] = True

            # 启动线程
            thread = threading.Thread(target=self._task_wrapper, args=(task_name,))
            thread.daemon = True  # 设置为守护线程，主线程退出时强制终止
            task_info["thread"] = thread
            thread.start()
            print(f"Task '{task_name}' started.")

    def stop_task(self, task_name):
        """停止指定任务"""
        with self.lock:
            if task_name not in self.tasks:
                print(f"Task '{task_name}' does not exist.")
                return
            task_info = self.tasks[task_name]
            if not task_info["running"]:
                print(f"Task '{task_name}' is not running.")
                return

            # 设置停止事件，等待线程退出
            task_info["stop_event"].set()

            # join 等待线程完成；
            # 不等待，可能主线程提前退出，无法拿到子线程的结果，或文件句柄被关闭，影响子线程
            task_info["thread"].join()
            task_info["running"] = False
            print(f"Task '{task_name}' stopped.")

    def _task_wrapper(self, task_name):
        """任务执行的包装器，用于循环执行任务"""
        task_info = self.tasks[task_name]
        stop_event = task_info["stop_event"]
        task_function = task_info["function"]
        sleep_time = task_info["sleep_time"]

        while not stop_event.is_set():
            task_function()  # 执行任务
            random_sleep(sleep_time)  # 模拟任务间隔，可根据需求调整

    def list_tasks(self):
        """列出当前任务的状态"""
        with self.lock:
            data = []
            for task_name, task_info in self.tasks.items():
                status = "Running" if task_info["running"] else "Stopped"
                thread_status = (
                    "Alive" if task_info["thread"] and task_info["thread"].is_alive() else "Not Started"
                )
                data.append([task_name, status, thread_status])
            
            # 打印表格
            headers = ["Task Name", "Status", "Thread Status"]
            print(tabulate(data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    # 示例任务函数
    def task1():
        print("Task 1 is running...")

    def task2():
        print("Task 2 is running...")

    def task3():
        print("Task 3 is running...")

    # 使用任务管理器
    manager = TaskManager()

    # 添加任务
    manager.add_task("task1", task1)
    manager.add_task("task2", task2)
    manager.add_task("task3", task3)

    # 启动和停止任务
    manager.start_task("task1")
    manager.start_task("task2")
    time.sleep(5)  # 模拟任务运行一段时间
    manager.stop_task("task1")
    manager.list_tasks()

    time.sleep(3)
    manager.stop_task("task2")
    manager.list_tasks()

    # 启动另一个任务
    manager.start_task("task3")
    time.sleep(4)
    manager.stop_task("task3")
