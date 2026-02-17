import time
import pyautogui
import pygetwindow as gw

def main():
    print("Click emulator window now.")
    time.sleep(5)

    windows = gw.getWindowsWithTitle("DeSmuME")
    if not windows:
        print("Emulator not found.")
        return

    window = windows[0]
    window.activate()
    time.sleep(1)

    print("Holding RIGHT ARROW for 1 second...")
    pyautogui.keyDown("right")
    time.sleep(1)
    pyautogui.keyUp("right")

    print("Done.")

if __name__ == "__main__":
    main()
