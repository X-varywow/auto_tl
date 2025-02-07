import json
import time
from pynput import mouse, keyboard

recorded_events = []
start_time = time.time()
mouse_press_times = {}

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
    if key == keyboard.Key.esc:
        return False

mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

# keyboard_listener.join()
# mouse_listener.stop()

# with open("recorded_events.json", "w") as file:
#     json.dump(recorded_events, file, indent=4)

print("Recording saved to recorded_events.json")

# Playback functionality
# def replay_events():
#     with open("recorded_events.json", "r") as file:
#         events = json.load(file)
    
#     mouse_controller = mouse.Controller()
#     keyboard_controller = keyboard.Controller()
#     start_time = time.time()
    
#     for event in events:
#         time.sleep(max(0, event['time'] - (time.time() - start_time)))
        
#         if event['type'] == 'mouse_click':
#             button = getattr(mouse.Button, event['button'].split('.')[-1])
#             if event['pressed']:
#                 mouse_controller.press(button)
#             else:
#                 mouse_controller.release(button)
#                 time.sleep(event.get('duration', 0))  # 模拟按压时长
#         elif event['type'] == 'mouse_move':
#             mouse_controller.position = (event['x'], event['y'])
#         elif event['type'] == 'mouse_scroll':
#             mouse_controller.scroll(event['dx'], event['dy'])
#         elif event['type'] == 'key_press':
#             key = eval(event['key'])
#             keyboard_controller.press(key)
#         elif event['type'] == 'key_release':
#             key = eval(event['key'])
#             keyboard_controller.release(key)

# if __name__ == "__main__":
#     replay_events()
