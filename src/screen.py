# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[1])

# Import system
from src.tools.search import Search
import numpy as np
from PIL import Image
from PIL import ImageGrab
import time
import pytesseract
import pyautogui
import win32gui


#proportioon Widht_screen/width_action_screen = 1.415
#proportion width_sction_screen/high_action_scrren = 1.255


class Screen:

    def __init__(self,mode = None):
        self.base_local_path = os.path.dirname(os.path.realpath(__file__))
        self.markers_path = f'{self.base_local_path}{os.sep}screen_markers{os.sep}'
        self.screen_size = None
        self.get_screen_size()
        self.game_active_screen = None
        self.get_game_active_screen()
        self.bottom_region = None
        self.get_bottom_region()
        self.fight_buttom_region = None
        self.get_fight_buttom_region()
        self.chat_input = None
        self.search = Search()





    def get_screen_size(self):
        self.screen_size = ImageGrab.grab('').size

    def get_game_active_screen(self):#(x1,y1,x2,y2)
        screen_proportion = 0.704
        action_screen_proportion = 0.709
        width = self.screen_size[0]*screen_proportion
        X = (self.screen_size[0] - width)/2
        high = action_screen_proportion * width
        self.game_active_screen = (
            round(X),
            0,
            round(X+width),
            round(0+high)
        )

    def get_bottom_region(self):
        self.bottom_region = (
            0,
            round(0.65*self.screen_size[1]),
            self.screen_size[0],
            self.screen_size[1]
        )

    def get_fight_buttom_region(self):
        self.fight_buttom_region = (
            0.75419*(self.game_active_screen[2] - self.game_active_screen[0] )+ self.game_active_screen[0],
            self.game_active_screen[3],
            self.game_active_screen[2],
            self.screen_size[1]
        )




