import time
import dxcam
import cv2

from controller import press, focus_emulator
import detectors


class BattleEnv:

    def __init__(self):
        self.prev_enemy_hp = 1.0
        self.prev_player_hp = 1.0

        self.camera = dxcam.create()
        focus_emulator()
        time.sleep(1)

    def capture(self):
        frame = self.camera.grab()
        if frame is None:
            return None
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def get_state(self):
        frame = self.capture()
        if frame is None:
            return "NO_FRAME"

        # Battle-specific states FIRST
        if detectors.move_menu_visible(frame):
            return "MOVE_MENU"

        if detectors.pokemon_menu_visible(frame):
            return "SWITCH_MENU"

        if detectors.level_up_screen_visible(frame):
            return "LEVEL_UP"

        if detectors.battle_finished(frame):
            return "DONE"

        # Dialogue LAST
        if detectors.bottom_dialogue_visible(frame):
            return "DIALOGUE"

        return "UNKNOWN"

    def step(self, action):
        """
        Actions:
        0 = press A
        1 = press B
        2 = press DOWN
        3 = do nothing
        """

        # --- Execute Action ---
        if action == 0:
            press("k")
        elif action == 1:
            press("j")
        elif action == 2:
            press("s")
        elif action == 3:
            pass

        time.sleep(0.3)

        # --- Get Current State ---
        state = self.get_state()

        reward = 0
        done = False

        # --- Only compute HP rewards during battle menu ---
        if state == "MOVE_MENU":

            frame = self.capture()

            if frame is not None:

                current_enemy_hp = detectors.enemy_hp_ratio(frame)
                current_player_hp = detectors.player_hp_ratio(frame)

                # --- Enemy damage (smoothed threshold) ---
                if self.prev_enemy_hp - current_enemy_hp > 0.02:
                    reward += 1

                # --- Enemy faint ---
                if current_enemy_hp < 0.05:
                    reward += 5

                # --- Player damage penalty ---
                if current_player_hp < self.prev_player_hp - 0.02:
                    reward -= 1

                # Update previous values
                self.prev_enemy_hp = current_enemy_hp
                self.prev_player_hp = current_player_hp

        # --- Battle End ---
        if state == "DONE":
            reward += 20
            done = True

            # Reset for next episode
            self.prev_enemy_hp = 1.0
            self.prev_player_hp = 1.0

        return state, reward, done


    