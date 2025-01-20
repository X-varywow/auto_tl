import win32gui

def get_window_position(hwnd):
    # 获取窗口的矩形区域
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    return (left, top), (right, bottom)

def find_window(title):
    # 寻找窗口
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        return hwnd
    else:
        return None

def enum_windows_callback(hwnd, top_windows):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != "":
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def list_windows():
    top_windows = []
    win32gui.EnumWindows(enum_windows_callback, top_windows)

    for hwnd, title in top_windows:
        print(f"句柄: {hwnd}, 标题: {title}")



if __name__ == "__main__":
    title = '窗口标题'
    hwnd = find_window(title)

    if hwnd:
        position = get_window_position(hwnd)
        print(f"窗口位置: {position}")
    else:
        print("没有找到窗口")