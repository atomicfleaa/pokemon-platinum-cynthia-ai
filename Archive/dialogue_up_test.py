import time
import dxcam
import cv2
import numpy as np
import pyautogui
import pygetwindow as gw


# ===== SETTINGS =====
SECONDS_TO_WAIT = 5
MOVE_HOLD = 0.3
A_HOLD = 0.35
STEP_DELAY = 0.4
TOTAL_STEPS = 300


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
    # DS A button is now mapped to K
    hold_key(window, "k", A_HOLD)kk
    time.sleep(0.2)


def move_up(window):
    hold_key(window, "w", MOVE_HOLD)


def is_dialogue_active(top_screen_bgr):
    h, w, _ = top_screen_bgr.shape

    # Bottom 30% of top screen
    region = top_screen_bgr[int(h * 0.65):h, :]

    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

    mean_brightness = np.mean(gray)

    # Dialogue box is very bright (white background)
    if mean_brightness > 190:
        print("Brightness:", mean_brightness)
        return True

    return False



def main():
    print("Click emulator window now.")
    time.sleep(SECONDS_TO_WAIT)

    window = get_desmume_window()
    if window is None:
        print("DeSmuME window not found.")
        return

    camera = dxcam.create()

    print("Walking upward and handling dialogue...")

    for _ in range(TOTAL_STEPS):
        frame = camera.grab()
        if frame is None:
            continue

        x, y = window.left, window.top
        w, h = window.width, window.height

        emu_frame = frame[y:y+h, x:x+w]
        top_screen = emu_frame[0:h//2, :]

        if is_dialogue_active(top_screen):
            print("Dialogue detected → pressing A (K)")
            press_a(window)
        else:
            move_up(window)

        time.sleep(STEP_DELAY)

    print("Done.")


if __name__ == "__main__":
    main()
