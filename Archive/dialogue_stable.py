import time
import dxcam
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw


SECONDS_TO_WAIT = 5


def hold_key(key, duration):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)


def press_a():
    print(">>> PRESSING K")
    hold_key("k", 0.4)


def move_up():
    hold_key("w", 0.3)


def is_dialogue_active(top_screen):
    h, w, _ = top_screen.shape

    # Bottom-right small region
    region = top_screen[int(h * 0.75):int(h * 0.95),
                        int(w * 0.80):int(w * 0.95)]

    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

    bright_pixels = np.sum(gray > 210)
    total_pixels = gray.size

    ratio = bright_pixels / total_pixels

    print("Arrow bright ratio:", ratio)

    return ratio > 0.05




def main():
    print("IMPORTANT: Click the DeSmuME window NOW.")
    time.sleep(SECONDS_TO_WAIT)

    camera = dxcam.create()

    print("Running loop...")

    while True:
        frame = camera.grab()
        if frame is None:
            continue

        windows = gw.getWindowsWithTitle("DeSmuME")
        if not windows:
            continue

        window = windows[0]

        x, y = window.left, window.top
        w, h = window.width, window.height

        emu_frame = frame[y:y+h, x:x+w]
        top_screen = emu_frame[0:h//2, :]

        if is_dialogue_active(top_screen):
            press_a()
        else:
            move_up()

        time.sleep(0.5)


if __name__ == "__main__":
    main()
