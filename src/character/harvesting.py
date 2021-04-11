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

class Harvesting:
    def __init__(self, screen: Screen, database: Database, get_pos: callable):
        self.screen = screen
        self.database = database
        self.get_pos = get_pos
        self.items_to_collect = None

    def set_items(self, items: list):
        self.items_to_collect = items

    def get_harvestables_cells(self, pos: tuple):

        cell_ids = self.database.get_harvestables_cells_by_pos_and_world_zone(harvestables=self.items_to_collect, pos=pos)
        cell_ids = [int(i[0]) for i in cell_ids]
        return cell_ids

    def select_all_items(self, cell_ids: list):
        keyboard.press('shift')
        for cell_id in cell_ids:
            position= self.screen.map_to_screen(cell_id)
            pyautogui.moveTo(position)
            time.sleep(0.05)
            pyautogui.click(position)
            time.sleep(0.15)
        keyboard.release('shift')

    def harvest(self):
        pos = self.screen.get_pos_ocr() + (1,)
        if len(pos) < 3:
            pos = self.screen.get_pos_ocr(option=2) + (1,)
        print(pos)
        cell_ids = self.get_harvestables_cells(pos=pos)
        self.select_all_items(cell_ids)


if __name__ == "__main__":
    def get_pos():
        print('A')
    screen = Screen()
    database = Database()
    har  = Harvesting(screen, database, list(range(1,80)), get_pos=get_pos)
    time.sleep(1)
    har.harvest()
