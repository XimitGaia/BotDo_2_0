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
    def __init__(self, screen: Screen, database: Database, get_pos: callable):
        self.screen = screen
        self.database = database
        self.get_pos = get_pos
        self.items_to_collect = None
        self.comparison_photos = {
            'initial_state': {},
            'after_click': {}
        }
        self.cells_to_process = list()

    def set_items(self, items: list):
        self.items_to_collect = items

    def get_harvestables_cells(self, pos: tuple):
        cell_ids = self.database.get_harvestables_cells_by_pos_and_world_zone(harvestables=self.items_to_collect, pos=pos)
        cell_ids = [int(i[0]) for i in cell_ids]
        return cell_ids

    # def check_image_and_update(self, image, state: str, cell_id: int):
    #     if state == 'after_click':
    #         self.check_if_is_selected_and_append(image=image, cell_id=cell_id)
    #     self.comparison_photos[state].update({cell_id: image})

    # def get_cell_image(self, cell_id):
    #     cell_region = self.get_cell_region(cell_id)
    #     image = ImageGrab.grab(cell_region)
    #     return image

    # def get_bright_density(self, image):
    #     number_of_pixels = image.size[0]*image.size[1]
    #     matrix = np.array(image)
    #     bright_counter = 0
    #     for row in matrix:
    #         for pixel in row:
    #             if pixel[0]
    #             bright_counter += pixel[2]
    #     return bright_counter/number_of_pixels

    # def is_item_selected(self, after_click_image, cell_id: int):
    #     initial_state_image = self.comparison_photos['initial_state'].get(cell_id).convert('HSV')
    #     after_click_image = after_click_image.convert('HSV')
    #     initial_state_image_bright_density = self.get_bright_density(initial_state_image)
    #     after_click_image_birght_density = self.get_bright_density(after_click_image)
    #     print(after_click_image_birght_density - initial_state_image_bright_density)
    #     if after_click_image_birght_density - initial_state_image_bright_density > 10:
    #         return True
    #     return False

    # def is_item_still_selected(self, check_image, cell_id: int):
    #     after_click_image = self.comparison_photos['after_click'].get(cell_id).convert('HSV')
    #     check_image = check_image.convert('HSV')
    #     check_image_bright_density = self.get_bright_density(check_image)
    #     after_click_image_birght_density = self.get_bright_density(after_click_image)
    #     if check_image_bright_density - after_click_image_birght_density < -10:
    #         return False
    #     return True

    # def check_if_is_selected_and_append(self, image, cell_id: int):
    #     if self.is_item_selected(after_click_image=image, cell_id=cell_id):
    #         print('isss  selected')
    #         self.cells_to_process.append(cell_id)

    # def is_harvest_over(self):
    #     for cell_id in self.cells_to_process:
    #         cell_image = self.get_cell_image(cell_id=cell_id)
    #         if not self.is_item_still_selected(check_image=cell_image, cell_id=cell_id):
    #             self.cells_to_process.remove(cell_id)
    #     if len(self.cells_to_process) < 1:
    #         return True
    #     return False

    def select_all_items(self, cell_ids: list):
        keyboard.press('shift')
        for cell_id in cell_ids:
            position = self.screen.map_to_screen(cell_id)
            position = (position[0], position[1]+int(self.screen.screen_size[0]*0.00366032210))
            # initial_state_image = self.get_cell_image(cell_id)
            pyautogui.moveTo(position)
            time.sleep(0.05)
            pyautogui.click(position)
            # pyautogui.moveTo((5, 5))
            # time.sleep(0.02)
            # after_click_image = self.get_cell_image(cell_id)
            # self.check_image_and_update(image=initial_state_image, state='initial_state', cell_id=cell_id)
            # self.check_image_and_update(image=after_click_image, state='after_click', cell_id=cell_id)
            time.sleep(0.15)
        keyboard.release('shift')

    def harvest(self):
        pos = self.get_pos()
        if len(pos) < 3:
            pos = self.screen.get_pos_ocr(option=2) + (1,)
        cell_ids = self.get_harvestables_cells(pos=pos)
        self.select_all_items(cell_ids)
        wait_time = 2.5*len(cell_ids)
        return wait_time

    def get_cell_region(self, cell_id: int):
        central_position = self.screen.map_to_screen(cell_id)
        radius = (0.0490483162518*self.screen.screen_size[0])/4
        region = (
            central_position[0]-radius,
            central_position[1]-radius,
            central_position[0]+radius,
            central_position[1]+radius
        )
        return region



if __name__ == "__main__":
    def get_pos():
        print('A')
    screen = Screen()
    database = Database()
    har = Harvesting(screen, database, get_pos=get_pos)
    time.sleep(1)
    har.select_all_items([416, 338])
    time.sleep(5)
    for image in har.comparison_photos['initial_state'].values():
        image.show()
    for image in har.comparison_photos['after_click'].values():
        image.show()

