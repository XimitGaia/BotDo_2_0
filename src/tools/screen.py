from search import Search
import numpy as np
from PIL import Image
from PIL import ImageGrab
import time
import os
import pytesseract



#proportioon Widht_screen/width_action_screen = 1.415
#proportion width_sction_screen/high_action_scrren = 1.255


class Screen:

    def __init__(self,mode = None):
        self.base_local_path = os.path.dirname(os.path.realpath(__file__))
        self.screen_size = None
        self.get_screen_size()
        self.game_active_screen = None
        self.get_game_active_screen()
        self.markers_path = f'{self.base_local_path}{os.sep}screen_markers{os.sep}'
        self.fight_regions = None
        self.get_fight_markers_regions()
        print(self.fight_regions)
        if mode == 'battle':
            print(time.time())
            self.markers_path = f'{self.base_local_path}{os.sep}screen_markers{os.sep}'
            self.fight_regions = None
            
            
            print(time.time())

        if mode == 'login':
            seila = None
            print(seila)
        #########

        self.get_game_active_screen()
        self.get_fight_markers_regions()


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
        marked_area = (matches[0][0],matches[0][1],matches[-1][0],matches[-1][1])
        if screen != '':
            marked_area = (
                marked_area[0]+screen[0],
                marked_area[1]+screen[1],
                marked_area[2]+screen[0], 
                marked_area[3]+screen[1]
            )
        return marked_area
    
    
    def get_fight_markers_regions(self):
        search_region = (0,
        0.65*self.screen_size[1],
        self.screen_size[0],
        self.screen_size[1]
        )
        self.fight_regions = {
            'res_region': self.get_marked_area(marker='res_marker',screen=search_region)),
            'name_region': self.get_marked_area(marker='name_marker',screen=search_region)),
            'hp_ap_mp_region': self.get_marked_area(marker='hp_ap_mp_marker',screen=search_region))
        }

    def get_game_active_screen(self):#(x1,y1,x2,y2)
        screen_proportion = 0.704
        action_screen_proportion = 0.709
        width = self.screen_size[0]*screen_proportion
        X = (self.screen_size[0] - width)/2
        high = action_screen_proportion * width
        self.game_active_screen = (
            round(X),
            0,
            round(X + width),
            round(high)
        )

s = Screen()
