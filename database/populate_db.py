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
        if finished_inserting:
            print(f'Remaining itens: {queue.qsize()}', end='\r')
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


def get_area_id(sub_area_id: int):
    for sub_area in sub_areas:
        if sub_area.get('id') == sub_area_id:
            return int(sub_area.get('areaId'))


def get_super_area_id(area_id: int):
    for area in areas:
        if area.get('id') == area_id:
            return int(area.get('superAreaId'))


def get_world_map_data(map_info: dict):
    sub_area_id = map_info.get("subAreaId")
    area_id = get_area_id(sub_area_id)
    super_area_id = get_super_area_id(area_id)
    map_id = int(map_info.get('id'))
    xcoord = map_info.get("posX")
    ycoord = map_info.get("posY")
    outdoor = map_info.get("outdoor")
    sub_area_id = sub_area_id
    area_id = area_id
    super_area_id = super_area_id
    return [map_id, xcoord, ycoord, -1, -1, -1, -1, outdoor, sub_area_id, area_id, ''], super_area_id


def get_maps_by_position():
    to_return = dict()
    map_positions = unpacker.dofus_open("MapPositions.d2o")
    for map_info in map_positions:
        map_data, super_area_id = get_world_map_data(map_info)
        if super_area_id != 0:
            continue
        pos = (map_data[1], map_data[2])
        if pos not in to_return:
            to_return.update({pos: [map_data]})
        else:
            to_return[pos].append(map_data)
    return to_return


def modify_neighborhoods(map_data: list, compare_data: list, best_neighborhood: dict, pos_index: int):
    map_data[pos_index] = best_neighborhood.get('map_id')
    compare_data[get_reciprocal_index(pos_index)] = {'map_id': map_data[0], 'confidence': best_neighborhood.get("confidence")}


def get_reciprocal_index(index):
    if index == 3:
        return 5
    if index == 4:
        return 6
    if index == 5:
        return 3
    if index == 6:
        return 4


def determine_neighborhood(map_data: list, comparation_maps: list, pos_index: int):
    possibles_neighborhood = list()
    index = 0
    for compare_data in comparation_maps:
        if compare_data[7]:
            confidence = 0
            if map_data[8] == compare_data[8]:
                confidence += 100
            if map_data[9] == compare_data[9]:
                confidence += 50
            possibles_neighborhood.append({'map_id': compare_data[0], 'confidence': confidence, 'list_index': index})
        index += 1
    if len(possibles_neighborhood) > 0:
        best_neighborhood = max(possibles_neighborhood, key=lambda k: k['confidence'])
        best_neighborhood_index = best_neighborhood.get('list_index')
        del best_neighborhood['list_index']
        to_erase = None
        possible_neighborhood_relative_confidence = best_neighborhood.get("confidence")
        if type(map_data[pos_index]) == dict:
            map_data_confidence = map_data[pos_index].get("confidence")
            if possible_neighborhood_relative_confidence <= map_data_confidence:
                return 0
            to_erase = map_data[pos_index].get("map_id")
        try:
            actual_neighborhood_confidence = comparation_maps[best_neighborhood_index][get_reciprocal_index(pos_index)].get("confidence")
        except:
            actual_neighborhood_confidence = 0
        if possible_neighborhood_relative_confidence <= actual_neighborhood_confidence:
            return 0
        for compare_data in comparation_maps:
            compare_data_id = compare_data[0]
            if compare_data_id == to_erase:
                erase_neighborhood(pos_index=pos_index, compare_data=compare_data)
            if compare_data_id == best_neighborhood.get('map_id'):
                modify_neighborhoods(
                    map_data=map_data,
                    compare_data=compare_data,
                    best_neighborhood=best_neighborhood,
                    pos_index=pos_index
                )
                return 1
    return 0



def erase_neighborhood(pos_index: int, compare_data: list):
    compare_data[get_reciprocal_index(pos_index)] = {'map_id': -1, 'confidence': 0}


