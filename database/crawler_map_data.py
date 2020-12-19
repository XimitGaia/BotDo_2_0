import os
import requests
import json
from PIL import Image
from sqlite import Database
from bs4 import BeautifulSoup
import re
import numpy as np


local_base_path = os.path.dirname(os.path.realpath(__file__))
map_positions = json.load(open(f'{local_base_path}{os.sep}MapPositions.json'))
map_scroll_actions = json.load(open(f'{local_base_path}{os.sep}MapScrollActions.json'))
sub_areas = json.load(open(f'{local_base_path}{os.sep}SubAreas.json'))


bounds = []
valid_positions = []
def get_continents_external_info():
    url = f'https://dofus-map.com/js/main.js?40'
    result = requests.get(url)
    if result.status_code == 200:
        coords = re.findall(r'//var groupBoundsDefinition = \'(.*)\'', result.text)
        coords = coords[0] + ' ' + coords[1]
        for group in coords.split(' '):
            group = group.split(':')
            x_coord = int(group[0])
            for y_itens in group[1].split(','):
                y_itens = y_itens.split('L')
                Y0 =  int(y_itens[0])
                Y1 =  int(y_itens[0]) + int(y_itens[1])
                for y_coord in range(Y0, Y1):
                    valid_positions.append((x_coord, y_coord))



def generate_continents_external_bounds():
    get_continents_external_info()
    for xcoord in range(-93, 50):
        for ycoord in range(-98,60):
            #print(type(xcoord),type(ycoord))
            # if (xcoord,ycoord) == (15,-33):
            #     print('toaqui')
            # if (xcoord,ycoord) == (14,-33):
            #     print('esquerda')
            # if (xcoord,ycoord) == (16,-33):
            #     print('direita')
            # if (xcoord,ycoord) == (15,-34):
            #     print('cima')
            # if (xcoord,ycoord) == (15,-32):
            #     print('baixo')
            if (xcoord, ycoord) in valid_positions:
                if (xcoord - 1, ycoord) in valid_positions:
                    Q = 1
                else:
                    Q = 0
                if (xcoord, ycoord + 1) in valid_positions:
                    X = 1
                else:
                    X = 0
                if (xcoord + 1, ycoord) in valid_positions:
                    B = 1
                else:
                    B = 0
                if (xcoord, ycoord - 1) in valid_positions:
                    T = 1
                else:
                    T = 0
                bounds.append((int(xcoord),int(ycoord), T, Q, X, B, 1))
                # bounds.append((int(xcoord),int(ycoord)))


def get_continents_internal_bounds():
    for map_direction_info in map_scroll_actions:
        map_id = map_direction_info["id"]
        for map_geral_info in map_positions:
            if map_geral_info["id"] == map_id:
                #if map_geral_info["worldMap"] == 1:
                xcoord = map_geral_info["posX"]
                ycoord = map_geral_info["posY"]
                T = int(map_direction_info["topExists"])
                Q = int(map_direction_info["leftExists"])
                X = int(map_direction_info["bottomExists"])
                B = int(map_direction_info["rightExists"])
                # print(T,Q,X,B)
                #print(type(xcoord),type(ycoord))
                bounds.append((xcoord, ycoord, T, Q, X, B, 1))
                # if ((T,Q,X,B)) != (0,0,0,0):
                #     if ((T,Q,X,B)) != (1,0,0,1):
                #         if ((T,Q,X,B)) != (0,1,1,0):
                #             bounds.append((xcoord, ycoord))
                break

generate_continents_external_bounds()
get_continents_internal_bounds()
print(bounds)
database = Database()
for row in bounds:
    database.insert_barrers(row = row)





    # a = Image.open("C:\\Users\\Lucas\\Desktop\\Untitled2.png")
    # pixel_a = a.load()
    # for i in range(a.size[0]):
    #     for j in range(a.size[1]):
    #         x = i- 94
    #         y = j -95
    #         if (x, y) in bounds:
    #             pixel_a[i*2,j] = (0,0,0)
#a.show()