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
        self.connection_error = list()

    def move_to(self, connection: tuple) -> bool:
        cell, offset_x, offset_y = connection[2:5]
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
                self.connection_error.append(next_move_data[5])
                self.register_path_to_move(start=self.current_map_id, destiny=self.moving_to)
                return True
            self.move_to(connection=next_move_data)
            return len(self.movement_queue) > 0
        self.previuous_move_data = None
        return False

    def djikstra(self, start, destiny):
        processed_connections = [i for i in self.database.get_connectors_by_origin_map_id(start) if i not in self.connection_error]
        path_connections = [processed_connections.copy()]
        last_connections = self.database.get_connectors_by_destiny_map_id(destiny)
        path_connections_index = 0
        while True:
            layer = list()
            for connection_id in path_connections[path_connections_index]:
                next_connections = [i for i in self.get_next_connectors(connection_id) if i not in processed_connections]
                processed_connections.extend(next_connections)
                layer.extend(next_connections)
            destiny_connections = list(set(last_connections) & set(layer))
            if len(destiny_connections) > 0:
                path_connections.append(destiny_connections)
                return ("sucess", path_connections)
            elif len(layer) > 0:
                path_connections.append(layer)
            else:
                return("error", path_connections)
            path_connections_index += 1

    def get_path(self, start: int, destiny: int):
        path_maps = self.djikstra(start=start, destiny=destiny)
        if path_maps[0] == "sucess":
            return self.djikstra_path_assembler(
                djikstra_list=path_maps[1]
            )
        return None

    def get_next_connectors(self, connection_id: int):
        connections = [
            i for i in self.database.get_next_connectors_by_connector_id(connection_id) if i not in self.connection_error
        ]
        return connections

    def djikstra_path_assembler(self, djikstra_list):
        connectors_path = [djikstra_list.pop()[0]]
        while len(djikstra_list) > 0:
            connection_layer = djikstra_list.pop()
            actual_connector = connectors_path[0]
            connectors = self.database.get_previous_connectors_by_connector_id(
                connection_id=actual_connector
            )
            next_connector = int(list(set(connectors) & set(connection_layer))[0])
            connectors_path.insert(0, next_connector)
        to_return = [self.database.get_connector_info_by_id(i) for i in connectors_path]
        return to_return

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
    f = m.get_path(101715479, 68551174)
    print(f)
