import ctypes


class WorldPoints:
    def __init__(self, map_id):
        self.map_id = map_id
        self.xcoord = None
        self.ycoord = None
        self.world_id = None
        self.set_from_map_id()

    def set_from_map_id(self):
        self.world_id = ctypes.c_int(((self.map_id & 1073479680) >> 18)).value
        self.xcoord = ctypes.c_int(self.map_id >> 9 & 511).value
        self.ycoord = ctypes.c_int(self.map_id & 511).value
        if ctypes.c_int(self.xcoord & 256).value == ctypes.c_int(256).value:
            self.xcoord = -(self.xcoord & 255)
        if ctypes.c_int(self.ycoord & 256).value == ctypes.c_int(256).value:
            self.ycoord = -(self.ycoord & 255)