def optmize_surfices(grouped_maps):
    modifications = -1
    while modifications != 0:
        print(modifications, '#'*200)
        modifications = 0
        for coordinates in grouped_maps:
            for map_data in grouped_maps.get(coordinates):
                if map_data[7]:
                    top = (coordinates[0], coordinates[1] - 1)
                    bottom = (coordinates[0], coordinates[1] + 1)
                    left = (coordinates[0] - 1, coordinates[1])
                    right = (coordinates[0] + 1, coordinates[1])
                    if top in grouped_maps:
                        modifications += determine_neighborhood(map_data=map_data, comparation_maps=grouped_maps[top], pos_index=3)
                    else:
                        map_data[3] = 0
                    if bottom in grouped_maps:
                        modifications += determine_neighborhood(map_data=map_data, comparation_maps=grouped_maps[bottom], pos_index=5)
                    else:
                        map_data[5] = 0
                    if left in grouped_maps:
                        modifications += determine_neighborhood(map_data=map_data, comparation_maps=grouped_maps[left], pos_index=4)
                    else:
                        map_data[4] = 0
                    if right in grouped_maps:
                        modifications += determine_neighborhood(map_data=map_data, comparation_maps=grouped_maps[right], pos_index=6)
                    else:
                        map_data[6] = 0
    destroy_confidence_dict(grouped_maps)


def destroy_confidence_dict(grouped_maps):
    for coordinates in grouped_maps:
        for map_data in grouped_maps.get(coordinates):
            for index in range(3, 7):
                if type(map_data[index]) == dict:
                    map_data[index] = map_data[index].get("map_id")


def world_map_inserter():
    print('Inserting maps... ', end='\r')
    grouped_maps = get_maps_by_position()
    optmize_surfices(grouped_maps)
    print(grouped_maps)
    for pos in grouped_maps:
        for map_data in grouped_maps[pos]:
            queue.put(("world_map", map_data))
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


def get_interactive_elements_list():
    to_return = list()
    elements = unpacker.dofus_open("elements.ele")
    for element in elements["elements_map"]:
        if "entity_look" in elements["elements_map"][element]:
            to_return.append(elements["elements_map"][element]["id"])
    del elements
    return to_return


def get_interactive_type(element_id, off_set_x, off_set_y):
    if str(element_id) in interactives.get('harvestables'):
        if abs(off_set_x) < 20 and abs(off_set_y) < 20:
            return 'harvestable'
        return 'trash'
    if element_id in interactives.get('connectors'):
        return 'connector'
    if element_id in interactives.get('zaaps'):
        return 'zaap'
    return 'unknown'


def interactives_inserter():
    print('Insterting interactives... ', end='\r')
    interactives_ids = get_interactive_elements_list()
    thread_list = list()
    for root, dirs, files in os.walk(f'{local_base_path}{os.sep}jsons{os.sep}maps'):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                thread = threading.Thread(target=insert_map_elements, args=(file_path, interactives_ids))
                thread.start()
                thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    print('Insterting interactives   OK')


def insert_map_elements(file_path, interactives_ids):
    with open(file_path, 'r') as json_file:
        map_data = json.load(json_file)
        map_id = map_data.get("mapId")
        layers = map_data.get("layers")
        for layer in layers:
            cells = layer.get("cells")
            for cell in cells:
                cell_id = cell.get("cellId")
                if cell_id == 559:
                    continue
                for element in cell.get("elements"):
                    element_id = element.get("elementId")
                    off_set_x = element.get("offsetX")
                    off_set_y = element.get("offsetY")
                    identifier = element.get("identifier")
                    interactive_type = get_interactive_type(element_id, off_set_x, off_set_y)
                    if interactive_type == 'trash':
                        continue
                    if element_id in interactives_ids or identifier != 0:
                        interactive_data = (
                            map_id,
                            element_id,
                            interactive_type,
                            cell_id,
                            off_set_x,
                            off_set_y
                        )
                        queue.put(('interactives', interactive_data))


def insert_harvestables_cells():
    print('Adding harvestable_cells values...', end='\r')
    database = Database()
    for key, value in interactives.get("harvestables").items():
        database.insert_harvestables_cells(harvestable_id=value, element_id=int(key))
    print('Adding harvestable_cells values   OK')


def create_harvestables_location_view():
    database = Database()
    database.create_harvestables_location_view()


def insert_zaaps():
    database = Database()
    database.insert_values_zaaps_2021_05_05()


# thread_insert = threading.Thread(target=consume_queue, args=(queue,))
# thread_insert.start()
# monsters_and_drops_inserter()
del items
areas = Unpacker.dofus_open('Areas.d2o')
sub_areas = Unpacker.dofus_open('SubAreas.d2o')
world_map_inserter()
# del areas
# del sub_areas
# monster_location_inserter()
# interactives_inserter()
# finished_inserting = True
# thread_insert.join()
# insert_harvestables_cells()
# insert_zaaps()
# create_harvestables_location_view()
