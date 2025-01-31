import win32gui
import time

def list_windows():
    top_windows = []
    win32gui.EnumWindows(enum_windows_callback, top_windows)

    for hwnd, title in top_windows:
        print(f"句柄: {hwnd}, 标题: {title}")

    return top_windows

def get_window_position(hwnd):
    # 获取窗口的矩形区域
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return (left, top), (right, bottom)

top_windows = list_windows()

def find_window(prefix="Torchlight:"):
    # 寻找窗口
    # hwnd = win32gui.FindWindow(None, title)
    # if hwnd:
    #     return hwnd
    # else:
    #     return None
    for hwnd, title in top_windows:
        if title.startswith(prefix):
            return hwnd


def enum_windows_callback(hwnd, top_windows):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != "":
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def is_window_active(hwnd):
    """
    检测窗口是否处于激活状态
    """
    active_hwnd = win32gui.GetForegroundWindow()
    return hwnd == active_hwnd

def check_active():
    hwnd = find_window()
    while not is_window_active(hwnd):
        print(f"应用窗口未激活")
        time.sleep(3)


if __name__ == "__main__":
    # list_windows()
    prefix="Torchlight:"
    hwnd = find_window()

    if hwnd:
        position = get_window_position(hwnd)
        print(f"窗口位置: {position}")
    else:
        print("没有找到窗口")