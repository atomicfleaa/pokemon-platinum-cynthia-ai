import time
import keyboard
import win32gui

WINDOW_TITLE = "DeSmuME"

import time
import win32gui


def focus_emulator(retries=10, delay=1):
    """
    Try multiple times to find and focus the DeSmuME window.
    Avoids race condition at startup.
    """

    for attempt in range(retries):

        def enum_handler(hwnd, result):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "DeSmuME" in title:
                    result.append(hwnd)

        windows = []
        win32gui.EnumWindows(enum_handler, windows)

        if windows:
            win32gui.SetForegroundWindow(windows[0])
            time.sleep(0.5)
            return True

        time.sleep(delay)

    print("Emulator not found.")
    return False


def press(key, hold=0.1):
    keyboard.press(key)
    time.sleep(hold)
    keyboard.release(key)
