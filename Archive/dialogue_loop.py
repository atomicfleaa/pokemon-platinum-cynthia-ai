import time
import random
import dxcam
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw


# ===== SETTINGS =====
SECONDS_TO_WAIT = 5
MOVE_HOLD = 0.25
A_HOLD = 0.35
STEP_DELAY = 0.6
TOTAL_STEPS = 200


def get_desmume_window():
    windows = gw.getWindowsWithTitle("DeSmuME")
    if not windows:
        return None
    return windows[0]


def hold_key(key, duration):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)


def move_random():
    direction = random.randint(0, 3)

    if direction == 0:
        hold_key("w", MOVE_HOLD)
    elif direction == 1:
        hold_key("s", MOVE_HOLD)
    elif direction == 2:
        hold_key("a", MOVE_HOLD)
    elif direction == 3:
        hold_key("d", MOVE_HOLD)


def press_a():
    hold_key("right", A_HOLD)
    time.sleep(0.2)


def is_dialogue_active(top_screen_bgr):
    h, w, _ = top_screen_bgr.shape

    # Bottom 40% of top screen
    region = top_screen_bgr[int(h * 0.6):h, :]

    # Convert to HSV for color detection
    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)

    # Purple range (dialogue border color)
    lower_purple = np.array([120, 50, 50])
    upper_purple = np.array([160, 255, 255])

    mask = cv2.inRange(hsv, lower_purple, upper_purple)

    purple_pixels = np.sum(mask > 0)
    total_pixels = region.shape[0] * region.shape[1]

    ratio = purple_pixels / total_pixels

    # If enough purple detected → dialogue
    if ratio > 0.02:
        return True

    return False


def main():
    print("Click the emulator window now.")
    time.sleep(SECONDS_TO_WAIT)

    window = get_desmume_window()
    if window is None:
        print("DeSmuME window not found.")
        return

    window.activate()
    time.sleep(1)

    camera = dxcam.create()

    print("Starting improved dialogue-aware AI...")

    for step in range(TOTAL_STEPS):
        frame = camera.grab()
        if frame is None:
            continue

        x, y = window.left, window.top
        w, h = window.width, window.height

        emu_frame = frame[y:y+h, x:x+w]

        # Take top screen only
        top_screen = emu_frame[0:h//2, :]

        if is_dialogue_active(top_screen):
            print("Dialogue detected → pressing A")
            press_a()
        else:
            move_random()

        time.sleep(STEP_DELAY)

    print("Done.")


if __name__ == "__main__":
    main()
