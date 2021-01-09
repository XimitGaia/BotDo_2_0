# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))

from screen import Screen
from database.sqlite import Database
import pyautogui
import time




class Moving:

    def __init__(self, screen: Screen, database: Database):
        self.screen = screen
        self.database = database

    def move_to(self, direction:str, percentage: int = 50):
        if direction == 'top' or direction == 'bottom':
            width = (self.screen.game_active_screen[2] - self.screen.game_active_screen[0])
            xcoord = round(self.screen.game_active_screen[0] + (width * (percentage / 100)))
            if direction == 'top':
                ycoord = self.screen.game_active_screen[1] + 5
                point = (xcoord, ycoord)
                pyautogui.moveTo(point)
                time.sleep(0.3)
                pyautogui.click(point)
                time.sleep(6)
                return (xcoord, ycoord)
            ycoord = self.screen.game_active_screen[3] - 5
            point = (xcoord, ycoord)
            pyautogui.moveTo(point)
            time.sleep(0.3)
            pyautogui.click(point)
            time.sleep(6)
            return (xcoord, ycoord)
        height = (self.screen.game_active_screen[3] - self.screen.game_active_screen[1])
        ycoord = self.screen.game_active_screen[1] + (height * (percentage / 100))
        if direction == 'left':
            xcoord = self.screen.game_active_screen[0] + 5
            point = (xcoord, ycoord)
            pyautogui.moveTo(point)
            time.sleep(0.3)
            pyautogui.click(point)
            time.sleep(6)
            return (xcoord, ycoord)
        xcoord = self.screen.game_active_screen[2] - 5
        point = (xcoord, ycoord)
        pyautogui.moveTo(point)
        time.sleep(0.3)
        pyautogui.click(point)
        time.sleep(6)
        return (xcoord, ycoord)

    def get_amakna_allowed_neightborhoods(self, pos):
        result = self.database.get_barrer(pos[0], pos[1], 1)
        if len(result) == 0:
            return (1, 1, 1, 1)
        #print(result[0][2:-1])
        return result[0][2:-1]

    def djikstra(self, start, destiny):
        processed_maps = list()
        djikstra_list = [[start]]
        index = 0
        while destiny not in djikstra_list[index]:
            print(len(djikstra_list))
            temp_list_positions = []
            for position in djikstra_list[index]:
                processed_maps.append(position)
                neighborhoods = self.get_amakna_allowed_neightborhoods(position)
                top, bot, left, right = self.get_neighborhoods(position)
                if neighborhoods[0] == 1:
                    if top not in processed_maps:
                        temp_list_positions.append(top)
                if neighborhoods[1] == 1:
                    if left not in processed_maps:
                        temp_list_positions.append(left)
                if neighborhoods[2] == 1:
                    if bot not in processed_maps:
                        temp_list_positions.append(bot)
                if neighborhoods[3] == 1:
                    if right not in processed_maps:
                        temp_list_positions.append(right)
                processed_maps.append(top)
                processed_maps.append(bot)
                processed_maps.append(left)
                processed_maps.append(right)
            djikstra_list.append(temp_list_positions)
            index += 1
            if temp_list_positions == []:
                print("Can't find a way !")
                break
        return djikstra_list

    def get_neighborhoods(self, position: tuple):
        top = (position[0], position[1] - 1)
        bot = (position[0], position[1] + 1)
        left = (position[0] - 1, position[1])
        right = (position[0] + 1, position[1])
        return top, bot, left, right

    def djikstra_path_assembler(self, end_point, djikstra_list):
        djikstra_list = djikstra_list[:-1]
        mounted_path = [end_point]
        while len(djikstra_list) > 1:
            layer_positions = djikstra_list.pop()
            top, bot, left, right = self.get_neighborhoods(mounted_path[0])







    # def amakna_go_to(self, destiny, queue, my_zaaps):
    #     pos_list()


<<<<<<< Updated upstream
s = Screen()
d = Database()
m = Moving(s,d)
time.sleep(1)
print(m.djikstra((-32,-50),(-32,-48)))
=======
# s = Screen()
# d = Database()
# m = Moving(s,d)
# time.sleep(1)
# print(m.djikstra((-32,-50),(-32,-48)))
>>>>>>> Stashed changes
