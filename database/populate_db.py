import sys
import os
import time
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


def get_surfice_sub_areas():
    database = Database()
    surfice_sub_areas = [i[0] for i in database.get_surfice_sub_areas()]
    return surfice_sub_areas


mines = [
        "Shifty Shaft",
        "Mine",
        "Canem Cave",
        "Aminita",
        "Anto Mine",
        "Charhole Cavern",
        "Con Cave",
        "Diggum Mine",
        "Dyna Mine",
        "Faultline Mine",
        "Ikiki Mine",
        "Incarnam Mine",
        "Kamana Mine",
        "Konk Cave",
        "Korussant Mine",
        "Krtek Mine",
        "Astrub Mines"
]


def is_mine(name, map_id):
    if name in mines:
        return True
    return False


def is_not_surfice(name, sub_area_id, surfice_sub_areas):
    if sub_area_id not in surfice_sub_areas:
        return True
    non_surfice_names = [
        "Temple",
        "Room",
        "Cavern",
        "Cave",
        "- Exit",
        "- Entrance",
        "Tunnel",
        "Dungeon"
    ]
    for non_surfice_name in non_surfice_names:
        if non_surfice_name in name:
            return True
    return False


def get_world_map_data(map_info: dict, surfice_sub_areas: list):
    map_id = int(map_info.get('id'))
    xcoord = map_info.get("posX")
    ycoord = map_info.get("posY")
    sub_area_id = map_info.get("subAreaId")
    name = get_name_by_id(map_info.get("nameId"))
    if name is None:
        name = " "
    if is_mine(name, map_id) or is_not_surfice(name, sub_area_id, surfice_sub_areas):
        data = [map_id, xcoord, ycoord, -1, -1, -1, -1, sub_area_id, 0]
    else:
        data = [map_id, xcoord, ycoord, -1, -1, -1, -1, sub_area_id, -1]
    return data


def get_maps_by_position():
    to_return = dict()
    map_positions = unpacker.dofus_open("MapPositions.d2o")
    surfice_sub_areas = get_surfice_sub_areas()
    for map_info in map_positions:
        map_data = get_world_map_data(map_info, surfice_sub_areas)
        pos = (map_data[1], map_data[2])
        if pos not in to_return:
            to_return.update({pos: [map_data]})
        else:
            to_return[pos].append(map_data)
    return to_return


def surfices_first_filter(grouped_maps: dict):
    for position in grouped_maps:
        possible_surfice = list()
        for map_data in grouped_maps[position]:
            if map_data[8] == -1:
                possible_surfice.append(map_data)
        if len(possible_surfice) == 1:
            for map_data in grouped_maps[position]:
                if map_data == possible_surfice[0]:
                    map_data[8] = 1
    return grouped_maps


def is_map_id_similar(map_id, comparation_id):
    id_lenght = len(str(map_id))
    if id_lenght == len(str(comparation_id)):
        if id_lenght >= 8:
            if str(map_id)[:-4] == str(comparation_id)[:-4]:
                return True
        if id_lenght >= 7:
            if str(map_id)[:-3] == str(comparation_id)[:-3]:
                return True
        if id_lenght >= 5:
            if str(map_id)[:-2] == str(comparation_id)[:-2]:
                return True
    return False


def try_determine_neighborhood(map_data: list, maps_to_compare: list, pos_index: int):
    if map_data[pos_index] == -1:
        possible_neighborhoods = list()
        for comparation_data in maps_to_compare:
            if comparation_data[8] == 1:
                return 0
            if is_map_id_similar(map_data[0], comparation_data[0]):
                possible_neighborhoods.append(comparation_data)
        if len(possible_neighborhoods) == 1:
            for comparation_data in maps_to_compare:
                if comparation_data == possible_neighborhoods[0]:
                    comparation_data[8] = 1
                    return 1
                else:
                    comparation_data[8] = 0
    return 0


def optmize_surfices(grouped_maps):
    modifications = 99
    while modifications != 0:
        # print(modifications)
        modifications = 0
        for y in range(-99, 61):
            for x in range(-94, 50):
                pos = (x, y)
                if pos in grouped_maps:
                    for map_data in grouped_maps[pos]:
                        if map_data[8] == 1:
                            top = (pos[0], pos[1] - 1)
                            if top in grouped_maps:
                                modifications += try_determine_neighborhood(map_data=map_data, maps_to_compare=grouped_maps[top], pos_index=3)
                            else:
                                map_data[3] = 0
                            bottom = (pos[0], pos[1] + 1)
                            if bottom in grouped_maps:
                                modifications += try_determine_neighborhood(map_data=map_data, maps_to_compare=grouped_maps[bottom], pos_index=5)
                            else:
                                map_data[5] = 0
                            left = (pos[0] - 1, pos[1])
                            if left in grouped_maps:
                                modifications += try_determine_neighborhood(map_data=map_data, maps_to_compare=grouped_maps[left], pos_index=4)
                            else:
                                map_data[4] = 0
                            right = (pos[0] + 1, pos[1])
                            if right in grouped_maps:
                                modifications += try_determine_neighborhood(map_data=map_data, maps_to_compare=grouped_maps[right], pos_index=6)
                            else:
                                map_data[6] = 0


def world_map_inserter():
    print('Inserting maps... ',end='\r')
    grouped_maps = get_maps_by_position()
    surfices_first_filter(grouped_maps)
    optmize_surfices(grouped_maps)
    for pos in grouped_maps:
        for map_data in grouped_maps[pos]:
            queue.put(("world_map", map_data))
    print('Inserting maps   OK')


def monster_location_inserter():
    print('Inserting monster location... ',end='\r')
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
    for element in elements["elements_map"].keys():
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
                    interactive_type = get_interactive_type(element_id, off_set_x, off_set_y)
                    if interactive_type == 'trash':
                        continue
                    if element_id in interactives_ids:
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

thread_insert = threading.Thread(target=consume_queue, args=(queue,))
thread_insert.start()
monsters_and_drops_inserter()
del items
world_map_inserter()
monster_location_inserter()
interactives_inserter()
finished_inserting = True
thread_insert.join()
insert_harvestables_cells()
insert_zaaps()
create_harvestables_location_view()
