import time
import dxcam
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw


SECONDS_TO_WAIT = 5


def get_desmume_window():
    windows = gw.getWindowsWithTitle("DeSmuME")
    if not windows:
        return None
    return windows[0]


def focus_window(window):
    window.activate()
    time.sleep(0.05)


def hold_key(window, key, duration):
    focus_window(window)
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)


def press_a(window):
    # DS A = K
    print(">>> PRESSING K")
    hold_key(window, "k", 0.4)


def move_up(window):
    hold_key(window, "w", 0.3)


def is_dialogue_active(top_screen):
    print("Checking dialogue...")

    h, w, _ = top_screen.shape
    region = top_screen[int(h * 0.65):h, :]

    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    mean_brightness = np.mean(gray)

    print("Brightness:", mean_brightness)

    return mean_brightness > 185


def main():
    print("Focus emulator window.")
    time.sleep(SECONDS_TO_WAIT)

    window = get_desmume_window()
    if window is None:
        print("No emulator window found.")
        return

    camera = dxcam.create()

    print("Starting loop...")

    while True:
        frame = camera.grab()
        if frame is None:
            continue

        x, y = window.left, window.top
        w, h = window.width, window.height

        emu_frame = frame[y:y+h, x:x+w]
        top_screen = emu_frame[0:h//2, :]

        if is_dialogue_active(top_screen):
            press_a(window)
        else:
            move_up(window)

        time.sleep(0.5)


if __name__ == "__main__":
    main()
