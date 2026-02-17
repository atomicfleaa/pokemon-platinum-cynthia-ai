import time
import dxcam
import cv2
import numpy as np
import pygetwindow as gw


SECONDS_TO_WAIT = 5


def get_desmume_window():
    windows = gw.getWindowsWithTitle("DeSmuME")
    if not windows:
        return None
    return windows[0]


def calculate_purple_ratio(top_screen_bgr):
    h, w, _ = top_screen_bgr.shape

    # Bottom 40% of top screen
    region = top_screen_bgr[int(h * 0.6):h, :]

    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)

    # Purple color range (dialogue border)
    lower_purple = np.array([120, 50, 50])
    upper_purple = np.array([160, 255, 255])

    mask = cv2.inRange(hsv, lower_purple, upper_purple)

    purple_pixels = np.sum(mask > 0)
    total_pixels = region.shape[0] * region.shape[1]

    ratio = purple_pixels / total_pixels

    return ratio


def main():
    print("Click emulator window now.")
    time.sleep(SECONDS_TO_WAIT)

    window = get_desmume_window()
    if window is None:
        print("DeSmuME window not found.")
        return

    window.activate()
    time.sleep(1)

    camera = dxcam.create()

    print("Starting dialogue detection test...")
    print("Open dialogue and watch the purple ratio change.\n")

    while True:
        frame = camera.grab()
        if frame is None:
            continue

        x, y = window.left, window.top
        w, h = window.width, window.height

        emu_frame = frame[y:y+h, x:x+w]

        # Top DS screen only
        top_screen = emu_frame[0:h//2, :]

        ratio = calculate_purple_ratio(top_screen)

        print("Purple ratio:", round(ratio, 5))

        time.sleep(0.5)


if __name__ == "__main__":
    main()
