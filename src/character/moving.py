# Autoloader
import sys
import os
from pathlib import Path

path = Path(__file__).resolve()
sys.path.append(str(path.parents[2]))

from src.screen_controllers.screen import Screen
from database.sqlite import Database
import pyautogui
import time
import keyboard


class Moving:
    def __init__(self, screen: Screen, database: Database, get_map_id: callable):
        self.screen = screen
        self.database = database
        self.next_map_id = None
        self.current_map_id = None
        self.moving_to = None
        self.movement_queue = None
        self.get_map_id = get_map_id
        self.max_attemps_to_move = 0

    def move_to(self, connection: tuple) -> bool:
        cell, offset_x, offset_y = connection[2:]
        offset_x *= self.screen.game_scale
        offset_y *= self.screen.game_scale
        point_centered = self.screen.map_to_screen(cell)
        point = (point_centered[0] + offset_x, point_centered[1] + offset_y)
        pyautogui.moveTo(point)
        keyboard.press("shift")
        time.sleep(0.3)
        # checar se tem monstro
        pyautogui.click(point)
        keyboard.release("shift")

    def get_next_move_data(self):
        next_move_data = None
        self.current_map_id = self.get_map_id()
        if self.next_map_id is None:
            self.next_map_id = self.current_map_id
        if self.next_map_id == self.current_map_id:
            self.max_attemps_to_move = 0
            next_move_data = self.pop_movement_queue()
            self.previuous_move_data = next_move_data
            self.next_map_id = next_move_data[1]
        elif self.max_attemps_to_move < 3:
            self.max_attemps_to_move += 1
            next_move_data = self.previuous_move_data
        return next_move_data

    def execute_movement(self) -> list:
        next_move_data = self.get_next_move_data()
        if next_move_data:
            if self.max_attemps_to_move > 2:
                # ver se tem outro elemento na msm celula como interativo
                # trocar entre todos antes de deletar connection
                # row = (
                #     0,
                #     self.current_map_id[0],
                #     self.current_map_id[1],
                #     1
                # )
                # self.database.update_world_map(row=row, column_name=direction)
                # self.register_path_to_move(self.current_map_id, self.moving_to)
                return [True, None]
            self.move_to(connection=next_move_data)
            return [len(self.movement_queue) > 0, next_move_data]
        self.previuous_move_data = None
        return [False, next_move_data]

    def djikstra(self, start, destiny):
        processed_maps = [start]
        path_maps = [[start]]
        path_maps_index = 0
        while destiny not in path_maps[-1]:
            layer = list()
            for map_id in path_maps[path_maps_index]:
                linked_maps = self.get_linked_maps(map_id)
                for linked_map_id in linked_maps:
                    if linked_map_id in processed_maps:
                        continue
                    processed_maps.append(linked_map_id)
                    layer.append(linked_map_id)
            if len(layer) > 0:
                path_maps.append(layer)
            else:
                break
            path_maps_index += 1
        return path_maps

    def get_path(self, start: int, destiny: int):
        path_maps = self.djikstra(start=start, destiny=destiny)
        if destiny in path_maps[-1]:
            return self.djikstra_path_assembler(
                destiny=destiny, djikstra_list=path_maps
            )
        return None

    def get_linked_maps(self, map_id: int):
        connections = [
            i[0] for i in self.database.get_connectors_by_map_id(world_map_id=map_id)
        ]
        return connections

    def djikstra_path_assembler(self, destiny, djikstra_list):
        djikstra_list = djikstra_list[:-1]
        mounted_path = [destiny]
        while len(djikstra_list) > 1:
            layer_positions = djikstra_list.pop()
            try:
                actual_map_id = mounted_path[0][0]
            except:
                actual_map_id = mounted_path[0]
            connectors = self.database.get_connectors_by_destiny(
                destiny_map_id=actual_map_id
            )
            connectors_ids = [i[0] for i in connectors]
            nex_map_id = int(list(set(connectors_ids) & set(layer_positions))[0])
            for connector in connectors:
                if connector[0] == nex_map_id:
                    mounted_path.insert(0, connector)
                    break
        return mounted_path[:-1]

    def register_path_to_move(self, start, destiny):
        self.moving_to = destiny
        path = self.get_path(start=start, destiny=destiny)
        if not path:
            print("FUDEU NO PATH, N ACHOU CAMINHO")
        self.movement_queue = path
        self.max_attemps_to_move = 0
        self.next_map_id = None

    def pop_movement_queue(self):
        to_return = self.movement_queue.pop(0)
        return to_return


if __name__ == "__main__":

    def a():
        print("i")

    s = Screen()
    d = Database()
    m = Moving(s, d, a)
    # f = m.get_path(191105026, 191106048)
    f = m.get_path(171967506, 171968530)
    print(f)
    time.sleep(1)
    for i in f:
        m.move_to(i)
        time.sleep(7)
