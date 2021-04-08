import sys
import os
from pathlib import Path
from multiprocessing import Process
import threading
path = Path(__file__).resolve()
sys.path.append(str(path.parents[2]))

import json, os
from database.sqlite import Database
local_base_path = os.path.dirname(os.path.realpath(__file__))

json_maps_path = "C:\\Users\\Lucas\\Desktop\\Dofus Decompiler\\cell_info_crossing\\json_maps"

database = Database()
del database

def word_map_file_get_cells(file_path: str, word_map_id: int, harvestables: dict):
    database = Database()
    with open(file_path) as file_json:
        map_file = json.load(file_json)
        layers = map_file.get('layers')
        # print(f'layers {len(layers)}')
        for layer in layers:
            cells = layer.get('cells')
            # print(f'cells {len(cells)}')
            for cell in cells:
                cell_id = cell.get("cellId")
                if cell_id == 0 or cell_id == 560:
                    continue
                elements = cell.get("elements")
                # print(f'cell_id {cell_id}')
                # print(f'elements {len(elements)}')
                for element in elements:
                    element_id = element.get("elementId")
                    if str(element_id) in harvestables and element.get("offsetX") == 0 and element.get("offsetY") == 0:
                        item_id = harvestables.get(str(element_id))
                        #print('Element found', cell_id, item_id)
                        #print(cell)
                        database.insert_haverstable_cell_cordinate((cell_id, item_id, word_map_id))
                        break

# with open(f'{local_base_path}{os.sep}haverst_graph_coordinate_to_item_id.json') as haverst_graph_coordinate_to_item_id:
#     harvestables = json.load(haverst_graph_coordinate_to_item_id)
#     word_map_file_get_cells("C:\\Users\\Lucas\\Desktop\\Dofus Decompiler\\cell_info_crossing\\json_maps\\maps1.d2p\\1\\97261061.json", 1, harvestables)

harvestables = None
with open(f'{local_base_path}{os.sep}haverst_graph_coordinate_to_item_id.json') as haverst_graph_coordinate_to_item_id:
    harvestables = json.load(haverst_graph_coordinate_to_item_id)


def insert_and_process(data: tuple):
    database = Database()
    word_map_id = database.insert_world_map(data)
    # print(f'Insertted map x{data[0]} y{data[1]} wId{data[6]}')
    threads = list()
    for root, dirs, files in os.walk(json_maps_path):
        for file in files:
            if file == f'{map_id}.json':
                file_path = os.path.join(root, file)
                thread = threading.Thread(target=word_map_file_get_cells, args=(file_path, word_map_id, harvestables))
                threads.append(thread)
                thread.start()
    for thread in threads:
        thread.join()


process_list = list()
with open(f'{local_base_path}{os.sep}MapPositions.json') as map_positions_json:
    map_positions = json.load(map_positions_json)
    total = len(map_positions)
    print(f'Total {total}')
    count = 0
    for map in map_positions:
        count += 1
        map_id = int(map.get('id'))
        xcoord = int(map.get("posX"))
        ycoord = int(map.get("posY"))
        world_map_zone = int(map.get("worldMap"))
        data = (xcoord, ycoord, 1, 1, 1, 1, world_map_zone)
        process = Process(target=insert_and_process, args=(data,))
        process_list.append(process)
        process.start()


for process in process_list:
    process.join()