import requests
import threading
from bs4 import BeautifulSoup
import re
import json
from sqlite import Database

def get_monsters_id(pag_number: int, monster_list_chunks: dict)-> dict:
    monsters = {}
    url = f'https://www.dofus.com/en/mmorpg/encyclopedia/monsters?page={pag_number}'
    #url = f'https://www.dofus.com/en/mmorpg/encyclopedia/monsters?text=&monster_level_min=1&monster_level_max=1600&monster_zones[0]=69&monster_zones[1]=50&monster_zones[2]=51&monster_zones[3]=18&monster_zones[4]=7&monster_zones[5]=11&monster_zones[6]=8&monster_zones[7]=63&monster_zones[8]=26&monster_zones[9]=68&monster_zones[10]=59&monster_zones[11]=74&monster_zones[12]=53&monster_zones[13]=71&monster_zones[14]=48&monster_zones[15]=45&monster_zones[16]=28&monster_zones[17]=42&monster_zones[18]=65&monster_zones[19]=30&monster_zones[20]=2&monster_zones[21]=62&monster_zones[22]=79&monster_zones[23]=61&monster_zones[24]=46&monster_zones[25]=78&monster_zones[26]=49&monster_zones[27]=12&monster_zones[28]=54&monster_zones[29]=5&monster_zones[30]=6&monster_zones[31]=1&monster_zones[32]=55&size=96&display=table&page={pag_number}'
    result = requests.get(url)
    if result.status_code == 200:
        soup = BeautifulSoup(result.text)
        for monster_info in soup.find_all('tr')[1:]:
            name = monster_info.find("a").text
            if name != '':
                id = re.findall(r'\"id\"\:\"(\d+)',str(monster_info.script))[0]
                monsters[id] = name
    monster_list_chunks[str(pag_number)] = monsters

def get_full_monster_list()-> list:
    monster_list_chunks = dict()
    monster_thread_chunks = list()
    for pag_number in range(0,82):
        chunck_thread = threading.Thread(target=get_monsters_id, args=(pag_number, monster_list_chunks))
        monster_thread_chunks.append(chunck_thread)
        chunck_thread.start()
    for chunck in monster_thread_chunks:
        chunck.join()
    final_list = dict()
    for chunck_key in monster_list_chunks.keys():
        final_list.update(monster_list_chunks.get(chunck_key))
    return final_list


def create_monster_list():      
    file = open("C:\\Users\\Lucas\\Desktop\\x\\database\\Monsters.json",'r')
    monsters = json.load(file)
    monsters_names = get_full_monster_list()
    print(monsters_names)
    monsters_list = list()
    count = 0
    for monster in monsters:
        count += 1
        monster_id = monster.get("id")
        grades = monster.get('grades')
        for grade in grades:
            
            monster = (
                    monster_id,
                    monsters_names.get(str(monster_id)),
                    grade.get('level'),
                    grade.get('lifePoints'),
                    grade.get('actionPoints'),
                    grade.get('movementPoints'),
                    grade.get('earthResistance'),
                    grade.get('airResistance'),
                    grade.get('fireResistance'),
                    grade.get('waterResistance'),
                    grade.get('neutralResistance'),
            )
            if monster[1] is not None:
                monsters_list.append(monster)
    return monsters_list

monsters = create_monster_list()
database = Database()
for row in monsters:
    database.insert_monsters(row=row)
    
