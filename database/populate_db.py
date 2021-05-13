import sys
import os
import threading
import json
from pathlib import Path
from multiprocessing import Queue
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))
from sqlite import Database
from unpackers.unpacker import Unpacker
import numpy as np
local_base_path = os.path.dirname(os.path.realpath(__file__))


unpacker = Unpacker()
unpacker.dump_dofus_maps()
interactives = json.load(open(f'{local_base_path}{os.sep}jsons{os.sep}interactives.json'))
i18n_en = unpacker.dofus_open("i18n_en.d2i")
items = unpacker.dofus_open("Items.d2o")
queue = Queue()
finished_inserting = False


def consume_queue(queue: Queue):
    database = Database()
    while not (queue.empty() and finished_inserting):
        try:
            data = queue.get(False)
        except:
            continue
        data_type = data[0]
        to_insert = data[1]
        if data_type == 'monster':
            database.insert_monsters(to_insert)
        elif data_type == 'drop':
            database.insert_drops(to_insert)
        elif data_type == 'world_map':
            database.insert_world_map(to_insert)
        elif data_type == 'monsters_location':
            database.insert_monster_location(to_insert)
        elif data_type == 'interactives':
            database.insert_interactives(to_insert)
        elif data_type == 'connector':
            database.insert_connector(to_insert)
        elif data_type == 'harvestables':
            database.insert_harvestables_cells(to_insert)
        if finished_inserting:
            print(f'Remaining itens: {queue.qsize()}              ', end='\r')
    return None


def get_name_by_id(id: int):
    return i18n_en["texts"].get(id)

# +:+:+: :+:+:+ :+:    :+: :+:+:   :+: :+:    :+:    :+:     :+:        :+:    :+: :+:    :+:
# ::::    ::::   ::::::::  ::::    :::  :::::::: ::::::::::: :::::::::: :::::::::   ::::::::
# +:+ +:+:+ +:+ +:+    +:+ :+:+:+  +:+ +:+           +:+     +:+        +:+    +:+ +:+
# +#+  +:+  +#+ +#+    +:+ +#+ +:+ +#+ +#++:++#++    +#+     +#++:++#   +#++:++#:  +#++:++#++
# +#+       +#+ +#+    +#+ +#+  +#+#+#        +#+    +#+     +#+        +#+    +#+        +#+
# #+#       #+# #+#    #+# #+#   #+#+# #+#    #+#    #+#     #+#        #+#    #+# #+#    #+#
# ###       ###  ########  ###    ####  ########     ###     ########## ###    ###  ########


def get_monster_type(monster):
    if monster.get("isBoss"):
        return "boss"
    if monster.get("isMiniBoss"):
        return "mini_boss"
    else:
        return "common"


def get_average_drop_rate(drop: list):
    grade_1 = drop.get("percentDropForGrade1")
    grade_2 = drop.get("percentDropForGrade2")
    grade_3 = drop.get("percentDropForGrade3")
    grade_4 = drop.get("percentDropForGrade4")
    grade_5 = drop.get("percentDropForGrade5")
    average_drop = (grade_1 + grade_2 + grade_3 + grade_4 + grade_5)/5
    return round(average_drop, 5)


def find_item_by_id(id: int):
    for item in items:
        if item.get("id") == id:
            return item


def drop_handler(drops):
    for drop in drops:
        item_id = drop.get("objectId")
        item = find_item_by_id(item_id)
        if item:
            monster_id =  drop.get("monsterId")
            drop_rate = get_average_drop_rate(drop=drop)
            item_level = item.get("level")
            item_name = get_name_by_id(item.get("nameId"))
            drop_data = (item_id, item_name, item_level, monster_id, drop_rate)
            queue.put(("drop", drop_data))


