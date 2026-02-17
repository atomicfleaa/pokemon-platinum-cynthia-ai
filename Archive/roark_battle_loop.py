import time
import cv2
import numpy as np
import dxcam
import keyboard
import win32gui

WINDOW_TITLE = "DeSmuME"

# ---------------------------
# Utility
# ---------------------------

def focus_emulator():
    hwnd = win32gui.FindWindow(None, WINDOW_TITLE)
    if hwnd == 0:
        print("Emulator not found.")
        return False
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    return True

def press(key, hold=0.1):
    keyboard.press(key)
    time.sleep(hold)
    keyboard.release(key)

# ---------------------------
# Screen Capture
# ---------------------------

camera = dxcam.create()

def capture():
    frame = camera.grab()
    if frame is None:
        return None
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# ---------------------------
# Visual Detectors
# ---------------------------

def bottom_dialogue_visible(frame):
    h, w, _ = frame.shape
    bottom = frame[int(h*0.65):h, :]
    brightness = np.mean(bottom)
    return brightness > 140  # tuned threshold

def move_menu_visible(frame):
    h, w, _ = frame.shape
    bottom = frame[int(h*0.55):int(h*0.75), :]
    green_pixels = np.sum(bottom[:,:,1] > 150)
    return green_pixels > 20000

def pokemon_menu_visible(frame):
    h, w, _ = frame.shape
    bottom = frame[int(h*0.55):int(h*0.85), :]
    blue_pixels = np.sum(bottom[:,:,2] > 150)
    return blue_pixels > 20000

def battle_finished(frame):
    # crude detection: no move menu and no dialogue
    return not move_menu_visible(frame) and not bottom_dialogue_visible(frame)

# ---------------------------
# Main Battle Logic
# ---------------------------

def run_battle():
    print("Starting Roark automation...")
    focus_emulator()

    while True:
        frame = capture()
        if frame is None:
            continue

        if bottom_dialogue_visible(frame):
            print("Dialogue → K")
            press("k")
            time.sleep(0.3)
            continue

        if move_menu_visible(frame):
            print("Move menu → Razor Leaf")
            press("k")  # Fight
            time.sleep(0.2)
            press("k")  # Slot 1 (Razor Leaf)
            time.sleep(0.8)
            continue

        if pokemon_menu_visible(frame):
            print("Switching to Shinx")
            press("s")  # move to slot 2
            time.sleep(0.2)
            press("k")
            time.sleep(0.8)
            continue

        if battle_finished(frame):
            print("Battle ended.")
            break

        time.sleep(0.05)

if __name__ == "__main__":
    time.sleep(3)
    run_battle()
