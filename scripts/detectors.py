import numpy as np
import cv2


# ---------------------------
# Dialogue / Menu Detection
# ---------------------------

def bottom_dialogue_visible(frame):
    h, w, _ = frame.shape
    bottom = frame[int(h * 0.65):h, :]
    brightness = np.mean(bottom)
    return brightness > 140


def move_menu_visible(frame):
    h, w, _ = frame.shape
    bottom = frame[int(h * 0.55):int(h * 0.75), :]
    green_pixels = np.sum(bottom[:, :, 1] > 150)
    return green_pixels > 20000


def pokemon_menu_visible(frame):
    h, w, _ = frame.shape
    bottom = frame[int(h * 0.55):int(h * 0.85), :]
    blue_pixels = np.sum(bottom[:, :, 2] > 150)
    return blue_pixels > 20000


def level_up_screen_visible(frame):
    h, w, _ = frame.shape
    right_panel = frame[int(h * 0.2):int(h * 0.6), int(w * 0.6):w]
    brightness = np.mean(right_panel)
    return brightness > 180


def battle_finished(frame):
    # Battle cannot be finished if move menu is visible
    if move_menu_visible(frame):
        return False

    # Battle cannot be finished if dialogue is visible
    if bottom_dialogue_visible(frame):
        return False

    # Only consider DONE if screen is mostly bright (post-battle fade)
    import numpy as np
    brightness = np.mean(frame)

    if brightness > 200:  # fade to white after victory
        return True

    return False




# ---------------------------
# HP Detection
# ---------------------------

def enemy_hp_ratio(frame):
    h, w, _ = frame.shape
    hp_region = frame[int(h * 0.15):int(h * 0.22), int(w * 0.55):int(w * 0.9)]
    green_pixels = np.sum(hp_region[:, :, 1] > 150)
    total_pixels = hp_region.shape[0] * hp_region.shape[1]
    return green_pixels / total_pixels


def player_hp_ratio(frame):
    h, w, _ = frame.shape
    hp_region = frame[int(h * 0.55):int(h * 0.62), int(w * 0.05):int(w * 0.45)]
    green_pixels = np.sum(hp_region[:, :, 1] > 150)
    total_pixels = hp_region.shape[0] * hp_region.shape[1]
    return green_pixels / total_pixels
