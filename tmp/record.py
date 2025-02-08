"""
2025.02.08 测试功能正常; 格式相较于上版本更全，且记录按压时长；用 json 保存，不用手动；
"""

import json
import time
import os
import pyautogui
from pynput import mouse, keyboard

recorded_events = []
start_time = time.time()
mouse_press_times = {}

mouse_controller = mouse.Controller()
keyboard_controller = keyboard.Controller()

def on_click(x, y, button, pressed):
    event_time = time.time() - start_time
    if pressed:
        mouse_press_times[button] = event_time  # 记录按下时间
    else:
        press_duration = event_time - mouse_press_times.get(button, event_time)
        raw = {
            'type': 'mouse_click',
            'time': event_time,
            'x': x,
            'y': y,
            'button': str(button),
            'pressed': pressed,
            'duration': press_duration  # 记录按压时长
        }
        recorded_events.append(raw)
        print(raw)

def on_move(x, y):
    raw = {
        'type': 'mouse_move',
        'time': time.time() - start_time,
        'x': x,
        'y': y
    }
    recorded_events.append(raw)
    print(raw)

def on_scroll(x, y, dx, dy):
    raw = {
        'type': 'mouse_scroll',
        'time': time.time() - start_time,
        'x': x,
        'y': y,
        'dx': dx,
        'dy': dy
    }
    recorded_events.append(raw)
    print(raw)

def on_press(key):
    global recorded_events
    if key == keyboard.Key.f6:
        print("F6键被按下，保存录制。")
        with open("./records/recorded_events.json", "w") as file:
            json.dump(recorded_events, file, indent=4)
        recorded_events = []
    if key == keyboard.Key.f5:
        print("F5键被按下，程序正常退出。")
        keyboard_listener.stop()
        mouse_listener.stop()
        os._exit(0)  # 退出程序; 其他地方调用也生效
    raw = {
        'type': 'key_press',
        'time': time.time() - start_time,
        'key': str(key)
    }
    recorded_events.append(raw)
    print(raw)

def on_release(key):
    raw = {
        'type': 'key_release',
        'time': time.time() - start_time,
        'key': str(key)
    }
    recorded_events.append(raw)
    print(raw)

    # false 会停止监听当前事件
    # if key == keyboard.Key.esc:
    #     return False
    

def replay_events(events):
    start_time = time.time()
    
    for event in events:
        time.sleep(max(0, event['time'] - (time.time() - start_time)))
        
        if event['type'] == 'mouse_click':
            pyautogui.moveTo(event['x'], event['y'], 0.1, pyautogui.easeInQuad)
            button = getattr(mouse.Button, event['button'].split('.')[-1])
            if event['pressed']:  # 不会有。。。
                mouse_controller.press(button)
            else:
                mouse_controller.press(button)
                time.sleep(event.get('duration', 0))  # 模拟按压时长
                mouse_controller.release(button)
        # elif event['type'] == 'mouse_move':
        #     mouse_controller.position = (event['x'], event['y'])
        elif event['type'] == 'mouse_scroll':
            mouse_controller.scroll(event['dx'], event['dy'])
        elif event['type'] == 'key_press':
            key = eval(event['key'])
            keyboard_controller.press(key)
        elif event['type'] == 'key_release':
            key = eval(event['key'])
            keyboard_controller.release(key)

def reduce_json_t(file_path, t = 5):
    with open(file_path, "r") as file:
        events = json.load(file)

    res = []
    for event in events:
        event['time'] -= t
        res.append(event)
    with open(file_path, "w") as file:
        json.dump(res, file, indent=4)


mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll) # on_move=on_move, 
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

# 引用的时候就会启动两个监听的线程
mouse_listener.start()
keyboard_listener.start()

# keyboard_listener.join()
# mouse_listener.stop()

print("Recording started...")


if __name__ == "__main__":
    mode = 2
    file_path = "./records/k7jianshi1.json"

    if mode == 1:
        # 功能1:录制
        time.sleep(1000)
    elif mode == 2:
        # 功能2:回放
        with open(file_path, "r") as file:
            events = json.load(file)
        for i in range(100):
            replay_events(events)
    else:
        # 功能3:编辑时间
        reduce_json_t(file_path, t = 29)