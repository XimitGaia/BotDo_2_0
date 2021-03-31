# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))

from src.screen_controllers.screen import Screen
from database.sqlite import Database
import pyautogui
import time

class Moving:

    def __init__(self, screen: Screen, database: Database, get_pos: callable):
        self.screen = screen
        self.database = database
        self.next_pos = None
        self.current_pos = None
        self.moving_to = None
        self.movement_queue = None
        self.get_pos = get_pos
        self.max_attemps_to_move = 0

    def move_to(self, direction: str, percentage: int = 50) -> bool:
        if direction == 'top' or direction == 'bottom':
            width = (self.screen.game_active_screen[2] - self.screen.game_active_screen[0])
            xcoord = round(self.screen.game_active_screen[0] + (width * (percentage / 100)))
            if direction == 'top':
                ycoord = self.screen.game_active_screen[1] + 5
                point = (xcoord, ycoord)
                pyautogui.moveTo(point)
                time.sleep(0.3)
                #checar se tem monstro
                pyautogui.click(point)
                time.sleep(6)
                return (xcoord, ycoord)
            ycoord = self.screen.game_active_screen[3] - 5
            point = (xcoord, ycoord)
            pyautogui.moveTo(point)
            time.sleep(0.3)
            #checar se tem monstro
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
            #checar se tem monstro
            pyautogui.click(point)
            time.sleep(6)
            return (xcoord, ycoord)
        xcoord = self.screen.game_active_screen[2] - 5
        point = (xcoord, ycoord)
        pyautogui.moveTo(point)
        time.sleep(0.3)
        #checar se tem monstro
        pyautogui.click(point)
        time.sleep(6)
        return (xcoord, ycoord)

    def get_next_pos(self):
        position_to_move = None
        self.current_pos = self.get_pos()
        if self.next_pos is None:
            self.next_pos = self.current_pos
        if self.next_pos == self.current_pos:
            self.max_attemps_to_move = 0
            position_to_move = self.pop_movement_queue()
            self.next_pos = position_to_move
        elif self.max_attemps_to_move < 3:
            self.max_attemps_to_move += 1
            position_to_move = self.next_pos
        return position_to_move

    def get_direction(self, pos):
        delta_x = pos[0] - self.current_pos[0]
        delta_y = pos[1] - self.current_pos[1]
        if delta_x == 0:
            if delta_y > 0:
                return 'bottom'
            else:
                return 'top'
        else:
            if delta_x > 0:
                return 'right'
            else:
                return 'left'

    def execute_movement(self) -> bool:
        next_pos = self.get_next_pos()
        if next_pos:
            direction = self.get_direction(next_pos)
            if (self.max_attemps_to_move > 2):
                row = (
                    0,
                    self.current_pos[0],
                    self.current_pos[1],
                    1
                )
                self.database.update_barrers(row=row, column_name=direction)
                self.register_path_to_move(self.current_pos, self.moving_to)
                return True
            self.move_to(direction=direction)
            #escalonar tempo pelos usuarios nao precisa espera se outra conta for jogar
            time.sleep(5)
            len_movement_queue = len(self.movement_queue)
            if len_movement_queue == 0:
                self.get_pos()
            return len_movement_queue > 0
        return False

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
            #print(len(djikstra_list))
            temp_list_positions = []
            for position in djikstra_list[index]:
                processed_maps.append(position)
                neighborhoods = self.get_amakna_allowed_neightborhoods(position)
                top, bottom, left, right = self.get_neighborhoods(position)
                if neighborhoods[0] == 1:
                    if top not in processed_maps:
                        temp_list_positions.append(top)
                if neighborhoods[1] == 1:
                    if left not in processed_maps:
                        temp_list_positions.append(left)
                if neighborhoods[2] == 1:
                    if bottom not in processed_maps:
                        temp_list_positions.append(bottom)
                if neighborhoods[3] == 1:
                    if right not in processed_maps:
                        temp_list_positions.append(right)
                processed_maps.append(top)
                processed_maps.append(bottom)
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
        bottom = (position[0], position[1] + 1)
        left = (position[0] - 1, position[1])
        right = (position[0] + 1, position[1])
        return top, bottom, left, right

    def djikstra_path_assembler(self, destiny, djikstra_list):
        print(f'djikstra_path_assembler {str(destiny)}', djikstra_list, '####')
        djikstra_list = djikstra_list[:-1]
        mounted_path = [destiny]
        while len(djikstra_list) > 1:
            layer_positions = djikstra_list.pop()
            top, bottom, left, right = self.get_neighborhoods(mounted_path[0])
            if top in layer_positions:
                mounted_path.insert(0, top)
                continue
            if bottom in layer_positions:
                mounted_path.insert(0, bottom)
                continue
            if left in layer_positions:
                mounted_path.insert(0, left)
                continue
            if right in layer_positions:
                mounted_path.insert(0, right)
                continue
        return mounted_path

    def register_path_to_move(self, start, destiny):
        self.moving_to = destiny
        djikstra_list = self.djikstra(start=start, destiny=destiny)
        path = self.djikstra_path_assembler(destiny=destiny, djikstra_list=djikstra_list)
        self.movement_queue = path
        self.max_attemps_to_move = 0
        self.next_pos = None

    def pop_movement_queue(self):
        to_return = self.movement_queue.pop(0)
        return to_return


# s = Screen()
# d = Database()
# m = Moving(s,d)
# time.sleep(1)
# a = m.djikstra((-32,-10),(-32,-48))
# print(a)
# print(m.djikstra_path_assembler((-32,-48), a))