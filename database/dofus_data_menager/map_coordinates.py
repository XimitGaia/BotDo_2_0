import ctypes


class MapCoordinates:

    def __init__(self, json):
        self.data = self.load_json(json)

    def load_json(self, json):
        data = dict()
        for group in json:
            compressed_coords = group.get("compressedCoords")
            map_ids = [int(i) for i in group.get("mapIds")]
            data.update({compressed_coords: map_ids})
        return data

    def get_map_coordinates_by_compressed_coord(self, compressed_coord: int):
        return self.data.get(compressed_coord)

    def get_map_coordinates_by_coords(self, xcoord: int, ycoord: int):
        xcompressed = self.get_compressed_value(xcoord)
        ycompressed = self.get_compressed_value(ycoord)
        compressed_coord = ctypes.c_int((xcompressed << 16) + ycompressed).value
        print('compressed:', compressed_coord)
        return self.get_map_coordinates_by_compressed_coord(compressed_coord=compressed_coord)

    def get_compressed_value(self, coord: int):
        if coord < 0:
            return ctypes.c_int(32768 | coord & 32767).value
        return ctypes.c_int(coord & 32767).value
