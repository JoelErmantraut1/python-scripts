# -*- coding:utf-8 -*-

"""
Author: Joel Ermantraut
Last Modification: 22/01/2020
Python Version: 3.9.1
Last Working Test: 22/01/2020

When double alt is pressed, activates for some seconds
the fast scroll function, where the scroll works N times
faster than usual.
"""

from pynput import keyboard, mouse
from threading import Timer

ctrl_key = keyboard.Key.alt
ctrl_times = 0
fast_scroll = False
time_interval = 5.0 # Time after desactivates fast scroll
time_ctrl_out = 0.5 # Max time between ctrl press
timer = None
times_faster = 2 # N times faster scroll
last_dy = 0
mouse_controller = mouse.Controller()

def ctrl_time_out():
    global ctrl_times

    ctrl_times = 0

def on_press(key):
    global ctrl_times, fast_scroll, time_interval, ctrl_key, timer

    if timer:
        timer.cancel()

    if key == ctrl_key:
        ctrl_times += 1
        if ctrl_times >= 2:
            ctrl_times = 0
            fast_scroll = not(fast_scroll)
        else:
            timer = Timer(time_ctrl_out, ctrl_time_out)
            timer.start()

    elif key == keyboard.Key.esc:
        return False

def on_scroll(x, y, dx, dy):
    global last_dy, fast_scroll, times_faster, ctrl_times, mouse_controller

    if last_dy < 0 and dy > 0 or last_dy > 0 and dy < 0:
        ctrl_times = 0
        fast_scroll = False
        last_dy = 0
        return

    if fast_scroll:
        dy = (times_faster - 1) * dy
        mouse_controller.scroll(dx, dy)

    last_dy = dy

def main():
    listener = mouse.Listener(
        on_scroll=on_scroll)
    listener.start()

    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
