# Autoloader
import sys
import os
from pathlib import Path

path = Path(__file__).resolve()
sys.path.append(str(path.parents[2]))
root_path = str(path.parents[1])

from src.screen_controllers.screen import Screen
from database.sqlite import Database
import keyboard
import pyautogui
import time
from PIL import ImageGrab
from PIL import Image
import numpy as np


class Harvesting:
    def __init__(self, screen: Screen, database: Database, get_map_id: callable):
        self.screen = screen
        self.database = database
        self.get_map_id = get_map_id
        self.items_to_collect = None
        self.comparison_photos = {"initial_state": {}, "after_click": {}}
        self.cells_to_process = list()

    def set_items(self, items: list):
        self.items_to_collect = items

    def get_harvestables_cells(self, map_id: int):
        cell_ids = self.database.get_harvestables_cells_by_map_id(
            harvestables=self.items_to_collect, map_id=map_id
        )
        return cell_ids

    def select_all_items(self, harvestables_pos: list):
        keyboard.press("shift")
        for pos in harvestables_pos:
            coords = self.screen.map_to_screen(pos[0])
            offset_x = pos[1] * self.screen.game_scale
            offset_y = pos[2] * self.screen.game_scale
            position = (
                coords[0] + offset_x,
                coords[1] + offset_y,
            )
            pyautogui.moveTo(position)
            time.sleep(0.07)
            pyautogui.click(position)
            time.sleep(0.2)
        keyboard.release("shift")

    def harvest(self):
        map_id = self.get_map_id()
        harvestables_pos = self.get_harvestables_cells(map_id=map_id)
        self.select_all_items(harvestables_pos)
        wait_time = 4 * len(harvestables_pos)
        return wait_time

    def get_cell_region(self, cell_id: int):
        central_position = self.screen.map_to_screen(cell_id)
        radius = (0.0490483162518 * self.screen.screen_size[0]) / 4
        region = (
            central_position[0] - radius,
            central_position[1] - radius,
            central_position[0] + radius,
            central_position[1] + radius,
        )
        return region


if __name__ == "__main__":

    def get_pos():
        print("A")

    screen = Screen()
    database = Database()
    har = Harvesting(screen, database, get_pos=get_pos)
    time.sleep(1)
    har.select_all_items([416, 338])
    time.sleep(5)
    for image in har.comparison_photos["initial_state"].values():
        image.show()
    for image in har.comparison_photos["after_click"].values():
        image.show()
