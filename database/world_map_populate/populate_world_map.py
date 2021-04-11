import sys
import os
from pathlib import Path
from multiprocessing import Process, Queue
import threading
path = Path(__file__).resolve()
sys.path.append(str(path.parents[2]))

import json, os
import time
from database.sqlite import Database
local_base_path = os.path.dirname(os.path.realpath(__file__))

json_maps_path = "C:\\Users\\Lucas\\Desktop\\Dofus Decompiler\\cell_info_crossing\\json_maps"

database = Database()
del database
queue_insert = Queue()
finished_inserting = False
started_all_threads = False

harvestables = None
with open(f'{local_base_path}{os.sep}haverst_graph_coordinate_to_item_id.json') as haverst_graph_coordinate_to_item_id:
    harvestables = json.load(haverst_graph_coordinate_to_item_id)

def world_map_file_get_cells(file_path: str, world_map_id: int):
    with open(file_path) as file_json:
        try:
            map_file = json.load(file_json)
        except:
            print(f"Failed to load: {file_path} - map_id: {world_map_id}")
            return None
        layers = map_file.get('layers')
        for layer in layers:
            cells = layer.get('cells')
            for cell in cells:
                cell_id = cell.get("cellId")
                if cell_id == 0 or cell_id == 560:
                    continue
                elements = cell.get("elements")
                for element in elements:
                    element_id = element.get("elementId")
                    if str(element_id) in harvestables and element.get("offsetX") == 0 and element.get("offsetY") == 0:
                        item_id = harvestables.get(str(element_id))
                        # print((cell_id, item_id, world_map_id))
                        queue_insert.put(('cell', (cell_id, item_id, world_map_id)))



def insert_and_process(data: tuple, map_id: int):
    queue_insert.put(('map', data))
    map_id = map_id
    for root, dirs, files in os.walk(json_maps_path):
        for file in files:
            if file == f'{map_id}.json':
                file_path = os.path.join(root, file)
                world_map_file_get_cells(file_path, data[0])
                return None


thread_list = list()
thread_consume = list()
beggone_process = False


def consume_queue(queue: Queue):
    database = Database()
    count = 0
    while not (queue.empty() and finished_inserting):
        count += 1
        try:
            data = queue.get(False)
        except:
            continue
        elemente_type = data[0]
        to_insert = data[1]
        if elemente_type == 'map':
            database.insert_world_map(to_insert)
        else:
            database.insert_haverstable_cell_cordinate(to_insert)
        if started_all_threads:
            print(f'Remaining itens: {queue.qsize()}', end='\r')
        # if queue.qsize() == 0:

    return None

thread_insert = threading.Thread(target=consume_queue, args=(queue_insert,))
thread_insert.start()

with open(f'{local_base_path}{os.sep}MapPositions.json') as map_positions_json:
    map_positions = json.load(map_positions_json)
    total = len(map_positions)
    print(f'Total {total}')
    world_map_id = 0
    print('Initializing threads...')
    for map in map_positions:
        world_map_id += 1
        map_id = int(map.get('id'))
        xcoord = int(map.get("posX"))
        ycoord = int(map.get("posY"))
        world_map_zone = int(map.get("worldMap"))
        data = (world_map_id, xcoord, ycoord, 1, 1, 1, 1, world_map_zone)
        thread = threading.Thread(target=insert_and_process, args=(data, map_id))
        thread_list.append(thread)
        thread.start()
        print(f'[{"#"*(int((world_map_id/total)*50))+ " "*(50 - int((world_map_id/total)*50))}] {round((world_map_id/total)*100,2)}%', end='\r')

print('')
print('Finalizing threads...')
started_all_threads = True
for thread in thread_list:
    thread.join()
finished_inserting = True
thread_insert.join()