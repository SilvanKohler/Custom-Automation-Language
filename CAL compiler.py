from threading import Thread
from time import sleep

from pynput import keyboard as kb
from pynput import mouse
from pynput.keyboard import Key, KeyCode

hotkey = None
Thread = Thread
KeyCode = KeyCode


def rightclick(pos):
    mouse.position = tuple([int(x) for x in str(pos).replace(" ", "").split(",")])
    mouse.click(mouse.Button.right)


def leftclick(pos):
    mouse.position = tuple([int(x) for x in str(pos).replace(" ", "").split(",")])
    mouse.click(mouse.Button.left)


def press(key):
    key = str(key)
    key = keys.get(key, key)
    keyboard.press(key)


def release(key):
    key = str(key)
    key = keys.get(key, key)
    keyboard.release(key)


def Type(string):
    keyboard.type(str(string))


def wait(s):
    sleep(int(s))


init = \
"""
running = False
def prg():
"""
end = \
"""
def on_press(key):
\tglobal running, prg
\tif key == KeyCode.from_char(hotkey) or key == str(hotkey) or key == hotkey:
\t\trunning = not running
\t\tif running:
\t\t\tt = Thread(target=prg)
\t\t\tt.start()
listener = kb.Listener(on_press=on_press)
listener.start()
print(f"not running, press {hotkey} to run")
listener.join()
"""

keys = {
    "alt": Key.alt,
    "alt_gr": Key.alt_gr,
    "alt_l": Key.alt_l,
    "alt_r": Key.alt_r,
    "backspace": Key.backspace,
    "caps_lock": Key.caps_lock,
    "cmd": Key.cmd,
    "cmd_l": Key.cmd_l,
    "cmd_r": Key.cmd_r,
    "ctrl": Key.ctrl,
    "ctrl_l": Key.ctrl_l,
    "ctrl_r": Key.ctrl_r,
    "delete": Key.delete,
    "down": Key.down,
    "end": Key.end,
    "enter": Key.enter,
    "esc": Key.esc,
    "f1": Key.f1,
    "f2": Key.f2,
    "f3": Key.f3,
    "f4": Key.f4,
    "f5": Key.f5,
    "f6": Key.f6,
    "f7": Key.f7,
    "f8": Key.f8,
    "f9": Key.f9,
    "f10": Key.f10,
    "f11": Key.f11,
    "f12": Key.f12,
    "f13": Key.f13,
    "f14": Key.f14,
    "f15": Key.f15,
    "f16": Key.f16,
    "f17": Key.f17,
    "f18": Key.f18,
    "f19": Key.f19,
    "f20": Key.f20,
    "home": Key.home,
    "left": Key.left,
    "page_down": Key.page_down,
    "page_up": Key.page_up,
    "right": Key.right,
    "shift": Key.shift,
    "shift_l": Key.shift_l,
    "shift_r": Key.shift_r,
    "space": Key.space,
    "tab": Key.tab,
    "up": Key.up,
    "insert": Key.insert,
    "menu": Key.menu,
    "num_lock": Key.num_lock,
    "pause": Key.pause,
    "print_screen": Key.print_screen,
    "scroll_lock": Key.scroll_lock
}
language = {
    "print": "print",
    "rightclick": "rightclick",
    "leftclick": "leftclick",
    "press": "press",
    "release": "release",
    "type": "Type",
    "wait": "wait",
    "comment": "comment",
    "loop": "while running:",
    "hotkey": "hotkey"
}
none = ""
doublequote = '"'
quote = "'"
indent = 1
doublebackslash = "\\\\"

keyboard = kb.Controller()
mouse = mouse.Controller()


def checkType(v):
    try:
        int(v)
        return "int"
    except ValueError:
        pass
    try:
        float(v)
        return "float"
    except ValueError:
        pass
    return "str"


def translate(instruction):
    global indent, hotkey, indent
    instruction = instruction.split(" ")
    statement = instruction[0]
    value = ""
    for x in instruction[1:]:
        # print(x)
        value += x + "" if instruction[1:][-1] == x else x + " "
    value = value.replace("\n", "")
    tabs = ""
    for x in range(indent):
        tabs += "\t"
    if statement == "loop":
        if value == "start":
            indent += 1
        elif value == "end":
            indent -= 1
    if indent > 1:
        stoptabs = ""
        for x in range(indent):
            stoptabs += "\t"
        stop = f"{stoptabs}if not running:\n\t{stoptabs}break\n"
    else:
        stop = ""
    if language.get(statement, False) and not language.get(statement, False) == "comment" and not language.get(
            statement, False) == "hotkey":
        return f"{tabs}" + f"{language.get(statement, False)}" + f"({doublequote if checkType(value) == 'str' else none}" + f"{value}" + f"{doublequote if checkType(value) == 'str' else none})\n" + stop if not statement == "loop" else f"{tabs}" + f"{language.get(statement, False)}\n" + stop if not value == "end" else False
    elif language.get(statement, False) and not language.get(statement, False) == "comment" and language.get(statement,
                                                                                                             False) == "hotkey":
        hotkey = keys.get(str(value), str(value))
    else:
        return False
    # print(statement, value)


instructions = []


def main():
    code = init
    with open("instructions.txt") as f:
        instructions = f.readlines()
    for instruction in instructions:
        translation = translate(instruction)
        code += (translation if translation else "")
    # print(hotkey)
    code += end
    print(code)
    exec(code)
    # print(mouse.position)


main()
