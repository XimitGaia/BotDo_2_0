import ctypes
from pathlib import Path
import sys

path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
from dofus_data_menager.map_coordinates import MapCoordinates
from dofus_data_menager.map_positions import MapPosition
from dofus_data_menager.world_points import WorldPoints
from database.unpackers.unpacker import Unpacker


class CharacterDisplacementManager:
    def __init__(self, map_id):
        self.map_positions_json = Unpacker.dofus_open("MapPositions.d2o")
        self.map_coordinates_json = Unpacker.dofus_open("MapCoordinates.d2o")
        self.map_coordinates = MapCoordinates(self.map_coordinates_json)
        self.map_positions = MapPosition(self.map_positions_json, self.map_coordinates)
        self.current_map_position = MapPosition(
            self.map_positions_json, self.map_coordinates
        )
        self.current_map_position.get_map_position_by_id(map_id)
        self.xcoord = self.current_map_position.xcoord
        self.ycoord = self.current_map_position.ycoord
        self.current_sub_area = self.current_map_position.sub_area_id
        self.current_area = self.current_map_position.area_id
        self.current_super_area = self.current_map_position.super_area_id

    def print_connectors_and_names(self):
        connectors = self.get_ordered_map_ids_from_coords(self.xcoord, self.ycoord)
        print(connectors)
        i18n = Unpacker.dofus_open("i18n_en.d2i").get("texts")
        to_print = list()
        for connector in connectors:
            self.map_positions.get_map_position_by_id(connector)
            to_print.append(
                (
                    i18n.get(self.map_positions.area_name_id),
                    i18n.get(self.map_positions.sub_area_name_id),
                )
            )
        print(to_print)

    def get_ordered_map_ids_from_coords(self, xcoord: int, ycoord: int):
        connectors = self.map_positions.get_map_id_by_coord(xcoord, ycoord)
        connectors_temp = list()
        connectors_maps = list()
        for connector in connectors:
            world_type = 0
            self.map_positions.get_map_position_by_id(connector)
            connector_world_id = WorldPoints(self.map_positions.id).world_id
            if connector_world_id == 0:
                world_type = 40
            if connector_world_id == 3:
                world_type = 30
            if connector_world_id == 2:
                world_type = 20
            if connector_world_id == 1:
                world_type = 10
            world_type += 100000
            if self.map_positions.has_priority_on_world_map:
                world_type += 10000
            if self.map_positions.outdoor:
                world_type += 1
            if self.map_positions.sub_area_id == self.current_sub_area:
                world_type += 100
            if self.map_positions.area_id == self.current_area:
                world_type += 50
            if self.map_positions.super_area_id == self.current_super_area:
                world_type += 25
            world_type += 100
            connectors_temp.append({"id": connector, "order": world_type})
        connectors_temp = sorted(connectors_temp, key=lambda k: k["order"])
        for connector in connectors_temp:
            connectors_maps.append(connector.get("id"))
        return connectors_maps[::-1]


c = CharacterDisplacementManager(88213774)
c.print_connectors_and_names()
