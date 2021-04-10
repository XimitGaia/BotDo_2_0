import sys
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[2]))
from database.sqlite import Database
import requests
import threading
import json
import time
#https://dofensive.com/api/spell.php?Id=8731&Language=en


queue = list()
queue_error = dict()

def get_monsters_id_lists():
    boss_id_list = list()
    mini_boss_id_list = list()
    monster_id_list = list()
    url = 'https://dofensive.com/api/monsterPreview.php?Language=en'
    result = requests.get(url)
    if result.status_code == 200:
        data = result.json()
        for monster in data:
            if monster['Type'] == 3:
                boss_id_list.append(monster['Id'])
            elif monster['Type'] == 2:
                mini_boss_id_list.append(monster['Id'])
            else:
                monster_id_list.append(monster['Id'])
        return boss_id_list, mini_boss_id_list, monster_id_list
    else:
        raise Exception("Erro na request list")

def get_url_by_id(id):
    return f'https://dofensive.com/api/monster.php?Id={id}&Language=en'

def get_monster_row_list_info(id, monster_type, retry=0):
    url = get_url_by_id(id)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'
    }
    try:
        result = requests.get(url, headers=headers)
    except Exception as e:
        if queue_error.get(monster_type) is None:
            queue_error.update({monster_type: [id]})
        else:
            queue_error[monster_type].append(id)
        return None
    if result.status_code == 200:
        data = result.json()
        if data is None:
            if queue_error.get(monster_type) is None:
                queue_error.update({monster_type: [id]})
            else:
                queue_error[monster_type].append(id)
        if data == int:
            print(f'Data is int for id = ({id})')
            return None
        monster_id = data.get('Id')
        monster_name = data.get('Name')
        grades = data.get('Grades')
        to_return = list()
        for grade in grades:
            resistances = grade.get('Resistances')
            monster_info = (
                monster_id,
                monster_name,
                grade.get('Level'),
                grade.get('LifePoints'),
                grade.get('ActionPoints'),
                grade.get('MovementPoints'),
                grade.get('PaDodge'),
                grade.get('PmDodge'),
                resistances.get('Earth'),
                resistances.get('Air'),
                resistances.get('Fire'),
                resistances.get('Water'),
                resistances.get('Neutral'),
                monster_type
            )
            to_return.append(monster_info)
        return to_return
    else:
        if queue_error.get(monster_type) is None:
            queue_error.update({monster_type: [id]})
        else:
            queue_error[monster_type].append(id)
        start_time = time.time()
        print(' '*50, end='\r')
        while (time.time() - start_time) < 120:
            print(f'Waiting - Status code {result.status_code}: 0{2 - int((time.time() - start_time)//60)}:{59 - int((time.time() - start_time)%60)}', end='\r')
            time.sleep(1)
        print(' '*50, end='\r')
        return None

def monster_queue_insert(id, monster_type):
    row_list = get_monster_row_list_info(id, monster_type)
    if row_list is not None:
        queue.extend(row_list)
    return None

def insert_monsters(monster_list, monster_type):
    total_monsters = len(monster_list)
    count = 0
    thread_list = list()
    for monster_id in monster_list:
        count += 1
        thread = threading.Thread(target=monster_queue_insert, args=(monster_id, monster_type))
        thread_list.append(thread)
        thread.start()
        time.sleep(0.1)
        if len(thread_list) > 5 or count == total_monsters:
            for thread in thread_list:
                thread.join()
                percentage = 100*(count/total_monsters)
                print(f"[{'#'*(int(percentage)//2) + ' '*(50-int(percentage)//2)}] {round(percentage,2)}%", end='\r')
            time.sleep(1)
            thread_list = list()
    print('')



def inserter():
    database = Database()
    while True:
        if len(queue) > 0:
            row = queue.pop(0)
            database.insert_monsters(row)
        else:
            time.sleep(0.2)
        if trigger and len(queue) == 0:
            return None

trigger = False
thread = threading.Thread(target=inserter, args=())
thread.start()
boss_id_list, mini_boss_id_list, monster_id_list = get_monsters_id_lists()
print(f'Bosses {len(boss_id_list)}')
print(f'Mini-bosses {len(mini_boss_id_list)}')
print(f'Monsters {len(monster_id_list)}')
print('Getting Bosses: ')
insert_monsters(boss_id_list, 'boss')
print('Getting Mini-bosses: ')
insert_monsters(mini_boss_id_list, 'mini_boss')
print('Getting Monsters: ')
insert_monsters(monster_id_list, 'monster')
print('Processing Errors:')
while True:
    erro_list_by_type = dict(queue_error)
    queue_error = dict()
    for monster_type, ids in erro_list_by_type.items():
        print(f'  Processing {len(ids)} of {monster_type}')
        insert_monsters(ids, monster_type)
    if len(queue_error) < 1:
        break
    time.sleep(10)
    print('Reprocessing Errors:')
trigger = True
print('Finishing...')
time.sleep(10)
print(queue)
time.sleep(10)
print(queue)
thread.join()







