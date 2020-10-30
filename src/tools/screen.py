from search import Search
import numpy as np
from PIL import Image
from PIL import ImageGrab
import time
import os
import pytesseract
import pyautogui


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
        self.bottom_region = (0,
            round(0.65*self.screen_size[1]),
            self.screen_size[0],
            self.screen_size[1]
            )
        self.chat_input = None
        #self.get_chat_input()
        if mode == 'battle':
            self.team = None
            self.cells = []
            self.walls = []
            self.holes = []
            self.others = []
            self.start_positions = []
        if mode == 'login':
            seila = None


    def get_screen_size(self):
        self.screen_size = ImageGrab.grab('').size

    def get_marked_area(self, 
    marker: str = '',
    screen = ''
    )->tuple:
        marker = Image.open(f'{self.markers_path}{marker}.png')
        screen = screen
        matches = Search.search(
            image=marker,
            screen=screen,
            match_tolerance=0.01,
            validator_group_porcentage=1,
            saturation_tolerance=0.01,
            bright_tolerance=0.01,          
        )
        if len(matches) <= 1:
            print('Marker not found')
            return None
        marked_area = (
            matches[0][0],
            matches[0][1],
            matches[-1][0],
            matches[-1][1]
        )
        if screen != '':
            marked_area = (
                marked_area[0]+screen[0],
                marked_area[1]+screen[1],
                marked_area[2]+screen[0], 
                marked_area[3]+screen[1] 
            )
        return marked_area
    
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

    def get_chat_input(self):
        region = self.get_marked_area(screen=self.bottom_region,marker='chat_input_marker')
        central_point = ((region[0]+region[2])/2 , (region[1]+region[3])/2)
        self.chat_input = central_point
        
##################################################################################################
#####################battle mode#############################################################

    def get_fight_markers_regions(self)->dict:
            return {
                'res_region': self.get_marked_area(marker='res_marker',screen=self.bottom_region),
                'name_region': self.get_marked_area(marker='name_marker',screen=self.bottom_region),
                'hp_ap_mp_region': self.get_marked_area(marker='hp_ap_mp_marker',screen=self.bottom_region)
            }

    def text_res_table_on_screen(self,table_region:tuple)->str:
        region_image = ImageGrab.grab(table_region)
        return pytesseract.image_to_string(region_image,config='--psm 4 -c tessedit_char_whitelist=-%0123456789')

    def text_hp_ap_mp_list_on_screen(self,list_region:tuple)->str:
        region_image = ImageGrab.grab(list_region)
        return pytesseract.image_to_string(region_image,config='--psm 6 -c tessedit_char_whitelist=-/0123456789')

    def get_action_screen_y_step(self):
        return (self.game_active_screen[3]-self.game_active_screen[1])/41
    
    def get_action_screen_x_step(self):
        return (self.game_active_screen[2]-self.game_active_screen[0])/14.5

    def get_comparation_group(self,point: tuple)->list:
        comparation_group = []
        for y in range(point[1]-1,point[1]+2):
            for x in range(point[0]-1,point[0]+2):
                comparation_group.append((x,y))
        return comparation_group

    def define_and_append_cell_group(self,position_number:int,pixels: list):
        a = 0
        if pixels[1:] == pixels[:-1]:# if all pixels are equal
            if pixels[0] == [142, 134, 94] or pixels[0] == [150, 142, 103]:
                self.cells.append(position_number)
            elif pixels[0] == [0, 0, 0]:
                self.holes.append(position_number)
            elif pixels[0] == [88, 83, 58]:
                self.walls.append(position_number)
            elif pixels[0] == [221, 34, 0]:
                self.cells.append(position_number)
                self.team = 'red'
                self.start_positions.append(position_number)
            elif pixels[0] == [0, 34, 221]:
                self.cells.append(position_number)
                self.team = 'blue'
                self.start_positions.append(position_number)
            else:# enemy start positions
                self.cells.append(position_number)
        else:
            self.cells.append(position_number)
            #self.others.append(position_number)

    def get_battle_map_info(self):
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
                comparation_group_pixels = []
                for xcoord,ycoord in comparation_group:
                    comparation_group_pixels.append(list(action_screen[ycoord][xcoord]))
                self.define_and_append_cell_group(position_number=position_number,pixels=comparation_group_pixels)
                position_number += 1
            if x_range_color == self.x_range_black:
                x_range_color = self.x_range_white
            else:
                x_range_color = self.x_range_black

    def map_to_screen(self, cell_number:int):
        ycoord = (cell_number//14)
        xcoord = cell_number - (ycoord*14)
        translation_x = self.game_active_screen[0]
        translation_y = self.game_active_screen[1]
        return (round(self.x_range_white[xcoord]+translation_x),round(self.y_range[ycoord]+translation_y))

###################################


ad = time.time()
s = Screen(mode='battle')
s.get_chat_input()
print(time.time()-ad)