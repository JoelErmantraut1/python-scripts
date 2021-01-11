#-*- coding:utf-8 -*-

"""
Controls volume with mouse wheel and Super key.

Super + Up = Increases volume
Super + Down = Decreases volume
Super + Middle Click = Mutes/Unmutes volume
"""

from pynput import mouse
from pynput import keyboard
import os

super_pressed = 0

volume_step = 2
mute_toggle_command = "amixer -D pulse sset Master toggle"
mute_off_command = "amixer -D pulse sset Master unmute"
volume_up_command = "amixer -D pulse sset Master {0}%+".format(volume_step)
volume_down_command = "amixer -D pulse sset Master {0}%-".format(volume_step)

# Volume commands

def on_click(x, y, button, pressed):
    if button == mouse.Button.middle and super_pressed and pressed:
        os.system(mute_toggle_command)

def on_scroll(x, y, dx, dy):
    global super_pressed

    if not super_pressed:
        return

    os.system(mute_off_command)
    if dy < 0:
        os.system(volume_down_command)
    else:
        os.system(volume_up_command)

def on_press(key):
    global super_pressed

    if key == keyboard.Key.cmd_l:
        super_pressed = 1

def on_release(key):
    global super_pressed

    if key == keyboard.Key.cmd_l:
        super_pressed = 0

def set_volume_controller():
    key_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    key_listener.start()

    with mouse.Listener(
        on_click=on_click,
        on_scroll=on_scroll) as listener:
        
        listener.join()

if __name__ == "__main__":
    set_volume_controller()