def monsters_and_drops_inserter():
    print('Inserting Monsters and Drops in Queue:')
    monsters = unpacker.dofus_open("Monsters.d2o")
    total = len(monsters)
    count = 1
    for monster in monsters:
        count += 1
        if monster.get("isQuestMonster"):
            continue
        monster_id = monster.get("nameId")
        monster_name = get_name_by_id(id=monster_id)
        monster_type = get_monster_type(monster=monster)
        can_trackle = monster.get("canTackle")
        can_be_pushed = monster.get("canBePushed")
        can_switch_pos = monster.get("canSwitchPos")
        can_switch_pos_on_target = monster.get("canSwitchPosOnTarget")
        can_be_carried = monster.get("canBeCarried")
        for grade in monster.get("grades"):
            monster_level = grade.get("level")
            monster_hp = grade.get("lifePoints")
            monster_pa = grade.get("actionPoints")
            monster_pm = grade.get("movementPoints")
            monster_pa_dodge = grade.get("paDodge")
            monster_pm_dodge = grade.get("pmDodge")
            monster_earth_res = grade.get("earthResistance")
            monster_air_res = grade.get("airResistance")
            monster_fire_res = grade.get("fireResistance")
            monster_water_res = grade.get("waterResistance")
            monster_neutral_res = grade.get("neutralResistance")
            monster_data = (
                monster_id,
                monster_name,
                monster_type,
                monster_level,
                monster_hp,
                monster_pa,
                monster_pm,
                monster_pa_dodge,
                monster_pm_dodge,
                monster_earth_res,
                monster_air_res,
                monster_fire_res,
                monster_water_res,
                monster_neutral_res,
                can_trackle,
                can_be_pushed,
                can_switch_pos,
                can_switch_pos_on_target,
                can_be_carried
            )
            queue.put(("monster", monster_data))
        drop_handler(monster.get("drops"))
        print(f'[{"#"*(int((count/total)*50))+ " "*(50 - int((count/total)*50))}] {round((count/total)*100,2)}%', end='\r')
    print('')

# ::::    ::::      :::     :::::::::   ::::::::
# +:+:+: :+:+:+   :+: :+:   :+:    :+: :+:    :+:
# +:+ +:+:+ +:+  +:+   +:+  +:+    +:+ +:+
# +#+  +:+  +#+ +#++:++#++: +#++:++#+  +#++:++#++
# +#+       +#+ +#+     +#+ +#+               +#+
# #+#       #+# #+#     #+# #+#        #+#    #+#
# ###       ### ###     ### ###         ########


def get_world_map_data(map_info: dict):
    map_id = int(map_info.get('id'))
    xcoord = map_info.get("posX")
    ycoord = map_info.get("posY")
    outdoor = map_info.get("outdoor")
    return (map_id, xcoord, ycoord, outdoor)


def world_map_inserter():
    map_positions = unpacker.dofus_open("MapPositions.d2o")
    for map_info in map_positions:
        queue.put(('world_map', get_world_map_data(map_info=map_info)))
    print('Inserting maps   OK')


def monster_location_inserter():
    print('Inserting monster location... ', end='\r')
    sub_areas = unpacker.dofus_open("SubAreas.d2o")
    for sub_area in sub_areas:
        for monster_id in sub_area.get("monsters"):
            for map_id in sub_area.get("mapIds"):
                queue.put(("monsters_location", (map_id, monster_id)))
    del sub_areas
    print('Inserting monster location   OK')


def set_connections():
    world_graph = unpacker.dofus_open("worldgraph.bin")
    edges = world_graph.get('edges')
    for i in edges:
        for j in edges[i]:
            vertex = edges[i][j]
            origin = int(vertex.get('from').get('map_id'))
            destiny = int(vertex.get('to').get('map_id'))
            for transition in vertex.get('transition'):
                move_type = transition.get('type')
                cell = transition.get('cell')
                if move_type == 0:
                    if cell in np.arange(13, 546, 28):
                        queue.put(('connector', (origin, destiny, move_type, cell, 72, 0)))
                    else:
                        queue.put(('connector', (origin, destiny, move_type, cell, 28, 0)))
                    continue
                elif move_type == 2:
                    if 531 < cell < 546:
                        queue.put(('connector', (origin, destiny, move_type, cell, 0, 38)))
                    else:
                        queue.put(('connector', (origin, destiny, move_type, cell, 0, 16)))
                    continue
                elif move_type == 4:
                    if cell in np.arange(14, 547, 28):
                        queue.put(('connector', (origin, destiny, move_type, cell, -72, 0)))
                    else:
                        queue.put(('connector', (origin, destiny, move_type, cell, -28, 0)))
                    continue
                elif move_type == 6:
                    if 13 < cell < 27:
                        queue.put(('connector', (origin, destiny, move_type, cell, 0, -30)))
                    else:
                        queue.put(('connector', (origin, destiny, move_type, cell, 0, -8)))
                    continue
                if origin not in connections:
                    connections.update({origin: dict()})
                connections[origin].update({cell: [origin, destiny, move_type, cell]})


