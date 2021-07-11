# Autoloader
import sys
import os
from pathlib import Path

path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[1])

# Import system
from screen import Screen
import pyautogui
import time


class Battle:
    def __init__(self, screen):
        self.screen = screen
        battle_info = self.screen.get_battle_map_info()
        # for pos in battle_info['cells']:
        #     position = self.screen.map_to_screen(pos)
        #     pyautogui.moveTo(position)
        #     time.sleep(0.05)


if __name__ == "__main__":

    screen = Screen()
    battle = Battle(screen=screen)
