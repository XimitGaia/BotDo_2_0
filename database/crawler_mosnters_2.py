import requests
import threading
from sqlite import Database
import json

def get_monsters_id_lists():
    boss_id_list = list()
    mini_boss_id_list = list()
    monster_id_list = list()
    url = f'https://dofensive.com/api/monsterPreview.php?Language=en'
    result = requests.get(url)
    if result.status_code == 200:
        data = result.json()
        print(len(data))
        for monster in data:
            if monster['Type'] == 3:
                boss_id_list.append(monster['Id'])
            elif monster['Type'] == 2:
                mini_boss_id_list.append(monster['Id'])
            else:
                monster_id_list.append(monster['Id'])
        return boss_id_list, mini_boss_id_list, monster_id_list

def get_url_by_id(id)>
    return f'https://dofensive.com/api/monster.php?Id={id}&Language=en'

def get_all_boss(boss_list,data):

    result = requests.get()



get_monsters_id_lists()