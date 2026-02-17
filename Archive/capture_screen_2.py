import time
import pyautogui
import pygetwindow as gw

def focus_desmume():
    windows = gw.getWindowsWithTitle("DeSmuME")
    if not windows:
        print("DeSmuME window not found.")
        return False

    window = windows[0]
    window.activate()
    time.sleep(1)  # give Windows time to switch focus
    return True

def press_key(key, duration=0.2):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def main():
    print("You have 3 seconds to click the emulator window...")
    time.sleep(3)

    if not focus_desmume():
        return

    print("Pressing UP (W)...")
    press_key("w")

    time.sleep(0.5)

    print("Pressing RIGHT (D)...")
    press_key("d")

    time.sleep(0.5)

    print("Pressing A button (Right Arrow)...")
    press_key("right")

    print("Done.")

if __name__ == "__main__":
    main()
