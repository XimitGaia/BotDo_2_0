from pathlib import Path
import sys
path = Path(__file__).resolve()
sys.path.append(str(path.parents[2]))
import ctypes
from dofus_data_menager.map_coordinates import MapCoordinates
from database.unpackers.unpacker import Unpacker


class MapPosition:

    def __init__(self, json, map_coordinates: MapCoordinates):
        self.json = json
        self.map_coordinates = map_coordinates
        self.id = None
        self.xcoord = None
        self.ycoord = None
        self.outdoor = None
        self.name_id = None
        self.sub_area_id = None
        self.world_map = None
        self.has_priority_on_world_map = None

    @staticmethod
    def serarch_by_id(json, map_id):
        for map_info in json:
            if map_info.get('id') == map_id:
                return map_info

    def get_map_position_by_id(self, map_id: int):
        map_info = MapPosition.serarch_by_id(self.json, map_id)
        self.id = int(map_info.get('id'))
        self.xcoord = map_info.get('posX')
        self.ycoord = map_info.get('posY')
        self.outdoor = map_info.get('outdoor')
        self.name_id = map_info.get('nameId')
        self.sub_area_id = map_info.get('subAreaId')
        self.world_map = map_info.get('worldMap')
        self.has_priority_on_world_map = map_info.get('hasPriorityOnWorldmap')
        self.area_name_id = None
        self.sub_area_name_id = None
        self.area_id = self.get_area_id()
        self.super_area_id = self.get_super_area_id()

    def get_area_id(self):
        sub_areas = Unpacker.dofus_open('SubAreas.d2o')
        for sub_area in sub_areas:
            if sub_area.get('id') == self.sub_area_id:
                self.sub_area_name_id = sub_area.get('nameId')
                return sub_area.get('areaId')

    def get_super_area_id(self):
        areas = Unpacker.dofus_open('Areas.d2o')
        for area in areas:
            if area.get('id') == self.area_id:
                self.area_name_id = area.get('nameId')
                return area.get('superAreaId')

    def get_map_id_by_coord(self, xcoord: int, ycoord: int):
        return self.map_coordinates.get_map_coordinates_by_coords(xcoord=xcoord, ycoord=ycoord)