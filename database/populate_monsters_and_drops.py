import sys
import os
import time
import threading
from pathlib import Path
from multiprocessing import Queue
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))
from sqlite import Database
from unpackers.unpacker import Unpacker
local_base_path = os.path.dirname(os.path.realpath(__file__))


unpacker = Unpacker()
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
        elemente_type = data[0]
        to_insert = data[1]
        # if elemente_type == 'map':
        #     database.insert_world_map(to_insert)
        if elemente_type == 'monster':
            database.insert_monsters(to_insert)
        else:
            database.insert_drops(to_insert)
        if finished_inserting:
            print(f'Remaining itens: {queue.qsize()}', end='\r')
    return None


def get_name_by_id(id: int):
    return i18n_en["texts"].get(id)


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

# def get_valid_areas() -> list:
#     valid_areas = list()
#     areas = unpacker.dofus_open("Areas.d2o")
#     for area in areas:
#         if area.get("superAreaId") == 0:
#             valid_areas.append(area.get("id"))
#     return valid_areas

# def get_valid_sub_areas() -> list:
#     valid_sub_areas = list()


thread_insert = threading.Thread(target=consume_queue, args=(queue,))
thread_insert.start()
monsters_and_drops_inserter()
finished_inserting = True
# del items
