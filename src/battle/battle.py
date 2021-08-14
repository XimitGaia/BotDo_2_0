# Autoloader
import sys
import os
from pathlib import Path

import keyboard

path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[1])

# Import system
from src.screen_controllers.screen import Screen
from database.sqlite import Database
import pyautogui
import numpy as np
import re
import time


class Battle:
    def __init__(self, screen: Screen, database: Database):
        self.screen = screen
        self.database = database
        self.battle_map_info = None
        self.monster_name_regex = re.compile(r"([a-zA-Z_\ ]+) L?v?I?l?O?m?")
        self.monster_level_regex = re.compile(r"L?v?I?l?.? ?(\d+)")

    def get_group_of_pixels_to_compare(self, point: tuple) -> list: #point = (x,y)
        group_of_cells_to_compare = []
        for y in range(point[1]-1, point[1]+2):
            for x in range(point[0]-1, point[0]+2):
                group_of_cells_to_compare.append((x, y))
        return group_of_cells_to_compare

    def update_battle_map_info(self):
        self.battle_map_info = self.get_battle_map_info()

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

    def get_occupied_cells(self):
        screen = self.screen.get_screen_image()
        occupied_cells = []
        for cell in self.battle_map_info["cells"]:
            point = self.screen.map_to_screen(cell)
            if screen.getpixel(point) != (142, 134, 94) and screen.getpixel(point) != (150, 142, 103):
                occupied_cells.append(cell)
        return occupied_cells

    def check_creature_mode(self):
        xcoord_1 = 1268 * self.screen.game_scale
        ycoord_1 = 986.666 * self.screen.game_scale
        xcoord_2 = 1426.666 * self.screen.game_scale
        ycoord_2 = 1018.666 * self.screen.game_scale
        if not self.screen.is_color_on_region(
                RGB=(0, 255, 255),
                region=(xcoord_1, ycoord_1, xcoord_2, ycoord_2)
        ):
            keyboard.press_and_release("'")

    def get_name_and_level(self):
        xcoord_1 = 781.333 * self.screen.game_scale
        ycoord_1 = 886.666 * self.screen.game_scale
        xcoord_2 = 1074.666 * self.screen.game_scale
        ycoord_2 = 917.333 * self.screen.game_scale
        text = self.screen.get_line_text_on_region(region=(xcoord_1, ycoord_1, xcoord_2, ycoord_2))
        name = self.monster_name_regex.search(string=text).group(1)
        if "Om" in text:
            level = 200
        else:
            level = int(self.monster_level_regex.search(string=text).group(1))
        return (name, level)

    def get_monster_info(self, name: str, level: int):
        data = self.database.get_monster_info_by_name_and_level(name=name, level=level)
        to_return = {
            "battle_status": "alive",
            "spells": {},
            "buffs": {},
            "actual_cell": None,
            "name": data[2],
            "level": data[4],
            "hp": data[5],
            "pa": data[6],
            "pm": data[7],
            "resist": {
                "earth": data[10],
                "air": data[11],
                "fire": data[12],
                "water": data[13],
                "neutral": data[14]
            },
            "pa_dodge": data[8],
            "pm_dodge": data[9],
            "can_trackle": data[15],
            "can_be_pushed": data[16],
            "can_switch_pos": data[17],
            "can_switch_pos_on_target": data[18],
            "can_be_carried": data[19],
            "primary_status": {
                "strength": data[20],
                "intelligence": data[21],
                "chance": data[22],
                "agility": data[23]
            }
        }
        return to_return



if __name__ == "__main__":
    database = Database()
    screen = Screen()
    battle = Battle(screen=screen, database=database)
    time.sleep(2)
    battle.update_battle_map_info()
    for i in battle.get_occupied_cells():
        pyautogui.moveTo(screen.map_to_screen(i))
        time.sleep(0.5)
        info = battle.get_name_and_level()
        if info[0] == "Pepinous":
            continue
        print(battle.get_monster_info(name=info[0], level=info[1]))
        time.sleep(0.5)