def interactives_and_harvestables_inserter():
    print('Insterting interactives... ', end='\r')
    thread_list = list()
    for root, dirs, files in os.walk(f'{local_base_path}{os.sep}jsons{os.sep}maps'):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                thread = threading.Thread(target=insert_map_elements_and_harvestables, args=(file_path,))
                thread.start()
                thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    print('Insterting interactives   OK')


def insert_map_elements_and_harvestables(file_path):
    with open(file_path, 'r') as json_file:
        map_data = json.load(json_file)
        map_id = int(map_data.get("mapId"))
        layers = map_data.get("layers")
        for layer in layers:
            cells = layer.get("cells")
            for cell in cells:
                cell_id = cell.get("cellId")
                if cell_id == 559:
                    continue
                for element in cell.get("elements"):
                    identifier = element.get("identifier")
                    if identifier is None:
                        continue
                    if identifier > 0:
                        element_id = int(element.get("elementId"))
                        element_data = elements["elements_map"].get(element_id)
                        if element_data.get('entity_look'):
                            offset_x = element.get("offsetX")
                            offset_y = element.get("offsetY") - element.get('altitude') * 10
                        else:
                            element_origin = element_data.get('origin')
                            element_size = element_data.get('size')
                            offset_x = element.get("offsetX") - element_origin.get('x') + element_size.get('x')//2
                            offset_y = element.get("offsetY") - element.get('altitude') * 10 - element_origin.get('y') + element_size.get('y')//2
                        harvestables = interactives.get('harvestables')
                        if str(element_id) in harvestables:
                            if abs(offset_x) < 50 and abs(offset_y) < 50:
                                queue.put(('harvestables', (map_id, harvestables.get(str(element_id)), cell_id, offset_x, offset_y)))
                            continue
                        if element_id in interactives.get('zaaps'):
                            queue.put(('interactives', (map_id, 'zaap', cell_id, offset_x, offset_y)))
                        if map_id in connections:
                            if cell_id in connections[map_id]:
                                connections[map_id][cell_id].extend([offset_x, offset_y])
                                data = tuple(connections[map_id][cell_id])
                                queue.put(('connector', data))
                                del connections[map_id][cell_id]
                                continue
                        queue.put(('interactives', (map_id, 'unknown', cell_id, offset_x, offset_y)))


def insert_connectors():
    for origin in connections:
        for cell in connections[origin]:
            data = tuple(connections[origin][cell])
            if len(data) == 4:
                data = data + (0, 0)
            queue.put(('connector', data))


def create_harvestables_location_view():
    database = Database()
    database.create_harvestables_location_view()


def insert_zaaps():
    database = Database()
    database.insert_values_zaaps_2021_05_05()


# thread_insert = threading.Thread(target=consume_queue, args=(queue,))
# thread_insert.start()
# monsters_and_drops_inserter()
# del items
# world_map_inserter()
# elements = unpacker.dofus_open('elements.ele')
# connections = dict()
# monster_location_inserter()
# set_connections()
# interactives_and_harvestables_inserter()
# insert_connectors()
# finished_inserting = True
# thread_insert.join()
# print('Finishing...', end='\r')
# insert_zaaps()
create_harvestables_location_view()
print('Finishing   OK')