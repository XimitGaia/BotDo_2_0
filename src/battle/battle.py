# Autoloader
import sys
import os
from pathlib import Path

path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[1])

# Import system
from src.screen_controllers.screen import Screen
import pyautogui
import numpy as np
import time


class Battle:
    def __init__(self, screen):
        self.screen = screen
        # self.battle_map_info = self.get_battle_map_info()
        # for pos in battle_info['cells']:
        #     position = self.screen.map_to_screen(pos)
        #     pyautogui.moveTo(position)
        #     time.sleep(0.05)

    def get_group_of_pixels_to_compare(self, point: tuple) -> list: #point = (x,y)
        group_of_cells_to_compare = []
        for y in range(point[1]-1, point[1]+2):
            for x in range(point[0]-1, point[0]+2):
                group_of_cells_to_compare.append((x, y))
        return group_of_cells_to_compare

    def get_battle_map_info(self):
        battle_map_info = {
            'cells': list(),
            'walls': list(),
            'holes': list(),
            'start_positions': list(),
        }
        action_screen = self.screen.get_active_screen_image()
        action_screen = np.array(action_screen)
        cell_number = 0
        # start difference between withe losangle and black losangle
        x_range_color = self.screen.x_range_black
        for y in self.screen.y_range:
            for x in x_range_color:
                group_of_pixels_to_compare = self.get_group_of_pixels_to_compare((round(x),round(y)))
                pixels = []
                for xcoord, ycoord in group_of_pixels_to_compare:
                    pixels.append(list(action_screen[ycoord][xcoord]))
                if pixels[1:] == pixels[:-1]:# if all pixels are equal
                    if pixels[0] == [142, 134, 94] or pixels[0] == [150, 142, 103]:
                        battle_map_info["cells"].append(cell_number)
                    elif pixels[0] == [0, 0, 0]:
                        battle_map_info["holes"].append(cell_number)
                    elif pixels[0] == [88, 83, 58]:
                        battle_map_info["walls"].append(cell_number)
                    elif pixels[0] == [221, 34, 0]:
                        battle_map_info["cells"].append(cell_number)
                        battle_map_info["start_positions"].append(cell_number)
                    elif pixels[0] == [0, 34, 221]:
                        battle_map_info["cells"].append(cell_number)
                        battle_map_info["start_positions"].append(cell_number)
                    else:
                        battle_map_info["cells"].append(cell_number)
                else:
                    battle_map_info["cells"].append(cell_number)
                cell_number += 1
            if x_range_color == self.screen.x_range_black:
                x_range_color = self.screen.x_range_white
            else:
                x_range_color = self.screen.x_range_black
        return battle_map_info


if __name__ == "__main__":

    screen = Screen()
    battle = Battle(screen=screen)
    time.sleep(1)
    print(battle.get_battle_map_info())