#        :::::::::      ::: ::::::::::: ::::::::::: :::        ::::::::::            :::   :::    ::::::::  :::::::::  ::::::::::
#       :+:    :+:   :+: :+:   :+:         :+:     :+:        :+:                  :+:+: :+:+:  :+:    :+: :+:    :+: :+:
#      +:+    +:+  +:+   +:+  +:+         +:+     +:+        +:+                 +:+ +:+:+ +:+ +:+    +:+ +:+    +:+ +:+
#     +#++:++#+  +#++:++#++: +#+         +#+     +#+        +#++:++#            +#+  +:+  +#+ +#+    +:+ +#+    +:+ +#++:++#
#    +#+    +#+ +#+     +#+ +#+         +#+     +#+        +#+                 +#+       +#+ +#+    +#+ +#+    +#+ +#+
#   #+#    #+# #+#     #+# #+#         #+#     #+#        #+#                 #+#       #+# #+#    #+# #+#    #+# #+#
#  #########  ###     ### ###         ###     ########## ##########          ###       ###  ########  #########  ##########




    def get_fight_markers_regions(self)->dict:
            return {
                'res_region': self.get_marked_area_or_points(marker='res_marker',screen=self.bottom_region),
                'name_region': self.get_marked_area_or_points(marker='name_marker',screen=self.bottom_region),
                'hp_ap_mp_region': self.get_marked_area_or_points(marker='hp_ap_mp_marker',screen=self.bottom_region)
            }

    def text_res_table_on_screen(self,table_region:tuple)->str:
        region_image = ImageGrab.grab(table_region)
        return pytesseract.image_to_string(region_image,config='--psm 4 -c tessedit_char_whitelist=-%0123456789')

    def text_hp_ap_mp_list_on_screen(self,region:tuple)->str:
        region_image = ImageGrab.grab(region)
        return pytesseract.image_to_string(region_image,config='--psm 6 -c tessedit_char_whitelist=-/0123456789')

    def get_timeline_region(self):
        return (self.game_active_screen[2],0,self.screen_size[0],self.screen_size[1])




    def get_action_screen_y_step(self):
        return (self.game_active_screen[3]-self.game_active_screen[1])/41

    def get_action_screen_x_step(self):
        return (self.game_active_screen[2]-self.game_active_screen[0])/14.5

    def get_comparation_group(self,point: tuple)->list: #point = (x,y)
        comparation_group = []
        for y in range(point[1]-1,point[1]+2):
            for x in range(point[0]-1,point[0]+2):
                comparation_group.append((x,y))
        return comparation_group

    def get_battle_map_info(self):
        #variables to return
        team = None
        cells = []
        walls = []
        holes = []
        start_positions = []
        timeline_region = self.get_timeline_region()
        #end of variables
        #define step and get the screen image to compare
        step_x = self.get_action_screen_x_step()
        step_y = self.get_action_screen_y_step()
        y_start = step_y * 0.5 # make the poinst match 1/4 of the high of the losangle
        action_screen = ImageGrab.grab(self.game_active_screen)
        action_screen = np.array(action_screen)
        position_number = 0 # number of the cell
        self.y_range = list(np.arange(y_start,len(action_screen)-step_y,step_y))
        self.x_range_black = list(
            np.arange(
                step_x * 0.5,
                len(action_screen[0]),
                step_x
            )
        )
        self.x_range_white = list(
            np.arange(
                step_x,
                len(action_screen[0]),
                step_x
            )
        )
        x_range_color = self.x_range_black # start difference between withe losangle and black losangle
        for y in self.y_range:
            for x in x_range_color:
                comparation_group = self.get_comparation_group((round(x),round(y)))
                pixels = []
                for xcoord,ycoord in comparation_group:
                    pixels.append(list(action_screen[ycoord][xcoord]))
                #define the group of the cell
                if pixels[1:] == pixels[:-1]:# if all pixels are equal
                    if pixels[0] == [142, 134, 94] or pixels[0] == [150, 142, 103]:
                        cells.append(position_number)
                    elif pixels[0] == [0, 0, 0]:
                        holes.append(position_number)
                    elif pixels[0] == [88, 83, 58]:
                        walls.append(position_number)
                    elif pixels[0] == [221, 34, 0]:
                        cells.append(position_number)
                        team = 'red'
                        start_positions.append(position_number)
                    elif pixels[0] == [0, 34, 221]:
                        cells.append(position_number)
                        team = 'blue'
                        start_positions.append(position_number)
                    else:# enemy start positions
                        cells.append(position_number)
                else:
                    cells.append(position_number)
            #change the index of the position and the translation of the row
                position_number += 1
            if x_range_color == self.x_range_black:
                x_range_color = self.x_range_white
            else:
                x_range_color = self.x_range_black

        return {
            'cells': cells,
            'walls': walls,
            'holes': holes,
            'start_positions': start_positions,
            'team': team,
            'timeline_region': timeline_region
        }

    def map_to_screen(self, cell_number:int):
        ycoord = (cell_number//14)
        xcoord = cell_number - (ycoord*14)
        translation_x = self.game_active_screen[0]
        translation_y = self.game_active_screen[1]
        if ycoord%2 == 0:
            return (round(self.x_range_black[xcoord]+translation_x),round(self.y_range[ycoord]+translation_y))
        return (round(self.x_range_white[xcoord]+translation_x),round(self.y_range[ycoord]+translation_y))

    def get_occupied_cells(self):
        screen = ImageGrab.grab('')
        occupied_cells = []
        for cell in self.cells:
            point = self.map_to_screen(cell)
            if screen.getpixel(point) != (142, 134, 94) and screen.getpixel(point) != (150, 142, 103):
                occupied_cells.append(cell)
        return occupied_cells








#        :::::::: ::::::::::: :::    ::: :::::::::: :::::::::   ::::::::
#      :+:    :+:    :+:     :+:    :+: :+:        :+:    :+: :+:    :+:
#     +:+    +:+    +:+     +:+    +:+ +:+        +:+    +:+ +:+
#    +#+    +:+    +#+     +#++:++#++ +#++:++#   +#++:++#:  +#++:++#++
#   +#+    +#+    +#+     +#+    +#+ +#+        +#+    +#+        +#+
#  #+#    #+#    #+#     #+#    #+# #+#        #+#    #+# #+#    #+#
#  ########     ###     ###    ### ########## ###    ###  ########

    def get_my_bag_type(self):
        width_constant = 0.195426195426195
        height_constant = 0.0982404692082
        ocr_config = '--psm 6 --oem 3'
        screen_image = ImageGrab.grab((
            0,
            0,
            width_constant * (self.game_active_screen[2] - self.game_active_screen[0]),
            height_constant * (self.game_active_screen[3] - self.game_active_screen[1])
        ))
        text = pytesseract.image_to_string(screen_image, config=ocr_config)
        if text.split(' ')[0].strip() == 'Kerub':
            return 'kerub'
        else:
            return 'amakna'

    def find_zaap_search_position(self):
        result = self.search.search_color(RGB=(0, 255, 255), region=(self.game_active_screen))
        result_width = max(result, key=lambda x: x[0])[0] - min(result, key=lambda x: x[0])[0]
        result_heigh = max(result, key=lambda x: x[1])[1] - min(result, key=lambda x: x[1])[1]
        xcoord = min(result, key=lambda x: x[0])[0] + 2.5 * result_width
        ycoord = min(result, key=lambda x: x[1])[1] + result_heigh/2
        return (xcoord, ycoord)

    def has_zaap_marker(self):
        result = self.search.search_color(RGB=(255, 0, 255), region=(self.game_active_screen))
        if result != []:
            return True
        return False

    def bring_character_to_front(self, character_window_number:int):
        win32gui.SetForegroundWindow(character_window_number)

    def get_chat_content(self,chat_position):
        chat_image = ImageGrab.grab(chat_position)
        ocr_config = '--psm 6 --oem 3'
        text = pytesseract.image_to_string(chat_image, config=ocr_config)
        return text

if __name__ == "__main__":
    screen = Screen()
    points = screen.game_active_screen
    print(points)
    print(screen.get_my_bag_type())

