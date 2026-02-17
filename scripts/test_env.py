import time
import logging
import os
from battle_env import BattleEnv

# ---------------------------
# Logging Setup (FILE ONLY)
# ---------------------------

log_path = os.path.abspath("battle_log.txt")

logging.basicConfig(
    filename=log_path,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    force=True
)

logging.info("Script started")

# ---------------------------
# Environment Setup
# ---------------------------

env = BattleEnv()

time.sleep(3)  # give time to click emulator if needed

# ---------------------------
# Main Loop
# ---------------------------

while True:

    state = env.get_state()
    logging.info(f"STATE: {state}")

    action = None

    # ---------------------------
    # Dialogue
    # ---------------------------

    if state == "DIALOGUE":
        action = 0

    # ---------------------------
    # Move Menu (Battle)
    # ---------------------------

    elif state == "MOVE_MENU":

        # Press Fight
        state, reward, done = env.step(0)
        logging.info(f"Reward: {reward}")
        logging.info("Pressed Fight")

        if done:
            logging.info("Battle finished.")
            break

        time.sleep(0.2)

        # Press Razor Leaf
        state, reward, done = env.step(0)
        logging.info(f"Reward: {reward}")
        logging.info("Pressed Razor Leaf")

        if done:
            logging.info("Battle finished.")
            break

        time.sleep(0.1)
        continue

    # ---------------------------
    # Switch Menu (Pokemon fainted)
    # ---------------------------

    elif state == "SWITCH_MENU":

        logging.info("Switch menu detected")

        # Wait for switch screen to fully render
        time.sleep(0.5)

        # Move cursor down (slot 2)
        state, reward, done = env.step(2)  # DOWN
        logging.info("Moved cursor to slot 2")

        time.sleep(0.3)

        # Confirm slot 2
        state, reward, done = env.step(0)  # A button
        logging.info("Confirmed slot 2")

        time.sleep(0.5)
        continue

    # ---------------------------
    # Level Up
    # ---------------------------

    elif state == "LEVEL_UP":
        action = 0

    # ---------------------------
    # Battle Done
    # ---------------------------

    elif state == "DONE":
        logging.info("Battle finished.")
        break

    # ---------------------------
    # Single-Action States
    # ---------------------------

    if action is not None:
        state, reward, done = env.step(action)
        logging.info(f"Reward: {reward}")

        if done:
            logging.info("Battle finished.")
            break

    time.sleep(0.1)

logging.info("Script ended")
