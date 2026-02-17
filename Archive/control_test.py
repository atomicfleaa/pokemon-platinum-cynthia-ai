import time
import keyboard
import pygetwindow as gw

def focus_desmume():
    windows = gw.getWindowsWithTitle("DeSmuME")
    if not windows:
        print("DeSmuME window not found.")
        return False
    window = windows[0]
    window.activate()
    time.sleep(0.5)
    return True

def main():
    print("Switching to emulator in 3 seconds...")
    time.sleep(3)

    if not focus_desmume():
        return

    print("Pressing UP (W)...")
    keyboard.press_and_release("w")
    time.sleep(0.5)

    print("Pressing RIGHT (D)...")
    keyboard.press_and_release("d")
    time.sleep(0.5)

    print("Pressing A button (Right Arrow)...")
    keyboard.press_and_release("right")
    time.sleep(0.5)

    print("Done.")

if __name__ == "__main__":
    main()
