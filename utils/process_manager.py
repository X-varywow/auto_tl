import multiprocessing
from multiprocessing import Manager
import time
from tabulate import tabulate
from utils.common import random_sleep

# manager_dict = Manager().dict()

class TaskManager:
    def __init__(self, shared_dict):
        self.tasks = shared_dict                 # 存储任务的状态和线程信息
        self.lock = multiprocessing.Lock()    # 保护任务状态dict的并发安全

    def add_task(self, task_name, task_function, sleep_time=1):
        """添加新任务"""
        if task_name in self.tasks:
            print(f"Task '{task_name}' already exists.")
            return

        # 创建任务状态
        task_info = {
            "running": False,  # 任务是否开启
            "process": None,    # 进程对象
            "stop_event": multiprocessing.Event(),  # 后续循坏判定的标识，通过内存地址绑定到对应的
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

            # 创建并启动进程
            process = multiprocessing.Process(
                target=self._task_wrapper,
                args=(task_name,)
            )
            task_info["process"] = process
            process.start()
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

            # 设置停止事件并等待进程结束
            task_info["stop_event"].set()
            task_info["process"].join()
            task_info["running"] = False
            print(f"Task '{task_name}' stopped.")

    def _task_wrapper(self, task_name):
        """任务执行包装器，用于循环执行任务"""
        task_info = self.tasks[task_name]
        stop_event = task_info["stop_event"]
        task_function = task_info["function"]
        sleep_time = task_info["sleep_time"]

        while not stop_event.is_set():
            task_function()  # 执行任务
            random_sleep(sleep_time)    # 模拟任务间隔

    def list_tasks(self):
        """以表格形式列出当前任务的状态"""
        with self.lock:
            data = []
            for task_name, task_info in self.tasks.items():
                status = "Running" if task_info["running"] else "Stopped"
                process_status = (
                    "Alive" if task_info["process"] and task_info["process"].is_alive() else "Not Started"
                )
                data.append([task_name, status, process_status])

            # 打印表格
            headers = ["Task Name", "Status", "Process Status"]
            print(tabulate(data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":

    manager_dict = Manager().dict()
    # 示例任务函数
    def cpu_intensive_task():
        # 模拟一个 CPU 密集型任务
        result = sum(i * i for i in range(10**6))
        print(f"Computed result: {result}")

    # 使用任务管理器
    manager = TaskManager(manager_dict)

    # 添加任务
    manager.add_task("task1", cpu_intensive_task)
    manager.add_task("task2", cpu_intensive_task)

    # 启动和停止任务
    manager.start_task("task1")
    manager.start_task("task2")
    time.sleep(5)  # 模拟任务运行一段时间
    manager.list_tasks()

    manager.stop_task("task1")
    manager.list_tasks()

    manager.stop_task("task2")
    manager.list_tasks()
