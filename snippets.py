#-*- coding:utf-8 -*-

"""
Author: Joel Ermantraut
Last Modification: 22/01/2020
Python Version: 3.9.1
Last Working Test: 10/02/2019

Classic snippets utility. Registers each keystroke
and a special trigger, that when is press, search
in the last keys a registered combination, and
rewrite the associated string if exists.
"""

from pynput import mouse
from pynput import keyboard
from time import sleep
import json
import os

key_logger_len = 10
key_logger = ['\0' for i in range(key_logger_len)]
disparador = "<ctrl>+<space>"

snippets_filename = os.getcwd() + "/.config/scripts/snippets.json"

snippets_list = dict()

keyboard_modifiers = [
    keyboard.Key.alt,
    keyboard.Key.alt_gr,
    keyboard.Key.alt_l,
    keyboard.Key.alt_r,
    keyboard.Key.cmd,
    keyboard.Key.cmd_l,
    keyboard.Key.cmd_r,
    keyboard.Key.ctrl,
    keyboard.Key.ctrl_l,
    keyboard.Key.ctrl_r,
    keyboard.Key.shift,
    keyboard.Key.shift_l,
    keyboard.Key.shift_r,
]

keyboard_special = [
    keyboard.Key.enter,
    keyboard.Key.backspace,
    keyboard.Key.caps_lock,
    keyboard.Key.delete,
    keyboard.Key.down,
    keyboard.Key.end,
    keyboard.Key.esc,
    keyboard.Key.home,
    keyboard.Key.insert,
    keyboard.Key.left,
    keyboard.Key.media_next,
    keyboard.Key.media_play_pause,
    keyboard.Key.media_previous,
    keyboard.Key.media_volume_down,
    keyboard.Key.media_volume_mute,
    keyboard.Key.media_volume_up,
    keyboard.Key.menu,
    keyboard.Key.num_lock,
    keyboard.Key.page_down,
    keyboard.Key.page_up,
    keyboard.Key.pause,
    keyboard.Key.print_screen,
    keyboard.Key.right,
    keyboard.Key.scroll_lock,
    keyboard.Key.up,
    keyboard.Key.f1,
    keyboard.Key.f2,
    keyboard.Key.f3,
    keyboard.Key.f4,
    keyboard.Key.f5,
    keyboard.Key.f6,
    keyboard.Key.f7,
    keyboard.Key.f8,
    keyboard.Key.f9,
    keyboard.Key.f10,
    keyboard.Key.f11,
    keyboard.Key.f12,
    keyboard.Key.f13,
    keyboard.Key.f14,
    keyboard.Key.f15,
    keyboard.Key.f16,
    keyboard.Key.f17,
    keyboard.Key.f18,
    keyboard.Key.f19,
    keyboard.Key.f20,
    keyboard.Key.space,
    keyboard.Key.tab,
]

key_controller = keyboard.Controller()

def add_logger(key_logger, key):
    if str(key) == "<65027>":
        return key_logger
    # Alt key not working well in this module

    for i in range(key_logger_len - 1):
        key_logger[i] = key_logger[i + 1]

    key_logger[-1] = key

    return key_logger

def on_press(key):
    global key_logger

    if key not in keyboard_modifiers and key not in keyboard_special:
        key_logger = add_logger(key_logger, key)

def on_disparador():
    global key_logger, snippets_list, key_controller

    for snippet in snippets_list.keys():
        success = 1
        for key_index in range(len(snippet)):
            key_char = snippet[key_index]
            new_list = key_logger[-len(snippet):]

            key_code = keyboard.KeyCode(char=key_char)
            if key_code.char != new_list[key_index].char:
                success = 0
                break

        if success:
            sleep(0.25)

            for i in range(len(snippet)):
                key_controller.tap(keyboard.Key.backspace)

            key_controller.type(snippets_list[snippet])

def load_snippets_file(filename):
    with open(filename, "r") as file:
        return json.load(file)

def set_snippets_listener():
    global disparador, snippets_filename, snippets_list

    snippets_list = load_snippets_file(snippets_filename)

    key_listener = keyboard.Listener(
        on_press=on_press)
    key_listener.start()

    with keyboard.GlobalHotKeys({
            disparador: on_disparador}) as h:
        h.join()

if __name__ == "__main__":
    set_snippets_listener()
