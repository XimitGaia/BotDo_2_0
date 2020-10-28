from search import Search
import numpy as np
from PIL import Image
import time
import os

class Screen:

    def __init__(self):
        self.base_local_path = os.path.dirname(os.path.realpath(__file__))
        self.markers = None
        self.get_markers_dict()# marker padron size is W = 5px, H = 5px
        print(self.get_marked_area())
    
    def get_markers_dict(self):
        self.markers = {
        'res_marker': Image.open(f'{self.base_local_path}{os.sep}screen_markers{os.sep}res_marker.png'),
        'hp_ap_mp_marker': Image.open(f'{self.base_local_path}{os.sep}screen_markers{os.sep}hp_ap_mp_marker.png'),
        'name_marker': Image.open(f'{self.base_local_path}{os.sep}screen_markers{os.sep}name_marker.png')
        }

    def get_marked_area(self, marker: str = 'res_marker')-> tuple:
        marker = self.markers[marker]
        time.sleep(3)
        matches = Search.search(
            image=marker,
            match_tolerance=0.01,
            validator_group_porcentage=1,
            saturation_tolerance=0.01,
            bright_tolerance=0.01,          
        )
        if len(matches) <= 1:
            print('Marker not found')
            return None
        print(matches)
        return (matches[0][0],matches[0][1],matches[-1][0],matches[-1][1])




s = Screen()