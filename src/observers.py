# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))

import time
from PIL import Image
from PIL import ImageGrab
from src.tools.search import Search
import threading
from src.state.state import State


class Observers:

    debug_map = dict({
        'battle': True
    })

    @staticmethod
    def battle_observer(state:State, debug: bool= False):
        print('to aqui')       
        def run():
            screen_size = ImageGrab.grab().size 
            bottom_region = (
                0,
                round(0.65*screen_size[1]),
                screen_size[0],
                screen_size[1]
                )
            if debug:
                counter = 0
            while True:
                if debug and Observers.debug_map.get('battle'):
                    print(f'tick battle observer, total: {counter}')
                    counter += 1
                    print(f'state.is_bussy -> {state.is_bussy}')
                    print(state.state)
                match_list = Search.search_color(RGB=(76, 0, 61), region= bottom_region)
                if len(match_list) > 0:
                    state.set_state(key='status', value='battle')


        thread = threading.Thread(target=run, args=())
        thread.daemon = True                            
        thread.start()  
        