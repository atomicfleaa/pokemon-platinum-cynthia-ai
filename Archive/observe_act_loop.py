import time
import random
import dxcam
import pyautogui
import pygetwindow as gw


# ===== SETTINGS =====
SECONDS_TO_WAIT = 5
STEP_DELAY = 0.4
HOLD_DURATION = 0.25
TOTAL_STEPS = 30


# ===== FIND EMULATOR WINDOW =====
def get_desmume_window():
    windows = gw.getWindowsWithTitle("DeSmuME")
    if not windows:
        return None
    return windows[0]


# ===== HOLD KEY FUNCTION =====
def hold_key(key, duration=HOLD_DURATION):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)


# ===== ACTION FUNCTION =====
def act(action):
    if action == 0:
        hold_key("w")       # up
    elif action == 1:
        hold_key("s")       # down
    elif action == 2:
        hold_key("a")       # left
    elif action == 3:
        hold_key("d")       # right
    elif action == 4:
        hold_key("right")   # A button


# ===== MAIN LOOP =====
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

    print("Starting movement loop...")

    for _ in range(TOTAL_STEPS):
        camera.grab()  # just to keep observation pipeline alive

        action = random.randint(0, 4)
        act(action)

        time.sleep(STEP_DELAY)

    print("Done.")


if __name__ == "__main__":
    main()
